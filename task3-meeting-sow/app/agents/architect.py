"""
Solution Architect Agent for Task 3: Meeting to Scope of Work.
Cross-references client requirements against Task 1's Knowledge Brain API
to classify each item into NATIVE_SETTING vs CUSTOM_DEVELOPMENT.
"""
from typing import List, Dict, Any
from app.models import RequirementItem
from app.kb_client import kb_client


class SolutionArchitectAgent:
    async def evaluate_requirements(self, raw_items: List[Dict[str, Any]]) -> List[RequirementItem]:
        evaluated: List[RequirementItem] = []

        for idx, item in enumerate(raw_items, 1):
            req_id = f"REQ-{idx:02d}"
            query_text = item.get("query", item["title"])

            # Query Task 1 Knowledge Brain API
            kb_resp = await kb_client.check_feature(query_text)
            citations = kb_resp.get("citations", [])

            # Determine resolution type
            is_native = item.get("default_type") == "NATIVE_SETTING"
            kb_title = None
            kb_url = None
            setting_loc = None

            if citations:
                top_c = citations[0]
                kb_title = top_c.get("title")
                kb_url = top_c.get("url")
                setting_loc = f"{top_c.get('category')} > {top_c.get('folder')}"
                if "setting" in (top_c.get("title", "") + top_c.get("snippet", "")).lower():
                    is_native = True

            # Custom exceptions that require development
            if any(term in item["title"].lower() for term in ["theme", "css", "migration", "webhook", "telehealth", "fhir", "epic"]):
                is_native = False

            res_type = "NATIVE_SETTING" if is_native else "CUSTOM_DEVELOPMENT"

            if res_type == "NATIVE_SETTING":
                complexity = "NONE"
                hours = 0.0
                notes = (
                    "Fully supported natively out-of-the-box in Brilliant Directories admin panel. "
                    "Zero custom code required ($0 cost), saving the client significant budget."
                )
            else:
                lower_title = item["title"].lower()
                if "fhir" in lower_title or "epic" in lower_title:
                    complexity = "HIGH"
                    hours = 60.0
                    notes = "Enterprise API bidirectional integration. Requires OAuth2 authentication, FHIR data models, and staging sandbox certification."
                elif "webhook" in lower_title:
                    complexity = "MEDIUM"
                    hours = 16.0
                    notes = "Outgoing event listener with HMAC signature verification and payload delivery queue."
                elif "migration" in lower_title or "sanitization" in lower_title:
                    complexity = "MEDIUM"
                    hours = 14.0
                    notes = "Custom Python script to normalize doctor CSV taxonomy, de-duplicate records, and geocode addresses."
                elif "telehealth" in lower_title:
                    complexity = "LOW"
                    hours = 8.0
                    notes = "Custom profile template widget checking user session before rendering launch button."
                else:
                    complexity = "LOW"
                    hours = 12.0
                    notes = "Custom CSS theme overrides for typography, color palette, and mobile responsiveness."

            evaluated.append(RequirementItem(
                id=req_id,
                title=item["title"],
                client_wording=item["client_wording"],
                category=item["category"],
                resolution_type=res_type,
                kb_article_title=kb_title,
                kb_article_url=kb_url,
                setting_location=setting_loc,
                complexity=complexity,
                estimated_hours=hours,
                consultant_notes=notes
            ))

        return evaluated


architect_agent = SolutionArchitectAgent()
