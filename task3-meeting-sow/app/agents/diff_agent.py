"""
Scope Auditor & Delta Agent for Task 3: Meeting to Scope of Work.
Compares Meeting 1 baseline against Follow-Up Meeting revisions:
- Identifies UNCHANGED items.
- Identifies MODIFIED items.
- Identifies NEW_REQUEST items.
- Detects OUT_OF_SCOPE_EXTRA scope creep and quotes it as a separate Change Order!
"""
from typing import List
from app.models import ScopeOfWork, ScopeDiffItem, ScopeDeltaReport, RequirementItem


class ScopeAuditorDiffAgent:
    def compare_meetings(
        self,
        baseline_sow: ScopeOfWork,
        followup_requirements: List[RequirementItem],
        followup_meeting_name: str = "Meeting 3 (Follow-up Scope Changes)"
    ) -> ScopeDeltaReport:
        diff_items: List[ScopeDiffItem] = []
        baseline_map = {r.title.lower(): r for r in baseline_sow.requirements}
        followup_map = {r.title.lower(): r for r in followup_requirements}

        rate = 125.0

        # Check existing baseline requirements against follow-up
        for b_title, b_req in baseline_map.items():
            if b_title in followup_map:
                f_req = followup_map[b_title]
                if f_req.estimated_hours != b_req.estimated_hours:
                    diff_items.append(ScopeDiffItem(
                        item_id=b_req.id,
                        title=b_req.title,
                        status="MODIFIED",
                        original_hours=b_req.estimated_hours,
                        new_hours=f_req.estimated_hours,
                        cost_difference=round((f_req.estimated_hours - b_req.estimated_hours) * rate, 2),
                        reasoning=f"Hours adjusted based on follow-up discussion. {f_req.consultant_notes}",
                        is_extra_quoted=False
                    ))
                else:
                    diff_items.append(ScopeDiffItem(
                        item_id=b_req.id,
                        title=b_req.title,
                        status="UNCHANGED",
                        original_hours=b_req.estimated_hours,
                        new_hours=b_req.estimated_hours,
                        cost_difference=0.0,
                        reasoning="Confirmed requirement carries forward unchanged from baseline agreement.",
                        is_extra_quoted=False
                    ))
            else:
                # Dropped or deferred
                diff_items.append(ScopeDiffItem(
                    item_id=b_req.id,
                    title=b_req.title,
                    status="REMOVED",
                    original_hours=b_req.estimated_hours,
                    new_hours=0.0,
                    cost_difference=round(-b_req.estimated_hours * rate, 2),
                    reasoning="Client requested to postpone or remove this item from Phase 1 launch scope.",
                    is_extra_quoted=False
                ))

        # Check for new requirements in follow-up not in baseline
        for f_title, f_req in followup_map.items():
            if f_title not in baseline_map:
                # Detect whether this is regular new request or out-of-scope extra
                if "fhir" in f_title or "epic" in f_title or "emr" in f_title:
                    diff_items.append(ScopeDiffItem(
                        item_id=f_req.id,
                        title=f_req.title,
                        status="OUT_OF_SCOPE_EXTRA",
                        original_hours=0.0,
                        new_hours=f_req.estimated_hours,
                        cost_difference=round(f_req.estimated_hours * rate, 2),
                        reasoning=(
                            "🚨 SCOPE CREEP DETECTED: Enterprise Epic EMR / FHIR integration represents "
                            "significant architecture complexity that threatens the 4-week launch timeline. "
                            "Quoted as an optional Phase 2 Addendum Change Order."
                        ),
                        is_extra_quoted=True
                    ))
                else:
                    diff_items.append(ScopeDiffItem(
                        item_id=f_req.id,
                        title=f_req.title,
                        status="NEW_REQUEST",
                        original_hours=0.0,
                        new_hours=f_req.estimated_hours,
                        cost_difference=round(f_req.estimated_hours * rate, 2),
                        reasoning="New functional request added during follow-up meeting and incorporated into Phase 1.",
                        is_extra_quoted=False
                    ))

        # Calculate totals
        hours_delta = sum(
            (item.new_hours - item.original_hours) for item in diff_items if not item.is_extra_quoted
        )
        cost_delta = round(hours_delta * rate, 2)
        has_creep = any(item.status == "OUT_OF_SCOPE_EXTRA" for item in diff_items)

        summary = (
            f"Delta Analysis between {baseline_sow.project_name} baseline and {followup_meeting_name}: "
            f"{sum(1 for i in diff_items if i.status == 'UNCHANGED')} items unchanged, "
            f"{sum(1 for i in diff_items if i.status == 'NEW_REQUEST')} new in-scope additions, "
            f"{sum(1 for i in diff_items if i.status == 'REMOVED')} deferred items, and "
            f"{sum(1 for i in diff_items if i.status == 'OUT_OF_SCOPE_EXTRA')} out-of-scope item quoted separately. "
            f"Net Phase 1 hours adjustment: {hours_delta:+.1f} hours (${cost_delta:+,.2f})."
        )

        return ScopeDeltaReport(
            baseline_meeting_name=baseline_sow.project_name,
            followup_meeting_name=followup_meeting_name,
            diff_items=diff_items,
            total_hours_delta=hours_delta,
            total_cost_delta=cost_delta,
            scope_creep_detected=has_creep,
            executive_delta_summary=summary
        )


diff_agent = ScopeAuditorDiffAgent()
