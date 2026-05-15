from __future__ import annotations

import json
from pathlib import Path

from orbitfabric import __version__
from orbitfabric.export.relationship_manifest import (
    relationship_manifest_to_dict,
    write_relationship_manifest,
)
from orbitfabric.model.loader import MissionModelLoader

DEMO_MISSION = Path("examples/demo-3u/mission")


def test_relationship_manifest_contains_identity_and_boundaries() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    manifest = relationship_manifest_to_dict(model, DEMO_MISSION)

    assert manifest["manifest_version"] == "0.1-candidate"
    assert manifest["kind"] == "orbitfabric.relationship_manifest"
    assert manifest["orbitfabric_version"] == __version__
    assert manifest["status"] == "candidate"
    assert manifest["mission"] == {
        "id": "demo-3u",
        "name": "Demo 3U Spacecraft",
        "model_version": "0.1.0",
    }
    assert manifest["source"]["mission_dir"] == str(DEMO_MISSION.resolve())
    assert manifest["source"]["entity_index_kind"] == "orbitfabric.entity_index"
    assert manifest["source"]["entity_index_version"] == "0.1"
    assert manifest["boundaries"] == {
        "source_of_truth": "mission_model",
        "core_derived_report": True,
        "read_only": True,
        "contains_entity_index": False,
        "contains_entity_records": False,
        "contains_relationship_manifest": True,
        "contains_relationship_records": True,
        "contains_relationship_graph": False,
        "contains_dependency_graph": False,
        "contains_yaml_ast": False,
        "contains_source_locations": False,
        "contains_plugin_api": False,
        "contains_studio_api": False,
        "contains_runtime_behavior": False,
        "contains_ground_behavior": False,
    }


def test_relationship_manifest_emits_admitted_relationship_records() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    manifest = relationship_manifest_to_dict(model, DEMO_MISSION)

    assert manifest["counts"] == {
        "total_relationships": 27,
        "relationship_types": {
            "command_emits_event": 4,
            "command_targets_subsystem": 4,
            "data_product_produced_by_payload": 1,
            "fault_emits_event": 2,
            "packet_includes_telemetry": 5,
            "payload_accepts_command": 2,
            "payload_belongs_to_subsystem": 1,
            "payload_generates_event": 2,
            "payload_produces_telemetry": 1,
            "telemetry_sourced_from_subsystem": 5,
        },
    }
    assert manifest["relationship_types"] == [
        {
            "relationship_type": "command_emits_event",
            "display_name": "Command emits event",
            "from_domain": "commands",
            "to_domain": "events",
            "derived_from": {
                "model_field": "commands[].emits",
            },
            "relationship_count": 4,
        },
        {
            "relationship_type": "command_targets_subsystem",
            "display_name": "Command targets subsystem",
            "from_domain": "commands",
            "to_domain": "subsystems",
            "derived_from": {
                "model_field": "commands[].target",
            },
            "relationship_count": 4,
        },
        {
            "relationship_type": "data_product_produced_by_payload",
            "display_name": "Data product produced by payload",
            "from_domain": "data_products",
            "to_domain": "payloads",
            "derived_from": {
                "model_field": "data_products[].producer",
            },
            "relationship_count": 1,
        },
        {
            "relationship_type": "fault_emits_event",
            "display_name": "Fault emits event",
            "from_domain": "faults",
            "to_domain": "events",
            "derived_from": {
                "model_field": "faults[].emits",
            },
            "relationship_count": 2,
        },
        {
            "relationship_type": "packet_includes_telemetry",
            "display_name": "Packet includes telemetry",
            "from_domain": "packets",
            "to_domain": "telemetry",
            "derived_from": {
                "model_field": "packets[].telemetry",
            },
            "relationship_count": 5,
        },
        {
            "relationship_type": "payload_accepts_command",
            "display_name": "Payload accepts command",
            "from_domain": "payloads",
            "to_domain": "commands",
            "derived_from": {
                "model_field": "payloads[].commands.accepted",
            },
            "relationship_count": 2,
        },
        {
            "relationship_type": "payload_belongs_to_subsystem",
            "display_name": "Payload belongs to subsystem",
            "from_domain": "payloads",
            "to_domain": "subsystems",
            "derived_from": {
                "model_field": "payloads[].subsystem",
            },
            "relationship_count": 1,
        },
        {
            "relationship_type": "payload_generates_event",
            "display_name": "Payload generates event",
            "from_domain": "payloads",
            "to_domain": "events",
            "derived_from": {
                "model_field": "payloads[].events.generated",
            },
            "relationship_count": 2,
        },
        {
            "relationship_type": "payload_produces_telemetry",
            "display_name": "Payload produces telemetry",
            "from_domain": "payloads",
            "to_domain": "telemetry",
            "derived_from": {
                "model_field": "payloads[].telemetry.produced",
            },
            "relationship_count": 1,
        },
        {
            "relationship_type": "telemetry_sourced_from_subsystem",
            "display_name": "Telemetry sourced from subsystem",
            "from_domain": "telemetry",
            "to_domain": "subsystems",
            "derived_from": {
                "model_field": "telemetry[].source",
            },
            "relationship_count": 5,
        },
    ]

    relationships = manifest["relationships"]
    assert len(relationships) == 27
    assert relationships == sorted(relationships, key=lambda item: item["relationship_id"])
    assert {
        relationship["relationship_id"] for relationship in relationships
    } >= {
        "commands:eps.get_status->command_emits_event:events:eps.status_requested",
        "commands:eps.get_status->command_targets_subsystem:subsystems:eps",
        "commands:payload.start_acquisition->command_emits_event:events:payload.acquisition_started",
        "commands:payload.start_acquisition->command_targets_subsystem:subsystems:payload",
        "commands:payload.stop_acquisition->command_emits_event:events:payload.acquisition_stopped",
        "commands:payload.stop_acquisition->command_targets_subsystem:subsystems:payload",
        "commands:radio.downlink_housekeeping->command_emits_event:events:radio.housekeeping_downlink_requested",
        "commands:radio.downlink_housekeeping->command_targets_subsystem:subsystems:radio",
        "data_products:payload.radiation_histogram->data_product_produced_by_payload:payloads:demo_iod_payload",
        "faults:eps.battery_critical_fault->fault_emits_event:events:eps.battery_critical",
        "faults:eps.battery_low_fault->fault_emits_event:events:eps.battery_low",
        "payloads:demo_iod_payload->payload_belongs_to_subsystem:subsystems:payload",
        "payloads:demo_iod_payload->payload_generates_event:events:payload.acquisition_started",
        "payloads:demo_iod_payload->payload_generates_event:events:payload.acquisition_stopped",
        "telemetry:eps.battery.current->telemetry_sourced_from_subsystem:subsystems:eps",
        "telemetry:eps.battery.voltage->telemetry_sourced_from_subsystem:subsystems:eps",
        "telemetry:obc.mode->telemetry_sourced_from_subsystem:subsystems:obc",
        "telemetry:payload.acquisition.active->telemetry_sourced_from_subsystem:subsystems:payload",
        "telemetry:radio.downlink.available->telemetry_sourced_from_subsystem:subsystems:radio",
    }


def test_relationship_manifest_relationships_reference_indexed_entities() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    manifest = relationship_manifest_to_dict(model, DEMO_MISSION)
    packet_ids = {packet.id for packet in model.packets}
    payload_ids = {payload.id for payload in model.payloads}
    telemetry_ids = {telemetry.id for telemetry in model.telemetry}
    command_ids = {command.id for command in model.commands}
    event_ids = {event.id for event in model.events}
    fault_ids = {fault.id for fault in model.faults}
    subsystem_ids = {subsystem.id for subsystem in model.subsystems}
    data_product_ids = {data_product.id for data_product in model.data_products}

    for relationship in manifest["relationships"]:
        if relationship["relationship_type"] == "command_emits_event":
            assert relationship["from"]["domain"] == "commands"
            assert relationship["from"]["id"] in command_ids
            assert relationship["to"]["domain"] == "events"
            assert relationship["to"]["id"] in event_ids
            assert relationship["derived_from"] == {
                "model_field": "commands[].emits",
            }
        elif relationship["relationship_type"] == "command_targets_subsystem":
            assert relationship["from"]["domain"] == "commands"
            assert relationship["from"]["id"] in command_ids
            assert relationship["to"]["domain"] == "subsystems"
            assert relationship["to"]["id"] in subsystem_ids
            assert relationship["derived_from"] == {
                "model_field": "commands[].target",
            }
        elif relationship["relationship_type"] == "data_product_produced_by_payload":
            assert relationship["from"]["domain"] == "data_products"
            assert relationship["from"]["id"] in data_product_ids
            assert relationship["to"]["domain"] == "payloads"
            assert relationship["to"]["id"] in payload_ids
            assert relationship["derived_from"] == {
                "model_field": "data_products[].producer",
            }
        elif relationship["relationship_type"] == "fault_emits_event":
            assert relationship["from"]["domain"] == "faults"
            assert relationship["from"]["id"] in fault_ids
            assert relationship["to"]["domain"] == "events"
            assert relationship["to"]["id"] in event_ids
            assert relationship["derived_from"] == {
                "model_field": "faults[].emits",
            }
        elif relationship["relationship_type"] == "packet_includes_telemetry":
            assert relationship["from"]["domain"] == "packets"
            assert relationship["from"]["id"] in packet_ids
            assert relationship["to"]["domain"] == "telemetry"
            assert relationship["to"]["id"] in telemetry_ids
            assert relationship["derived_from"] == {
                "model_field": "packets[].telemetry",
            }
        elif relationship["relationship_type"] == "payload_accepts_command":
            assert relationship["from"]["domain"] == "payloads"
            assert relationship["from"]["id"] in payload_ids
            assert relationship["to"]["domain"] == "commands"
            assert relationship["to"]["id"] in command_ids
            assert relationship["derived_from"] == {
                "model_field": "payloads[].commands.accepted",
            }
        elif relationship["relationship_type"] == "payload_belongs_to_subsystem":
            assert relationship["from"]["domain"] == "payloads"
            assert relationship["from"]["id"] in payload_ids
            assert relationship["to"]["domain"] == "subsystems"
            assert relationship["to"]["id"] in subsystem_ids
            assert relationship["derived_from"] == {
                "model_field": "payloads[].subsystem",
            }
        elif relationship["relationship_type"] == "payload_generates_event":
            assert relationship["from"]["domain"] == "payloads"
            assert relationship["from"]["id"] in payload_ids
            assert relationship["to"]["domain"] == "events"
            assert relationship["to"]["id"] in event_ids
            assert relationship["derived_from"] == {
                "model_field": "payloads[].events.generated",
            }
        elif relationship["relationship_type"] == "payload_produces_telemetry":
            assert relationship["from"]["domain"] == "payloads"
            assert relationship["from"]["id"] in payload_ids
            assert relationship["to"]["domain"] == "telemetry"
            assert relationship["to"]["id"] in telemetry_ids
            assert relationship["derived_from"] == {
                "model_field": "payloads[].telemetry.produced",
            }
        elif relationship["relationship_type"] == "telemetry_sourced_from_subsystem":
            assert relationship["from"]["domain"] == "telemetry"
            assert relationship["from"]["id"] in telemetry_ids
            assert relationship["to"]["domain"] == "subsystems"
            assert relationship["to"]["id"] in subsystem_ids
            assert relationship["derived_from"] == {
                "model_field": "telemetry[].source",
            }
        else:
            raise AssertionError("unexpected relationship type")


def test_relationship_manifest_declares_derivation_policy() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    manifest = relationship_manifest_to_dict(model, DEMO_MISSION)

    assert manifest["derivation_policy"] == {
        "requires_explicit_loaded_mission_model_fields": True,
        "references_entity_index_entities": True,
        "forbids_naming_heuristics": True,
        "forbids_raw_yaml_scanning": True,
        "forbids_downstream_assumptions": True,
    }


def test_write_relationship_manifest_is_deterministic_json(tmp_path: Path) -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    output_file = tmp_path / "relationship_manifest.json"

    written_file = write_relationship_manifest(model, DEMO_MISSION, output_file)

    assert written_file == output_file
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert content.endswith("\n")

    parsed = json.loads(content)
    assert parsed == relationship_manifest_to_dict(model, DEMO_MISSION)
