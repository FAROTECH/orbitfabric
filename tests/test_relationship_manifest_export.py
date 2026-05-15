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


def test_relationship_manifest_emits_packet_telemetry_relationship_records() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    manifest = relationship_manifest_to_dict(model, DEMO_MISSION)

    assert manifest["counts"] == {
        "total_relationships": 5,
        "relationship_types": {
            "packet_includes_telemetry": 5,
        },
    }
    assert manifest["relationship_types"] == [
        {
            "relationship_type": "packet_includes_telemetry",
            "display_name": "Packet includes telemetry",
            "from_domain": "packets",
            "to_domain": "telemetry",
            "derived_from": {
                "model_field": "packets[].telemetry",
            },
            "relationship_count": 5,
        }
    ]
    assert manifest["relationships"] == [
        {
            "relationship_id": (
                "packets:comm_status->packet_includes_telemetry:"
                "telemetry:radio.downlink.available"
            ),
            "relationship_type": "packet_includes_telemetry",
            "from": {
                "domain": "packets",
                "id": "comm_status",
            },
            "to": {
                "domain": "telemetry",
                "id": "radio.downlink.available",
            },
            "derived_from": {
                "model_field": "packets[].telemetry",
            },
        },
        {
            "relationship_id": (
                "packets:hk_fast->packet_includes_telemetry:telemetry:eps.battery.current"
            ),
            "relationship_type": "packet_includes_telemetry",
            "from": {
                "domain": "packets",
                "id": "hk_fast",
            },
            "to": {
                "domain": "telemetry",
                "id": "eps.battery.current",
            },
            "derived_from": {
                "model_field": "packets[].telemetry",
            },
        },
        {
            "relationship_id": (
                "packets:hk_fast->packet_includes_telemetry:telemetry:eps.battery.voltage"
            ),
            "relationship_type": "packet_includes_telemetry",
            "from": {
                "domain": "packets",
                "id": "hk_fast",
            },
            "to": {
                "domain": "telemetry",
                "id": "eps.battery.voltage",
            },
            "derived_from": {
                "model_field": "packets[].telemetry",
            },
        },
        {
            "relationship_id": "packets:hk_fast->packet_includes_telemetry:telemetry:obc.mode",
            "relationship_type": "packet_includes_telemetry",
            "from": {
                "domain": "packets",
                "id": "hk_fast",
            },
            "to": {
                "domain": "telemetry",
                "id": "obc.mode",
            },
            "derived_from": {
                "model_field": "packets[].telemetry",
            },
        },
        {
            "relationship_id": (
                "packets:payload_status->packet_includes_telemetry:"
                "telemetry:payload.acquisition.active"
            ),
            "relationship_type": "packet_includes_telemetry",
            "from": {
                "domain": "packets",
                "id": "payload_status",
            },
            "to": {
                "domain": "telemetry",
                "id": "payload.acquisition.active",
            },
            "derived_from": {
                "model_field": "packets[].telemetry",
            },
        },
    ]


def test_relationship_manifest_relationships_reference_indexed_entities() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    manifest = relationship_manifest_to_dict(model, DEMO_MISSION)
    packet_ids = {packet.id for packet in model.packets}
    telemetry_ids = {telemetry.id for telemetry in model.telemetry}

    for relationship in manifest["relationships"]:
        assert relationship["relationship_type"] == "packet_includes_telemetry"
        assert relationship["from"]["domain"] == "packets"
        assert relationship["from"]["id"] in packet_ids
        assert relationship["to"]["domain"] == "telemetry"
        assert relationship["to"]["id"] in telemetry_ids
        assert relationship["derived_from"] == {
            "model_field": "packets[].telemetry",
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
