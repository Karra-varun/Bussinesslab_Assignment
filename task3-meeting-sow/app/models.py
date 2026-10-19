"""
Data Models and Pydantic Schemas for Task 3: Meeting to Scope of Work.
"""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime


class RequirementItem(BaseModel):
    id: str
    title: str
    client_wording: str
    category: str
    resolution_type: Literal["NATIVE_SETTING", "CUSTOM_DEVELOPMENT"]
    kb_article_title: Optional[str] = None
    kb_article_url: Optional[str] = None
    setting_location: Optional[str] = None
    complexity: Literal["NONE", "LOW", "MEDIUM", "HIGH"] = "LOW"
    estimated_hours: float = 0.0
    consultant_notes: str = ""


class DeveloperTask(BaseModel):
    task_id: str
    requirement_id: str
    title: str
    description: str
    role: Literal["Solutions Architect", "Frontend/UI Engineer", "Backend/Integration Engineer", "QA Specialist"]
    hours: float
    hourly_rate: float
    total_cost: float


class ScopeOfWork(BaseModel):
    sow_id: str
    project_name: str
    client_name: str
    executive_summary: str
    timeline_weeks: int
    requirements: List[RequirementItem] = Field(default_factory=list)
    developer_tasks: List[DeveloperTask] = Field(default_factory=list)
    total_native_settings: int = 0
    total_custom_tasks: int = 0
    total_estimated_hours: float = 0.0
    total_estimated_cost: float = 0.0
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ScopeDiffItem(BaseModel):
    item_id: str
    title: str
    status: Literal["UNCHANGED", "MODIFIED", "NEW_REQUEST", "OUT_OF_SCOPE_EXTRA", "REMOVED"]
    original_hours: float = 0.0
    new_hours: float = 0.0
    cost_difference: float = 0.0
    reasoning: str
    is_extra_quoted: bool = False


class ScopeDeltaReport(BaseModel):
    baseline_meeting_name: str
    followup_meeting_name: str
    diff_items: List[ScopeDiffItem] = Field(default_factory=list)
    total_hours_delta: float = 0.0
    total_cost_delta: float = 0.0
    scope_creep_detected: bool = False
    executive_delta_summary: str = ""


class Proposal(BaseModel):
    proposal_id: str
    sow: ScopeOfWork
    delta_report: Optional[ScopeDeltaReport] = None
    is_approved_by_human: bool = False
    approved_at: Optional[str] = None
    approved_by: Optional[str] = None
    client_ready_markdown: str = ""


class ProcessMeetingRequest(BaseModel):
    transcript_text: str
    client_name: str = "Dr. Elena Vance"
    project_name: str = "HealthMatch Directory Platform"
    baseline_sow_id: Optional[str] = None
    is_followup_meeting: bool = False
