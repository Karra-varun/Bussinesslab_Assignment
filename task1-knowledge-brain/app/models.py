"""
Pydantic schemas and data models for Task 1: The Knowledge Brain.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class ImageMetadata(BaseModel):
    url: str
    alt: str = ""
    caption: str = ""
    ocr_text: str = ""
    ui_context: str = ""
    article_id: str = ""


class Article(BaseModel):
    id: str
    url: str
    title: str
    category: str = "General"
    folder: str = "Overview"
    breadcrumbs: List[str] = Field(default_factory=list)
    content_html: str = ""
    content_text: str = ""
    screenshots: List[ImageMetadata] = Field(default_factory=list)
    last_modified: Optional[str] = None
    content_hash: str = ""
    is_deleted: bool = False
    source: str = "help_center"  # "help_center" or "expert_resolution"


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    category_filter: Optional[str] = None
    include_screenshots: bool = True
    model_override: Optional[str] = None


class Citation(BaseModel):
    article_id: str
    title: str
    url: str
    category: str
    folder: str
    snippet: str
    screenshot_url: Optional[str] = None
    screenshot_caption: Optional[str] = None
    relevance_score: float = 0.0


class QueryResponse(BaseModel):
    query: str
    answer: str
    citations: List[Citation] = Field(default_factory=list)
    confidence: float
    is_fallback: bool = False
    fallback_reason: Optional[str] = None
    human_ticket_id: Optional[str] = None
    latency_ms: float = 0.0
    model_used: str = "grounded-rag-claude"


class SyncStatus(BaseModel):
    status: str  # "idle", "syncing", "completed", "error"
    total_articles: int
    last_sync_time: Optional[str]
    sitemap_url: str
    categories: List[str] = Field(default_factory=list)


class SyncReport(BaseModel):
    total_scanned: int = 0
    added: int = 0
    updated: int = 0
    removed: int = 0
    execution_time_sec: float = 0.0
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    details: List[str] = Field(default_factory=list)


class ExpertTicket(BaseModel):
    ticket_id: str
    question: str
    context: Optional[str] = ""
    category: str = "Unassigned"
    status: str = "OPEN"  # "OPEN", "RESOLVED"
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    resolved_at: Optional[str] = None
    resolved_by: Optional[str] = None
    expert_answer: Optional[str] = None


class ResolveTicketRequest(BaseModel):
    answer: str
    expert_name: str = "Senior AI Consultant"
    category: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
