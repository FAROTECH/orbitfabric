from __future__ import annotations

import json
from pathlib import Path

from orbitfabric import __version__
from orbitfabric.export.model_summary import (
    _assert_domain_specs_match_loader,
    model_summary_to_dict,
    write_model_summary,
)
from orbitfabric.model.loader import MissionModelLoader

DEMO_MISSION = Path("examples/demo-3u/mission")


def test_model_summary_contains_mission_identity_and_boundaries() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    summary = model_summary_to_dict(model, DEMO_MISSION)

    assert summary["summary_version"] == "0.1"
    assert summary["kind"] == "orbitfabric.model_summary"
    assert summary["orbitfabric_version"] == __version__
    assert summary["mission"] == {
        "id": "demo-3u",
        "name": "Demo 3U Spacecraft",
        "model_version": "0.1.0",
    }
    assert summary["source"]["mission_dir"] == str(DEMO_MISSION.resolve())
    assert summary["boundaries"] == {
        "source_of_truth": "mission_model",
        "core_derived_report": True,
        "contains_entity_index": False,
        "contains_relationship_manifest": False,
        "contains_plugin_api": False,
        "contains_runtime_behavior": False,
        "contains_ground_behavior": False,
    }


def test_model_summary_counts_all_contract_domains() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    summary = model_summary_to_dict(model, DEMO_MISSION)

    assert summary["counts"] == {
        "spacecraft": 1,
        "subsystems": len(model.subsystems),
        "modes": len(model.modes),
        "mode_transitions": len(model.mode_transitions),
        "telemetry": len(model.telemetry),
        "commands": len(model.commands),
        "events": len(model.events),
        "faults": len(model.faults),
        "packets": len(model.packets),
        "policies": 1,
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


def test_model_summary_domains_are_read_only_contract_domains() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    summary = model_summary_to_dict(model, DEMO_MISSION)
    domains = {domain["id"]: domain for domain in summary["domains"]}

    assert domains["spacecraft"]["required"] is True
    assert domains["spacecraft"]["present"] is True
    assert domains["spacecraft"]["source_file"] == "spacecraft.yaml"
    assert domains["spacecraft"]["count"] == 1
    assert domains["spacecraft"]["count_provenance"] == "loaded_mission_model"

    assert domains["payloads"]["required"] is False
    assert domains["payloads"]["present"] is True
    assert domains["payloads"]["source_file"] == "payloads.yaml"
    assert domains["payloads"]["count"] == len(model.payloads)

    assert domains["contact_profiles"]["required"] is False
    assert domains["contact_profiles"]["present"] is True
    assert domains["contact_profiles"]["source_file"] == "contacts.yaml"
    assert domains["contact_profiles"]["count"] == len(
        model.contacts.contact_profiles
    )

    assert domains["command_sources"]["required"] is False
    assert domains["command_sources"]["present"] is True
    assert domains["command_sources"]["source_file"] == "commandability.yaml"
    assert domains["command_sources"]["count"] == len(
        model.commandability.sources
    )


def test_model_summary_marks_absent_optional_domains(tmp_path: Path) -> None:
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
    summary = model_summary_to_dict(model, mission_dir)
    domains = {domain["id"]: domain for domain in summary["domains"]}

    assert domains["payloads"]["present"] is False
    assert domains["payloads"]["count"] == 0
    assert domains["data_products"]["present"] is False
    assert domains["data_products"]["count"] == 0
    assert domains["contact_profiles"]["present"] is False
    assert domains["contact_profiles"]["count"] == 0
    assert domains["command_sources"]["present"] is False
    assert domains["command_sources"]["count"] == 0


def test_write_model_summary_is_deterministic_json(tmp_path: Path) -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    output_file = tmp_path / "model_summary.json"

    written_file = write_model_summary(model, DEMO_MISSION, output_file)

    assert written_file == output_file
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert content.endswith("\n")

    parsed = json.loads(content)
    assert parsed == model_summary_to_dict(model, DEMO_MISSION)


def test_model_summary_domain_specs_match_loader_files() -> None:
    _assert_domain_specs_match_loader()
