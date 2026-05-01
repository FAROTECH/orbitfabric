from __future__ import annotations

from typing import Any

from orbitfabric.lint.finding import LintFinding
from orbitfabric.model.mission import MissionModel, PayloadContract


def check_payloads(model: MissionModel) -> list[LintFinding]:
    """Check Payload / IOD Payload Contract lifecycle consistency."""
    findings: list[LintFinding] = []

    payloads_by_id = {payload.id: payload for payload in model.payloads}

    for payload in model.payloads:
        findings.extend(_check_lifecycle_definition(payload))

    for command in model.commands:
        findings.extend(
            _check_lifecycle_reference_group(
                payloads_by_id=payloads_by_id,
                command_id=command.id,
                container=command.preconditions,
                location="preconditions",
                code_unknown_payload="OF-PAY-003",
                code_unknown_state="OF-PAY-004",
            )
        )
        findings.extend(
            _check_lifecycle_reference_group(
                payloads_by_id=payloads_by_id,
                command_id=command.id,
                container=command.expected_effects,
                location="expected_effects",
                code_unknown_payload="OF-PAY-005",
                code_unknown_state="OF-PAY-006",
            )
        )

    return findings


def _check_lifecycle_definition(payload: PayloadContract) -> list[LintFinding]:
    findings: list[LintFinding] = []
    states = payload.lifecycle.states

    if not states:
        findings.append(
            LintFinding(
                severity="ERROR",
                code="OF-PAY-001",
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
                code="OF-PAY-002",
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


def _check_lifecycle_reference_group(
    payloads_by_id: dict[str, PayloadContract],
    command_id: str,
    container: Any,
    location: str,
    code_unknown_payload: str,
    code_unknown_state: str,
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
                code=code_unknown_payload,
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
                code=code_unknown_payload,
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
                code=code_unknown_state,
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
