from __future__ import annotations

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