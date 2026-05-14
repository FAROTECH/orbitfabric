from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from orbitfabric import __version__
from orbitfabric.model.loader import OPTIONAL_FILES, REQUIRED_FILES
from orbitfabric.model.mission import MissionModel


def model_summary_to_dict(model: MissionModel, mission_dir: Path) -> dict[str, Any]:
    """Return a deterministic read-only Mission Model summary."""
    mission_dir = mission_dir.resolve()
    domains = [_domain_record(model, mission_dir, item) for item in _domain_specs()]

    return {
        "summary_version": "0.1",
        "kind": "orbitfabric.model_summary",
        "orbitfabric_version": __version__,
        "mission": {
            "id": model.spacecraft.id,
            "name": model.spacecraft.name,
            "model_version": model.spacecraft.model_version,
        },
        "source": {
            "mission_dir": str(mission_dir),
        },
        "boundaries": {
            "source_of_truth": "mission_model",
            "core_derived_report": True,
            "contains_entity_index": False,
            "contains_relationship_manifest": False,
            "contains_plugin_api": False,
            "contains_runtime_behavior": False,
            "contains_ground_behavior": False,
        },
        "counts": {domain["id"]: domain["count"] for domain in domains},
        "domains": domains,
    }


def write_model_summary(
    model: MissionModel,
    mission_dir: Path,
    output_file: Path,
) -> Path:
    """Write a deterministic Mission Model summary JSON file."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(
        json.dumps(model_summary_to_dict(model, mission_dir), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output_file


def _domain_record(
    model: MissionModel,
    mission_dir: Path,
    spec: dict[str, str],
) -> dict[str, Any]:
    source_file = spec["source_file"]
    count = _domain_count(model, spec["id"])

    return {
        "id": spec["id"],
        "display_name": spec["display_name"],
        "source_file": source_file,
        "required": spec["required"] == "true",
        "present": (mission_dir / source_file).exists(),
        "count": count,
        "count_provenance": "loaded_mission_model",
    }


def _domain_specs() -> list[dict[str, str]]:
    return [
        {
            "id": "spacecraft",
            "display_name": "Spacecraft",
            "source_file": "spacecraft.yaml",
            "required": "true",
        },
        {
            "id": "subsystems",
            "display_name": "Subsystems",
            "source_file": "subsystems.yaml",
            "required": "true",
        },
        {
            "id": "modes",
            "display_name": "Modes",
            "source_file": "modes.yaml",
            "required": "true",
        },
        {
            "id": "mode_transitions",
            "display_name": "Mode Transitions",
            "source_file": "modes.yaml",
            "required": "true",
        },
        {
            "id": "telemetry",
            "display_name": "Telemetry",
            "source_file": "telemetry.yaml",
            "required": "true",
        },
        {
            "id": "commands",
            "display_name": "Commands",
            "source_file": "commands.yaml",
            "required": "true",
        },
        {
            "id": "events",
            "display_name": "Events",
            "source_file": "events.yaml",
            "required": "true",
        },
        {
            "id": "faults",
            "display_name": "Faults",
            "source_file": "faults.yaml",
            "required": "true",
        },
        {
            "id": "packets",
            "display_name": "Packets",
            "source_file": "packets.yaml",
            "required": "true",
        },
        {
            "id": "policies",
            "display_name": "Policies",
            "source_file": "policies.yaml",
            "required": "true",
        },
        {
            "id": "payloads",
            "display_name": "Payloads",
            "source_file": "payloads.yaml",
            "required": "false",
        },
        {
            "id": "data_products",
            "display_name": "Data Products",
            "source_file": "data_products.yaml",
            "required": "false",
        },
        {
            "id": "contact_profiles",
            "display_name": "Contact Profiles",
            "source_file": "contacts.yaml",
            "required": "false",
        },
        {
            "id": "link_profiles",
            "display_name": "Link Profiles",
            "source_file": "contacts.yaml",
            "required": "false",
        },
        {
            "id": "contact_windows",
            "display_name": "Contact Windows",
            "source_file": "contacts.yaml",
            "required": "false",
        },
        {
            "id": "downlink_flows",
            "display_name": "Downlink Flows",
            "source_file": "contacts.yaml",
            "required": "false",
        },
        {
            "id": "command_sources",
            "display_name": "Command Sources",
            "source_file": "commandability.yaml",
            "required": "false",
        },
        {
            "id": "commandability_rules",
            "display_name": "Commandability Rules",
            "source_file": "commandability.yaml",
            "required": "false",
        },
        {
            "id": "autonomous_actions",
            "display_name": "Autonomous Actions",
            "source_file": "commandability.yaml",
            "required": "false",
        },
        {
            "id": "recovery_intents",
            "display_name": "Recovery Intents",
            "source_file": "commandability.yaml",
            "required": "false",
        },
    ]


def _domain_count(model: MissionModel, domain_id: str) -> int:
    counts = {
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
    return counts[domain_id]


def _assert_domain_specs_match_loader() -> None:
    expected_files = set(REQUIRED_FILES) | set(OPTIONAL_FILES)
    actual_files = {domain["source_file"] for domain in _domain_specs()}

    if actual_files != expected_files:
        raise AssertionError("model summary domain specs must match loader files")
