from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from orbitfabric import __version__
from orbitfabric.model.errors import MissionModelError, ModelDiagnostic
from orbitfabric.model.scenario import LoadedScenario, ScenarioStep
from orbitfabric.model.scenario_loader import ScenarioLoader

DECLARATION_KIND = "orbitfabric.scenario_declaration"
DECLARATION_VERSION = "0.1-candidate"

_SUPPORTED_EXPECT_KEYS = {
    "command_status",
    "payload_lifecycle",
    "data_flow",
    "scenario_status",
}


def scenario_declaration_from_file(scenario_file: Path) -> dict[str, Any]:
    """Return a complete declared-Scenario envelope or a structured failure."""
    scenario_file = scenario_file.resolve()
    scenario_sha256 = _sha256_file_if_readable(scenario_file)

    try:
        loaded = ScenarioLoader().load(scenario_file)
        if scenario_sha256 is None:
            scenario_sha256 = _sha256_file_if_readable(scenario_file)
        if scenario_sha256 is None:
            raise MissionModelError(
                [
                    ModelDiagnostic(
                        severity="ERROR",
                        code="OF-SCN-019",
                        file=str(scenario_file),
                        domain="scenario",
                        object_id=loaded.scenario.scenario.id,
                        message="unable to fingerprint the consumed scenario bytes",
                        suggestion="Ensure the scenario file remains readable during export.",
                    )
                ]
            )
        atoms = _normalize_declared_atoms(loaded)
    except MissionModelError as exc:
        return failed_scenario_declaration_to_dict(
            scenario_sha256=scenario_sha256,
            diagnostics=exc.diagnostics,
        )
    except OSError as exc:
        return failed_scenario_declaration_to_dict(
            scenario_sha256=scenario_sha256,
            diagnostics=[
                ModelDiagnostic(
                    severity="ERROR",
                    code="OF-SCN-019",
                    file=str(scenario_file),
                    domain="scenario",
                    message=f"unable to read scenario input: {exc}",
                    suggestion="Ensure the scenario and referenced Mission Model are readable.",
                )
            ],
        )

    metadata = loaded.scenario.scenario
    mission = loaded.mission_model.spacecraft
    return {
        "kind": DECLARATION_KIND,
        "declaration_version": DECLARATION_VERSION,
        "orbitfabric_version": __version__,
        "result": "loaded",
        "scenario": {
            "id": metadata.id,
            "name": metadata.name,
            "description": metadata.description,
        },
        "mission": {
            "id": mission.id,
            "model_version": mission.model_version,
        },
        "source": {
            "scenario_sha256": scenario_sha256,
        },
        "boundaries": _boundaries(),
        "atom_count": len(atoms),
        "atoms": atoms,
        "diagnostics": [],
    }


def failed_scenario_declaration_to_dict(
    *,
    scenario_sha256: str | None,
    diagnostics: list[ModelDiagnostic],
) -> dict[str, Any]:
    """Return a failed declaration envelope without partial Scenario semantics."""
    return {
        "kind": DECLARATION_KIND,
        "declaration_version": DECLARATION_VERSION,
        "orbitfabric_version": __version__,
        "result": "failed",
        "scenario": None,
        "mission": None,
        "source": {
            "scenario_sha256": scenario_sha256,
        },
        "boundaries": _boundaries(),
        "atom_count": None,
        "atoms": None,
        "diagnostics": [_diagnostic_to_dict(item) for item in diagnostics],
    }


def write_scenario_declaration(scenario_file: Path, output_file: Path) -> Path:
    """Write one deterministic Core-owned declared-Scenario JSON envelope."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(
        json.dumps(
            scenario_declaration_from_file(scenario_file),
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return output_file


def _normalize_declared_atoms(loaded: LoadedScenario) -> list[dict[str, Any]]:
    scenario = loaded.scenario
    atoms: list[dict[str, Any]] = []

    def append_atom(
        *,
        role: str,
        kind: str,
        step_index: int | None,
        within_step_ordinal: int | None,
        scenario_time_s: int | float | None,
        references: list[dict[str, Any]],
        declaration: Any,
    ) -> None:
        atoms.append(
            {
                "id": f"atom-{len(atoms) + 1:04d}",
                "role": role,
                "kind": kind,
                "step_index": step_index,
                "within_step_ordinal": within_step_ordinal,
                "scenario_time_s": scenario_time_s,
                "references": references,
                "declaration": declaration,
            }
        )

    metadata = scenario.scenario
    append_atom(
        role="metadata",
        kind="scenario_metadata",
        step_index=None,
        within_step_ordinal=None,
        scenario_time_s=None,
        references=[],
        declaration={
            "id": metadata.id,
            "name": metadata.name,
            "description": metadata.description,
        },
    )

    append_atom(
        role="initial_state",
        kind="initial_mode",
        step_index=None,
        within_step_ordinal=None,
        scenario_time_s=None,
        references=[_entity_reference("mode", "modes", scenario.initial_state.mode)],
        declaration={"value": scenario.initial_state.mode},
    )

    for telemetry_id, value in sorted(scenario.initial_state.telemetry.items()):
        append_atom(
            role="initial_state",
            kind="initial_telemetry",
            step_index=None,
            within_step_ordinal=None,
            scenario_time_s=None,
            references=[_entity_reference("telemetry", "telemetry", telemetry_id)],
            declaration={"value": value},
        )

    for step_index, step in enumerate(scenario.steps):
        normalized = _normalize_step(loaded, step, step_index)
        for ordinal, item in enumerate(normalized):
            append_atom(
                role=item["role"],
                kind=item["kind"],
                step_index=step_index,
                within_step_ordinal=ordinal,
                scenario_time_s=step.t,
                references=item["references"],
                declaration=item["declaration"],
            )

    return atoms


def _normalize_step(
    loaded: LoadedScenario,
    step: ScenarioStep,
    step_index: int,
) -> list[dict[str, Any]]:
    if step.command is None and step.args:
        raise _normalization_error(
            loaded,
            step_index,
            "scenario step has command arguments without a command",
        )

    expect = step.expect or {}
    unknown_expect_keys = sorted(set(expect) - _SUPPORTED_EXPECT_KEYS)
    if unknown_expect_keys:
        raise _normalization_error(
            loaded,
            step_index,
            "scenario declaration cannot normalize unsupported expect key(s): "
            + ", ".join(unknown_expect_keys),
        )

    records: list[dict[str, Any]] = []

    if step.command is not None:
        records.append(
            _record(
                role="action",
                kind="command",
                references=[_entity_reference("command", "commands", step.command)],
                declaration={"arguments": step.args},
            )
        )

    if "command_status" in expect:
        if step.command is None or expect["command_status"] is None:
            raise _normalization_error(
                loaded,
                step_index,
                "command_status expectation requires a command and a non-null expected status",
            )
        records.append(
            _record(
                role="expectation",
                kind="expect_command_status",
                references=[_entity_reference("command", "commands", step.command)],
                declaration={"expected": expect["command_status"]},
            )
        )

    if step.inject is not None:
        records.append(
            _record(
                role="action",
                kind="telemetry_injection",
                references=[
                    _entity_reference("telemetry", "telemetry", step.inject.telemetry)
                ],
                declaration={"value": step.inject.value},
            )
        )

    if step.expect_event is not None:
        records.append(
            _record(
                role="expectation",
                kind="expect_event",
                references=[_entity_reference("event", "events", step.expect_event)],
                declaration={"expected": True},
            )
        )

    if step.expect_mode is not None:
        records.append(
            _record(
                role="expectation",
                kind="expect_mode",
                references=[_entity_reference("mode", "modes", step.expect_mode)],
                declaration={"expected": step.expect_mode},
            )
        )

    if step.expect_command is not None:
        records.append(
            _record(
                role="expectation",
                kind="expect_command",
                references=[
                    _entity_reference("command", "commands", step.expect_command.id)
                ],
                declaration={
                    "dispatch": step.expect_command.dispatch,
                    "expected_present": True,
                },
            )
        )

    for telemetry_id, expected in sorted((step.expect_telemetry or {}).items()):
        records.append(
            _record(
                role="expectation",
                kind="expect_telemetry",
                references=[_entity_reference("telemetry", "telemetry", telemetry_id)],
                declaration={"expected": expected},
            )
        )

    if "payload_lifecycle" in expect:
        records.append(_normalize_payload_lifecycle(loaded, expect["payload_lifecycle"], step_index))

    if "data_flow" in expect:
        records.append(_normalize_data_flow(loaded, expect["data_flow"], step_index))

    if "scenario_status" in expect:
        if expect["scenario_status"] is None:
            raise _normalization_error(
                loaded,
                step_index,
                "scenario_status expectation must not be null",
            )
        records.append(
            _record(
                role="expectation",
                kind="expect_scenario_status",
                references=[],
                declaration={"expected": expect["scenario_status"]},
            )
        )

    if not records:
        raise _normalization_error(
            loaded,
            step_index,
            "scenario step contains no normalizable semantic content",
        )

    return records


def _normalize_payload_lifecycle(
    loaded: LoadedScenario,
    value: Any,
    step_index: int,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise _normalization_error(
            loaded,
            step_index,
            "payload_lifecycle expectation must be an object",
        )
    payload_id = value.get("payload")
    state = value.get("state")
    if not isinstance(payload_id, str) or not isinstance(state, str):
        raise _normalization_error(
            loaded,
            step_index,
            "payload_lifecycle expectation requires string payload and state",
        )
    if payload_id not in loaded.mission_model.payload_ids:
        raise MissionModelError(
            [
                ModelDiagnostic(
                    severity="ERROR",
                    code="OF-SCN-018",
                    file=str(loaded.scenario_file),
                    domain="scenario",
                    object_id=loaded.scenario.scenario.id,
                    message=(
                        "scenario payload lifecycle expectation references unknown payload "
                        f"'{payload_id}'"
                    ),
                    suggestion="Use a payload defined in payloads.yaml.",
                )
            ]
        )
    return _record(
        role="expectation",
        kind="expect_payload_lifecycle",
        references=[_entity_reference("payload", "payloads", payload_id)],
        declaration={"payload": payload_id, "state": state},
    )


def _normalize_data_flow(
    loaded: LoadedScenario,
    value: Any,
    step_index: int,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise _normalization_error(
            loaded,
            step_index,
            "data_flow expectation must be an object",
        )
    data_product = value.get("data_product")
    if not isinstance(data_product, str):
        raise _normalization_error(
            loaded,
            step_index,
            "data_flow expectation requires string data_product",
        )

    references = [
        _entity_reference("subject_data_product", "data_products", data_product)
    ]
    for field, role, domain in (
        ("triggered_by_command", "triggered_by_command", "commands"),
        ("eligible_downlink_flow", "eligible_downlink_flow", "downlink_flows"),
        ("contact_window", "contact_window", "contact_windows"),
    ):
        if field not in value:
            continue
        target_id = value[field]
        if not isinstance(target_id, str):
            raise _normalization_error(
                loaded,
                step_index,
                f"data_flow expectation field {field} must be a string when present",
            )
        references.append(_entity_reference(role, domain, target_id))

    return _record(
        role="expectation",
        kind="expect_data_flow",
        references=references,
        declaration=dict(value),
    )


def _record(
    *,
    role: str,
    kind: str,
    references: list[dict[str, Any]],
    declaration: Any,
) -> dict[str, Any]:
    return {
        "role": role,
        "kind": kind,
        "references": references,
        "declaration": declaration,
    }


def _entity_reference(role: str, domain: str, entity_id: str) -> dict[str, Any]:
    return {
        "role": role,
        "entity": {
            "domain": domain,
            "id": entity_id,
        },
    }


def _normalization_error(
    loaded: LoadedScenario,
    step_index: int,
    message: str,
) -> MissionModelError:
    return MissionModelError(
        [
            ModelDiagnostic(
                severity="ERROR",
                code="OF-SCN-020",
                file=str(loaded.scenario_file),
                domain="scenario",
                object_id=loaded.scenario.scenario.id,
                message=f"step {step_index}: {message}",
                suggestion="Use only documented Core Scenario semantics.",
            )
        ]
    )


def _sha256_file_if_readable(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def _boundaries() -> dict[str, bool | str]:
    return {
        "source_of_truth": "scenario_yaml",
        "core_derived_report": True,
        "read_only": True,
        "contains_declared_scenario": True,
        "contains_complete_atom_accounting": True,
        "contains_structured_diagnostics": True,
        "contains_yaml_ast": False,
        "contains_simulation_evidence": False,
        "contains_target_projection": False,
        "contains_runtime_behavior": False,
        "contains_ground_behavior": False,
        "contains_plugin_api": False,
        "contains_studio_api": False,
    }


def _diagnostic_to_dict(diagnostic: ModelDiagnostic) -> dict[str, Any]:
    return {
        "severity": diagnostic.severity,
        "code": diagnostic.code,
        "file": diagnostic.file,
        "domain": diagnostic.domain,
        "object_id": diagnostic.object_id,
        "message": diagnostic.message,
        "suggestion": diagnostic.suggestion,
    }
