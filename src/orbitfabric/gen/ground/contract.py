from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class GroundCommandArgument:
    """Command argument exposed through the ground-facing contract."""

    name: str
    value_type: str
    minimum: float | int | None = None
    maximum: float | int | None = None
    enum_values: tuple[str, ...] = ()
    default: Any | None = None
    description: str | None = None


@dataclass(frozen=True)
class GroundTelemetryItem:
    """Telemetry item exported to ground-facing dictionaries."""

    model_id: str
    name: str
    value_type: str
    unit: str
    source: str
    sampling: str
    criticality: str
    persistence: str
    downlink_priority: str
    limits: dict[str, Any] = field(default_factory=dict)
    enum_values: tuple[str, ...] = ()
    quality: dict[str, Any] = field(default_factory=dict)
    description: str | None = None


@dataclass(frozen=True)
class GroundCommand:
    """Command exported to ground-facing dictionaries."""

    model_id: str
    target: str
    description: str
    arguments: tuple[GroundCommandArgument, ...]
    allowed_modes: tuple[str, ...]
    preconditions: Any | None
    requires_ack: bool
    timeout_ms: int | None
    risk: str
    emits: tuple[str, ...] = ()
    expected_effects: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GroundEvent:
    """Event exported to ground-facing dictionaries."""

    model_id: str
    source: str
    severity: str
    description: str
    downlink_priority: str | None = None
    persistence: str | None = None


@dataclass(frozen=True)
class GroundFault:
    """Fault exported to ground-facing dictionaries."""

    model_id: str
    source: str
    severity: str
    description: str
    condition: dict[str, Any]
    emits: tuple[str, ...] = ()
    recovery: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GroundDataProduct:
    """Data product exported to ground-facing dictionaries."""

    model_id: str
    producer: str
    producer_type: str
    type: str
    estimated_size_bytes: int
    priority: str
    payload: str | None = None
    storage: dict[str, Any] = field(default_factory=dict)
    downlink: dict[str, Any] = field(default_factory=dict)
    description: str | None = None


@dataclass(frozen=True)
class GroundPacket:
    """Packet membership exported to ground-facing dictionaries."""

    model_id: str
    name: str
    type: str
    max_payload_bytes: int
    period: str | None
    telemetry: tuple[str, ...]
    description: str | None = None


@dataclass(frozen=True)
class GroundContract:
    """Ground-facing contract surface derived from a validated Mission Model."""

    mission_id: str
    mission_name: str
    model_version: str
    generation_profile: str
    telemetry: tuple[GroundTelemetryItem, ...] = ()
    commands: tuple[GroundCommand, ...] = ()
    events: tuple[GroundEvent, ...] = ()
    faults: tuple[GroundFault, ...] = ()
    data_products: tuple[GroundDataProduct, ...] = ()
    packets: tuple[GroundPacket, ...] = ()
