from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from orbitfabric import __version__
from orbitfabric.model.loader import OPTIONAL_FILES, REQUIRED_FILES
from orbitfabric.model.mission import MissionModel

EntityPair = tuple[str, Any]


def entity_index_to_dict(model: MissionModel, mission_dir: Path) -> dict[str, Any]:
    """Return a deterministic read-only Mission Model entity index."""
    mission_dir = mission_dir.resolve()
    domains = [_domain_record(model, mission_dir, spec) for spec in _domain_specs()]
    entities = [
        entity
        for spec in _domain_specs()
        for entity in _entity_records(model, mission_dir, spec)
    ]

    return {
        "index_version": "0.1",
        "kind": "orbitfabric.entity_index",
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
        },
        "counts": {
            "total_entities": len(entities),
            "domains": {domain["id"]: domain["entity_count"] for domain in domains},
        },
        "domains": domains,
        "entities": entities,
    }


def write_entity_index(
    model: MissionModel,
    mission_dir: Path,
    output_file: Path,
) -> Path:
    """Write a deterministic Mission Model entity index JSON file."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(
        json.dumps(entity_index_to_dict(model, mission_dir), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output_file


def _domain_record(
    model: MissionModel,
    mission_dir: Path,
    spec: dict[str, Any],
) -> dict[str, Any]:
    entities = _entity_records(model, mission_dir, spec)
    source_file = spec["source_file"]

    return {
        "id": spec["id"],
        "display_name": spec["display_name"],
        "source_file": source_file,
        "required": spec["required"],
        "present": (mission_dir / source_file).exists(),
        "indexed": spec["indexed"],
        "model_count": _domain_count(model, spec["id"]),
        "entity_count": len(entities),
        "count_provenance": "loaded_mission_model",
    }


def _entity_records(
    model: MissionModel,
    mission_dir: Path,
    spec: dict[str, Any],
) -> list[dict[str, Any]]:
    if not spec["indexed"]:
        return []

    source_file = spec["source_file"]
    present = (mission_dir / source_file).exists()

    return [
        _entity_record(
            item_id=item_id,
            item=item,
            domain=spec["id"],
            entity_type=spec["entity_type"],
            source_file=source_file,
            required_domain=spec["required"],
            present=present,
        )
        for item_id, item in sorted(_domain_entities(model, spec["id"]), key=lambda pair: pair[0])
    ]


def _entity_record(
    item_id: str,
    item: Any,
    domain: str,
    entity_type: str,
    source_file: str,
    required_domain: bool,
    present: bool,
) -> dict[str, Any]:
    display_name = getattr(item, "name", None) or item_id

    return {
        "id": item_id,
        "domain": domain,
        "entity_type": entity_type,
        "display_name": display_name,
        "source_file": source_file,
        "provenance": "loaded_mission_model",
        "required_domain": required_domain,
        "present": present,
    }


def _domain_entities(model: MissionModel, domain_id: str) -> list[EntityPair]:
    if domain_id == "spacecraft":
        return [(model.spacecraft.id, model.spacecraft)]
    if domain_id == "subsystems":
        return [(item.id, item) for item in model.subsystems]
    if domain_id == "modes":
        return [(item_id, item) for item_id, item in model.modes.items()]
    if domain_id == "telemetry":
        return [(item.id, item) for item in model.telemetry]
    if domain_id == "commands":
        return [(item.id, item) for item in model.commands]
    if domain_id == "events":
        return [(item.id, item) for item in model.events]
    if domain_id == "faults":
        return [(item.id, item) for item in model.faults]
    if domain_id == "packets":
        return [(item.id, item) for item in model.packets]
    if domain_id == "payloads":
        return [(item.id, item) for item in model.payloads]
    if domain_id == "data_products":
        return [(item.id, item) for item in model.data_products]
    if domain_id == "contact_profiles":
        return [(item.id, item) for item in model.contacts.contact_profiles]
    if domain_id == "link_profiles":
        return [(item.id, item) for item in model.contacts.link_profiles]
    if domain_id == "contact_windows":
        return [(item.id, item) for item in model.contacts.contact_windows]
    if domain_id == "downlink_flows":
        return [(item.id, item) for item in model.contacts.downlink_flows]
    if domain_id == "command_sources":
        return [(item.id, item) for item in model.commandability.sources]
    if domain_id == "commandability_rules":
        return [(item.id, item) for item in model.commandability.rules]
    if domain_id == "autonomous_actions":
        return [(item.id, item) for item in model.commandability.autonomous_actions]
    if domain_id == "recovery_intents":
        return [(item.id, item) for item in model.commandability.recovery_intents]
    return []


def _domain_specs() -> list[dict[str, Any]]:
    return [
        _domain_spec("spacecraft", "Spacecraft", "spacecraft.yaml", True, True, "spacecraft"),
        _domain_spec("subsystems", "Subsystems", "subsystems.yaml", True, True, "subsystem"),
        _domain_spec("modes", "Modes", "modes.yaml", True, True, "mode"),
        _domain_spec(
            "mode_transitions",
            "Mode Transitions",
            "modes.yaml",
            True,
            False,
            None,
        ),
        _domain_spec("telemetry", "Telemetry", "telemetry.yaml", True, True, "telemetry"),
        _domain_spec("commands", "Commands", "commands.yaml", True, True, "command"),
        _domain_spec("events", "Events", "events.yaml", True, True, "event"),
        _domain_spec("faults", "Faults", "faults.yaml", True, True, "fault"),
        _domain_spec("packets", "Packets", "packets.yaml", True, True, "packet"),
        _domain_spec("policies", "Policies", "policies.yaml", True, False, None),
        _domain_spec("payloads", "Payloads", "payloads.yaml", False, True, "payload"),
        _domain_spec(
            "data_products",
            "Data Products",
            "data_products.yaml",
            False,
            True,
            "data_product",
        ),
        _domain_spec(
            "contact_profiles",
            "Contact Profiles",
            "contacts.yaml",
            False,
            True,
            "contact_profile",
        ),
        _domain_spec(
            "link_profiles",
            "Link Profiles",
            "contacts.yaml",
            False,
            True,
            "link_profile",
        ),
        _domain_spec(
            "contact_windows",
            "Contact Windows",
            "contacts.yaml",
            False,
            True,
            "contact_window",
        ),
        _domain_spec(
            "downlink_flows",
            "Downlink Flows",
            "contacts.yaml",
            False,
            True,
            "downlink_flow",
        ),
        _domain_spec(
            "command_sources",
            "Command Sources",
            "commandability.yaml",
            False,
            True,
            "command_source",
        ),
        _domain_spec(
            "commandability_rules",
            "Commandability Rules",
            "commandability.yaml",
            False,
            True,
            "commandability_rule",
        ),
        _domain_spec(
            "autonomous_actions",
            "Autonomous Actions",
            "commandability.yaml",
            False,
            True,
            "autonomous_action",
        ),
        _domain_spec(
            "recovery_intents",
            "Recovery Intents",
            "commandability.yaml",
            False,
            True,
            "recovery_intent",
        ),
    ]


def _domain_spec(
    domain_id: str,
    display_name: str,
    source_file: str,
    required: bool,
    indexed: bool,
    entity_type: str | None,
) -> dict[str, Any]:
    return {
        "id": domain_id,
        "display_name": display_name,
        "source_file": source_file,
        "required": required,
        "indexed": indexed,
        "entity_type": entity_type,
    }


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
        raise AssertionError("entity index domain specs must match loader files")
