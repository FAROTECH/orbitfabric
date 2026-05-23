from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from orbitfabric import __version__
from orbitfabric.cli import app
from orbitfabric.export.coverage_summary import (
    coverage_summary_to_dict,
    write_coverage_summary,
)
from orbitfabric.export.entity_index import write_entity_index
from orbitfabric.export.relationship_manifest import write_relationship_manifest
from orbitfabric.export.scenario_run_index import write_scenario_run_index
from orbitfabric.model.loader import MissionModelLoader
from orbitfabric.model.scenario_loader import ScenarioLoader
from orbitfabric.sim.json_report import write_simulation_report_json
from orbitfabric.sim.runner import ScenarioRunner

DEMO_MISSION = Path("examples/demo-3u/mission")
DATA_FLOW_SCENARIO = Path("examples/demo-3u/scenarios/payload_data_flow_evidence.yaml")
runner = CliRunner()


def test_coverage_summary_contains_identity_sources_and_boundaries(
    tmp_path: Path,
) -> None:
    paths = _write_core_inputs(tmp_path)

    payload = coverage_summary_to_dict(
        DEMO_MISSION,
        paths["entity_index"],
        paths["relationship_manifest"],
        paths["scenario_run_index"],
    )

    assert payload["coverage_version"] == "0.1-candidate"
    assert payload["kind"] == "orbitfabric.coverage_summary"
    assert payload["orbitfabric_version"] == __version__
    assert payload["mission"] == {
        "id": "demo-3u",
        "name": "Demo 3U Spacecraft",
        "model_version": "0.1.0",
    }
    assert payload["source"]["entity_index_kind"] == "orbitfabric.entity_index"
    assert payload["source"]["relationship_manifest_kind"] == (
        "orbitfabric.relationship_manifest"
    )
    assert payload["source"]["scenario_run_index_kind"] == (
        "orbitfabric.scenario_run_index"
    )
    assert payload["boundaries"] == {
        "source_of_truth": "core_structured_outputs",
        "core_derived_report": True,
        "read_only": True,
        "contains_coverage_metrics": True,
        "contains_health_score": False,
        "contains_model_completeness_score": False,
        "contains_relationship_graph": False,
        "contains_dependency_graph": False,
        "contains_yaml_ast": False,
        "contains_source_locations": False,
        "contains_plugin_api": False,
        "contains_studio_api": False,
        "contains_runtime_behavior": False,
        "contains_ground_behavior": False,
        "coverage_derived_from_entity_index": True,
        "coverage_derived_from_relationship_manifest": True,
        "coverage_derived_from_scenario_run_index": True,
        "coverage_derived_from_simulation_json": True,
        "coverage_derived_from_logs": False,
    }


def test_coverage_summary_contains_entity_coverage(tmp_path: Path) -> None:
    paths = _write_core_inputs(tmp_path)

    payload = coverage_summary_to_dict(
        DEMO_MISSION,
        paths["entity_index"],
        paths["relationship_manifest"],
        paths["scenario_run_index"],
    )

    assert payload["scenario_runs"] == {
        "total": 1,
        "passed": 1,
        "failed": 0,
    }

    assert payload["entity_coverage"]["commands"] == {
        "total": 4,
        "covered": 2,
        "uncovered": 2,
        "coverage_ratio": 0.5,
        "covered_ids": [
            "payload.start_acquisition",
            "payload.stop_acquisition",
        ],
        "uncovered_ids": [
            "eps.get_status",
            "radio.downlink_housekeeping",
        ],
    }
    assert payload["entity_coverage"]["events"] == {
        "total": 8,
        "covered": 2,
        "uncovered": 6,
        "coverage_ratio": 0.25,
        "covered_ids": [
            "payload.acquisition_started",
            "payload.acquisition_stopped",
        ],
        "uncovered_ids": [
            "adcs.safe_attitude_requested",
            "eps.battery_critical",
            "eps.battery_low",
            "obc.safe_mode_entered",
            "payload.fault_detected",
            "radio.downlink_started",
        ],
    }
    assert payload["entity_coverage"]["data_products"] == {
        "total": 1,
        "covered": 1,
        "uncovered": 0,
        "coverage_ratio": 1.0,
        "covered_ids": ["payload.radiation_histogram"],
        "uncovered_ids": [],
    }


def test_coverage_summary_contains_expectation_and_relationship_coverage(
    tmp_path: Path,
) -> None:
    paths = _write_core_inputs(tmp_path)

    payload = coverage_summary_to_dict(
        DEMO_MISSION,
        paths["entity_index"],
        paths["relationship_manifest"],
        paths["scenario_run_index"],
    )

    assert payload["expectation_coverage"]["total"] == 12
    assert payload["expectation_coverage"]["passed"] == 12
    assert payload["expectation_coverage"]["failed"] == 0
    assert payload["expectation_coverage"]["pass_ratio"] == 1.0
    assert payload["expectation_coverage"]["by_type"]["data_flow"] == {
        "total": 1,
        "passed": 1,
        "failed": 0,
        "pass_ratio": 1.0,
    }

    relationships = payload["relationship_coverage"]
    assert relationships["supported_relationship_types"] == [
        "data_product_produced_by_payload",
        "data_product_produced_by_subsystem",
        "downlink_flow_includes_data_product",
    ]
    assert relationships["total_supported_relationships"] == 2
    assert relationships["covered_supported_relationships"] == 2
    assert relationships["uncovered_supported_relationships"] == 0
    assert relationships["coverage_ratio"] == 1.0
    assert relationships["covered_relationship_ids"] == [
        "data_products:payload.radiation_histogram->"
        "data_product_produced_by_payload:payloads:demo_iod_payload",
        "downlink_flows:science_next_available_contact->"
        "downlink_flow_includes_data_product:"
        "data_products:payload.radiation_histogram",
    ]
    assert relationships["uncovered_relationship_ids"] == []


def test_write_coverage_summary_is_deterministic_json(tmp_path: Path) -> None:
    paths = _write_core_inputs(tmp_path)
    output_file = tmp_path / "coverage_summary.json"

    written_file = write_coverage_summary(
        DEMO_MISSION,
        paths["entity_index"],
        paths["relationship_manifest"],
        paths["scenario_run_index"],
        output_file,
    )

    assert written_file == output_file
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert content.endswith("\n")

    parsed = json.loads(content)
    assert parsed == coverage_summary_to_dict(
        DEMO_MISSION,
        paths["entity_index"],
        paths["relationship_manifest"],
        paths["scenario_run_index"],
    )


def test_coverage_summary_command_writes_json_report(tmp_path: Path) -> None:
    paths = _write_core_inputs(tmp_path)
    output_file = tmp_path / "coverage_summary.json"

    result = runner.invoke(
        app,
        [
            "export",
            "coverage-summary",
            "examples/demo-3u/mission",
            "--entity-index",
            str(paths["entity_index"]),
            "--relationship-manifest",
            str(paths["relationship_manifest"]),
            "--scenario-run-index",
            str(paths["scenario_run_index"]),
            "--json",
            str(output_file),
        ],
    )

    assert result.exit_code == 0
    assert output_file.exists()
    assert "OrbitFabric Coverage Summary Export" in result.output
    assert "Scenario runs: 1" in result.output
    assert "Coverage: emitted" in result.output
    assert "JSON report written to" in result.output

    payload = json.loads(output_file.read_text(encoding="utf-8"))

    assert payload["kind"] == "orbitfabric.coverage_summary"
    assert payload["coverage_version"] == "0.1-candidate"
    assert payload["entity_coverage"]["data_products"]["coverage_ratio"] == 1.0


def _write_core_inputs(tmp_path: Path) -> dict[str, Path]:
    model = MissionModelLoader().load(DEMO_MISSION)
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()

    entity_index_file = reports_dir / "entity_index.json"
    relationship_manifest_file = reports_dir / "relationship_manifest.json"
    simulation_report_file = reports_dir / "payload_data_flow_evidence_report.json"
    scenario_run_index_file = reports_dir / "scenario_run_index.json"

    write_entity_index(model, DEMO_MISSION, entity_index_file)
    write_relationship_manifest(model, DEMO_MISSION, relationship_manifest_file)
    _write_sim_report(DATA_FLOW_SCENARIO, simulation_report_file)
    write_scenario_run_index(reports_dir, scenario_run_index_file)

    return {
        "entity_index": entity_index_file,
        "relationship_manifest": relationship_manifest_file,
        "scenario_run_index": scenario_run_index_file,
        "simulation_report": simulation_report_file,
    }


def _write_sim_report(scenario_file: Path, output_file: Path) -> None:
    loaded = ScenarioLoader().load(scenario_file)
    result = ScenarioRunner().run(loaded)
    write_simulation_report_json(result, output_file)
