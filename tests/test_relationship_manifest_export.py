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

EXPECTED_RELATIONSHIP_TYPE_COUNTS = {
    "autonomous_action_dispatches_command": 2,
    "command_emits_event": 4,
    "command_targets_subsystem": 4,
    "commandability_rule_constrains_command": 1,
    "data_product_produced_by_payload": 1,
    "downlink_flow_includes_data_product": 1,
    "event_sourced_from_subsystem": 8,
    "fault_emits_event": 3,
    "fault_sourced_from_subsystem": 3,
    "packet_includes_telemetry": 5,
    "payload_accepts_command": 2,
    "payload_belongs_to_subsystem": 1,
    "payload_generates_event": 2,
    "payload_may_raise_fault": 1,
    "payload_produces_telemetry": 1,
    "recovery_intent_reacts_to_fault": 2,
    "telemetry_sourced_from_subsystem": 5,
}

EXPECTED_RELATIONSHIP_TYPE_SPECS = {
    "autonomous_action_dispatches_command": {
        "display_name": "Autonomous action dispatches command",
        "from_domain": "autonomous_actions",
        "to_domain": "commands",
        "model_field": "commandability.autonomous_actions[].dispatches.command",
    },
    "command_emits_event": {
        "display_name": "Command emits event",
        "from_domain": "commands",
        "to_domain": "events",
        "model_field": "commands[].emits",
    },
    "command_targets_subsystem": {
        "display_name": "Command targets subsystem",
        "from_domain": "commands",
        "to_domain": "subsystems",
        "model_field": "commands[].target",
    },
    "commandability_rule_constrains_command": {
        "display_name": "Commandability rule constrains command",
        "from_domain": "commandability_rules",
        "to_domain": "commands",
        "model_field": "commandability.rules[].command",
    },
    "data_product_produced_by_payload": {
        "display_name": "Data product produced by payload",
        "from_domain": "data_products",
        "to_domain": "payloads",
        "model_field": "data_products[].producer",
    },
    "downlink_flow_includes_data_product": {
        "display_name": "Downlink flow includes data product",
        "from_domain": "downlink_flows",
        "to_domain": "data_products",
        "model_field": "downlink_flows[].eligible_data_products",
    },
    "event_sourced_from_subsystem": {
        "display_name": "Event sourced from subsystem",
        "from_domain": "events",
        "to_domain": "subsystems",
        "model_field": "events[].source",
    },
    "fault_emits_event": {
        "display_name": "Fault emits event",
        "from_domain": "faults",
        "to_domain": "events",
        "model_field": "faults[].emits",
    },
    "fault_sourced_from_subsystem": {
        "display_name": "Fault sourced from subsystem",
        "from_domain": "faults",
        "to_domain": "subsystems",
        "model_field": "faults[].source",
    },
    "packet_includes_telemetry": {
        "display_name": "Packet includes telemetry",
        "from_domain": "packets",
        "to_domain": "telemetry",
        "model_field": "packets[].telemetry",
    },
    "payload_accepts_command": {
        "display_name": "Payload accepts command",
        "from_domain": "payloads",
        "to_domain": "commands",
        "model_field": "payloads[].commands.accepted",
    },
    "payload_belongs_to_subsystem": {
        "display_name": "Payload belongs to subsystem",
        "from_domain": "payloads",
        "to_domain": "subsystems",
        "model_field": "payloads[].subsystem",
    },
    "payload_generates_event": {
        "display_name": "Payload generates event",
        "from_domain": "payloads",
        "to_domain": "events",
        "model_field": "payloads[].events.generated",
    },
    "payload_may_raise_fault": {
        "display_name": "Payload may raise fault",
        "from_domain": "payloads",
        "to_domain": "faults",
        "model_field": "payloads[].faults.possible",
    },
    "payload_produces_telemetry": {
        "display_name": "Payload produces telemetry",
        "from_domain": "payloads",
        "to_domain": "telemetry",
        "model_field": "payloads[].telemetry.produced",
    },
    "recovery_intent_reacts_to_fault": {
        "display_name": "Recovery intent reacts to fault",
        "from_domain": "recovery_intents",
        "to_domain": "faults",
        "model_field": "commandability.recovery_intents[].fault",
    },
    "telemetry_sourced_from_subsystem": {
        "display_name": "Telemetry sourced from subsystem",
        "from_domain": "telemetry",
        "to_domain": "subsystems",
        "model_field": "telemetry[].source",
    },
}


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
        "total_relationships": 46,
        "relationship_types": EXPECTED_RELATIONSHIP_TYPE_COUNTS,
    }
    assert manifest["relationship_types"] == [
        {
            "relationship_type": relationship_type,
            "display_name": spec["display_name"],
            "from_domain": spec["from_domain"],
            "to_domain": spec["to_domain"],
            "derived_from": {
                "model_field": spec["model_field"],
            },
            "relationship_count": EXPECTED_RELATIONSHIP_TYPE_COUNTS[relationship_type],
        }
        for relationship_type, spec in sorted(EXPECTED_RELATIONSHIP_TYPE_SPECS.items())
    ]

    relationships = manifest["relationships"]
    assert len(relationships) == 46
    assert relationships == sorted(relationships, key=lambda item: item["relationship_id"])
    assert {
        relationship["relationship_id"] for relationship in relationships
    } >= {
        "autonomous_actions:stop_payload_on_battery_critical->autonomous_action_dispatches_command:commands:payload.stop_acquisition",
        "autonomous_actions:stop_payload_on_battery_low->autonomous_action_dispatches_command:commands:payload.stop_acquisition",
        "commandability_rules:payload_start_ground_rule->commandability_rule_constrains_command:commands:payload.start_acquisition",
        "commands:eps.get_status->command_emits_event:events:eps.status_requested",
        "commands:eps.get_status->command_targets_subsystem:subsystems:eps",
        "commands:payload.start_acquisition->command_emits_event:events:payload.acquisition_started",
        "commands:payload.start_acquisition->command_targets_subsystem:subsystems:payload",
        "commands:payload.stop_acquisition->command_emits_event:events:payload.acquisition_stopped",
        "commands:payload.stop_acquisition->command_targets_subsystem:subsystems:payload",
        "commands:radio.downlink_housekeeping->command_emits_event:events:radio.housekeeping_downlink_requested",
        "commands:radio.downlink_housekeeping->command_targets_subsystem:subsystems:radio",
        "data_products:payload.radiation_histogram->data_product_produced_by_payload:payloads:demo_iod_payload",
        "downlink_flows:science_next_available_contact->downlink_flow_includes_data_product:data_products:payload.radiation_histogram",
        "events:eps.battery_critical->event_sourced_from_subsystem:subsystems:eps",
        "events:eps.battery_low->event_sourced_from_subsystem:subsystems:eps",
        "events:eps.status_requested->event_sourced_from_subsystem:subsystems:eps",
        "events:obc.mode_changed->event_sourced_from_subsystem:subsystems:obc",
        "events:payload.acquisition_started->event_sourced_from_subsystem:subsystems:payload",
        "events:payload.acquisition_stopped->event_sourced_from_subsystem:subsystems:payload",
        "events:payload.command_timeout->event_sourced_from_subsystem:subsystems:payload",
        "events:radio.housekeeping_downlink_requested->event_sourced_from_subsystem:subsystems:radio",
        "faults:eps.battery_critical_fault->fault_emits_event:events:eps.battery_critical",
        "faults:eps.battery_critical_fault->fault_sourced_from_subsystem:subsystems:eps",
        "faults:eps.battery_low_fault->fault_emits_event:events:eps.battery_low",
        "faults:eps.battery_low_fault->fault_sourced_from_subsystem:subsystems:eps",
        "faults:payload.command_timeout_fault->fault_emits_event:events:payload.command_timeout",
        "faults:payload.command_timeout_fault->fault_sourced_from_subsystem:subsystems:payload",
        "payloads:demo_iod_payload->payload_belongs_to_subsystem:subsystems:payload",
        "payloads:demo_iod_payload->payload_generates_event:events:payload.acquisition_started",
        "payloads:demo_iod_payload->payload_generates_event:events:payload.acquisition_stopped",
        "payloads:demo_iod_payload->payload_may_raise_fault:faults:payload.command_timeout_fault",
        "recovery_intents:payload_battery_critical_recovery->recovery_intent_reacts_to_fault:faults:eps.battery_critical_fault",
        "recovery_intents:payload_battery_low_recovery->recovery_intent_reacts_to_fault:faults:eps.battery_low_fault",
        "telemetry:eps.battery.current->telemetry_sourced_from_subsystem:subsystems:eps",
        "telemetry:eps.battery.voltage->telemetry_sourced_from_subsystem:subsystems:eps",
        "telemetry:obc.mode->telemetry_sourced_from_subsystem:subsystems:obc",
        "telemetry:payload.acquisition.active->telemetry_sourced_from_subsystem:subsystems:payload",
        "telemetry:radio.downlink.available->telemetry_sourced_from_subsystem:subsystems:radio",
    }


def test_relationship_manifest_relationships_reference_indexed_entities() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    manifest = relationship_manifest_to_dict(model, DEMO_MISSION)
    indexed_ids_by_domain = {
        "autonomous_actions": {item.id for item in model.commandability.autonomous_actions},
        "commandability_rules": {item.id for item in model.commandability.rules},
        "commands": {item.id for item in model.commands},
        "data_products": {item.id for item in model.data_products},
        "downlink_flows": {item.id for item in model.contacts.downlink_flows},
        "events": {item.id for item in model.events},
        "faults": {item.id for item in model.faults},
        "packets": {item.id for item in model.packets},
        "payloads": {item.id for item in model.payloads},
        "recovery_intents": {item.id for item in model.commandability.recovery_intents},
        "subsystems": {item.id for item in model.subsystems},
        "telemetry": {item.id for item in model.telemetry},
    }

    for relationship in manifest["relationships"]:
        relationship_type = relationship["relationship_type"]
        spec = EXPECTED_RELATIONSHIP_TYPE_SPECS[relationship_type]
        from_domain = spec["from_domain"]
        to_domain = spec["to_domain"]

        assert relationship["from"]["domain"] == from_domain
        assert relationship["from"]["id"] in indexed_ids_by_domain[from_domain]
        assert relationship["to"]["domain"] == to_domain
        assert relationship["to"]["id"] in indexed_ids_by_domain[to_domain]
        assert relationship["derived_from"] == {
            "model_field": spec["model_field"],
        }


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
