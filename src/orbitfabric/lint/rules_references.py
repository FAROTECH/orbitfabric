from __future__ import annotations

from orbitfabric.lint.finding import LintFinding
from orbitfabric.model.mission import MissionModel


def check_references(model: MissionModel) -> list[LintFinding]:
    """Check cross-file Mission Model references."""
    findings: list[LintFinding] = []

    subsystem_ids = model.subsystem_ids
    telemetry_ids = model.telemetry_ids
    event_ids = model.event_ids
    command_ids = model.command_ids
    mode_ids = model.mode_ids

    for item in model.telemetry:
        if item.source not in subsystem_ids:
            findings.append(
                LintFinding(
                    severity="ERROR",
                    code="OF-REF-001",
                    file="telemetry.yaml",
                    domain="telemetry",
                    object_id=item.id,
                    message=(
                        f"telemetry source '{item.source}' does not reference "
                        "an existing subsystem"
                    ),
                    suggestion=(
                        "Add the subsystem to subsystems.yaml or fix the "
                        "telemetry source."
                    ),
                )
            )

    for command in model.commands:
        if command.target not in subsystem_ids:
            findings.append(
                LintFinding(
                    severity="ERROR",
                    code="OF-REF-002",
                    file="commands.yaml",
                    domain="commands",
                    object_id=command.id,
                    message=(
                        f"command target '{command.target}' does not reference "
                        "an existing subsystem"
                    ),
                    suggestion=(
                        "Add the subsystem to subsystems.yaml or fix the "
                        "command target."
                    ),
                )
            )

        for event_id in command.emits:
            if event_id not in event_ids:
                findings.append(
                    LintFinding(
                        severity="ERROR",
                        code="OF-REF-006",
                        file="commands.yaml",
                        domain="commands",
                        object_id=command.id,
                        message=f"command emits unknown event '{event_id}'",
                        suggestion=(
                            "Add the event to events.yaml or fix the command "
                            "emits list."
                        ),
                    )
                )

        for mode_id in command.allowed_modes:
            if mode_id not in mode_ids:
                findings.append(
                    LintFinding(
                        severity="ERROR",
                        code="OF-REF-008",
                        file="commands.yaml",
                        domain="commands",
                        object_id=command.id,
                        message=(
                            f"command allowed mode '{mode_id}' does not "
                            "reference an existing mode"
                        ),
                        suggestion="Add the mode to modes.yaml or fix allowed_modes.",
                    )
                )

    for event in model.events:
        if event.source not in subsystem_ids:
            findings.append(
                LintFinding(
                    severity="ERROR",
                    code="OF-REF-003",
                    file="events.yaml",
                    domain="events",
                    object_id=event.id,
                    message=(
                        f"event source '{event.source}' does not reference "
                        "an existing subsystem"
                    ),
                    suggestion=(
                        "Add the subsystem to subsystems.yaml or fix the "
                        "event source."
                    ),
                )
            )

    for fault in model.faults:
        if fault.source not in subsystem_ids:
            findings.append(
                LintFinding(
                    severity="ERROR",
                    code="OF-REF-004",
                    file="faults.yaml",
                    domain="faults",
                    object_id=fault.id,
                    message=(
                        f"fault source '{fault.source}' does not reference "
                        "an existing subsystem"
                    ),
                    suggestion=(
                        "Add the subsystem to subsystems.yaml or fix the "
                        "fault source."
                    ),
                )
            )

        if fault.condition.telemetry is not None:
            if fault.condition.telemetry not in telemetry_ids:
                findings.append(
                    LintFinding(
                        severity="ERROR",
                        code="OF-REF-005",
                        file="faults.yaml",
                        domain="faults",
                        object_id=fault.id,
                        message=(
                            "fault condition references unknown telemetry "
                            f"'{fault.condition.telemetry}'"
                        ),
                        suggestion=(
                            "Add the telemetry item to telemetry.yaml or fix "
                            "the fault condition."
                        ),
                    )
                )

        for event_id in fault.emits:
            if event_id not in event_ids:
                findings.append(
                    LintFinding(
                        severity="ERROR",
                        code="OF-REF-007",
                        file="faults.yaml",
                        domain="faults",
                        object_id=fault.id,
                        message=f"fault emits unknown event '{event_id}'",
                        suggestion=(
                            "Add the event to events.yaml or fix the fault "
                            "emits list."
                        ),
                    )
                )

        if fault.recovery is not None:
            if fault.recovery.mode_transition is not None:
                if fault.recovery.mode_transition not in mode_ids:
                    findings.append(
                        LintFinding(
                            severity="ERROR",
                            code="OF-REF-009",
                            file="faults.yaml",
                            domain="faults",
                            object_id=fault.id,
                            message=(
                                "fault recovery references unknown target mode "
                                f"'{fault.recovery.mode_transition}'"
                            ),
                            suggestion=(
                                "Add the mode to modes.yaml or fix the recovery "
                                "mode_transition."
                            ),
                        )
                    )

            for command_id in fault.recovery.auto_commands:
                if command_id not in command_ids:
                    findings.append(
                        LintFinding(
                            severity="ERROR",
                            code="OF-FLT-005",
                            file="faults.yaml",
                            domain="faults",
                            object_id=fault.id,
                            message=(
                                f"fault recovery references unknown command "
                                f"'{command_id}'"
                            ),
                            suggestion=(
                                "Add the command to commands.yaml or fix "
                                "recovery.auto_commands."
                            ),
                        )
                    )

    for packet in model.packets:
        for telemetry_id in packet.telemetry:
            if telemetry_id not in telemetry_ids:
                findings.append(
                    LintFinding(
                        severity="ERROR",
                        code="OF-REF-010",
                        file="packets.yaml",
                        domain="packets",
                        object_id=packet.id,
                        message=f"packet references unknown telemetry '{telemetry_id}'",
                        suggestion=(
                            "Add the telemetry item to telemetry.yaml or fix "
                            "the packet telemetry list."
                        ),
                    )
                )

    return findings