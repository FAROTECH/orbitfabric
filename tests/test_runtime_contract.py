from __future__ import annotations

from pathlib import Path

from orbitfabric.gen.runtime import build_runtime_contract
from orbitfabric.model.loader import MissionModelLoader

DEMO_MISSION = Path("examples/demo-3u/mission")


def test_build_runtime_contract_from_demo_mission() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    contract = build_runtime_contract(model)

    assert contract.mission_id == "demo-3u"
    assert contract.mission_name == "Demo 3U Spacecraft"
    assert contract.model_version == "0.1.0"
    assert contract.generation_profile == "cpp17"
    assert len(contract.modes) == len(model.modes)
    assert len(contract.telemetry) == len(model.telemetry)
    assert len(contract.commands) == len(model.commands)
    assert len(contract.events) == len(model.events)
    assert len(contract.faults) == len(model.faults)
    assert len(contract.packets) == len(model.packets)
    assert len(contract.payloads) == len(model.payloads)
    assert len(contract.data_products) == len(model.data_products)


def test_runtime_contract_uses_deterministic_numeric_ids() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    contract = build_runtime_contract(model)

    command_ids = [command.model_id for command in contract.commands]
    command_numeric_ids = [command.numeric_id for command in contract.commands]

    assert command_ids == sorted(command_ids)
    assert command_numeric_ids == list(range(1, len(contract.commands) + 1))


def test_runtime_contract_exports_command_arguments() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    contract = build_runtime_contract(model)

    start_command = next(
        command
        for command in contract.commands
        if command.model_id == "payload.start_acquisition"
    )

    assert start_command.symbol_name == "PayloadStartAcquisition"
    assert len(start_command.arguments) == 1

    argument = start_command.arguments[0]

    assert argument.model_id == "duration_s"
    assert argument.symbol_name == "DurationS"
    assert argument.value_type == "uint16"
    assert argument.minimum == 1
    assert argument.maximum == 600


def test_runtime_contract_exports_data_product_policies() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    contract = build_runtime_contract(model)

    data_product = next(
        item
        for item in contract.data_products
        if item.model_id == "payload.radiation_histogram"
    )

    assert data_product.symbol_name == "PayloadRadiationHistogram"
    assert data_product.metadata["storage_policy"] == "science"
    assert data_product.metadata["downlink_policy"] == "next_available_contact"

    assert [item.model_id for item in contract.storage_policies] == ["science"]
    assert [item.model_id for item in contract.downlink_policies] == [
        "next_available_contact"
    ]


def test_runtime_contract_supports_explicit_generation_profile() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    contract = build_runtime_contract(model, generation_profile="test-profile")

    assert contract.generation_profile == "test-profile"
