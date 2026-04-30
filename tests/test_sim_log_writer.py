from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from orbitfabric.cli import app
from orbitfabric.model.scenario_loader import ScenarioLoader
from orbitfabric.sim.log_writer import simulation_result_to_log_text, write_simulation_log
from orbitfabric.sim.runner import ScenarioRunner

DEMO_SCENARIO = Path("examples/demo-3u/scenarios/battery_low_during_payload.yaml")
runner = CliRunner()


def test_simulation_result_to_log_text() -> None:
    loaded = ScenarioLoader().load(DEMO_SCENARIO)
    result = ScenarioRunner().run(loaded)

    text = simulation_result_to_log_text(result)

    assert "OrbitFabric Scenario Log v0.1" in text
    assert "Mission: demo-3u" in text
    assert "Scenario: battery_low_during_payload" in text
    assert "Result: PASSED" in text
    assert "[00:32] EVENT eps.battery_low severity=WARNING" in text
    assert "[00:32] COMMAND payload.stop_acquisition -> AUTO_DISPATCHED" in text
    assert "Failed expectations: 0" in text


def test_write_simulation_log(tmp_path: Path) -> None:
    loaded = ScenarioLoader().load(DEMO_SCENARIO)
    result = ScenarioRunner().run(loaded)
    output_path = tmp_path / "scenario.log"

    write_simulation_log(result, output_path)

    assert output_path.exists()
    text = output_path.read_text(encoding="utf-8")
    assert "OrbitFabric Scenario Log v0.1" in text
    assert "SCENARIO PASSED" in text


def test_sim_command_writes_log_file(tmp_path: Path) -> None:
    output_path = tmp_path / "battery_low.log"

    result = runner.invoke(
        app,
        [
            "sim",
            str(DEMO_SCENARIO),
            "--log",
            str(output_path),
        ],
    )

    assert result.exit_code == 0
    assert output_path.exists()
    assert "Log written to" in result.output

    text = output_path.read_text(encoding="utf-8")
    assert "Scenario: battery_low_during_payload" in text
    assert "Result: PASSED" in text