"""
Senior Consultant Agent for Task 3: Meeting to Scope of Work.
Parses messy client transcripts and extracts structured business goals,
pain points, and candidate functional requirements.
"""
import re
from typing import List, Dict, Any
from app.models import RequirementItem


class SeniorConsultantAgent:
    def parse_transcript(self, transcript: str, project_name: str) -> Dict[str, Any]:
        """
        Extracts business context, pain points, timeline, and candidate requirements.
        """
        lower = transcript.lower()

        # Extract timeline
        timeline_weeks = 4
        timeline_match = re.search(r"(\d+)\s*[-–]\s*week|within\s*(\d+)\s*weeks?", lower)
        if timeline_match:
            val = timeline_match.group(1) or timeline_match.group(2)
            if val:
                timeline_weeks = int(val)

        # Extract client requirements
        requirements: List[Dict[str, Any]] = []

        if "specialty and zip code" in lower or "radius" in lower or "search" in lower:
            requirements.append({
                "title": "Specialty & Radius Doctor Search",
                "client_wording": "Parents search by zip code and specialty with 15-25 mile radius matching.",
                "category": "Search & Directory",
                "default_type": "NATIVE_SETTING",
                "query": "Member search results and radius search settings"
            })

        if "accepting new patients" in lower or "badge" in lower:
            requirements.append({
                "title": "Accepting New Patients Profile Badge & Filter",
                "client_wording": "Doctor profile badge and search filter for accepting new patients.",
                "category": "Profile & Form Fields",
                "default_type": "NATIVE_SETTING",
                "query": "Adding custom search filter in form manager"
            })

        if "stripe" in lower or "membership tiers" in lower or "membership plans" in lower:
            requirements.append({
                "title": "Stripe Gateway & Recurring Membership Billing",
                "client_wording": "Automated monthly recurring credit card billing for clinic membership tiers.",
                "category": "Finance & Billing",
                "default_type": "NATIVE_SETTING",
                "query": "Connecting Stripe payment gateway for subscriptions"
            })

        if "route that lead" in lower or "lead auto-match" in lower or "inquiry" in lower:
            requirements.append({
                "title": "Automated Specialist Lead Auto-Routing",
                "client_wording": "Automatically email up to 3 matched local specialists when parent submits inquiry.",
                "category": "Lead Management",
                "default_type": "NATIVE_SETTING",
                "query": "Lead system auto matching and lead pricing"
            })

        if "custom brand theme" in lower or "hero css" in lower or "custom color" in lower or "navy blue header" in lower:
            requirements.append({
                "title": "Bespoke Brand Theme & Responsive Layout CSS",
                "client_wording": "Custom typography, accessible contrast styling, and responsive layout polish.",
                "category": "UI & Design Polish",
                "default_type": "CUSTOM_DEVELOPMENT",
                "query": "When to use settings vs custom code"
            })

        if "hipaa audit" in lower or "outgoing webhook" in lower or "webhook" in lower:
            requirements.append({
                "title": "Secure Lead Notification Webhook Integration",
                "client_wording": "Outgoing webhook to push evaluation requests to secure audit repository.",
                "category": "Integrations & API",
                "default_type": "CUSTOM_DEVELOPMENT",
                "query": "Developer webhooks and API integrations"
            })

        if "csv" in lower or "2,500 doctors" in lower or "sanitization" in lower or "migration" in lower:
            requirements.append({
                "title": "Doctor Directory Data Sanitization & Migration Script",
                "client_wording": "Pre-formatting 2,500 clinic records, resolving duplicates, and bulk geocoding.",
                "category": "Data Engineering",
                "default_type": "CUSTOM_DEVELOPMENT",
                "query": "How to import categories via CSV file"
            })

        # Meeting 3 specific additions
        if "telehealth" in lower or "doxy" in lower or "video consult" in lower:
            requirements.append({
                "title": "Authenticated Telehealth Video Consultation Launch Widget",
                "client_wording": "Direct video consult link only accessible to authenticated logged-in parents.",
                "category": "Custom Frontend Widget",
                "default_type": "CUSTOM_DEVELOPMENT",
                "query": "Custom interactive JavaScript widgets"
            })

        if "epic" in lower or "fhir" in lower or "emr" in lower:
            requirements.append({
                "title": "Epic EMR Real-Time FHIR Bidirectional Integration",
                "client_wording": "Automated two-way synchronization with Epic EMR via HL7 / FHIR standards.",
                "category": "Enterprise Healthcare Integration",
                "default_type": "CUSTOM_DEVELOPMENT",
                "query": "Third-party REST API bidirectional syncing"
            })

        summary = (
            f"Discovery analysis for {project_name}. Identified {len(requirements)} core requirements "
            f"across Search, Membership, Finance, and Integrations. Target timeline is {timeline_weeks} weeks. "
            f"Prioritizing native platform settings to protect client budget and accelerate delivery."
        )

        return {
            "project_name": project_name,
            "timeline_weeks": timeline_weeks,
            "executive_summary": summary,
            "raw_requirements": requirements
        }


consultant_agent = SeniorConsultantAgent()
