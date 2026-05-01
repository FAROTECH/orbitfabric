from __future__ import annotations

from typing import Any

from orbitfabric.lint.finding import LintFinding
from orbitfabric.model.mission import MissionModel, PayloadContract, Subsystem


def check_payloads(model: MissionModel) -> list[LintFinding]:
    """Check Payload / IOD Payload Contract consistency."""
    findings: list[LintFinding] = []

    payloads_by_id = {payload.id: payload for payload in model.payloads}
    subsystems_by_id = {subsystem.id: subsystem for subsystem in model.subsystems}

    for payload in model.payloads:
        findings.extend(_check_payload_subsystem(payload, subsystems_by_id))
        findings.extend(_check_lifecycle_definition(payload))
        findings.extend(_check_payload_references(model, payload))

    for command in model.commands:
        findings.extend(
            _check_lifecycle_reference_group(
                payloads_by_id=payloads_by_id,
                command_id=command.id,
                container=command.preconditions,
                location="preconditions",
                code="OF-PAY-009",
            )
        )
        findings.extend(
            _check_lifecycle_reference_group(
                payloads_by_id=payloads_by_id,
                command_id=command.id,
                container=command.expected_effects,
                location="expected_effects",
                code="OF-PAY-010",
            )
        )

    return findings


def _check_payload_subsystem(
    payload: PayloadContract,
    subsystems_by_id: dict[str, Subsystem],
) -> list[LintFinding]:
    findings: list[LintFinding] = []
    subsystem = subsystems_by_id.get(payload.subsystem)

    if subsystem is None:
        findings.append(
            LintFinding(
                severity="ERROR",
                code="OF-PAY-001",
                file="payloads.yaml",
                domain="payloads",
                object_id=payload.id,
                message=(
                    f"payload subsystem '{payload.subsystem}' does not reference "
                    "an existing subsystem"
                ),
                suggestion="Add the subsystem to subsystems.yaml or fix payload.subsystem.",
            )
        )
        return findings

    if subsystem.type != "payload":
        findings.append(
            LintFinding(
                severity="ERROR",
                code="OF-PAY-002",
                file="payloads.yaml",
                domain="payloads",
                object_id=payload.id,
                message=(
                    f"payload subsystem '{payload.subsystem}' references subsystem "
                    f"type '{subsystem.type}', expected 'payload'"
                ),
                suggestion="Use a subsystem with type 'payload' or fix payload.subsystem.",
            )
        )

    return findings


def _check_lifecycle_definition(payload: PayloadContract) -> list[LintFinding]:
    findings: list[LintFinding] = []
    states = payload.lifecycle.states

    if not payload.lifecycle.initial_state:
        findings.append(
            LintFinding(
                severity="ERROR",
                code="OF-PAY-003",
                file="payloads.yaml",
                domain="payloads",
                object_id=payload.id,
                message="payload lifecycle must define an initial_state",
                suggestion="Set lifecycle.initial_state to one of lifecycle.states.",
            )
        )

    if not states:
        findings.append(
            LintFinding(
                severity="ERROR",
                code="OF-PAY-004",
                file="payloads.yaml",
                domain="payloads",
                object_id=payload.id,
                message="payload lifecycle must define at least one state",
                suggestion="Add at least one lifecycle state to lifecycle.states.",
            )
        )
        return findings

    if payload.lifecycle.initial_state not in states:
        findings.append(
            LintFinding(
                severity="ERROR",
                code="OF-PAY-004",
                file="payloads.yaml",
                domain="payloads",
                object_id=payload.id,
                message=(
                    f"payload lifecycle initial state '{payload.lifecycle.initial_state}' "
                    "is not declared in lifecycle.states"
                ),
                suggestion="Add the initial state to lifecycle.states or fix initial_state.",
            )
        )

    return findings


def _check_payload_references(
    model: MissionModel,
    payload: PayloadContract,
) -> list[LintFinding]:
    findings: list[LintFinding] = []

    findings.extend(
        _check_reference_list(
            values=payload.telemetry.produced,
            known_ids=model.telemetry_ids,
            payload_id=payload.id,
            code="OF-PAY-005",
            label="telemetry",
            file="telemetry.yaml",
        )
    )
    findings.extend(
        _check_reference_list(
            values=payload.commands.accepted,
            known_ids=model.command_ids,
            payload_id=payload.id,
            code="OF-PAY-006",
            label="command",
            file="commands.yaml",
        )
    )
    findings.extend(
        _check_reference_list(
            values=payload.events.generated,
            known_ids=model.event_ids,
            payload_id=payload.id,
            code="OF-PAY-007",
            label="event",
            file="events.yaml",
        )
    )
    findings.extend(
        _check_reference_list(
            values=payload.faults.possible,
            known_ids=model.fault_ids,
            payload_id=payload.id,
            code="OF-PAY-008",
            label="fault",
            file="faults.yaml",
        )
    )

    return findings


def _check_reference_list(
    values: list[str],
    known_ids: set[str],
    payload_id: str,
    code: str,
    label: str,
    file: str,
) -> list[LintFinding]:
    findings: list[LintFinding] = []

    for value in values:
        if value not in known_ids:
            findings.append(
                LintFinding(
                    severity="ERROR",
                    code=code,
                    file="payloads.yaml",
                    domain="payloads",
                    object_id=payload_id,
                    message=f"payload references unknown {label} '{value}'",
                    suggestion=f"Add the {label} to {file} or fix the payload reference.",
                )
            )

    return findings


def _check_lifecycle_reference_group(
    payloads_by_id: dict[str, PayloadContract],
    command_id: str,
    container: Any,
    location: str,
    code: str,
) -> list[LintFinding]:
    findings: list[LintFinding] = []

    reference = _extract_payload_lifecycle_reference(container)
    if reference is None:
        return findings

    payload_id = reference.get("payload")
    state = reference.get("state")

    if not isinstance(payload_id, str) or not payload_id:
        findings.append(
            LintFinding(
                severity="ERROR",
                code=code,
                file="commands.yaml",
                domain="commands",
                object_id=command_id,
                message=f"command {location} payload lifecycle reference must define a payload id",
                suggestion="Set payload_lifecycle.payload to an existing payload id.",
            )
        )
        return findings

    payload = payloads_by_id.get(payload_id)
    if payload is None:
        findings.append(
            LintFinding(
                severity="ERROR",
                code=code,
                file="commands.yaml",
                domain="commands",
                object_id=command_id,
                message=(
                    f"command {location} references unknown payload lifecycle "
                    f"payload '{payload_id}'"
                ),
                suggestion="Add the payload to payloads.yaml or fix the payload reference.",
            )
        )
        return findings

    if not isinstance(state, str) or state not in payload.lifecycle.states:
        findings.append(
            LintFinding(
                severity="ERROR",
                code=code,
                file="commands.yaml",
                domain="commands",
                object_id=command_id,
                message=(
                    f"command {location} references unknown lifecycle state "
                    f"'{state}' for payload '{payload_id}'"
                ),
                suggestion="Use one of the lifecycle states declared in payloads.yaml.",
            )
        )

    return findings


def _extract_payload_lifecycle_reference(container: Any) -> dict[str, Any] | None:
    if not isinstance(container, dict):
        return None

    reference = container.get("payload_lifecycle")
    if reference is None:
        return None

    if isinstance(reference, dict):
        return reference

    return {}
