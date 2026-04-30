from __future__ import annotations

from orbitfabric.lint.finding import LintFinding
from orbitfabric.model.mission import MissionModel, Packet


def check_packets(model: MissionModel) -> list[LintFinding]:
    """Check packet engineering consistency."""
    findings: list[LintFinding] = []

    for packet in model.packets:
        findings.extend(_check_packet_not_empty(packet))
        findings.extend(_check_packet_size_positive(packet))

    return findings


def _check_packet_not_empty(packet: Packet) -> list[LintFinding]:
    if packet.telemetry:
        return []

    return [
        LintFinding(
            severity="ERROR",
            code="OF-PKT-002",
            file="packets.yaml",
            domain="packets",
            object_id=packet.id,
            message="packet must not be empty",
            suggestion="Add at least one telemetry item to the packet.",
        )
    ]


def _check_packet_size_positive(packet: Packet) -> list[LintFinding]:
    if packet.max_payload_bytes > 0:
        return []

    return [
        LintFinding(
            severity="ERROR",
            code="OF-PKT-003",
            file="packets.yaml",
            domain="packets",
            object_id=packet.id,
            message="packet max_payload_bytes must be positive",
            suggestion="Set max_payload_bytes to a positive integer.",
        )
    ]