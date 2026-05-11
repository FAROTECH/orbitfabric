from __future__ import annotations

import json
from pathlib import Path

from orbitfabric.gen.ground import (
    build_ground_contract,
    ground_dictionary_documents,
    write_ground_dictionary_json_files,
)
from orbitfabric.model.loader import MissionModelLoader

DEMO_MISSION = Path("examples/demo-3u/mission")


def test_ground_dictionary_documents_include_expected_domains() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    contract = build_ground_contract(model)

    documents = ground_dictionary_documents(contract)

    assert set(documents) == {
        "telemetry_dictionary",
        "command_dictionary",
        "event_dictionary",
        "fault_dictionary",
        "data_product_dictionary",
        "packet_dictionary",
    }
    assert len(documents["telemetry_dictionary"]) == len(contract.telemetry)
    assert len(documents["command_dictionary"]) == len(contract.commands)
    assert len(documents["event_dictionary"]) == len(contract.events)
    assert len(documents["fault_dictionary"]) == len(contract.faults)
    assert len(documents["data_product_dictionary"]) == len(contract.data_products)
    assert len(documents["packet_dictionary"]) == len(contract.packets)


def test_ground_dictionary_documents_preserve_deterministic_ordering() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    contract = build_ground_contract(model)

    documents = ground_dictionary_documents(contract)

    for dictionary in documents.values():
        model_ids = [item["model_id"] for item in dictionary]
        assert model_ids == sorted(model_ids)


def test_ground_dictionary_documents_export_command_and_telemetry_metadata() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    contract = build_ground_contract(model)

    documents = ground_dictionary_documents(contract)

    telemetry = next(
        item
        for item in documents["telemetry_dictionary"]
        if item["model_id"] == "eps.battery.voltage"
    )
    assert telemetry["value_type"] == "float32"
    assert telemetry["unit"] == "V"
    assert telemetry["criticality"] == "high"
    assert telemetry["limits"]["warning_low"] == 6.8

    command = next(
        item
        for item in documents["command_dictionary"]
        if item["model_id"] == "payload.start_acquisition"
    )
    assert command["target"] == "payload"
    assert command["requires_ack"] is True
    assert command["timeout_ms"] == 1000
    assert command["risk"] == "medium"
    assert command["expected_effects"]["data_products"] == [
        "payload.radiation_histogram"
    ]
    assert command["arguments"][0]["name"] == "duration_s"
    assert command["arguments"][0]["value_type"] == "uint16"


def test_write_ground_dictionary_json_files(tmp_path: Path) -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    contract = build_ground_contract(model)

    written_files = write_ground_dictionary_json_files(contract, tmp_path)

    assert written_files == [
        tmp_path / "dictionaries" / "telemetry_dictionary.json",
        tmp_path / "dictionaries" / "command_dictionary.json",
        tmp_path / "dictionaries" / "event_dictionary.json",
        tmp_path / "dictionaries" / "fault_dictionary.json",
        tmp_path / "dictionaries" / "data_product_dictionary.json",
        tmp_path / "dictionaries" / "packet_dictionary.json",
    ]

    for output_file in written_files:
        assert output_file.exists()
        content = output_file.read_text(encoding="utf-8")
        assert content.endswith("\n")
        assert isinstance(json.loads(content), list)

    telemetry_document = json.loads(
        (tmp_path / "dictionaries" / "telemetry_dictionary.json").read_text(
            encoding="utf-8"
        )
    )
    assert telemetry_document == ground_dictionary_documents(contract)[
        "telemetry_dictionary"
    ]
