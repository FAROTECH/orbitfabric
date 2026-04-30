from __future__ import annotations

from orbitfabric.lint.finding import LintFinding
from orbitfabric.model.mission import Fault, MissionModel


def check_faults(model: MissionModel) -> list[LintFinding]:
    """Check fault engineering consistency."""
    findings: list[LintFinding] = []

    for fault in model.faults:
        findings.extend(_check_fault_emits_event(fault))

    return findings


def _check_fault_emits_event(fault: Fault) -> list[LintFinding]:
    if fault.emits:
        return []

    return [
        LintFinding(
            severity="ERROR",
            code="OF-FLT-003",
            file="faults.yaml",
            domain="faults",
            object_id=fault.id,
            message="fault must emit at least one event",
            suggestion="Add at least one event ID to the fault emits list.",
        )
    ]