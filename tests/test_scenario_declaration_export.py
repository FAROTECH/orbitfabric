from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml

from orbitfabric import __version__
from orbitfabric.export.scenario_declaration import (
    DECLARATION_KIND,
    DECLARATION_VERSION,
    scenario_declaration_from_file,
    write_scenario_declaration,
)

BATTERY_SCENARIO = Path("examples/demo-3u/scenarios/battery_low_during_payload.yaml")
DATA_FLOW_SCENARIO = Path("examples/demo-3u/scenarios/payload_data_flow_evidence.yaml")
UNIVERSITY_SCENARIO = Path(
    "examples/university-cubesat-minislice/scenarios/payload_data_constrained_downlink.yaml"
)
DEMO_MISSION = Path("examples/demo-3u/mission").resolve()


def test_scenario_declaration_exposes_exact_source_identity_and_core_boundaries() -> None:
    declaration = scenario_declaration_from_file(BATTERY_SCENARIO)

    assert declaration["kind"] == DECLARATION_KIND
    assert declaration["declaration_version"] == DECLARATION_VERSION
    assert declaration["orbitfabric_version"] == __version__
    assert declaration["result"] == "loaded"
    assert declaration["scenario"]["id"] == "battery_low_during_payload"
    assert declaration["mission"]["id"] == "demo-3u"
    assert declaration["source"]["scenario_sha256"] == hashlib.sha256(
        BATTERY_SCENARIO.read_bytes()
    ).hexdigest()
    assert declaration["atom_count"] == len(declaration["atoms"])
    assert declaration["diagnostics"] == []
    assert declaration["boundaries"] == {
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


def test_scenario_declaration_atomizes_command_and_status_in_one_step() -> None:
    declaration = scenario_declaration_from_file(BATTERY_SCENARIO)

    atoms = [atom for atom in declaration["atoms"] if atom["step_index"] == 1]

    assert [(atom["kind"], atom["within_step_ordinal"]) for atom in atoms] == [
        ("command", 0),
        ("expect_command_status", 1),
    ]
    assert {atom["scenario_time_s"] for atom in atoms} == {5}
    assert atoms[0]["references"] == [
        {
            "role": "command",
            "entity": {"domain": "commands", "id": "payload.start_acquisition"},
        }
    ]
    assert atoms[0]["declaration"] == {"arguments": {"duration_s": 300}}
    assert atoms[1]["declaration"] == {"expected": "ACCEPTED"}


def test_scenario_declaration_normalizes_data_flow_role_labelled_entity_refs() -> None:
    declaration = scenario_declaration_from_file(DATA_FLOW_SCENARIO)

    atom = next(atom for atom in declaration["atoms"] if atom["kind"] == "expect_data_flow")

    refs = {
        ref["role"]: (ref["entity"]["domain"], ref["entity"]["id"])
        for ref in atom["references"]
    }
    assert refs == {
        "subject_data_product": ("data_products", "payload.radiation_histogram"),
        "triggered_by_command": ("commands", "payload.start_acquisition"),
        "eligible_downlink_flow": ("downlink_flows", "science_next_available_contact"),
        "contact_window": ("contact_windows", "demo_contact_001"),
    }
    assert atom["declaration"]["storage_intent_declared"] is True
    assert atom["declaration"]["downlink_intent_declared"] is True


def test_scenario_declaration_splits_multi_telemetry_expectation_deterministically() -> None:
    declaration = scenario_declaration_from_file(UNIVERSITY_SCENARIO)

    atoms = [
        atom
        for atom in declaration["atoms"]
        if atom["step_index"] == 4 and atom["kind"] == "expect_telemetry"
    ]

    assert [atom["references"][0]["entity"]["id"] for atom in atoms] == [
        "data_storage.used_bytes",
        "payload.data_generated_bytes",
        "payload.data_pending_bytes",
        "payload.status",
    ]
    assert [atom["within_step_ordinal"] for atom in atoms] == [0, 1, 2, 3]
    assert {atom["scenario_time_s"] for atom in atoms} == {8}


def test_scenario_declaration_starts_with_correlatable_metadata_and_initial_atoms() -> None:
    declaration = scenario_declaration_from_file(BATTERY_SCENARIO)

    atoms = declaration["atoms"]
    assert atoms[0]["id"] == "atom-0001"
    assert atoms[0]["kind"] == "scenario_metadata"
    assert atoms[0]["role"] == "metadata"
    assert atoms[0]["references"] == []
    assert atoms[1]["kind"] == "initial_mode"
    assert atoms[1]["references"][0]["entity"] == {"domain": "modes", "id": "NOMINAL"}
    assert [atom["id"] for atom in atoms] == [
        f"atom-{index:04d}" for index in range(1, len(atoms) + 1)
    ]


def test_scenario_declaration_fails_closed_on_unknown_expect_semantics(tmp_path: Path) -> None:
    scenario_file = tmp_path / "unknown-expect.yaml"
    _write_scenario(
        scenario_file,
        steps=[{"t": 1, "expect": {"future_semantics": {"value": True}}}],
    )

    declaration = scenario_declaration_from_file(scenario_file)

    assert declaration["result"] == "failed"
    assert declaration["scenario"] is None
    assert declaration["mission"] is None
    assert declaration["atoms"] is None
    assert declaration["atom_count"] is None
    assert declaration["source"]["scenario_sha256"] == hashlib.sha256(
        scenario_file.read_bytes()
    ).hexdigest()
    assert any(item["code"] == "OF-SCN-020" for item in declaration["diagnostics"])


def test_scenario_declaration_does_not_emit_unvalidated_payload_entity_ref(tmp_path: Path) -> None:
    scenario_file = tmp_path / "unknown-payload.yaml"
    _write_scenario(
        scenario_file,
        steps=[
            {
                "t": 1,
                "expect": {
                    "payload_lifecycle": {
                        "payload": "missing_payload",
                        "state": "READY",
                    }
                },
            }
        ],
    )

    declaration = scenario_declaration_from_file(scenario_file)

    assert declaration["result"] == "failed"
    assert declaration["atoms"] is None
    assert any(
        item["code"] == "OF-SCN-018"
        and "missing_payload" in item["message"]
        for item in declaration["diagnostics"]
    )


def test_scenario_declaration_missing_source_is_machine_readable_failure(tmp_path: Path) -> None:
    scenario_file = tmp_path / "missing.yaml"

    declaration = scenario_declaration_from_file(scenario_file)

    assert declaration["result"] == "failed"
    assert declaration["scenario"] is None
    assert declaration["mission"] is None
    assert declaration["source"]["scenario_sha256"] is None
    assert declaration["atoms"] is None
    assert declaration["diagnostics"][0]["code"] == "OF-SCN-000"


def test_write_scenario_declaration_is_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"

    write_scenario_declaration(DATA_FLOW_SCENARIO, first)
    write_scenario_declaration(DATA_FLOW_SCENARIO, second)

    assert first.read_bytes() == second.read_bytes()
    assert first.read_text(encoding="utf-8").endswith("\n")
    assert json.loads(first.read_text(encoding="utf-8")) == scenario_declaration_from_file(
        DATA_FLOW_SCENARIO
    )


def _write_scenario(path: Path, *, steps: list[dict[str, object]]) -> None:
    payload = {
        "scenario": {
            "id": path.stem,
            "name": path.stem,
            "description": "CR0 declared-surface failure fixture",
        },
        "mission": {"path": str(DEMO_MISSION)},
        "initial_state": {"mode": "NOMINAL", "telemetry": {}},
        "steps": steps,
    }
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
