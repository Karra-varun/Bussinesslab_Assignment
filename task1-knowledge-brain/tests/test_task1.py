"""
Unit and integration tests for Task 1: The Knowledge Brain.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.rag import rag_store
from app.models import Article


@pytest.mark.asyncio
async def test_health_check():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/v1/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "healthy"
        assert data["indexed_articles"] >= 5


@pytest.mark.asyncio
async def test_query_grounded_answer():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/api/v1/query", json={
            "query": "Where do I configure the social media tab in settings?",
            "top_k": 3
        })
        assert res.status_code == 200
        data = res.json()
        assert data["is_fallback"] is False
        assert len(data["citations"]) > 0
        assert "social media" in data["answer"].lower()
        # Verify citation has valid fields
        citation = data["citations"][0]
        assert citation["title"]
        assert citation["url"]
        assert citation["relevance_score"] > 0.3


@pytest.mark.asyncio
async def test_query_low_confidence_fallback_and_ticket_creation():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/api/v1/query", json={
            "query": "How do I deploy a quantum blockchain smart contract on Mars?",
            "top_k": 3
        })
        assert res.status_code == 200
        data = res.json()
        assert data["is_fallback"] is True
        assert data["human_ticket_id"] is not None
        assert "TICK-" in data["human_ticket_id"]


@pytest.mark.asyncio
async def test_expert_ticket_resolution_and_continuous_learning():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Step 1: Create a ticket
        ticket_res = await client.post("/api/v1/expert-tickets?question=What+is+the+VIP+Enterprise+SLA+refund+period%3F")
        assert ticket_res.status_code == 200
        ticket_id = ticket_res.json()["ticket_id"]

        # Step 2: Resolve the ticket with verified expert answer
        resolve_res = await client.post(f"/api/v1/expert-tickets/{ticket_id}/resolve", json={
            "answer": "VIP Enterprise SLA refunds are processed within exactly 48 hours via Finance > Concierge.",
            "expert_name": "Senior Partner Consultant",
            "category": "Enterprise Billing"
        })
        assert resolve_res.status_code == 200
        assert resolve_res.json()["status"] == "RESOLVED"

        # Step 3: Query the same question - it should now retrieve the expert verified answer!
        query_res = await client.post("/api/v1/query", json={
            "query": "What is the VIP Enterprise SLA refund period?",
            "top_k": 3
        })
        assert query_res.status_code == 200
        qdata = query_res.json()
        assert qdata["is_fallback"] is False
        assert "48 hours" in qdata["answer"]


@pytest.mark.asyncio
async def test_purge_removed_articles():
    # Artificially add a temporary article
    temp_art = Article(
        id="temp_99999",
        url="https://support.brilliantdirectories.com/support/solutions/articles/99999-obsolete-feature",
        title="Obsolete Deprecated Feature",
        category="Deprecated",
        folder="Old",
        content_text="This feature has been deprecated.",
        content_hash="hash999"
    )
    rag_store.index_articles([temp_art])
    assert "temp_99999" in rag_store.articles

    # Purge it
    rag_store.remove_article("temp_99999")
    assert "temp_99999" not in rag_store.articles
