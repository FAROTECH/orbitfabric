from __future__ import annotations

import csv
import json
from pathlib import Path

from orbitfabric.gen.ground import build_ground_contract, write_ground_dictionary_csv_files
from orbitfabric.model.loader import MissionModelLoader

DEMO_MISSION = Path("examples/demo-3u/mission")


def test_write_ground_dictionary_csv_files(tmp_path: Path) -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    contract = build_ground_contract(model)

    written_files = write_ground_dictionary_csv_files(contract, tmp_path)

    assert written_files == [
        tmp_path / "csv" / "telemetry_dictionary.csv",
        tmp_path / "csv" / "command_dictionary.csv",
        tmp_path / "csv" / "event_dictionary.csv",
        tmp_path / "csv" / "fault_dictionary.csv",
        tmp_path / "csv" / "data_product_dictionary.csv",
        tmp_path / "csv" / "packet_dictionary.csv",
    ]

    for output_file in written_files:
        assert output_file.exists()
        assert output_file.read_text(encoding="utf-8")


def test_ground_csv_telemetry_headers_and_rows(tmp_path: Path) -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    contract = build_ground_contract(model)

    write_ground_dictionary_csv_files(contract, tmp_path)

    telemetry_file = tmp_path / "csv" / "telemetry_dictionary.csv"
    with telemetry_file.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))

    assert rows
    assert rows[0].keys() == {
        "model_id",
        "name",
        "value_type",
        "unit",
        "source",
        "sampling",
        "criticality",
        "persistence",
        "downlink_priority",
        "limits",
        "enum_values",
        "quality",
        "description",
    }
    assert [row["model_id"] for row in rows] == sorted(row["model_id"] for row in rows)

    battery_voltage = next(
        row for row in rows if row["model_id"] == "eps.battery.voltage"
    )
    assert battery_voltage["name"] == "Battery Voltage"
    assert battery_voltage["value_type"] == "float32"
    assert battery_voltage["unit"] == "V"
    assert json.loads(battery_voltage["limits"])["warning_low"] == 6.8
    assert json.loads(battery_voltage["quality"]) == {
        "default": "good",
        "required": True,
    }


def test_ground_csv_command_nested_fields_are_json_cells(tmp_path: Path) -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    contract = build_ground_contract(model)

    write_ground_dictionary_csv_files(contract, tmp_path)

    command_file = tmp_path / "csv" / "command_dictionary.csv"
    with command_file.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))

    command = next(row for row in rows if row["model_id"] == "payload.start_acquisition")

    assert command["target"] == "payload"
    assert command["risk"] == "medium"
    assert json.loads(command["allowed_modes"]) == ["NOMINAL"]
    assert json.loads(command["emits"]) == ["payload.acquisition_started"]
    assert json.loads(command["arguments"])[0]["name"] == "duration_s"
    assert json.loads(command["expected_effects"])["data_products"] == [
        "payload.radiation_histogram"
    ]
