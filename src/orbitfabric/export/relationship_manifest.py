from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from orbitfabric import __version__
from orbitfabric.export.entity_index import entity_index_to_dict
from orbitfabric.model.mission import MissionModel


def relationship_manifest_to_dict(
    model: MissionModel,
    mission_dir: Path,
) -> dict[str, Any]:
    """Return the candidate relationship manifest skeleton.

    This function defines the deterministic envelope for the future
    Relationship Manifest Surface.

    It intentionally emits no relationship records yet.
    Relationship types must be admitted one by one in later PRs, only when
    they can be derived from explicit loaded Mission Model fields without
    naming heuristics or downstream assumptions.
    """
    mission_dir = mission_dir.resolve()
    entity_index = entity_index_to_dict(model, mission_dir)

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
            "total_relationships": 0,
            "relationship_types": {},
        },
        "relationship_types": [],
        "relationships": [],
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
    """Write the candidate relationship manifest skeleton JSON file."""
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
