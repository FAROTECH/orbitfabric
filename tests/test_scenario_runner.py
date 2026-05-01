from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from orbitfabric.cli import app
from orbitfabric.model.scenario_loader import ScenarioLoader
from orbitfabric.sim.runner import ScenarioRunner

DEMO_SCENARIO = Path("examples/demo-3u/scenarios/battery_low_during_payload.yaml")
PAYLOAD_SCENARIO = Path("examples/demo-3u/scenarios/nominal_payload_acquisition.yaml")
runner = CliRunner()


def test_runner_executes_battery_low_scenario() -> None:
    loaded = ScenarioLoader().load(DEMO_SCENARIO)

    result = ScenarioRunner().run(loaded)

    assert result.passed
    assert result.result_label == "PASSED"
    assert result.state.current_mode == "DEGRADED"
    assert result.state.telemetry["payload.acquisition.active"] is False

    emitted_events = {event.event_id for event in result.state.events}
    assert "payload.acquisition_started" in emitted_events
    assert "eps.battery_low" in emitted_events
    assert "payload.acquisition_stopped" in emitted_events

    auto_commands = {
        command.command_id
        for command in result.state.commands
        if command.dispatch == "AUTO"
    }
    assert "payload.stop_acquisition" in auto_commands


def test_runner_executes_nominal_payload_lifecycle_scenario() -> None:
    loaded = ScenarioLoader().load(PAYLOAD_SCENARIO)

    result = ScenarioRunner().run(loaded)

    assert result.passed
    assert result.result_label == "PASSED"
    assert result.state.current_mode == "PAYLOAD_ACTIVE"
    assert result.state.telemetry["payload.acquisition.active"] is False
    assert result.state.payload_lifecycle["demo_iod_payload"] == "READY"

    emitted_events = {event.event_id for event in result.state.events}
    assert "payload.acquisition_started" in emitted_events
    assert "payload.acquisition_stopped" in emitted_events

    ground_commands = {
        command.command_id
        for command in result.state.commands
        if command.dispatch == "GROUND"
    }
    assert "payload.start_acquisition" in ground_commands
    assert "payload.stop_acquisition" in ground_commands


def test_sim_cli_executes_demo_scenario() -> None:
    result = runner.invoke(app, ["sim", str(DEMO_SCENARIO)])

    assert result.exit_code == 0
    assert "OrbitFabric Scenario Simulator v0.1" in result.output
    assert "Scenario: battery_low_during_payload" in result.output
    assert "COMMAND payload.start_acquisition -> ACCEPTED" in result.output
    assert "EVENT eps.battery_low severity=WARNING" in result.output
    assert "COMMAND payload.stop_acquisition -> AUTO_DISPATCHED" in result.output
    assert "Result: PASSED" in result.output


def test_sim_cli_executes_nominal_payload_lifecycle_scenario() -> None:
    result = runner.invoke(app, ["sim", str(PAYLOAD_SCENARIO)])

    assert result.exit_code == 0
    assert "OrbitFabric Scenario Simulator v0.1" in result.output
    assert "Scenario: nominal_payload_acquisition" in result.output
    assert "PAYLOAD demo_iod_payload LIFECYCLE=READY" in result.output
    assert "COMMAND payload.start_acquisition -> ACCEPTED" in result.output
    assert "PAYLOAD demo_iod_payload LIFECYCLE=ACQUIRING" in result.output
    assert "COMMAND payload.stop_acquisition -> ACCEPTED" in result.output
    assert "Result: PASSED" in result.output