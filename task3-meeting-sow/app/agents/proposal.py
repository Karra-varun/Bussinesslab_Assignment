"""
Proposal & SOW Generator Agent for Task 3: Meeting to Scope of Work.
Generates:
1. Formal Scope of Work (SOW)
2. Granular Developer Task List with Hour Estimates
3. Client-Ready Executive Proposal
4. Human Approval Workflow enforcement
"""
import uuid
from datetime import datetime, timezone
from typing import Optional
from app.models import ScopeOfWork, Proposal, ScopeDeltaReport


class ProposalGeneratorAgent:
    def assemble_proposal(
        self,
        sow: ScopeOfWork,
        delta_report: Optional[ScopeDeltaReport] = None
    ) -> Proposal:
        proposal_id = f"PROP-{uuid.uuid4().hex[:6].upper()}"

        markdown_lines = []
        markdown_lines.append(f"# Executive Proposal & Scope of Work")
        markdown_lines.append(f"**Project**: {sow.project_name}")
        markdown_lines.append(f"**Client**: {sow.client_name}")
        markdown_lines.append(f"**Prepared by**: Applied AI Tech Consultancy (@BusinessLabs)")
        markdown_lines.append(f"**Date**: {datetime.now(timezone.utc).strftime('%B %d, %Y')}")
        markdown_lines.append(f"**Proposal ID**: `{proposal_id}`\n")
        markdown_lines.append(f"---\n")

        markdown_lines.append(f"## 1. Executive Summary")
        markdown_lines.append(f"{sow.executive_summary}\n")

        markdown_lines.append(f"## 2. Architectural Efficiency Strategy (Settings vs Custom Code)")
        markdown_lines.append(
            f"By leveraging the native capabilities of Brilliant Directories, our team was able to map "
            f"**{sow.total_native_settings} core requirements** directly to out-of-the-box admin settings ($0 development cost). "
            f"Only **{sow.total_custom_tasks} specialized capabilities** require custom engineering code, saving the client thousands in unnecessary development fees.\n"
        )

        markdown_lines.append(f"## 3. Scope of Work & Feature Architecture")
        for req in sow.requirements:
            icon = "⚙️ [Native Setting - $0]" if req.resolution_type == "NATIVE_SETTING" else "💻 [Custom Code]"
            markdown_lines.append(f"### {req.title} {icon}")
            markdown_lines.append(f"**Client Request**: *\"{req.client_wording}\"*")
            markdown_lines.append(f"**Category**: {req.category}")
            if req.resolution_type == "NATIVE_SETTING":
                markdown_lines.append(f"**Admin Location**: `{req.setting_location or 'Dashboard Settings'}`")
                if req.kb_article_url:
                    markdown_lines.append(f"**Documentation Reference**: [{req.kb_article_title or 'Help Center Guide'}]({req.kb_article_url})")
            else:
                markdown_lines.append(f"**Engineering Complexity**: {req.complexity} | **Estimated Hours**: {req.estimated_hours} hrs")
            markdown_lines.append(f"**Consultant Notes**: {req.consultant_notes}\n")

        markdown_lines.append(f"## 4. Engineering Tasks & Developer Estimates")
        markdown_lines.append(f"| Task ID | Description | Role | Hours | Cost |")
        markdown_lines.append(f"|---------|-------------|------|-------|------|")
        for t in sow.developer_tasks:
            markdown_lines.append(f"| `{t.task_id}` | {t.title} | {t.role} | {t.hours:.1f} hrs | ${t.total_cost:,.2f} |")
        markdown_lines.append(f"| **TOTAL** | **All Engineering Tasks** | **Multi-Role Team** | **{sow.total_estimated_hours:.1f} hrs** | **${sow.total_estimated_cost:,.2f}** |\n")

        if delta_report:
            markdown_lines.append(f"## 5. Follow-Up Meeting Delta & Scope Change Analysis")
            markdown_lines.append(f"{delta_report.executive_delta_summary}\n")
            markdown_lines.append(f"| Requirement | Status | Original | Revised | Cost Delta |")
            markdown_lines.append(f"|-------------|--------|----------|---------|------------|")
            for d in delta_report.diff_items:
                badge = d.status
                if d.status == "OUT_OF_SCOPE_EXTRA":
                    badge = "🚨 OUT OF SCOPE (Phase 2 Addendum)"
                markdown_lines.append(f"| {d.title} | **{badge}** | {d.original_hours:.1f} hrs | {d.new_hours:.1f} hrs | ${d.cost_difference:+,.2f} |")
            markdown_lines.append(f"\n**Net Phase 1 Adjustment**: {delta_report.total_hours_delta:+.1f} hrs (${delta_report.total_cost_delta:+,.2f})\n")

        markdown_lines.append(f"## 6. Project Timeline & Delivery Milestones")
        markdown_lines.append(f"- **Week 1**: Architecture validation, Stripe gateway authentication, and category taxonomy import.")
        markdown_lines.append(f"- **Week 2**: Custom design theme implementation and mobile responsiveness QA.")
        markdown_lines.append(f"- **Week 3**: Outgoing webhook dispatcher and doctor CSV data cleansing.")
        markdown_lines.append(f"- **Week 4**: End-to-end user acceptance testing, payment simulation, and live production launch.\n")

        markdown_lines.append(f"## 7. Investment Summary & Approval Gate")
        markdown_lines.append(f"- **Total Estimated Hours**: {sow.total_estimated_hours:.1f} hrs")
        markdown_lines.append(f"- **Total Phase 1 Investment**: **${sow.total_estimated_cost:,.2f}**")
        markdown_lines.append(f"- **Human Approval Status**: 🔒 *Pending Senior Consultant Sign-Off*\n")

        client_markdown = "\n".join(markdown_lines)

        return Proposal(
            proposal_id=proposal_id,
            sow=sow,
            delta_report=delta_report,
            is_approved_by_human=False,
            approved_at=None,
            approved_by=None,
            client_ready_markdown=client_markdown
        )


proposal_generator = ProposalGeneratorAgent()
