"""
FastAPI Entrypoint for Task 1: The Knowledge Brain.
Exposes clean REST API endpoints, OpenAPI documentation, and serves the Web Interface.
"""
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from typing import List, Optional
from pathlib import Path
import os

from app.config import settings, BASE_DIR
from app.models import (
    QueryRequest, QueryResponse, Article, SyncReport,
    SyncStatus, ExpertTicket, ResolveTicketRequest
)
from app.rag import rag_store
from app.chatbot import chatbot
from app.sync import sync_engine
from app.scraper import scraper
from app.human_loop import expert_manager

from contextlib import asynccontextmanager

# Seed initial articles immediately on module load
def _init_articles():
    articles_to_index = []
    for art_dict in scraper.state.get("article_index", {}).values():
        try:
            articles_to_index.append(Article(**art_dict))
        except Exception:
            pass
    if articles_to_index:
        rag_store.index_articles(articles_to_index)
    expert_manager._load_persisted_tickets()

_init_articles()

@asynccontextmanager
async def lifespan(app: FastAPI):
    _init_articles()
    yield

app = FastAPI(
    title="Knowledge Brain API",
    description=(
        "Core Knowledge Brain service for Brilliant Directories Help Center. "
        "Provides polite scraping, incremental sitemap sync, multimodal screenshot understanding, "
        "hybrid RAG search, and human-in-the-loop expert escalation."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Static files
static_dir = BASE_DIR / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return HTMLResponse("<h1>Knowledge Brain API is running. Visit <a href='/docs'>/docs</a> for API.</h1>")


@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Knowledge Brain API",
        "version": settings.version,
        "indexed_articles": len(rag_store.articles),
        "total_expert_tickets": len(expert_manager.tickets),
        "open_tickets": len(expert_manager.list_tickets("OPEN"))
    }


@app.post("/api/v1/query", response_model=QueryResponse)
async def query_knowledge_base(request: QueryRequest):
    """
    Main query endpoint for Chatbot, Task 2 (Inbox Agent), and Task 3 (Scope of Work).
    Returns grounded answers, citations, confidence score, and triggers fallback if unknown.
    """
    return await chatbot.answer_query(request)


@app.get("/api/v1/articles", response_model=List[Article])
async def list_articles(
    category: Optional[str] = None,
    limit: int = Query(default=20, ge=1, le=100)
):
    """List indexed help center articles with optional category filtering."""
    results = []
    for art in rag_store.articles.values():
        if category and art.category.lower() != category.lower():
            continue
        results.append(art)
        if len(results) >= limit:
            break
    return results


@app.get("/api/v1/articles/{article_id}", response_model=Article)
async def get_article(article_id: str):
    """Retrieve full article content, screenshots, and metadata."""
    if article_id in rag_store.articles:
        return rag_store.articles[article_id]
    raise HTTPException(status_code=404, detail=f"Article {article_id} not found")


@app.post("/api/v1/sync", response_model=SyncReport)
async def trigger_sync(background_tasks: BackgroundTasks, force: bool = False):
    """
    Trigger incremental daily sitemap sync.
    Detects added, updated, and removed articles, immediately updating the RAG index.
    """
    report = await sync_engine.execute_sync()
    return report


@app.get("/api/v1/sync/status", response_model=SyncStatus)
async def get_sync_status():
    """Retrieve current synchronization status and statistics."""
    return sync_engine.get_status()


@app.get("/api/v1/expert-tickets", response_model=List[ExpertTicket])
async def get_expert_tickets(status: Optional[str] = None):
    """List human escalation tickets (filter by OPEN or RESOLVED)."""
    return expert_manager.list_tickets(status)


@app.post("/api/v1/expert-tickets", response_model=ExpertTicket)
async def create_expert_ticket(question: str, context: str = "", category: str = "Unassigned"):
    """Manually escalate an unanswered question to a human expert."""
    return expert_manager.create_ticket(question, context, category)


@app.post("/api/v1/expert-tickets/{ticket_id}/resolve", response_model=ExpertTicket)
async def resolve_expert_ticket(ticket_id: str, req: ResolveTicketRequest):
    """
    Resolve a human expert ticket.
    The expert's verified answer automatically and immediately flows back into the RAG memory store!
    """
    ticket = expert_manager.resolve_ticket(ticket_id, req)
    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")
    return ticket


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=True)
