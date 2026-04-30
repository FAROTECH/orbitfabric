from __future__ import annotations

from orbitfabric.lint.finding import LintFinding
from orbitfabric.model.mission import Event, MissionModel


def check_events(model: MissionModel) -> list[LintFinding]:
    """Check event engineering consistency."""
    findings: list[LintFinding] = []

    for event in model.events:
        findings.extend(_check_downlink_priority(event))
        findings.extend(_check_persistence(event))

    return findings


def _check_downlink_priority(event: Event) -> list[LintFinding]:
    if event.downlink_priority is not None:
        return []

    return [
        LintFinding(
            severity="WARNING",
            code="OF-EVT-002",
            file="events.yaml",
            domain="events",
            object_id=event.id,
            message="event should define downlink priority",
            suggestion="Add downlink_priority to the event definition.",
        )
    ]


def _check_persistence(event: Event) -> list[LintFinding]:
    if event.persistence is not None:
        return []

    return [
        LintFinding(
            severity="WARNING",
            code="OF-EVT-003",
            file="events.yaml",
            domain="events",
            object_id=event.id,
            message="event should define persistence policy",
            suggestion="Add persistence to the event definition.",
        )
    ]