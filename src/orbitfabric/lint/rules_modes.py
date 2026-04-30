from __future__ import annotations

from orbitfabric.lint.finding import LintFinding
from orbitfabric.model.mission import MissionModel


def check_modes(model: MissionModel) -> list[LintFinding]:
    """Check operational mode consistency."""
    findings: list[LintFinding] = []
    mode_ids = model.mode_ids

    initial_modes = [mode_id for mode_id, mode in model.modes.items() if mode.initial]

    if len(initial_modes) != 1:
        findings.append(
            LintFinding(
                severity="ERROR",
                code="OF-MODE-001",
                file="modes.yaml",
                domain="modes",
                message=(
                    "exactly one initial mode must be defined "
                    f"but found {len(initial_modes)}"
                ),
                suggestion="Set initial: true on exactly one mode.",
            )
        )

    for transition in model.mode_transitions:
        if transition.from_mode not in mode_ids:
            findings.append(
                LintFinding(
                    severity="ERROR",
                    code="OF-MODE-003",
                    file="modes.yaml",
                    domain="mode_transitions",
                    object_id=transition.reason,
                    message=f"mode transition source '{transition.from_mode}' is not a known mode",
                    suggestion="Add the source mode to modes.yaml or fix the transition.",
                )
            )

        if transition.to not in mode_ids:
            findings.append(
                LintFinding(
                    severity="ERROR",
                    code="OF-MODE-003",
                    file="modes.yaml",
                    domain="mode_transitions",
                    object_id=transition.reason,
                    message=f"mode transition target '{transition.to}' is not a known mode",
                    suggestion="Add the target mode to modes.yaml or fix the transition.",
                )
            )

    return findings