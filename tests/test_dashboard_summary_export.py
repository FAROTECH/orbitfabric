from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from orbitfabric import __version__
from orbitfabric.cli import app
from orbitfabric.export.dashboard_summary import (
    dashboard_summary_to_dict,
    write_dashboard_summary,
)
from orbitfabric.lint.engine import LintEngine
from orbitfabric.model.loader import MissionModelLoader

DEMO_MISSION = Path("examples/demo-3u/mission")
runner = CliRunner()


def test_dashboard_summary_contains_mission_identity_and_boundaries() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    lint_report = LintEngine().run(model)

    summary = dashboard_summary_to_dict(model, DEMO_MISSION, lint_report)

    assert summary["dashboard_version"] == "0.1-candidate"
    assert summary["kind"] == "orbitfabric.dashboard_summary"
    assert summary["orbitfabric_version"] == __version__
    assert summary["mission"] == {
        "id": "demo-3u",
        "name": "Demo 3U Spacecraft",
        "model_version": "0.1.0",
    }
    assert summary["source"]["mission_dir"] == str(DEMO_MISSION.resolve())
    assert summary["source"]["model_summary_kind"] == "orbitfabric.model_summary"
    assert summary["source"]["entity_index_kind"] == "orbitfabric.entity_index"
    assert summary["source"]["relationship_manifest_kind"] == (
        "orbitfabric.relationship_manifest"
    )
    assert summary["boundaries"] == {
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


def test_dashboard_summary_contains_validation_and_inventory() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    lint_report = LintEngine().run(model)

    summary = dashboard_summary_to_dict(model, DEMO_MISSION, lint_report)

    assert summary["validation"] == {
        "tool": "orbitfabric-lint",
        "result": "passed",
        "errors": 0,
        "warnings": 0,
        "info": 0,
    }

    assert summary["model_domains"]["required"] == {
        "total": 10,
        "present": 10,
        "missing": 0,
    }
    assert summary["model_domains"]["optional"] == {
        "total": 10,
        "present": 10,
        "missing": 0,
    }
    assert summary["model_domains"]["counts"]["commands"] == len(model.commands)
    assert summary["model_domains"]["counts"]["data_products"] == len(
        model.data_products
    )

    assert summary["entity_inventory"]["total_entities"] > 0
    assert summary["entity_inventory"]["domains"]["commands"] == len(
        model.commands
    )
    assert summary["entity_inventory"]["domains"]["data_products"] == len(
        model.data_products
    )

    assert summary["relationship_inventory"]["total_relationships"] > 0
    assert (
        summary["relationship_inventory"]["relationship_types"][
            "data_product_produced_by_payload"
        ]
        == 1
    )


def test_dashboard_summary_marks_coverage_unavailable() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    lint_report = LintEngine().run(model)

    summary = dashboard_summary_to_dict(model, DEMO_MISSION, lint_report)

    assert summary["coverage"] == {
        "status": "not_available",
        "reason": (
            "Coverage metrics are not emitted by OrbitFabric Core "
            "in this report version."
        ),
        "requires_core_output": "coverage_summary.json",
    }


def test_write_dashboard_summary_is_deterministic_json(tmp_path: Path) -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    lint_report = LintEngine().run(model)
    output_file = tmp_path / "dashboard_summary.json"

    written_file = write_dashboard_summary(
        model,
        DEMO_MISSION,
        lint_report,
        output_file,
    )

    assert written_file == output_file
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert content.endswith("\n")

    parsed = json.loads(content)
    assert parsed == dashboard_summary_to_dict(model, DEMO_MISSION, lint_report)


def test_dashboard_summary_command_writes_json_report(tmp_path: Path) -> None:
    output_file = tmp_path / "dashboard_summary.json"

    result = runner.invoke(
        app,
        [
            "export",
            "dashboard-summary",
            "examples/demo-3u/mission",
            "--json",
            str(output_file),
        ],
    )

    assert result.exit_code == 0
    assert output_file.exists()
    assert "OrbitFabric Dashboard Summary Export" in result.output
    assert "Coverage: not_available" in result.output
    assert "JSON report written to" in result.output

    payload = json.loads(output_file.read_text(encoding="utf-8"))

    assert payload["kind"] == "orbitfabric.dashboard_summary"
    assert payload["dashboard_version"] == "0.1-candidate"
    assert payload["mission"]["id"] == "demo-3u"
    assert payload["validation"]["result"] == "passed"
    assert payload["coverage"]["status"] == "not_available"
