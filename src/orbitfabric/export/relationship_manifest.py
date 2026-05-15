from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from orbitfabric import __version__
from orbitfabric.export.entity_index import entity_index_to_dict
from orbitfabric.model.mission import MissionModel, Packet

REL_PACKET_INCLUDES_TELEMETRY = "packet_includes_telemetry"


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
    return [
        record
        for packet in sorted(model.packets, key=lambda item: item.id)
        for record in _packet_telemetry_relationship_records(packet)
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


def _relationship_type_counts(relationships: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for relationship in relationships:
        relationship_type = relationship["relationship_type"]
        counts[relationship_type] = counts.get(relationship_type, 0) + 1
    return dict(sorted(counts.items()))


def _relationship_types(type_counts: dict[str, int]) -> list[dict[str, Any]]:
    specs = {
        REL_PACKET_INCLUDES_TELEMETRY: {
            "relationship_type": REL_PACKET_INCLUDES_TELEMETRY,
            "display_name": "Packet includes telemetry",
            "from_domain": "packets",
            "to_domain": "telemetry",
            "derived_from": {
                "model_field": "packets[].telemetry",
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
