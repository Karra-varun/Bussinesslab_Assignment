"""
Developer Estimator Agent for Task 3: Meeting to Scope of Work.
Breaks down custom requirements into engineering tasks with hour estimates,
roles, hourly rates, and total costs.
"""
from typing import List, Tuple
from app.models import RequirementItem, DeveloperTask
from app.config import settings


class DeveloperEstimatorAgent:
    def estimate_tasks(self, requirements: List[RequirementItem]) -> Tuple[List[DeveloperTask], float, float]:
        tasks: List[DeveloperTask] = []
        task_counter = 1
        rate = settings.developer_hourly_rate

        for req in requirements:
            if req.resolution_type != "CUSTOM_DEVELOPMENT":
                continue

            # Subdivide requirement into realistic engineering tasks
            title_lower = req.title.lower()

            if "theme" in title_lower or "css" in title_lower:
                tasks.append(DeveloperTask(
                    task_id=f"DEV-{task_counter:03d}",
                    requirement_id=req.id,
                    title="Design System & Typography Overrides",
                    description="Implement brand fonts, color tokens, and header/footer CSS styling.",
                    role="Frontend/UI Engineer",
                    hours=8.0,
                    hourly_rate=rate,
                    total_cost=round(8.0 * rate, 2)
                ))
                task_counter += 1
                tasks.append(DeveloperTask(
                    task_id=f"DEV-{task_counter:03d}",
                    requirement_id=req.id,
                    title="Mobile Responsive QA & Viewport Audit",
                    description="Cross-browser testing across iOS Safari and Android Chrome.",
                    role="QA Specialist",
                    hours=4.0,
                    hourly_rate=rate,
                    total_cost=round(4.0 * rate, 2)
                ))
                task_counter += 1

            elif "webhook" in title_lower:
                tasks.append(DeveloperTask(
                    task_id=f"DEV-{task_counter:03d}",
                    requirement_id=req.id,
                    title="Outgoing Event Webhook Dispatcher",
                    description="Develop secure POST webhook payload dispatcher with HMAC signature.",
                    role="Backend/Integration Engineer",
                    hours=10.0,
                    hourly_rate=rate,
                    total_cost=round(10.0 * rate, 2)
                ))
                task_counter += 1
                tasks.append(DeveloperTask(
                    task_id=f"DEV-{task_counter:03d}",
                    requirement_id=req.id,
                    title="HIPAA Audit Payload Logging & Error Retry",
                    description="Configure retry queue and structured JSON logging for HIPAA compliance.",
                    role="Solutions Architect",
                    hours=6.0,
                    hourly_rate=rate,
                    total_cost=round(6.0 * rate, 2)
                ))
                task_counter += 1

            elif "migration" in title_lower or "sanitization" in title_lower:
                tasks.append(DeveloperTask(
                    task_id=f"DEV-{task_counter:03d}",
                    requirement_id=req.id,
                    title="CSV Data Cleansing & Deduplication Script",
                    description="Python script to validate 2,500 doctor NPI records and remove duplicates.",
                    role="Backend/Integration Engineer",
                    hours=10.0,
                    hourly_rate=rate,
                    total_cost=round(10.0 * rate, 2)
                ))
                task_counter += 1
                tasks.append(DeveloperTask(
                    task_id=f"DEV-{task_counter:03d}",
                    requirement_id=req.id,
                    title="Geocoding Batch Import & Validation",
                    description="Batch geocode clinic latitude/longitude coordinates and verify map pins.",
                    role="QA Specialist",
                    hours=4.0,
                    hourly_rate=rate,
                    total_cost=round(4.0 * rate, 2)
                ))
                task_counter += 1

            elif "telehealth" in title_lower:
                tasks.append(DeveloperTask(
                    task_id=f"DEV-{task_counter:03d}",
                    requirement_id=req.id,
                    title="Authenticated Telehealth Launch Button Widget",
                    description="Custom profile widget verifying logged-in parent session before rendering video link.",
                    role="Frontend/UI Engineer",
                    hours=6.0,
                    hourly_rate=rate,
                    total_cost=round(6.0 * rate, 2)
                ))
                task_counter += 1
                tasks.append(DeveloperTask(
                    task_id=f"DEV-{task_counter:03d}",
                    requirement_id=req.id,
                    title="Telehealth Session Security QA",
                    description="Verify unauthenticated visitors cannot inspect or access video consult URLs.",
                    role="QA Specialist",
                    hours=2.0,
                    hourly_rate=rate,
                    total_cost=round(2.0 * rate, 2)
                ))
                task_counter += 1

            elif "fhir" in title_lower or "epic" in title_lower:
                tasks.append(DeveloperTask(
                    task_id=f"DEV-{task_counter:03d}",
                    requirement_id=req.id,
                    title="SMART-on-FHIR OAuth 2.0 Auth Bridge",
                    description="Enterprise OAuth 2.0 connection to Epic hospital gateway.",
                    role="Solutions Architect",
                    hours=20.0,
                    hourly_rate=rate,
                    total_cost=round(20.0 * rate, 2)
                ))
                task_counter += 1
                tasks.append(DeveloperTask(
                    task_id=f"DEV-{task_counter:03d}",
                    requirement_id=req.id,
                    title="HL7 / FHIR Resource Mapping & Sync Engine",
                    description="Bidirectional sync for Practitioner and Appointment resources.",
                    role="Backend/Integration Engineer",
                    hours=30.0,
                    hourly_rate=rate,
                    total_cost=round(30.0 * rate, 2)
                ))
                task_counter += 1
                tasks.append(DeveloperTask(
                    task_id=f"DEV-{task_counter:03d}",
                    requirement_id=req.id,
                    title="Sandbox End-to-End Compliance Testing",
                    description="Integration testing in Epic sandbox environment.",
                    role="QA Specialist",
                    hours=10.0,
                    hourly_rate=rate,
                    total_cost=round(10.0 * rate, 2)
                ))
                task_counter += 1

            else:
                tasks.append(DeveloperTask(
                    task_id=f"DEV-{task_counter:03d}",
                    requirement_id=req.id,
                    title=f"Custom Development for {req.title}",
                    description=req.consultant_notes,
                    role="Backend/Integration Engineer",
                    hours=req.estimated_hours,
                    hourly_rate=rate,
                    total_cost=round(req.estimated_hours * rate, 2)
                ))
                task_counter += 1

        total_hours = sum(t.hours for t in tasks)
        total_cost = sum(t.total_cost for t in tasks)
        return tasks, total_hours, total_cost


estimator_agent = DeveloperEstimatorAgent()
