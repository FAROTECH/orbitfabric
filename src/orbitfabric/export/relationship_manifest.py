from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from orbitfabric import __version__
from orbitfabric.export.entity_index import entity_index_to_dict
from orbitfabric.model.mission import Command, Fault, MissionModel, Packet, PayloadContract

REL_COMMAND_EMITS_EVENT = "command_emits_event"
REL_COMMAND_TARGETS_SUBSYSTEM = "command_targets_subsystem"
REL_FAULT_EMITS_EVENT = "fault_emits_event"
REL_PACKET_INCLUDES_TELEMETRY = "packet_includes_telemetry"
REL_PAYLOAD_ACCEPTS_COMMAND = "payload_accepts_command"
REL_PAYLOAD_GENERATES_EVENT = "payload_generates_event"
REL_PAYLOAD_PRODUCES_TELEMETRY = "payload_produces_telemetry"


def relationship_manifest_to_dict(
    model: MissionModel,
    mission_dir: Path,
) -> dict[str, Any]:
    """Return a deterministic candidate relationship manifest.

    This function defines the deterministic envelope for the future
    Relationship Manifest Surface and emits only explicitly admitted
    relationship families.

    Relationship records must be derived from explicit loaded Mission Model
    fields without naming heuristics or downstream assumptions.
    """
    mission_dir = mission_dir.resolve()
    entity_index = entity_index_to_dict(model, mission_dir)
    relationships = _relationship_records(model)
    relationship_type_counts = _relationship_type_counts(relationships)

    return {
        "manifest_version": "0.1-candidate",
        "kind": "orbitfabric.relationship_manifest",
        "orbitfabric_version": __version__,
        "status": "candidate",
        "mission": {
            "id": model.spacecraft.id,
            "name": model.spacecraft.name,
            "model_version": model.spacecraft.model_version,
        },
        "source": {
            "mission_dir": str(mission_dir),
            "entity_index_kind": entity_index["kind"],
            "entity_index_version": entity_index["index_version"],
        },
        "boundaries": {
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
        },
        "counts": {
            "total_relationships": len(relationships),
            "relationship_types": relationship_type_counts,
        },
        "relationship_types": _relationship_types(relationship_type_counts),
        "relationships": relationships,
        "derivation_policy": {
            "requires_explicit_loaded_mission_model_fields": True,
            "references_entity_index_entities": True,
            "forbids_naming_heuristics": True,
            "forbids_raw_yaml_scanning": True,
            "forbids_downstream_assumptions": True,
        },
    }


def write_relationship_manifest(
    model: MissionModel,
    mission_dir: Path,
    output_file: Path,
) -> Path:
    """Write the candidate relationship manifest JSON file."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(
        json.dumps(
            relationship_manifest_to_dict(model, mission_dir),
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return output_file


def _relationship_records(model: MissionModel) -> list[dict[str, Any]]:
    records = [
        record
        for command in sorted(model.commands, key=lambda item: item.id)
        for record in _command_event_relationship_records(command)
    ]
    records.extend(
        record
        for command in sorted(model.commands, key=lambda item: item.id)
        for record in _command_subsystem_relationship_records(command, model.subsystem_ids)
    )
    records.extend(
        record
        for fault in sorted(model.faults, key=lambda item: item.id)
        for record in _fault_event_relationship_records(fault)
    )
    records.extend(
        record
        for packet in sorted(model.packets, key=lambda item: item.id)
        for record in _packet_telemetry_relationship_records(packet)
    )
    records.extend(
        record
        for payload in sorted(model.payloads, key=lambda item: item.id)
        for record in _payload_telemetry_relationship_records(payload)
    )
    records.extend(
        record
        for payload in sorted(model.payloads, key=lambda item: item.id)
        for record in _payload_command_relationship_records(payload)
    )
    records.extend(
        record
        for payload in sorted(model.payloads, key=lambda item: item.id)
        for record in _payload_event_relationship_records(payload)
    )
    return sorted(records, key=lambda item: item["relationship_id"])


def _command_event_relationship_records(command: Command) -> list[dict[str, Any]]:
    return [
        {
            "relationship_id": (
                f"commands:{command.id}->{REL_COMMAND_EMITS_EVENT}:events:{event_id}"
            ),
            "relationship_type": REL_COMMAND_EMITS_EVENT,
            "from": {
                "domain": "commands",
                "id": command.id,
            },
            "to": {
                "domain": "events",
                "id": event_id,
            },
            "derived_from": {
                "model_field": "commands[].emits",
            },
        }
        for event_id in sorted(command.emits)
    ]


def _command_subsystem_relationship_records(
    command: Command,
    subsystem_ids: set[str],
) -> list[dict[str, Any]]:
    if command.target not in subsystem_ids:
        return []

    return [
        {
            "relationship_id": (
                f"commands:{command.id}->{REL_COMMAND_TARGETS_SUBSYSTEM}:"
                f"subsystems:{command.target}"
            ),
            "relationship_type": REL_COMMAND_TARGETS_SUBSYSTEM,
            "from": {
                "domain": "commands",
                "id": command.id,
            },
            "to": {
                "domain": "subsystems",
                "id": command.target,
            },
            "derived_from": {
                "model_field": "commands[].target",
            },
        }
    ]


def _fault_event_relationship_records(fault: Fault) -> list[dict[str, Any]]:
    return [
        {
            "relationship_id": f"faults:{fault.id}->{REL_FAULT_EMITS_EVENT}:events:{event_id}",
            "relationship_type": REL_FAULT_EMITS_EVENT,
            "from": {
                "domain": "faults",
                "id": fault.id,
            },
            "to": {
                "domain": "events",
                "id": event_id,
            },
            "derived_from": {
                "model_field": "faults[].emits",
            },
        }
        for event_id in sorted(fault.emits)
    ]


def _packet_telemetry_relationship_records(packet: Packet) -> list[dict[str, Any]]:
    return [
        {
            "relationship_id": (
                f"packets:{packet.id}->{REL_PACKET_INCLUDES_TELEMETRY}:"
                f"telemetry:{telemetry_id}"
            ),
            "relationship_type": REL_PACKET_INCLUDES_TELEMETRY,
            "from": {
                "domain": "packets",
                "id": packet.id,
            },
            "to": {
                "domain": "telemetry",
                "id": telemetry_id,
            },
            "derived_from": {
                "model_field": "packets[].telemetry",
            },
        }
        for telemetry_id in sorted(packet.telemetry)
    ]


def _payload_telemetry_relationship_records(
    payload: PayloadContract,
) -> list[dict[str, Any]]:
    return [
        {
            "relationship_id": (
                f"payloads:{payload.id}->{REL_PAYLOAD_PRODUCES_TELEMETRY}:"
                f"telemetry:{telemetry_id}"
            ),
            "relationship_type": REL_PAYLOAD_PRODUCES_TELEMETRY,
            "from": {
                "domain": "payloads",
                "id": payload.id,
            },
            "to": {
                "domain": "telemetry",
                "id": telemetry_id,
            },
            "derived_from": {
                "model_field": "payloads[].telemetry.produced",
            },
        }
        for telemetry_id in sorted(payload.telemetry.produced)
    ]


def _payload_command_relationship_records(
    payload: PayloadContract,
) -> list[dict[str, Any]]:
    return [
        {
            "relationship_id": (
                f"payloads:{payload.id}->{REL_PAYLOAD_ACCEPTS_COMMAND}:"
                f"commands:{command_id}"
            ),
            "relationship_type": REL_PAYLOAD_ACCEPTS_COMMAND,
            "from": {
                "domain": "payloads",
                "id": payload.id,
            },
            "to": {
                "domain": "commands",
                "id": command_id,
            },
            "derived_from": {
                "model_field": "payloads[].commands.accepted",
            },
        }
        for command_id in sorted(payload.commands.accepted)
    ]


def _payload_event_relationship_records(
    payload: PayloadContract,
) -> list[dict[str, Any]]:
    return [
        {
            "relationship_id": (
                f"payloads:{payload.id}->{REL_PAYLOAD_GENERATES_EVENT}:"
                f"events:{event_id}"
            ),
            "relationship_type": REL_PAYLOAD_GENERATES_EVENT,
            "from": {
                "domain": "payloads",
                "id": payload.id,
            },
            "to": {
                "domain": "events",
                "id": event_id,
            },
            "derived_from": {
                "model_field": "payloads[].events.generated",
            },
        }
        for event_id in sorted(payload.events.generated)
    ]


def _relationship_type_counts(relationships: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for relationship in relationships:
        relationship_type = relationship["relationship_type"]
        counts[relationship_type] = counts.get(relationship_type, 0) + 1
    return dict(sorted(counts.items()))


def _relationship_types(type_counts: dict[str, int]) -> list[dict[str, Any]]:
    specs = {
        REL_COMMAND_EMITS_EVENT: {
            "relationship_type": REL_COMMAND_EMITS_EVENT,
            "display_name": "Command emits event",
            "from_domain": "commands",
            "to_domain": "events",
            "derived_from": {
                "model_field": "commands[].emits",
            },
        },
        REL_COMMAND_TARGETS_SUBSYSTEM: {
            "relationship_type": REL_COMMAND_TARGETS_SUBSYSTEM,
            "display_name": "Command targets subsystem",
            "from_domain": "commands",
            "to_domain": "subsystems",
            "derived_from": {
                "model_field": "commands[].target",
            },
        },
        REL_FAULT_EMITS_EVENT: {
            "relationship_type": REL_FAULT_EMITS_EVENT,
            "display_name": "Fault emits event",
            "from_domain": "faults",
            "to_domain": "events",
            "derived_from": {
                "model_field": "faults[].emits",
            },
        },
        REL_PACKET_INCLUDES_TELEMETRY: {
            "relationship_type": REL_PACKET_INCLUDES_TELEMETRY,
            "display_name": "Packet includes telemetry",
            "from_domain": "packets",
            "to_domain": "telemetry",
            "derived_from": {
                "model_field": "packets[].telemetry",
            },
        },
        REL_PAYLOAD_ACCEPTS_COMMAND: {
            "relationship_type": REL_PAYLOAD_ACCEPTS_COMMAND,
            "display_name": "Payload accepts command",
            "from_domain": "payloads",
            "to_domain": "commands",
            "derived_from": {
                "model_field": "payloads[].commands.accepted",
            },
        },
        REL_PAYLOAD_GENERATES_EVENT: {
            "relationship_type": REL_PAYLOAD_GENERATES_EVENT,
            "display_name": "Payload generates event",
            "from_domain": "payloads",
            "to_domain": "events",
            "derived_from": {
                "model_field": "payloads[].events.generated",
            },
        },
        REL_PAYLOAD_PRODUCES_TELEMETRY: {
            "relationship_type": REL_PAYLOAD_PRODUCES_TELEMETRY,
            "display_name": "Payload produces telemetry",
            "from_domain": "payloads",
            "to_domain": "telemetry",
            "derived_from": {
                "model_field": "payloads[].telemetry.produced",
            },
        },
    }

    return [
        {
            **specs[relationship_type],
            "relationship_count": count,
        }
        for relationship_type, count in sorted(type_counts.items())
    ]
