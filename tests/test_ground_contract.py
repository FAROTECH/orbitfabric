from __future__ import annotations

from pathlib import Path

from orbitfabric.gen.ground import build_ground_contract
from orbitfabric.model.loader import MissionModelLoader

DEMO_MISSION = Path("examples/demo-3u/mission")


def test_build_ground_contract_from_demo_mission() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    contract = build_ground_contract(model)

    assert contract.mission_id == "demo-3u"
    assert contract.mission_name == "Demo 3U Spacecraft"
    assert contract.model_version == "0.1.0"
    assert contract.generation_profile == "generic"
    assert len(contract.telemetry) == len(model.telemetry)
    assert len(contract.commands) == len(model.commands)
    assert len(contract.events) == len(model.events)
    assert len(contract.faults) == len(model.faults)
    assert len(contract.data_products) == len(model.data_products)
    assert len(contract.packets) == len(model.packets)


def test_ground_contract_uses_deterministic_ordering() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    contract = build_ground_contract(model)

    assert [item.model_id for item in contract.telemetry] == sorted(
        item.id for item in model.telemetry
    )
    assert [item.model_id for item in contract.commands] == sorted(
        item.id for item in model.commands
    )
    assert [item.model_id for item in contract.events] == sorted(
        item.id for item in model.events
    )
    assert [item.model_id for item in contract.faults] == sorted(
        item.id for item in model.faults
    )
    assert [item.model_id for item in contract.data_products] == sorted(
        item.id for item in model.data_products
    )
    assert [item.model_id for item in contract.packets] == sorted(
        item.id for item in model.packets
    )


def test_ground_contract_exports_telemetry_metadata() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    contract = build_ground_contract(model)

    telemetry = next(
        item for item in contract.telemetry if item.model_id == "eps.battery.voltage"
    )

    assert telemetry.name == "Battery Voltage"
    assert telemetry.value_type == "float32"
    assert telemetry.unit == "V"
    assert telemetry.source == "eps"
    assert telemetry.sampling == "1Hz"
    assert telemetry.criticality == "high"
    assert telemetry.persistence == "store_and_downlink"
    assert telemetry.downlink_priority == "high"
    assert telemetry.limits["warning_low"] == 6.8
    assert telemetry.limits["critical_low"] == 6.4
    assert telemetry.quality == {"required": True, "default": "good"}


def test_ground_contract_exports_command_metadata() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    contract = build_ground_contract(model)

    command = next(
        item for item in contract.commands if item.model_id == "payload.start_acquisition"
    )

    assert command.target == "payload"
    assert command.allowed_modes == ("NOMINAL",)
    assert command.requires_ack is True
    assert command.timeout_ms == 1000
    assert command.risk == "medium"
    assert command.emits == ("payload.acquisition_started",)
    assert command.expected_effects["data_products"] == [
        "payload.radiation_histogram"
    ]
    assert command.preconditions == {
        "payload_lifecycle": {
            "payload": "demo_iod_payload",
            "state": "READY",
        }
    }
    assert len(command.arguments) == 1

    argument = command.arguments[0]
    assert argument.name == "duration_s"
    assert argument.value_type == "uint16"
    assert argument.minimum == 1
    assert argument.maximum == 600


def test_ground_contract_exports_event_fault_data_product_and_packet_metadata() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    contract = build_ground_contract(model)

    event = next(item for item in contract.events if item.model_id == "eps.battery_low")
    assert event.source == "eps"
    assert event.severity == "warning"
    assert event.downlink_priority == "high"
    assert event.persistence == "store_and_downlink"

    fault = next(
        item for item in contract.faults if item.model_id == "eps.battery_low_fault"
    )
    assert fault.source == "eps"
    assert fault.severity == "warning"
    assert fault.condition["telemetry"] == "eps.battery.voltage"
    assert fault.condition["value"] == 6.8
    assert fault.emits == ("eps.battery_low",)
    assert fault.recovery == {
        "mode_transition": "DEGRADED",
        "auto_commands": ["payload.stop_acquisition"],
    }

    data_product = next(
        item
        for item in contract.data_products
        if item.model_id == "payload.radiation_histogram"
    )
    assert data_product.producer == "demo_iod_payload"
    assert data_product.producer_type == "payload"
    assert data_product.type == "histogram"
    assert data_product.estimated_size_bytes == 4096
    assert data_product.priority == "high"
    assert data_product.storage == {
        "class": "science",
        "retention": "7d",
        "overflow_policy": "drop_oldest",
    }
    assert data_product.downlink == {"policy": "next_available_contact"}

    packet = next(item for item in contract.packets if item.model_id == "hk_fast")
    assert packet.name == "Fast Housekeeping Packet"
    assert packet.type == "json"
    assert packet.max_payload_bytes == 512
    assert packet.period == "1s"
    assert packet.telemetry == (
        "obc.mode",
        "eps.battery.voltage",
        "eps.battery.current",
    )


def test_ground_contract_supports_explicit_generation_profile() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    contract = build_ground_contract(model, generation_profile="test-profile")

    assert contract.generation_profile == "test-profile"
