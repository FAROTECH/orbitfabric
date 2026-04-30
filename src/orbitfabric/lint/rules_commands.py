from __future__ import annotations

from orbitfabric.lint.finding import LintFinding
from orbitfabric.model.mission import Command, MissionModel

RISKY_COMMAND_LEVELS = {"medium", "high", "critical"}


def check_commands(model: MissionModel) -> list[LintFinding]:
    """Check command engineering consistency."""
    findings: list[LintFinding] = []

    for command in model.commands:
        findings.extend(_check_timeout(command))
        findings.extend(_check_expected_effects(command))
        findings.extend(_check_safe_mode_risk(command))

    return findings


def _check_timeout(command: Command) -> list[LintFinding]:
    if command.timeout_ms is not None:
        return []

    return [
        LintFinding(
            severity="WARNING",
            code="OF-CMD-005",
            file="commands.yaml",
            domain="commands",
            object_id=command.id,
            message="command should define timeout_ms",
            suggestion="Add timeout_ms to make command behavior testable.",
        )
    ]


def _check_expected_effects(command: Command) -> list[LintFinding]:
    if command.expected_effects:
        return []

    return [
        LintFinding(
            severity="WARNING",
            code="OF-CMD-006",
            file="commands.yaml",
            domain="commands",
            object_id=command.id,
            message="command should define expected effects",
            suggestion="Add expected_effects or explicitly justify no expected effects.",
        )
    ]


def _check_safe_mode_risk(command: Command) -> list[LintFinding]:
    if command.risk not in RISKY_COMMAND_LEVELS:
        return []

    if "SAFE" not in command.allowed_modes:
        return []

    return [
        LintFinding(
            severity="ERROR",
            code="OF-CMD-007",
            file="commands.yaml",
            domain="commands",
            object_id=command.id,
            message="medium/high/critical-risk command is allowed in SAFE mode",
            suggestion="Remove SAFE from allowed_modes or lower the command risk.",
        )
    ]