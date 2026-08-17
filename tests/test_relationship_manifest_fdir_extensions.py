from __future__ import annotations

from pathlib import Path

from orbitfabric.export.relationship_manifest import relationship_manifest_to_dict
from orbitfabric.model.loader import MissionModelLoader

DEMO_MISSION = Path("examples/demo-3u/mission")


def _relationships_by_type() -> dict[str, list[dict[str, object]]]:
    model = MissionModelLoader().load(DEMO_MISSION)
    manifest = relationship_manifest_to_dict(model, DEMO_MISSION)

    result: dict[str, list[dict[str, object]]] = {}
    for relationship in manifest["relationships"]:
        result.setdefault(relationship["relationship_type"], []).append(relationship)
    return result


def test_fault_condition_exposes_observed_telemetry_relationship() -> None:
    relationships = _relationships_by_type()["fault_observes_telemetry"]

    low_battery = next(
        item
        for item in relationships
        if item["from"] == {"domain": "faults", "id": "eps.battery_low_fault"}
    )

    assert low_battery["to"] == {
        "domain": "telemetry",
        "id": "eps.battery.voltage",
    }
    assert low_battery["derived_from"] == {
        "model_field": "faults[].condition.telemetry",
    }


def test_fault_recovery_exposes_target_mode_relationship() -> None:
    relationships = _relationships_by_type()["fault_recovery_targets_mode"]

    low_battery = next(
        item
        for item in relationships
        if item["from"] == {"domain": "faults", "id": "eps.battery_low_fault"}
    )

    assert low_battery["to"] == {"domain": "modes", "id": "DEGRADED"}
    assert low_battery["derived_from"] == {
        "model_field": "faults[].recovery.mode_transition",
    }


def test_fault_recovery_exposes_auto_command_relationship() -> None:
    relationships = _relationships_by_type()["fault_recovery_dispatches_command"]

    low_battery = next(
        item
        for item in relationships
        if item["from"] == {"domain": "faults", "id": "eps.battery_low_fault"}
    )

    assert low_battery["to"] == {
        "domain": "commands",
        "id": "payload.stop_acquisition",
    }
    assert low_battery["derived_from"] == {
        "model_field": "faults[].recovery.auto_commands",
    }


def test_autonomous_action_exposes_fault_trigger_and_command_source() -> None:
    relationships = _relationships_by_type()

    trigger = next(
        item
        for item in relationships["autonomous_action_triggered_by_fault"]
        if item["from"]
        == {"domain": "autonomous_actions", "id": "stop_payload_on_battery_low"}
    )
    assert trigger["to"] == {
        "domain": "faults",
        "id": "eps.battery_low_fault",
    }
    assert trigger["derived_from"] == {
        "model_field": "commandability.autonomous_actions[].trigger.fault",
    }

    source = next(
        item
        for item in relationships["autonomous_action_uses_command_source"]
        if item["from"]
        == {"domain": "autonomous_actions", "id": "stop_payload_on_battery_low"}
    )
    assert source["to"] == {
        "domain": "command_sources",
        "id": "onboard_autonomy",
    }
    assert source["derived_from"] == {
        "model_field": "commandability.autonomous_actions[].dispatches.source",
    }


def test_recovery_intent_exposes_target_mode_and_commands() -> None:
    relationships = _relationships_by_type()

    target_mode = next(
        item
        for item in relationships["recovery_intent_targets_mode"]
        if item["from"]
        == {"domain": "recovery_intents", "id": "payload_battery_low_recovery"}
    )
    assert target_mode["to"] == {"domain": "modes", "id": "DEGRADED"}
    assert target_mode["derived_from"] == {
        "model_field": "commandability.recovery_intents[].target_mode",
    }

    command = next(
        item
        for item in relationships["recovery_intent_includes_command"]
        if item["from"]
        == {"domain": "recovery_intents", "id": "payload_battery_low_recovery"}
    )
    assert command["to"] == {
        "domain": "commands",
        "id": "payload.stop_acquisition",
    }
    assert command["derived_from"] == {
        "model_field": "commandability.recovery_intents[].commands",
    }


def test_minimum_fdir_extension_is_additive_and_explicit() -> None:
    relationships = _relationships_by_type()

    expected_new_types = {
        "fault_observes_telemetry",
        "fault_recovery_targets_mode",
        "fault_recovery_dispatches_command",
        "autonomous_action_triggered_by_fault",
        "autonomous_action_uses_command_source",
        "recovery_intent_targets_mode",
        "recovery_intent_includes_command",
    }

    assert expected_new_types <= relationships.keys()

    # Existing relationship families remain available; C4 extends the surface
    # rather than replacing the v1 relationship contract.
    assert "fault_emits_event" in relationships
    assert "autonomous_action_dispatches_command" in relationships
    assert "recovery_intent_reacts_to_fault" in relationships
