from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from orbitfabric import __version__
from orbitfabric.cli import app
from orbitfabric.model.scenario_loader import ScenarioLoader
from orbitfabric.sim.json_report import simulation_result_to_dict
from orbitfabric.sim.runner import ScenarioRunner

DEMO_SCENARIO = Path("examples/demo-3u/scenarios/battery_low_during_payload.yaml")
runner = CliRunner()


def test_simulation_result_to_dict_for_demo_scenario() -> None:
    loaded = ScenarioLoader().load(DEMO_SCENARIO)
    result = ScenarioRunner().run(loaded)

    payload = simulation_result_to_dict(result)

    assert payload["tool"] == "orbitfabric-sim"
    assert payload["version"] == __version__
    assert payload["mission"] == "demo-3u"
    assert payload["scenario"] == "battery_low_during_payload"
    assert payload["result"] == "passed"
    assert payload["summary"]["failed_expectations"] == 0
    assert payload["summary"]["data_flow_evidence"] == 1
    assert payload["final_state"]["mode"] == "DEGRADED"
    assert payload["final_state"]["telemetry"]["payload.acquisition.active"] is False

    event_ids = {event["event_id"] for event in payload["events"]}
    assert "eps.battery_low" in event_ids
    assert "payload.acquisition_stopped" in event_ids

    auto_commands = {
        command["command_id"]
        for command in payload["commands"]
        if command["dispatch"] == "AUTO"
    }
    assert "payload.stop_acquisition" in auto_commands

    assert payload["data_flow_evidence"] == [
        {
            "t": 5,
            "data_product_id": "payload.radiation_histogram",
            "producer": "demo_iod_payload",
            "producer_type": "payload",
            "triggered_by_command": "payload.start_acquisition",
            "storage_intent": {
                "declared": True,
                "class": "science",
                "retention": "7d",
                "overflow_policy": "drop_oldest",
            },
            "downlink_intent": {
                "declared": True,
                "policy": "next_available_contact",
            },
            "eligible_downlink_flows": ["science_next_available_contact"],
            "contact_windows": ["demo_contact_001"],
        }
    ]


def test_sim_command_writes_json_report(tmp_path: Path) -> None:
    output_path = tmp_path / "battery_low_report.json"

    result = runner.invoke(
        app,
        [
            "sim",
            str(DEMO_SCENARIO),
            "--json",
            str(output_path),
        ],
    )

    assert result.exit_code == 0
    assert output_path.exists()
    assert "JSON report written to" in result.output

    payload = json.loads(output_path.read_text(encoding="utf-8"))

    assert payload["tool"] == "orbitfabric-sim"
    assert payload["mission"] == "demo-3u"
    assert payload["scenario"] == "battery_low_during_payload"
    assert payload["result"] == "passed"
    assert payload["summary"]["failed_expectations"] == 0
    assert payload["summary"]["data_flow_evidence"] == 1
    assert payload["data_flow_evidence"][0]["data_product_id"] == "payload.radiation_histogram"
    assert payload["data_flow_evidence"][0]["triggered_by_command"] == "payload.start_acquisition"