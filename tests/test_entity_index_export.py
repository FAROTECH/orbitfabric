from __future__ import annotations

import json
from pathlib import Path

from orbitfabric import __version__
from orbitfabric.export.entity_index import (
    _assert_domain_specs_match_loader,
    entity_index_to_dict,
    write_entity_index,
)
from orbitfabric.model.loader import MissionModelLoader

DEMO_MISSION = Path("examples/demo-3u/mission")


def test_entity_index_contains_mission_identity_and_boundaries() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    index = entity_index_to_dict(model, DEMO_MISSION)

    assert index["index_version"] == "0.1"
    assert index["kind"] == "orbitfabric.entity_index"
    assert index["orbitfabric_version"] == __version__
    assert index["mission"] == {
        "id": "demo-3u",
        "name": "Demo 3U Spacecraft",
        "model_version": "0.1.0",
    }
    assert index["source"]["mission_dir"] == str(DEMO_MISSION.resolve())
    assert index["boundaries"] == {
        "source_of_truth": "mission_model",
        "core_derived_report": True,
        "read_only": True,
        "contains_entity_index": True,
        "contains_entity_records": True,
        "contains_relationship_manifest": False,
        "contains_relationship_graph": False,
        "contains_dependency_graph": False,
        "contains_yaml_ast": False,
        "contains_source_locations": False,
        "contains_plugin_api": False,
        "contains_studio_api": False,
        "contains_runtime_behavior": False,
        "contains_ground_behavior": False,
    }


def test_entity_index_contains_domain_summaries() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    index = entity_index_to_dict(model, DEMO_MISSION)
    domains = {domain["id"]: domain for domain in index["domains"]}

    assert domains["spacecraft"] == {
        "id": "spacecraft",
        "display_name": "Spacecraft",
        "source_file": "spacecraft.yaml",
        "required": True,
        "present": True,
        "indexed": True,
        "model_count": 1,
        "entity_count": 1,
        "count_provenance": "loaded_mission_model",
    }
    assert domains["mode_transitions"]["indexed"] is False
    assert domains["mode_transitions"]["model_count"] == len(model.mode_transitions)
    assert domains["mode_transitions"]["entity_count"] == 0
    assert domains["policies"]["indexed"] is False
    assert domains["policies"]["model_count"] == 1
    assert domains["policies"]["entity_count"] == 0
    assert domains["payloads"]["required"] is False
    assert domains["payloads"]["present"] is True
    assert domains["payloads"]["indexed"] is True
    assert domains["payloads"]["entity_count"] == len(model.payloads)


def test_entity_index_contains_id_bearing_entities() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    index = entity_index_to_dict(model, DEMO_MISSION)
    entities = {(entity["domain"], entity["id"]): entity for entity in index["entities"]}

    assert entities[("spacecraft", "demo-3u")] == {
        "id": "demo-3u",
        "domain": "spacecraft",
        "entity_type": "spacecraft",
        "display_name": "Demo 3U Spacecraft",
        "source_file": "spacecraft.yaml",
        "provenance": "loaded_mission_model",
        "required_domain": True,
        "present": True,
    }
    assert entities[("commands", "payload.start_acquisition")]["entity_type"] == "command"
    assert entities[("commands", "payload.start_acquisition")]["display_name"] == (
        "payload.start_acquisition"
    )
    assert entities[("telemetry", "eps.battery.voltage")]["entity_type"] == "telemetry"
    assert entities[("payloads", "demo_iod_payload")]["entity_type"] == "payload"
    assert entities[("data_products", "payload.radiation_histogram")]["entity_type"] == (
        "data_product"
    )
    assert entities[("contact_windows", "demo_contact_001")]["entity_type"] == (
        "contact_window"
    )
    assert entities[("command_sources", "ground_operator")]["entity_type"] == (
        "command_source"
    )


def test_entity_index_does_not_create_synthetic_records_for_non_id_domains() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    index = entity_index_to_dict(model, DEMO_MISSION)
    entity_domains = {entity["domain"] for entity in index["entities"]}

    assert "mode_transitions" not in entity_domains
    assert "policies" not in entity_domains


def test_entity_index_counts_total_entities_and_domains() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    index = entity_index_to_dict(model, DEMO_MISSION)

    expected_domain_counts = {
        "spacecraft": 1,
        "subsystems": len(model.subsystems),
        "modes": len(model.modes),
        "mode_transitions": 0,
        "telemetry": len(model.telemetry),
        "commands": len(model.commands),
        "events": len(model.events),
        "faults": len(model.faults),
        "packets": len(model.packets),
        "policies": 0,
        "payloads": len(model.payloads),
        "data_products": len(model.data_products),
        "contact_profiles": len(model.contacts.contact_profiles),
        "link_profiles": len(model.contacts.link_profiles),
        "contact_windows": len(model.contacts.contact_windows),
        "downlink_flows": len(model.contacts.downlink_flows),
        "command_sources": len(model.commandability.sources),
        "commandability_rules": len(model.commandability.rules),
        "autonomous_actions": len(model.commandability.autonomous_actions),
        "recovery_intents": len(model.commandability.recovery_intents),
    }

    assert index["counts"]["domains"] == expected_domain_counts
    assert index["counts"]["total_entities"] == sum(expected_domain_counts.values())
    assert index["counts"]["total_entities"] == len(index["entities"])


def test_entity_index_marks_absent_optional_domains(tmp_path: Path) -> None:
    mission_dir = tmp_path / "mission"
    mission_dir.mkdir()

    for source_file in DEMO_MISSION.glob("*.yaml"):
        if source_file.name in {
            "payloads.yaml",
            "data_products.yaml",
            "contacts.yaml",
            "commandability.yaml",
        }:
            continue
        (mission_dir / source_file.name).write_text(
            source_file.read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    model = MissionModelLoader().load(mission_dir)
    index = entity_index_to_dict(model, mission_dir)
    domains = {domain["id"]: domain for domain in index["domains"]}

    assert domains["payloads"]["present"] is False
    assert domains["payloads"]["entity_count"] == 0
    assert domains["data_products"]["present"] is False
    assert domains["data_products"]["entity_count"] == 0
    assert domains["contact_profiles"]["present"] is False
    assert domains["contact_profiles"]["entity_count"] == 0
    assert domains["command_sources"]["present"] is False
    assert domains["command_sources"]["entity_count"] == 0
    assert not any(entity["source_file"] == "payloads.yaml" for entity in index["entities"])


def test_write_entity_index_is_deterministic_json(tmp_path: Path) -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    output_file = tmp_path / "entity_index.json"

    written_file = write_entity_index(model, DEMO_MISSION, output_file)

    assert written_file == output_file
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert content.endswith("\n")

    parsed = json.loads(content)
    assert parsed == entity_index_to_dict(model, DEMO_MISSION)


def test_entity_index_domain_specs_match_loader_files() -> None:
    _assert_domain_specs_match_loader()
