from __future__ import annotations

from orbitfabric.lint.finding import LintFinding
from orbitfabric.model.mission import (
    AutonomousActionContract,
    CommandSource,
    CommandabilityRule,
    MissionModel,
    RecoveryIntent,
)

HIGH_RISK_COMMAND_LEVELS = {"high", "critical"}


def check_commandability(model: MissionModel) -> list[LintFinding]:
    """Check Commandability and Autonomy Contract consistency."""
    findings: list[LintFinding] = []

    for source in model.commandability.sources:
        findings.extend(_check_command_source(model, source))

    for rule in model.commandability.rules:
        findings.extend(_check_commandability_rule(model, rule))

    for action in model.commandability.autonomous_actions:
        findings.extend(_check_autonomous_action(model, action))

    for recovery_intent in model.commandability.recovery_intents:
        findings.extend(_check_recovery_intent(model, recovery_intent))

    if _has_commandability_domain_content(model):
        findings.extend(_check_high_risk_commands_have_confirmation_intent(model))

    return findings


def _check_command_source(
    model: MissionModel,
    source: CommandSource,
) -> list[LintFinding]:
    findings: list[LintFinding] = []

    if source.type == "ground" and source.requires_contact and source.contact_profile is None:
        findings.append(
            LintFinding(
                severity="WARNING",
                code="OF-CAB-004",
                file="commandability.yaml",
                domain="command_sources",
                object_id=source.id,
                message="ground command source requires contact but has no contact profile",
                suggestion="Set contact_profile or set requires_contact to false.",
            )
        )

    if source.contact_profile is not None and source.contact_profile not in model.contact_profile_ids:
        findings.append(
            LintFinding(
                severity="ERROR",
                code="OF-CAB-005",
                file="commandability.yaml",
                domain="command_sources",
                object_id=source.id,
                message=(
                    "command source references unknown contact profile "
                    f"'{source.contact_profile}'"
                ),
                suggestion="Add the contact profile to contacts.yaml or fix source.contact_profile.",
            )
        )

    return findings


def _check_commandability_rule(
    model: MissionModel,
    rule: CommandabilityRule,
) -> list[LintFinding]:
    findings: list[LintFinding] = []

    if rule.command not in model.command_ids:
        findings.append(
            LintFinding(
                severity="ERROR",
                code="OF-CAB-001",
                file="commandability.yaml",
                domain="commandability_rules",
                object_id=rule.id,
                message=f"commandability rule references unknown command '{rule.command}'",
                suggestion="Add the command to commands.yaml or fix rule.command.",
            )
        )

    for mode_id in rule.allowed_modes:
        if mode_id in model.mode_ids:
            continue

        findings.append(
            LintFinding(
                severity="ERROR",
                code="OF-CAB-002",
                file="commandability.yaml",
                domain="commandability_rules",
                object_id=rule.id,
                message=f"commandability rule references unknown mode '{mode_id}'",
                suggestion="Add the mode to modes.yaml or fix rule.allowed_modes.",
            )
        )

    for source_id in rule.sources:
        if source_id in model.command_source_ids:
            continue

        findings.append(
            LintFinding(
                severity="ERROR",
                code="OF-CAB-003",
                file="commandability.yaml",
                domain="commandability_rules",
                object_id=rule.id,
                message=f"commandability rule references unknown source '{source_id}'",
                suggestion="Add the source to commandability.sources or fix rule.sources.",
            )
        )

    for event_id in rule.expected_events:
        if event_id in model.event_ids:
            continue

        findings.append(
            LintFinding(
                severity="ERROR",
                code="OF-CAB-006",
                file="commandability.yaml",
                domain="commandability_rules",
                object_id=rule.id,
                message=f"commandability rule references unknown expected event '{event_id}'",
                suggestion="Add the event to events.yaml or fix rule.expected_events.",
            )
        )

    return findings


def _check_autonomous_action(
    model: MissionModel,
    action: AutonomousActionContract,
) -> list[LintFinding]:
    findings: list[LintFinding] = []

    if action.dispatches.command not in model.command_ids:
        findings.append(
            LintFinding(
                severity="ERROR",
                code="OF-AUT-001",
                file="commandability.yaml",
                domain="autonomous_actions",
                object_id=action.id,
                message=(
                    "autonomous action dispatches unknown command "
                    f"'{action.dispatches.command}'"
                ),
                suggestion="Add the command to commands.yaml or fix dispatches.command.",
            )
        )

    if action.dispatches.source not in model.command_source_ids:
        findings.append(
            LintFinding(
                severity="ERROR",
                code="OF-AUT-002",
                file="commandability.yaml",
                domain="autonomous_actions",
                object_id=action.id,
                message=(
                    "autonomous action references unknown source "
                    f"'{action.dispatches.source}'"
                ),
                suggestion="Add the source to commandability.sources or fix dispatches.source.",
            )
        )

    findings.extend(_check_autonomous_trigger_references(model, action))

    for event_id in action.expected_events:
        if event_id in model.event_ids:
            continue

        findings.append(
            LintFinding(
                severity="ERROR",
                code="OF-AUT-004",
                file="commandability.yaml",
                domain="autonomous_actions",
                object_id=action.id,
                message=f"autonomous action references unknown expected event '{event_id}'",
                suggestion="Add the event to events.yaml or fix expected_events.",
            )
        )

    if not action.expected_events and not action.expected_effects:
        findings.append(
            LintFinding(
                severity="WARNING",
                code="OF-AUT-005",
                file="commandability.yaml",
                domain="autonomous_actions",
                object_id=action.id,
                message="autonomous action lacks expected events or effects",
                suggestion="Add expected_events or expected_effects to make the assumption testable.",
            )
        )

    return findings


def _check_autonomous_trigger_references(
    model: MissionModel,
    action: AutonomousActionContract,
) -> list[LintFinding]:
    findings: list[LintFinding] = []
    trigger = action.trigger

    if trigger.event is not None and trigger.event not in model.event_ids:
        findings.append(_unknown_trigger_finding(action, "event", trigger.event))

    if trigger.fault is not None and trigger.fault not in model.fault_ids:
        findings.append(_unknown_trigger_finding(action, "fault", trigger.fault))

    if trigger.telemetry is not None and trigger.telemetry not in model.telemetry_ids:
        findings.append(_unknown_trigger_finding(action, "telemetry", trigger.telemetry))

    if trigger.mode is not None and trigger.mode not in model.mode_ids:
        findings.append(_unknown_trigger_finding(action, "mode", trigger.mode))

    return findings


def _unknown_trigger_finding(
    action: AutonomousActionContract,
    trigger_kind: str,
    trigger_value: str,
) -> LintFinding:
    return LintFinding(
        severity="ERROR",
        code="OF-AUT-003",
        file="commandability.yaml",
        domain="autonomous_actions",
        object_id=action.id,
        message=(
            "autonomous action trigger references unknown "
            f"{trigger_kind} '{trigger_value}'"
        ),
        suggestion=f"Add the {trigger_kind} to the Mission Model or fix action.trigger.",
    )


def _check_recovery_intent(
    model: MissionModel,
    recovery_intent: RecoveryIntent,
) -> list[LintFinding]:
    findings: list[LintFinding] = []

    for command_id in recovery_intent.commands:
        if command_id in model.command_ids:
            continue

        findings.append(
            LintFinding(
                severity="ERROR",
                code="OF-REC-001",
                file="commandability.yaml",
                domain="recovery_intents",
                object_id=recovery_intent.id,
                message=f"recovery intent references unknown command '{command_id}'",
                suggestion="Add the command to commands.yaml or fix recovery_intent.commands.",
            )
        )

    if recovery_intent.fault is not None and recovery_intent.fault not in model.fault_ids:
        findings.append(_unknown_recovery_reference(recovery_intent, "fault", recovery_intent.fault))

    if recovery_intent.event is not None and recovery_intent.event not in model.event_ids:
        findings.append(_unknown_recovery_reference(recovery_intent, "event", recovery_intent.event))

    if recovery_intent.target_mode is not None and recovery_intent.target_mode not in model.mode_ids:
        findings.append(
            _unknown_recovery_reference(recovery_intent, "mode", recovery_intent.target_mode)
        )

    for event_id in recovery_intent.expected_events:
        if event_id in model.event_ids:
            continue

        findings.append(
            LintFinding(
                severity="ERROR",
                code="OF-REC-003",
                file="commandability.yaml",
                domain="recovery_intents",
                object_id=recovery_intent.id,
                message=f"recovery intent references unknown expected event '{event_id}'",
                suggestion="Add the event to events.yaml or fix recovery_intent.expected_events.",
            )
        )

    return findings


def _unknown_recovery_reference(
    recovery_intent: RecoveryIntent,
    reference_kind: str,
    reference_value: str,
) -> LintFinding:
    return LintFinding(
        severity="ERROR",
        code="OF-REC-002",
        file="commandability.yaml",
        domain="recovery_intents",
        object_id=recovery_intent.id,
        message=f"recovery intent references unknown {reference_kind} '{reference_value}'",
        suggestion=f"Add the {reference_kind} to the Mission Model or fix recovery_intent.",
    )


def _check_high_risk_commands_have_confirmation_intent(
    model: MissionModel,
) -> list[LintFinding]:
    commandability_by_command = {
        rule.command: rule for rule in model.commandability.rules if rule.command in model.command_ids
    }
    findings: list[LintFinding] = []

    for command in model.commands:
        if command.risk not in HIGH_RISK_COMMAND_LEVELS:
            continue

        rule = commandability_by_command.get(command.id)
        if rule is not None and rule.confirmation == "required":
            continue

        findings.append(
            LintFinding(
                severity="WARNING",
                code="OF-CAB-007",
                file="commandability.yaml",
                domain="commandability_rules",
                object_id=command.id,
                message="high-risk command lacks explicit required confirmation intent",
                suggestion=(
                    "Add a commandability rule with confirmation: required, or lower "
                    "the command risk if appropriate."
                ),
            )
        )

    return findings


def _has_commandability_domain_content(model: MissionModel) -> bool:
    return any(
        (
            model.commandability.sources,
            model.commandability.rules,
            model.commandability.autonomous_actions,
            model.commandability.recovery_intents,
        )
    )
