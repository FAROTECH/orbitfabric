from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from typer.testing import CliRunner

from orbitfabric.cli import app
from orbitfabric.model.errors import MissionModelError
from orbitfabric.model.scenario_loader import ScenarioLoader

DEMO_SCENARIO = Path("examples/demo-3u/scenarios/battery_low_during_payload.yaml")
runner = CliRunner()


def test_load_demo_scenario() -> None:
    loaded = ScenarioLoader().load(DEMO_SCENARIO)

    assert loaded.scenario.scenario.id == "battery_low_during_payload"
    assert loaded.mission_model.spacecraft.id == "demo-3u"
    assert loaded.scenario.initial_state.mode == "NOMINAL"
    assert len(loaded.scenario.steps) == 13


def test_sim_cli_loads_demo_scenario() -> None:
    result = runner.invoke(app, ["sim", str(DEMO_SCENARIO)])

    assert result.exit_code == 0
    assert "OrbitFabric Scenario Simulator v0.1" in result.output
    assert "Scenario: battery_low_during_payload" in result.output
    assert "Mission: demo-3u" in result.output
    assert "Result: PASSED" in result.output


def test_scenario_loader_rejects_missing_file() -> None:
    with pytest.raises(MissionModelError) as exc_info:
        ScenarioLoader().load(Path("missing-scenario.yaml"))

    assert exc_info.value.diagnostics[0].code == "OF-SCN-000"

def test_validate_scenario_cli_loads_demo_scenario() -> None:
    result = runner.invoke(app, ["validate", "scenario", str(DEMO_SCENARIO)])

    assert result.exit_code == 0
    assert "OrbitFabric Scenario Validation v0.1" in result.output
    assert "Scenario: battery_low_during_payload" in result.output
    assert "Mission: demo-3u" in result.output
    assert "Initial mode: NOMINAL" in result.output
    assert "Steps: 13" in result.output
    assert "Result: PASSED" in result.output
    assert "Timeline:" not in result.output
    assert "COMMAND payload.start_acquisition" not in result.output


def test_validate_scenario_cli_rejects_unknown_command(tmp_path: Path) -> None:
    scenario_path = _copy_demo_scenario_with_unknown_command(tmp_path)

    result = runner.invoke(app, ["validate", "scenario", str(scenario_path)])

    assert result.exit_code == 1
    assert "OF-SCN-001" in result.output
    assert "unknown command" in result.output
    assert "Result: FAILED" in result.output


def _copy_demo_scenario_with_unknown_command(tmp_path: Path) -> Path:
    source = Path("examples/demo-3u")
    demo_dir = tmp_path / "demo-3u"
    shutil.copytree(source, demo_dir)

    scenario_path = demo_dir / "scenarios" / "battery_low_during_payload.yaml"
    scenario = scenario_path.read_text(encoding="utf-8")
    scenario = scenario.replace(
        "command: payload.start_acquisition",
        "command: payload.unknown_command",
        1,
    )
    scenario_path.write_text(scenario, encoding="utf-8")

    return scenario_path