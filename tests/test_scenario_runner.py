from __future__ import annotations

import shutil
from pathlib import Path

from typer.testing import CliRunner

from orbitfabric import __version__
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


def test_runner_records_data_flow_evidence_for_declared_data_product() -> None:
    loaded = ScenarioLoader().load(PAYLOAD_SCENARIO)

    result = ScenarioRunner().run(loaded)

    assert result.passed
    assert len(result.state.data_flow_evidence) == 1

    evidence = result.state.data_flow_evidence[0]
    assert evidence.t == 5
    assert evidence.data_product_id == "payload.radiation_histogram"
    assert evidence.producer == "demo_iod_payload"
    assert evidence.producer_type == "payload"
    assert evidence.command_id == "payload.start_acquisition"
    assert evidence.storage_intent == {
        "declared": True,
        "class": "science",
        "retention": "7d",
        "overflow_policy": "drop_oldest",
    }
    assert evidence.downlink_intent == {
        "declared": True,
        "policy": "next_available_contact",
    }
    assert evidence.eligible_downlink_flows == ["science_next_available_contact"]
    assert evidence.contact_windows == ["demo_contact_001"]


def test_runner_checks_data_flow_expectation() -> None:
    loaded = ScenarioLoader().load(PAYLOAD_SCENARIO)

    result = ScenarioRunner().run(loaded)

    assert result.passed
    assert any(
        "DATA_FLOW payload.radiation_histogram EXPECTATION_MET" in entry.message
        for entry in result.state.logs
    )


def test_runner_fails_missing_data_flow_expectation(tmp_path: Path) -> None:
    scenario_path = _copy_payload_scenario_with_replacement(
        tmp_path,
        "data_product: payload.radiation_histogram",
        "data_product: payload.missing_runtime_evidence",
    )
    loaded = ScenarioLoader().load(scenario_path)

    result = ScenarioRunner().run(loaded)

    assert not result.passed
    assert "missing data flow evidence for payload.missing_runtime_evidence" in (
        result.state.failed_expectations
    )


def test_sim_cli_executes_demo_scenario() -> None:
    result = runner.invoke(app, ["sim", str(DEMO_SCENARIO)])

    assert result.exit_code == 0
    assert f"OrbitFabric Scenario Simulator {__version__}" in result.output
    assert "Scenario: battery_low_during_payload" in result.output
    assert "COMMAND payload.start_acquisition -> ACCEPTED" in result.output
    assert "EVENT eps.battery_low severity=WARNING" in result.output
    assert "COMMAND payload.stop_acquisition -> AUTO_DISPATCHED" in result.output
    assert "Result: PASSED" in result.output


def test_sim_cli_executes_nominal_payload_lifecycle_scenario() -> None:
    result = runner.invoke(app, ["sim", str(PAYLOAD_SCENARIO)])

    assert result.exit_code == 0
    assert f"OrbitFabric Scenario Simulator {__version__}" in result.output
    assert "Scenario: nominal_payload_acquisition" in result.output
    assert "PAYLOAD demo_iod_payload LIFECYCLE=READY" in result.output
    assert "COMMAND payload.start_acquisition -> ACCEPTED" in result.output
    assert "PAYLOAD demo_iod_payload LIFECYCLE=ACQUIRING" in result.output
    assert "DATA_PRODUCT payload.radiation_histogram CONTRACT_EVIDENCE_RECORDED" in result.output
    assert "DATA_FLOW payload.radiation_histogram EXPECTATION_MET" in result.output
    assert "COMMAND payload.stop_acquisition -> ACCEPTED" in result.output
    assert "Result: PASSED" in result.output


def _copy_payload_scenario_with_replacement(
    tmp_path: Path,
    old: str,
    new: str,
) -> Path:
    source = Path("examples/demo-3u")
    demo_dir = tmp_path / "demo-3u"
    shutil.copytree(source, demo_dir)

    scenario_path = demo_dir / "scenarios" / "nominal_payload_acquisition.yaml"
    scenario = scenario_path.read_text(encoding="utf-8")
    scenario_path.write_text(scenario.replace(old, new, 1), encoding="utf-8")

    return scenario_path
