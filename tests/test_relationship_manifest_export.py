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


def test_relationship_manifest_skeleton_contains_identity_and_boundaries() -> None:
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


def test_relationship_manifest_skeleton_emits_no_relationship_records_yet() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    manifest = relationship_manifest_to_dict(model, DEMO_MISSION)

    assert manifest["counts"] == {
        "total_relationships": 0,
        "relationship_types": {},
    }
    assert manifest["relationship_types"] == []
    assert manifest["relationships"] == []


def test_relationship_manifest_skeleton_declares_derivation_policy() -> None:
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
