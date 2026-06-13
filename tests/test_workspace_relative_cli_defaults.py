from __future__ import annotations

import shutil
from pathlib import Path

from pytest import MonkeyPatch
from typer.testing import CliRunner

from orbitfabric.cli import app

runner = CliRunner()


def test_generation_defaults_are_mission_workspace_relative(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    workspace = _copy_demo_workspace(tmp_path)
    mission_dir = workspace / "mission"

    isolated_cwd = tmp_path / "cwd"
    isolated_cwd.mkdir()
    monkeypatch.chdir(isolated_cwd)
    cwd_generated_dir = isolated_cwd / "generated"

    docs_result = runner.invoke(app, ["gen", "docs", str(mission_dir)])
    assert docs_result.exit_code == 0, docs_result.output
    assert (workspace / "generated" / "docs" / "telemetry.md").exists()
    assert (workspace / "generated" / "docs" / "data_flow.md").exists()

    data_flow_result = runner.invoke(app, ["gen", "data-flow", str(mission_dir)])
    assert data_flow_result.exit_code == 0, data_flow_result.output
    assert (workspace / "generated" / "docs" / "data_flow.md").exists()

    runtime_result = runner.invoke(app, ["gen", "runtime", str(mission_dir)])
    assert runtime_result.exit_code == 0, runtime_result.output
    assert (
        workspace
        / "generated"
        / "runtime"
        / "cpp17"
        / "runtime_contract_manifest.json"
    ).exists()

    ground_result = runner.invoke(app, ["gen", "ground", str(mission_dir)])
    assert ground_result.exit_code == 0, ground_result.output
    assert (
        workspace
        / "generated"
        / "ground"
        / "generic"
        / "ground_contract_manifest.json"
    ).exists()

    assert not cwd_generated_dir.exists()


def test_export_defaults_are_mission_workspace_relative(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    workspace = _copy_demo_workspace(tmp_path)
    mission_dir = workspace / "mission"
    reports_dir = workspace / "generated" / "reports"

    isolated_cwd = tmp_path / "cwd"
    isolated_cwd.mkdir()
    monkeypatch.chdir(isolated_cwd)
    cwd_generated_dir = isolated_cwd / "generated"

    model_summary_result = runner.invoke(
        app,
        ["export", "model-summary", str(mission_dir)],
    )
    assert model_summary_result.exit_code == 0, model_summary_result.output
    assert (reports_dir / "model_summary.json").exists()

    entity_index_result = runner.invoke(
        app,
        ["export", "entity-index", str(mission_dir)],
    )
    assert entity_index_result.exit_code == 0, entity_index_result.output
    assert (reports_dir / "entity_index.json").exists()

    relationship_manifest_result = runner.invoke(
        app,
        ["export", "relationship-manifest", str(mission_dir)],
    )
    assert relationship_manifest_result.exit_code == 0, relationship_manifest_result.output
    assert (reports_dir / "relationship_manifest.json").exists()

    dashboard_summary_result = runner.invoke(
        app,
        ["export", "dashboard-summary", str(mission_dir)],
    )
    assert dashboard_summary_result.exit_code == 0, dashboard_summary_result.output
    assert (reports_dir / "dashboard_summary.json").exists()

    assert not cwd_generated_dir.exists()


def test_coverage_summary_defaults_are_mission_workspace_relative(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    workspace = _copy_demo_workspace(tmp_path)
    mission_dir = workspace / "mission"
    scenario_file = workspace / "scenarios" / "payload_data_flow_evidence.yaml"
    reports_dir = workspace / "generated" / "reports"

    isolated_cwd = tmp_path / "cwd"
    isolated_cwd.mkdir()
    monkeypatch.chdir(isolated_cwd)
    cwd_generated_dir = isolated_cwd / "generated"

    entity_index_result = runner.invoke(
        app,
        ["export", "entity-index", str(mission_dir)],
    )
    assert entity_index_result.exit_code == 0, entity_index_result.output

    relationship_manifest_result = runner.invoke(
        app,
        ["export", "relationship-manifest", str(mission_dir)],
    )
    assert relationship_manifest_result.exit_code == 0, relationship_manifest_result.output

    simulation_report = reports_dir / "payload_data_flow_evidence_report.json"
    sim_result = runner.invoke(
        app,
        ["sim", str(scenario_file), "--json", str(simulation_report)],
    )
    assert sim_result.exit_code == 0, sim_result.output
    assert simulation_report.exists()

    scenario_run_index_result = runner.invoke(
        app,
        [
            "export",
            "scenario-run-index",
            "--simulation-reports",
            str(reports_dir),
            "--json",
            str(reports_dir / "scenario_run_index.json"),
        ],
    )
    assert scenario_run_index_result.exit_code == 0, scenario_run_index_result.output

    coverage_summary_result = runner.invoke(
        app,
        ["export", "coverage-summary", str(mission_dir)],
    )
    assert coverage_summary_result.exit_code == 0, coverage_summary_result.output
    assert (reports_dir / "coverage_summary.json").exists()

    assert not cwd_generated_dir.exists()


def test_explicit_relative_output_path_remains_cwd_relative(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    workspace = _copy_demo_workspace(tmp_path)
    mission_dir = workspace / "mission"

    isolated_cwd = tmp_path / "cwd"
    isolated_cwd.mkdir()
    monkeypatch.chdir(isolated_cwd)

    explicit_output = Path("explicit/generated/docs")

    result = runner.invoke(
        app,
        [
            "gen",
            "docs",
            str(mission_dir),
            "--output-dir",
            str(explicit_output),
        ],
    )

    assert result.exit_code == 0, result.output
    assert (isolated_cwd / explicit_output / "telemetry.md").exists()
    assert not (workspace / "explicit" / "generated" / "docs").exists()


def _copy_demo_workspace(tmp_path: Path) -> Path:
    workspace = tmp_path / "demo-3u"
    shutil.copytree(Path("examples/demo-3u"), workspace)
    return workspace