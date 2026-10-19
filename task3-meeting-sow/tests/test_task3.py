"""
Unit and Integration Tests for Task 3: Meeting to Scope of Work.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.agents.consultant import consultant_agent
from app.agents.architect import architect_agent
from app.agents.estimator import estimator_agent
from app.agents.diff_agent import diff_agent


@pytest.mark.asyncio
async def test_health_check():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/v1/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_sample_transcripts_available():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/v1/transcripts")
        assert res.status_code == 200
        data = res.json()
        assert "meeting_1_discovery.txt" in data
        assert "meeting_2_architecture.txt" in data
        assert "meeting_3_followup_changes.txt" in data


@pytest.mark.asyncio
async def test_consultant_and_architect_pipeline():
    transcript_sample = (
        "We need a medical directory where parents search by specialty and zip code, "
        "see an accepting new patients badge, and pay monthly via Stripe. "
        "We also need a custom brand theme and an outgoing webhook to our audit system."
    )
    c_res = consultant_agent.parse_transcript(transcript_sample, "Test Medical Directory")
    assert len(c_res["raw_requirements"]) >= 4

    evaluated = await architect_agent.evaluate_requirements(c_res["raw_requirements"])
    native_items = [r for r in evaluated if r.resolution_type == "NATIVE_SETTING"]
    custom_items = [r for r in evaluated if r.resolution_type == "CUSTOM_DEVELOPMENT"]

    assert len(native_items) >= 2, "Native settings like Search and Stripe must be recognized ($0)"
    assert len(custom_items) >= 1, "Custom theme / webhook must be recognized as development work"


@pytest.mark.asyncio
async def test_developer_estimator():
    transcript_sample = "We need a custom brand theme and an outgoing webhook."
    c_res = consultant_agent.parse_transcript(transcript_sample, "Test")
    evaluated = await architect_agent.evaluate_requirements(c_res["raw_requirements"])
    tasks, th, tc = estimator_agent.estimate_tasks(evaluated)

    assert len(tasks) > 0
    assert th > 0.0
    assert tc == th * 125.0


@pytest.mark.asyncio
async def test_process_meeting_and_human_approval_gate():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Step 1: Process Meeting 1
        res = await client.post("/api/v1/process-transcript", json={
            "transcript_text": "We need doctor search by specialty, Stripe billing, and a custom theme.",
            "client_name": "Dr. Elena Vance",
            "project_name": "HealthMatch"
        })
        assert res.status_code == 200
        proposal = res.json()
        assert proposal["is_approved_by_human"] is False, "Must not be approved before human review"
        prop_id = proposal["proposal_id"]

        # Step 2: Human approves proposal
        appr_res = await client.post(f"/api/v1/proposals/{prop_id}/approve?approver_name=Senior+Consultant")
        assert appr_res.status_code == 200
        appr_data = appr_res.json()
        assert appr_data["is_approved_by_human"] is True
        assert appr_data["approved_by"] == "Senior Consultant"


@pytest.mark.asyncio
async def test_scope_diff_and_out_of_scope_creep_detection():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Step 1: Run delta analysis comparing Meeting 1 baseline with Meeting 3 follow-up
        res = await client.post("/api/v1/process-delta")
        assert res.status_code == 200
        data = res.json()
        assert data["delta_report"] is not None

        delta = data["delta_report"]
        assert delta["scope_creep_detected"] is True, "Must detect out-of-scope Epic EMR creep"

        diff_statuses = [d["status"] for d in delta["diff_items"]]
        assert "OUT_OF_SCOPE_EXTRA" in diff_statuses
        assert "NEW_REQUEST" in diff_statuses

        creep_item = [d for d in delta["diff_items"] if d["status"] == "OUT_OF_SCOPE_EXTRA"][0]
        assert "Epic" in creep_item["title"] or "FHIR" in creep_item["title"]
        assert creep_item["is_extra_quoted"] is True
