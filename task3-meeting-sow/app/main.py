"""
FastAPI Entrypoint for Task 3: Meeting to Scope of Work.
Runs on Port 8003.
"""
import uuid
from typing import Dict, Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from datetime import datetime, timezone

from app.config import settings, BASE_DIR, TRANSCRIPTS_DIR
from app.models import (
    ProcessMeetingRequest, ScopeOfWork, Proposal,
    ScopeDeltaReport
)
from app.agents.consultant import consultant_agent
from app.agents.architect import architect_agent
from app.agents.estimator import estimator_agent
from app.agents.diff_agent import diff_agent
from app.agents.proposal import proposal_generator

app = FastAPI(
    title="Meeting-to-SOW Multi-Agent API",
    description="Multi-agent system turning client meeting transcripts into Scopes of Work, Developer Estimates, and Proposals with human approval gates.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for SOWs and Proposals
sow_db: Dict[str, ScopeOfWork] = {}
proposal_db: Dict[str, Proposal] = {}

# Static directory
static_dir = BASE_DIR / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return HTMLResponse("<h1>Meeting to Scope of Work Studio is running. Visit <a href='/docs'>/docs</a></h1>")


@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Meeting-to-SOW Multi-Agent Service",
        "total_proposals": len(proposal_db),
        "total_sows": len(sow_db)
    }


@app.get("/api/v1/transcripts")
async def list_sample_transcripts():
    """Returns sample role-played transcripts for easy testing in the UI."""
    transcripts = {}
    for p in TRANSCRIPTS_DIR.glob("*.txt"):
        try:
            with open(p, "r", encoding="utf-8") as f:
                transcripts[p.name] = f.read()
        except Exception:
            pass
    return transcripts


@app.post("/api/v1/process-transcript", response_model=Proposal)
async def process_transcript(req: ProcessMeetingRequest):
    """
    Executes the multi-agent pipeline:
    1. Consultant Agent extracts requirements & timeline.
    2. Architect Agent checks Task 1 Knowledge Brain API (native settings vs custom code).
    3. Estimator Agent breaks custom items into engineering tasks with hour estimates.
    4. Proposal Generator synthesizes SOW, estimates, and client proposal.
    """
    # Step 1: Senior Consultant Agent
    consultant_res = consultant_agent.parse_transcript(req.transcript_text, req.project_name)

    # Step 2: Solution Architect Agent
    evaluated_reqs = await architect_agent.evaluate_requirements(consultant_res["raw_requirements"])

    # Step 3: Developer Estimator Agent
    tasks, total_hours, total_cost = estimator_agent.estimate_tasks(evaluated_reqs)

    native_count = sum(1 for r in evaluated_reqs if r.resolution_type == "NATIVE_SETTING")
    custom_count = sum(1 for r in evaluated_reqs if r.resolution_type == "CUSTOM_DEVELOPMENT")

    sow_id = f"SOW-{uuid.uuid4().hex[:6].upper()}"
    sow = ScopeOfWork(
        sow_id=sow_id,
        project_name=req.project_name,
        client_name=req.client_name,
        executive_summary=consultant_res["executive_summary"],
        timeline_weeks=consultant_res["timeline_weeks"],
        requirements=evaluated_reqs,
        developer_tasks=tasks,
        total_native_settings=native_count,
        total_custom_tasks=custom_count,
        total_estimated_hours=total_hours,
        total_estimated_cost=total_cost,
        created_at=datetime.now(timezone.utc).isoformat()
    )
    sow_db[sow_id] = sow

    # Step 4: Proposal Generator Agent
    proposal = proposal_generator.assemble_proposal(sow)
    proposal_db[proposal.proposal_id] = proposal

    return proposal


@app.post("/api/v1/process-delta", response_model=Proposal)
async def process_delta_meeting(
    baseline_sow_id: Optional[str] = None,
    followup_transcript: Optional[str] = None
):
    """
    Compares baseline SOW against follow-up meeting revisions:
    Detects modified, new, and OUT_OF_SCOPE_EXTRA requirements.
    """
    # If no baseline provided, generate or fetch first
    if not baseline_sow_id or baseline_sow_id not in sow_db:
        # Create baseline from Meeting 1
        m1_path = TRANSCRIPTS_DIR / "meeting_1_discovery.txt"
        m1_text = open(m1_path, "r", encoding="utf-8").read() if m1_path.exists() else ""
        c_res = consultant_agent.parse_transcript(m1_text, "HealthMatch Pediatric Directory")
        ev_reqs = await architect_agent.evaluate_requirements(c_res["raw_requirements"])
        tasks, th, tc = estimator_agent.estimate_tasks(ev_reqs)
        baseline = ScopeOfWork(
            sow_id=f"SOW-BASELINE-{uuid.uuid4().hex[:4].upper()}",
            project_name="HealthMatch Pediatric Directory (Meeting 1 Baseline)",
            client_name="Dr. Elena Vance",
            executive_summary=c_res["executive_summary"],
            timeline_weeks=4,
            requirements=ev_reqs,
            developer_tasks=tasks,
            total_native_settings=sum(1 for r in ev_reqs if r.resolution_type == "NATIVE_SETTING"),
            total_custom_tasks=sum(1 for r in ev_reqs if r.resolution_type == "CUSTOM_DEVELOPMENT"),
            total_estimated_hours=th,
            total_estimated_cost=tc,
            created_at=datetime.now(timezone.utc).isoformat()
        )
        sow_db[baseline.sow_id] = baseline
    else:
        baseline = sow_db[baseline_sow_id]

    # Process Follow-up transcript
    if not followup_transcript:
        m3_path = TRANSCRIPTS_DIR / "meeting_3_followup_changes.txt"
        followup_transcript = open(m3_path, "r", encoding="utf-8").read() if m3_path.exists() else ""

    followup_res = consultant_agent.parse_transcript(followup_transcript, "HealthMatch Follow-up Revisions")
    followup_reqs = await architect_agent.evaluate_requirements(followup_res["raw_requirements"])

    # Run Scope Auditor & Diff Agent
    delta_report = diff_agent.compare_meetings(baseline, followup_reqs)

    # Re-estimate active Phase 1 tasks
    active_phase1_reqs = [
        r for r in followup_reqs
        if not ("epic" in r.title.lower() or "fhir" in r.title.lower())
    ]
    tasks, th, tc = estimator_agent.estimate_tasks(active_phase1_reqs)

    revised_sow = ScopeOfWork(
        sow_id=f"SOW-REVISED-{uuid.uuid4().hex[:4].upper()}",
        project_name="HealthMatch Pediatric Directory (Revised Scope)",
        client_name="Dr. Elena Vance",
        executive_summary=followup_res["executive_summary"],
        timeline_weeks=4,
        requirements=followup_reqs,
        developer_tasks=tasks,
        total_native_settings=sum(1 for r in followup_reqs if r.resolution_type == "NATIVE_SETTING"),
        total_custom_tasks=sum(1 for r in followup_reqs if r.resolution_type == "CUSTOM_DEVELOPMENT"),
        total_estimated_hours=th,
        total_estimated_cost=tc,
        created_at=datetime.now(timezone.utc).isoformat()
    )
    sow_db[revised_sow.sow_id] = revised_sow

    revised_proposal = proposal_generator.assemble_proposal(revised_sow, delta_report)
    proposal_db[revised_proposal.proposal_id] = revised_proposal

    return revised_proposal


@app.post("/api/v1/proposals/{proposal_id}/approve", response_model=Proposal)
async def approve_proposal(proposal_id: str, approver_name: str = "Lead Tech Consultant"):
    """
    Human Consultant Approval Gate.
    Ensures nothing reaches the client until a human expert inspects and approves it.
    """
    proposal = proposal_db.get(proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    proposal.is_approved_by_human = True
    proposal.approved_at = datetime.now(timezone.utc).isoformat()
    proposal.approved_by = approver_name

    # Update proposal markdown with approval signature
    proposal.client_ready_markdown += (
        f"\n\n---\n### ✅ Consultant Sign-Off\n"
        f"Approved for Client Presentation by **{approver_name}** on {datetime.now(timezone.utc).strftime('%B %d, %Y at %H:%M UTC')}."
    )

    return proposal


@app.get("/api/v1/proposals/{proposal_id}", response_model=Proposal)
async def get_proposal(proposal_id: str):
    proposal = proposal_db.get(proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return proposal


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=True)
