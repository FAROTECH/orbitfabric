from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class RuntimeArgument:
    """Command argument exposed through the runtime-facing contract."""

    model_id: str
    symbol_name: str
    value_type: str
    minimum: float | int | None = None
    maximum: float | int | None = None
    enum_values: tuple[str, ...] = ()
    default: Any | None = None
    description: str | None = None


@dataclass(frozen=True)
class RuntimeElement:
    """Generic contract element exported to runtime-facing artifacts."""

    model_id: str
    symbol_name: str
    numeric_id: int
    description: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RuntimeCommand(RuntimeElement):
    """Command element with typed arguments."""

    arguments: tuple[RuntimeArgument, ...] = ()


@dataclass(frozen=True)
class RuntimeContract:
    """Software-facing contract surface derived from a validated Mission Model."""

    mission_id: str
    mission_name: str
    model_version: str
    generation_profile: str
    modes: tuple[RuntimeElement, ...] = ()
    telemetry: tuple[RuntimeElement, ...] = ()
    commands: tuple[RuntimeCommand, ...] = ()
    events: tuple[RuntimeElement, ...] = ()
    faults: tuple[RuntimeElement, ...] = ()
    packets: tuple[RuntimeElement, ...] = ()
    payloads: tuple[RuntimeElement, ...] = ()
    data_products: tuple[RuntimeElement, ...] = ()
    storage_policies: tuple[RuntimeElement, ...] = ()
    downlink_policies: tuple[RuntimeElement, ...] = ()
