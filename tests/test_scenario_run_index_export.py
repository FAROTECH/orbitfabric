from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from orbitfabric import __version__
from orbitfabric.cli import app
from orbitfabric.export.scenario_run_index import (
    scenario_run_index_to_dict,
    write_scenario_run_index,
)
from orbitfabric.model.scenario_loader import ScenarioLoader
from orbitfabric.sim.json_report import write_simulation_report_json
from orbitfabric.sim.runner import ScenarioRunner

DEMO_SCENARIO = Path("examples/demo-3u/scenarios/battery_low_during_payload.yaml")
DATA_FLOW_SCENARIO = Path("examples/demo-3u/scenarios/payload_data_flow_evidence.yaml")
runner = CliRunner()


def test_scenario_run_index_contains_identity_and_boundaries(
    tmp_path: Path,
) -> None:
    reports_dir = _write_demo_reports(tmp_path)

    index = scenario_run_index_to_dict(reports_dir)

    assert index["index_version"] == "0.1-candidate"
    assert index["kind"] == "orbitfabric.scenario_run_index"
    assert index["orbitfabric_version"] == __version__
    assert index["source"] == {
        "simulation_reports_dir": str(reports_dir.resolve()),
        "input_report_tool": "orbitfabric-sim",
    }
    assert index["boundaries"] == {
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


def test_scenario_run_index_contains_runs_and_summary(tmp_path: Path) -> None:
    reports_dir = _write_demo_reports(tmp_path)

    index = scenario_run_index_to_dict(reports_dir)

    assert index["summary"] == {
        "total": 2,
        "passed": 2,
        "failed": 0,
    }

    runs = {(run["mission"], run["scenario"]): run for run in index["runs"]}

    battery_low = runs[("demo-3u", "battery_low_during_payload")]
    assert battery_low["report_file"] == "battery_low_report.json"
    assert battery_low["result"] == "passed"
    assert battery_low["summary"]["failed_expectations"] == 0
    assert battery_low["summary"]["data_flow_evidence"] == 1

    data_flow = runs[("demo-3u", "payload_data_flow_evidence")]
    assert data_flow["report_file"] == "payload_data_flow_report.json"
    assert data_flow["result"] == "passed"
    assert data_flow["summary"]["failed_expectations"] == 0
    assert data_flow["summary"]["data_flow_evidence"] == 1


def test_scenario_run_index_ignores_non_simulation_json(tmp_path: Path) -> None:
    reports_dir = _write_demo_reports(tmp_path)
    (reports_dir / "lint_report.json").write_text(
        json.dumps(
            {
                "tool": "orbitfabric-lint",
                "mission": "demo-3u",
                "result": "passed",
            }
        ),
        encoding="utf-8",
    )
    (reports_dir / "dashboard_summary.json").write_text(
        json.dumps(
            {
                "kind": "orbitfabric.dashboard_summary",
                "mission": {"id": "demo-3u"},
            }
        ),
        encoding="utf-8",
    )

    index = scenario_run_index_to_dict(reports_dir)

    assert index["summary"]["total"] == 2
    assert {run["report_file"] for run in index["runs"]} == {
        "battery_low_report.json",
        "payload_data_flow_report.json",
    }


def test_write_scenario_run_index_is_deterministic_json(tmp_path: Path) -> None:
    reports_dir = _write_demo_reports(tmp_path)
    output_file = tmp_path / "scenario_run_index.json"

    written_file = write_scenario_run_index(reports_dir, output_file)

    assert written_file == output_file
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert content.endswith("\n")

    parsed = json.loads(content)
    assert parsed == scenario_run_index_to_dict(reports_dir)


def test_scenario_run_index_command_writes_json_report(tmp_path: Path) -> None:
    reports_dir = _write_demo_reports(tmp_path)
    output_file = tmp_path / "scenario_run_index.json"

    result = runner.invoke(
        app,
        [
            "export",
            "scenario-run-index",
            "--simulation-reports",
            str(reports_dir),
            "--json",
            str(output_file),
        ],
    )

    assert result.exit_code == 0
    assert output_file.exists()
    assert "OrbitFabric Scenario Run Index Export" in result.output
    assert "Scenario runs indexed: 2" in result.output
    assert "Coverage: not_available" in result.output
    assert "JSON report written to" in result.output

    payload = json.loads(output_file.read_text(encoding="utf-8"))

    assert payload["kind"] == "orbitfabric.scenario_run_index"
    assert payload["index_version"] == "0.1-candidate"
    assert payload["summary"] == {
        "total": 2,
        "passed": 2,
        "failed": 0,
    }


def _write_demo_reports(tmp_path: Path) -> Path:
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()

    _write_sim_report(DEMO_SCENARIO, reports_dir / "battery_low_report.json")
    _write_sim_report(DATA_FLOW_SCENARIO, reports_dir / "payload_data_flow_report.json")

    return reports_dir


def _write_sim_report(scenario_file: Path, output_file: Path) -> None:
    loaded = ScenarioLoader().load(scenario_file)
    result = ScenarioRunner().run(loaded)
    write_simulation_report_json(result, output_file)
