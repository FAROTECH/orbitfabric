from __future__ import annotations

import json
import shutil
from pathlib import Path

from typer.testing import CliRunner

from orbitfabric import __version__
from orbitfabric.cli import app
from orbitfabric.model.scenario_loader import ScenarioLoader
from orbitfabric.sim.json_report import simulation_result_to_dict
from orbitfabric.sim.runner import ScenarioRunner

DEMO_SCENARIO = Path("examples/demo-3u/scenarios/battery_low_during_payload.yaml")
DATA_FLOW_SCENARIO = Path("examples/demo-3u/scenarios/payload_data_flow_evidence.yaml")
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


def test_simulation_result_to_dict_for_data_flow_evidence_scenario() -> None:
    loaded = ScenarioLoader().load(DATA_FLOW_SCENARIO)
    result = ScenarioRunner().run(loaded)

    payload = simulation_result_to_dict(result)

    assert payload["mission"] == "demo-3u"
    assert payload["scenario"] == "payload_data_flow_evidence"
    assert payload["result"] == "passed"
    assert payload["summary"]["data_flow_evidence"] == 1
    assert payload["summary"]["failed_expectations"] == 0
    assert payload["data_flow_evidence"][0]["data_product_id"] == (
        "payload.radiation_histogram"
    )
    assert payload["data_flow_evidence"][0]["triggered_by_command"] == (
        "payload.start_acquisition"
    )


def test_simulation_result_to_dict_contains_structured_expectation_accounting() -> None:
    loaded = ScenarioLoader().load(DATA_FLOW_SCENARIO)
    result = ScenarioRunner().run(loaded)

    payload = simulation_result_to_dict(result)

    assert payload["summary"]["expectations"] == 12
    assert payload["summary"]["passed_expectations"] == 12
    assert payload["summary"]["failed_expectations"] == 0
    assert payload["expectations"]["total"] == 12
    assert payload["expectations"]["passed"] == 12
    assert payload["expectations"]["failed"] == 0
    assert payload["failed_expectations"] == []

    records = payload["expectations"]["records"]
    assert len(records) == 12
    assert {
        record["expectation_type"] for record in records
    } == {
        "mode",
        "payload_lifecycle",
        "command_status",
        "event",
        "telemetry",
        "data_flow",
        "scenario_status",
    }
    assert all(record["result"] == "passed" for record in records)

    data_flow_record = next(
        record for record in records if record["expectation_type"] == "data_flow"
    )
    assert data_flow_record["target"] == "payload.radiation_histogram"
    assert data_flow_record["expected"]["triggered_by_command"] == (
        "payload.start_acquisition"
    )
    assert data_flow_record["actual"]["triggered_by_command"] == (
        "payload.start_acquisition"
    )
    assert data_flow_record["message"] == "expectation passed"


def test_failed_simulation_report_keeps_legacy_failed_expectations(
    tmp_path: Path,
) -> None:
    scenario_path = _copy_data_flow_scenario_with_failing_telemetry(tmp_path)
    loaded = ScenarioLoader().load(scenario_path)
    result = ScenarioRunner().run(loaded)

    payload = simulation_result_to_dict(result)

    assert payload["result"] == "failed"
    assert payload["summary"]["expectations"] == 12
    assert payload["summary"]["passed_expectations"] == 10
    assert payload["summary"]["failed_expectations"] == 2
    assert payload["expectations"]["total"] == 12
    assert payload["expectations"]["passed"] == 10
    assert payload["expectations"]["failed"] == 2
    assert payload["failed_expectations"] == [
        "expected telemetry payload.acquisition.active=false but got true",
        "expected scenario status PASSED but got FAILED",
    ]

    failed_records = [
        record
        for record in payload["expectations"]["records"]
        if record["result"] == "failed"
    ]
    assert [record["expectation_type"] for record in failed_records] == [
        "telemetry",
        "scenario_status",
    ]
    assert failed_records[0] == {
        "t": 8,
        "expectation_type": "telemetry",
        "target": "payload.acquisition.active",
        "expected": False,
        "actual": True,
        "result": "failed",
        "message": "expected telemetry payload.acquisition.active=false but got true",
    }


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
    assert payload["data_flow_evidence"][0]["data_product_id"] == (
        "payload.radiation_histogram"
    )
    assert payload["data_flow_evidence"][0]["triggered_by_command"] == (
        "payload.start_acquisition"
    )


def test_sim_command_writes_data_flow_evidence_json_report(tmp_path: Path) -> None:
    output_path = tmp_path / "payload_data_flow_evidence_report.json"

    result = runner.invoke(
        app,
        [
            "sim",
            str(DATA_FLOW_SCENARIO),
            "--json",
            str(output_path),
        ],
    )

    assert result.exit_code == 0
    assert output_path.exists()
    assert "JSON report written to" in result.output

    payload = json.loads(output_path.read_text(encoding="utf-8"))

    assert payload["scenario"] == "payload_data_flow_evidence"
    assert payload["result"] == "passed"
    assert payload["summary"]["data_flow_evidence"] == 1
    assert payload["summary"]["failed_expectations"] == 0
    assert payload["summary"]["expectations"] == 12
    assert payload["summary"]["passed_expectations"] == 12
    assert payload["expectations"]["failed"] == 0
    assert payload["data_flow_evidence"][0]["data_product_id"] == (
        "payload.radiation_histogram"
    )


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
