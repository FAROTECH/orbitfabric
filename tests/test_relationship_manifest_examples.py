from __future__ import annotations

from pathlib import Path

from orbitfabric.export.relationship_manifest import relationship_manifest_to_dict
from orbitfabric.model.loader import MissionModelLoader

SPACELAB_MINISLICE = Path("examples/spacelab-inspired-communications-minislice/mission")


def test_relationship_manifest_emits_downlink_flow_records_for_spacelab_minislice() -> None:
    model = MissionModelLoader().load(SPACELAB_MINISLICE)

    manifest = relationship_manifest_to_dict(model, SPACELAB_MINISLICE)
    relationships = manifest["relationships"]
    downlink_relationships = [
        relationship
        for relationship in relationships
        if relationship["relationship_type"] == "downlink_flow_includes_data_product"
    ]

    assert len(downlink_relationships) == 7
    assert {
        relationship["relationship_id"] for relationship in downlink_relationships
    } == {
        "downlink_flows:spacelab_inspired_priority_downlink->downlink_flow_includes_data_product:data_products:critical_housekeeping_packet",
        "downlink_flows:spacelab_inspired_priority_downlink->downlink_flow_includes_data_product:data_products:decoder_reception_log",
        "downlink_flows:spacelab_inspired_priority_downlink->downlink_flow_includes_data_product:data_products:downlink_summary_report",
        "downlink_flows:spacelab_inspired_priority_downlink->downlink_flow_includes_data_product:data_products:periodic_beacon_packet",
        "downlink_flows:spacelab_inspired_priority_downlink->downlink_flow_includes_data_product:data_products:requested_data_frame_batch",
        "downlink_flows:spacelab_inspired_priority_downlink->downlink_flow_includes_data_product:data_products:requested_telemetry_frame_batch",
        "downlink_flows:spacelab_inspired_priority_downlink->downlink_flow_includes_data_product:data_products:scenario_evidence_log",
    }
    assert manifest["counts"]["relationship_types"][
        "downlink_flow_includes_data_product"
    ] == 7


def test_relationship_manifest_records_reference_loaded_entities_for_spacelab_minislice() -> None:
    model = MissionModelLoader().load(SPACELAB_MINISLICE)

    manifest = relationship_manifest_to_dict(model, SPACELAB_MINISLICE)
    domain_ids = {
        "commands": {command.id for command in model.commands},
        "data_products": {data_product.id for data_product in model.data_products},
        "downlink_flows": {flow.id for flow in model.contacts.downlink_flows},
        "events": {event.id for event in model.events},
        "faults": {fault.id for fault in model.faults},
        "packets": {packet.id for packet in model.packets},
        "payloads": {payload.id for payload in model.payloads},
        "subsystems": {subsystem.id for subsystem in model.subsystems},
        "telemetry": {telemetry.id for telemetry in model.telemetry},
    }

    for relationship in manifest["relationships"]:
        assert relationship["from"]["domain"] in domain_ids
        assert relationship["to"]["domain"] in domain_ids
        assert relationship["from"]["id"] in domain_ids[relationship["from"]["domain"]]
        assert relationship["to"]["id"] in domain_ids[relationship["to"]["domain"]]


def test_relationship_manifest_ordering_is_deterministic_for_spacelab_minislice() -> None:
    model = MissionModelLoader().load(SPACELAB_MINISLICE)

    first_manifest = relationship_manifest_to_dict(model, SPACELAB_MINISLICE)
    second_manifest = relationship_manifest_to_dict(model, SPACELAB_MINISLICE)

    assert first_manifest == second_manifest
    assert first_manifest["relationships"] == sorted(
        first_manifest["relationships"],
        key=lambda item: item["relationship_id"],
    )
