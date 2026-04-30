from __future__ import annotations

from orbitfabric.lint.finding import LintFinding
from orbitfabric.model.mission import MissionModel, TelemetryItem

NUMERIC_TYPES = {
    "uint8",
    "uint16",
    "uint32",
    "int8",
    "int16",
    "int32",
    "float32",
    "float64",
}


def check_telemetry(model: MissionModel) -> list[LintFinding]:
    """Check telemetry engineering consistency."""
    findings: list[LintFinding] = []

    for item in model.telemetry:
        findings.extend(_check_high_criticality_limits(item))
        findings.extend(_check_enum_values(item))
        findings.extend(_check_quality_policy(item))

    return findings


def _check_high_criticality_limits(item: TelemetryItem) -> list[LintFinding]:
    if item.type not in NUMERIC_TYPES:
        return []

    if item.criticality not in {"high", "critical"}:
        return []

    if item.limits is not None:
        return []

    return [
        LintFinding(
            severity="ERROR",
            code="OF-TLM-001",
            file="telemetry.yaml",
            domain="telemetry",
            object_id=item.id,
            message="high/critical numeric telemetry must define operational limits",
            suggestion="Add warning or critical limits to the telemetry item.",
        )
    ]


def _check_enum_values(item: TelemetryItem) -> list[LintFinding]:
    if item.type != "enum":
        return []

    if item.enum:
        return []

    return [
        LintFinding(
            severity="ERROR",
            code="OF-TLM-006",
            file="telemetry.yaml",
            domain="telemetry",
            object_id=item.id,
            message="enum telemetry must define enum values",
            suggestion="Add a non-empty enum list to the telemetry item.",
        )
    ]


def _check_quality_policy(item: TelemetryItem) -> list[LintFinding]:
    if item.quality is not None:
        return []

    return [
        LintFinding(
            severity="WARNING",
            code="OF-TLM-007",
            file="telemetry.yaml",
            domain="telemetry",
            object_id=item.id,
            message="telemetry quality policy should be defined",
            suggestion="Add a quality policy with required/default fields.",
        )
    ]