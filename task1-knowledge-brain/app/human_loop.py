"""
Human-in-the-Loop Expert Escalation and Continuous Learning Engine.
Handles:
1. Creating expert escalation tickets when chatbot confidence falls below threshold.
2. Managing expert queue (listing pending/resolved tickets).
3. Resolving tickets: Expert provides verified solution.
4. Auto-ingesting the expert's resolution back into RAG knowledge memory with top authority!
"""
import json
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Optional
from app.config import TICKETS_DIR
from app.models import ExpertTicket, ResolveTicketRequest
from app.rag import rag_store


class ExpertFeedbackManager:
    def __init__(self):
        self.tickets: Dict[str, ExpertTicket] = {}
        self._load_persisted_tickets()

    def _load_persisted_tickets(self):
        for ticket_path in TICKETS_DIR.glob("*.json"):
            try:
                with open(ticket_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    t = ExpertTicket(**data)
                    self.tickets[t.ticket_id] = t
                    if t.status == "RESOLVED" and t.expert_answer:
                        rag_store.index_expert_answer(
                            ticket_id=t.ticket_id,
                            question=t.question,
                            answer=t.expert_answer,
                            category=t.category
                        )
            except Exception:
                pass

    def create_ticket(self, question: str, context: str = "", category: str = "Unassigned") -> ExpertTicket:
        """Create a new human expert task."""
        ticket_id = f"TICK-{uuid.uuid4().hex[:6].upper()}"
        ticket = ExpertTicket(
            ticket_id=ticket_id,
            question=question,
            context=context,
            category=category,
            status="OPEN",
            created_at=datetime.now(timezone.utc).isoformat()
        )
        self.tickets[ticket_id] = ticket
        self._save_ticket(ticket)
        return ticket

    def list_tickets(self, status: Optional[str] = None) -> List[ExpertTicket]:
        items = list(self.tickets.values())
        if status:
            items = [t for t in items if t.status.upper() == status.upper()]
        items.sort(key=lambda t: t.created_at, reverse=True)
        return items

    def get_ticket(self, ticket_id: str) -> Optional[ExpertTicket]:
        return self.tickets.get(ticket_id)

    def resolve_ticket(self, ticket_id: str, req: ResolveTicketRequest) -> Optional[ExpertTicket]:
        """Expert answers the ticket; answer flows back into memory immediately."""
        ticket = self.tickets.get(ticket_id)
        if not ticket:
            return None

        ticket.status = "RESOLVED"
        ticket.resolved_at = datetime.now(timezone.utc).isoformat()
        ticket.resolved_by = req.expert_name
        ticket.expert_answer = req.answer
        if req.category:
            ticket.category = req.category

        self._save_ticket(ticket)

        # Ingest verified answer into RAG memory store
        rag_store.index_expert_answer(
            ticket_id=ticket.ticket_id,
            question=ticket.question,
            answer=req.answer,
            category=ticket.category
        )

        return ticket

    def _save_ticket(self, ticket: ExpertTicket):
        target_path = TICKETS_DIR / f"{ticket.ticket_id}.json"
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(ticket.model_dump(), f, indent=2)


expert_manager = ExpertFeedbackManager()
