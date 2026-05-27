from __future__ import annotations

import json
import shutil
from pathlib import Path

from orbitfabric.export.coverage_summary import coverage_summary_to_dict
from orbitfabric.export.dashboard_summary import dashboard_summary_to_dict
from orbitfabric.export.entity_index import write_entity_index
from orbitfabric.export.relationship_manifest import write_relationship_manifest
from orbitfabric.export.scenario_run_index import (
    scenario_run_index_to_dict,
    write_scenario_run_index,
)
from orbitfabric.lint.engine import LintEngine
from orbitfabric.model.loader import MissionModelLoader
from orbitfabric.model.scenario_loader import ScenarioLoader
from orbitfabric.sim.json_report import (
    simulation_result_to_dict,
    write_simulation_report_json,
)
from orbitfabric.sim.runner import ScenarioRunner

DEMO_MISSION = Path("examples/demo-3u/mission")
DATA_FLOW_SCENARIO = Path(
    "examples/demo-3u/scenarios/payload_data_flow_evidence.yaml"
)

MISSION_IDENTITY = {
    "id": "demo-3u",
    "name": "Demo 3U Spacecraft",
    "model_version": "0.1.0",
}


def test_dashboard_summary_candidate_contract_signature() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    lint_report = LintEngine().run(model)

    payload = dashboard_summary_to_dict(model, DEMO_MISSION, lint_report)

    assert payload["kind"] == "orbitfabric.dashboard_summary"
    assert payload["dashboard_version"] == "0.1-candidate"
    assert payload["mission"] == MISSION_IDENTITY
    assert payload["source"]["model_summary_kind"] == "orbitfabric.model_summary"
    assert payload["source"]["entity_index_kind"] == "orbitfabric.entity_index"
    assert payload["source"]["relationship_manifest_kind"] == (
        "orbitfabric.relationship_manifest"
    )
    assert payload["boundaries"] == {
        "source_of_truth": "mission_model",
        "core_derived_report": True,
        "read_only": True,
        "contains_dashboard_summary": True,
        "contains_coverage_metrics": False,
        "contains_health_score": False,
        "contains_scenario_run_index": False,
        "contains_expectation_accounting": False,
        "contains_relationship_graph": False,
        "contains_dependency_graph": False,
        "contains_yaml_ast": False,
        "contains_source_locations": False,
        "contains_plugin_api": False,
        "contains_studio_api": False,
        "contains_runtime_behavior": False,
        "contains_ground_behavior": False,
    }
    assert payload["coverage"] == {
        "status": "not_available",
        "reason": (
            "Coverage metrics are not emitted by OrbitFabric Core "
            "in this report version."
        ),
        "requires_core_output": "coverage_summary.json",
    }


def test_scenario_run_index_candidate_contract_signature(tmp_path: Path) -> None:
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()
    _write_sim_report(DATA_FLOW_SCENARIO, reports_dir / "data_flow.json")
    (reports_dir / "dashboard_summary.json").write_text(
        json.dumps({"kind": "orbitfabric.dashboard_summary"}),
        encoding="utf-8",
    )

    payload = scenario_run_index_to_dict(reports_dir)

    assert payload["kind"] == "orbitfabric.scenario_run_index"
    assert payload["index_version"] == "0.1-candidate"
    assert payload["source"] == {
        "simulation_reports_dir": str(reports_dir.resolve()),
        "input_report_tool": "orbitfabric-sim",
    }
    assert payload["boundaries"] == {
        "source_of_truth": "simulation_json_reports",
        "core_derived_report": True,
        "read_only": True,
        "contains_scenario_run_index": True,
        "contains_coverage_metrics": False,
        "contains_health_score": False,
        "contains_expectation_accounting": False,
        "contains_relationship_graph": False,
        "contains_dependency_graph": False,
        "contains_yaml_ast": False,
        "contains_source_locations": False,
        "contains_plugin_api": False,
        "contains_studio_api": False,
        "contains_runtime_behavior": False,
        "contains_ground_behavior": False,
        "derived_from_simulation_json": True,
        "derived_from_logs": False,
    }
    assert set(payload["summary"]) == {"total", "passed", "failed"}
    assert payload["summary"] == {"total": 1, "passed": 1, "failed": 0}
    assert len(payload["runs"]) == 1

    run = payload["runs"][0]
    assert set(run) == {
        "report_file",
        "report_path",
        "mission",
        "scenario",
        "result",
        "summary",
    }
    assert run["mission"] == "demo-3u"
    assert run["scenario"] == "payload_data_flow_evidence"
    assert run["result"] == "passed"
    assert {
        "events",
        "commands",
        "mode_transitions",
        "data_flow_evidence",
        "expectations",
        "passed_expectations",
        "failed_expectations",
    } <= set(run["summary"])


def test_simulation_json_expectation_accounting_signature() -> None:
    loaded = ScenarioLoader().load(DATA_FLOW_SCENARIO)
    result = ScenarioRunner().run(loaded)

    payload = simulation_result_to_dict(result)

    assert payload["tool"] == "orbitfabric-sim"
    assert payload["mission"] == "demo-3u"
    assert payload["scenario"] == "payload_data_flow_evidence"
    assert payload["result"] == "passed"
    assert payload["summary"]["expectations"] == 12
    assert payload["summary"]["passed_expectations"] == 12
    assert payload["summary"]["failed_expectations"] == 0
    assert payload["failed_expectations"] == []
    assert set(payload["expectations"]) == {
        "total",
        "passed",
        "failed",
        "records",
    }
    assert payload["expectations"]["total"] == 12
    assert payload["expectations"]["passed"] == 12
    assert payload["expectations"]["failed"] == 0

    records = payload["expectations"]["records"]
    assert records
    assert all(
        set(record) == {
            "t",
            "expectation_type",
            "target",
            "expected",
            "actual",
            "result",
            "message",
        }
        for record in records
    )
    assert {record["result"] for record in records} == {"passed"}


def test_simulation_json_failed_expectations_legacy_signature(
    tmp_path: Path,
) -> None:
    scenario_path = _copy_data_flow_scenario_with_failing_telemetry(tmp_path)
    loaded = ScenarioLoader().load(scenario_path)
    result = ScenarioRunner().run(loaded)

    payload = simulation_result_to_dict(result)

    assert payload["result"] == "failed"
    assert payload["summary"]["failed_expectations"] == 2
    assert payload["expectations"]["failed"] == 2
    assert payload["failed_expectations"] == [
        "expected telemetry payload.acquisition.active=false but got true",
        "expected scenario status PASSED but got FAILED",
    ]
    assert [
        record["message"]
        for record in payload["expectations"]["records"]
        if record["result"] == "failed"
    ] == payload["failed_expectations"]


def test_coverage_summary_candidate_contract_signature(tmp_path: Path) -> None:
    paths = _write_core_inputs(tmp_path)

    payload = coverage_summary_to_dict(
        DEMO_MISSION,
        paths["entity_index"],
        paths["relationship_manifest"],
        paths["scenario_run_index"],
    )

    assert payload["kind"] == "orbitfabric.coverage_summary"
    assert payload["coverage_version"] == "0.1-candidate"
    assert payload["mission"] == MISSION_IDENTITY
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
    assert set(payload["scenario_runs"]) == {"total", "passed", "failed"}
    assert set(payload["entity_coverage"]) == {
        "commands",
        "events",
        "data_products",
    }

    for entity_signature in payload["entity_coverage"].values():
        assert set(entity_signature) == {
            "total",
            "covered",
            "uncovered",
            "coverage_ratio",
            "covered_ids",
            "uncovered_ids",
        }

    assert set(payload["expectation_coverage"]) == {
        "total",
        "passed",
        "failed",
        "pass_ratio",
        "by_type",
    }
    assert payload["expectation_coverage"]["total"] == 12
    assert payload["expectation_coverage"]["passed"] == 12
    assert payload["expectation_coverage"]["failed"] == 0

    relationships = payload["relationship_coverage"]
    assert set(relationships) == {
        "supported_relationship_types",
        "total_supported_relationships",
        "covered_supported_relationships",
        "uncovered_supported_relationships",
        "coverage_ratio",
        "covered_relationship_ids",
        "uncovered_relationship_ids",
        "by_type",
    }
    assert relationships["supported_relationship_types"] == [
        "data_product_produced_by_payload",
        "data_product_produced_by_subsystem",
        "downlink_flow_includes_data_product",
    ]
    assert set(relationships["by_type"]) == set(
        relationships["supported_relationship_types"]
    )
    for relationship_type_signature in relationships["by_type"].values():
        assert set(relationship_type_signature) == {
            "total",
            "covered",
            "uncovered",
            "coverage_ratio",
            "covered_ids",
            "uncovered_ids",
        }
    assert "unsupported" in payload
    assert set(payload["unsupported"]) == {
        "entity_domains",
        "relationship_types",
    }


def _write_core_inputs(tmp_path: Path) -> dict[str, Path]:
    model = MissionModelLoader().load(DEMO_MISSION)
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()

    entity_index_file = reports_dir / "entity_index.json"
    relationship_manifest_file = reports_dir / "relationship_manifest.json"
    simulation_report_file = reports_dir / "payload_data_flow_report.json"
    scenario_run_index_file = reports_dir / "scenario_run_index.json"

    write_entity_index(model, DEMO_MISSION, entity_index_file)
    write_relationship_manifest(model, DEMO_MISSION, relationship_manifest_file)
    _write_sim_report(DATA_FLOW_SCENARIO, simulation_report_file)
    write_scenario_run_index(reports_dir, scenario_run_index_file)

    return {
        "entity_index": entity_index_file,
        "relationship_manifest": relationship_manifest_file,
        "scenario_run_index": scenario_run_index_file,
    }


def _write_sim_report(scenario_file: Path, output_file: Path) -> None:
    loaded = ScenarioLoader().load(scenario_file)
    result = ScenarioRunner().run(loaded)
    write_simulation_report_json(result, output_file)


def _copy_data_flow_scenario_with_failing_telemetry(tmp_path: Path) -> Path:
    source = Path("examples/demo-3u")
    demo_dir = tmp_path / "demo-3u"
    shutil.copytree(source, demo_dir)

    scenario_path = demo_dir / "scenarios" / "payload_data_flow_evidence.yaml"
    scenario = scenario_path.read_text(encoding="utf-8")
    scenario_path.write_text(
        scenario.replace(
            "  - t: 8\n"
            "    expect_telemetry:\n"
            "      payload.acquisition.active: true\n",
            "  - t: 8\n"
            "    expect_telemetry:\n"
            "      payload.acquisition.active: false\n",
            1,
        ),
        encoding="utf-8",
    )

    return scenario_path
