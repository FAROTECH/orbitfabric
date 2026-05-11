from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from orbitfabric.gen.ground.contract import (
    GroundCommand,
    GroundCommandArgument,
    GroundContract,
    GroundDataProduct,
    GroundEvent,
    GroundFault,
    GroundPacket,
    GroundTelemetryItem,
)
from orbitfabric.model.mission import Command, MissionModel


def build_ground_contract(
    model: MissionModel,
    *,
    generation_profile: str = "generic",
) -> GroundContract:
    """Build the ground-facing contract surface from a validated Mission Model."""
    return GroundContract(
        mission_id=model.spacecraft.id,
        mission_name=model.spacecraft.name,
        model_version=model.spacecraft.model_version,
        generation_profile=generation_profile,
        telemetry=_telemetry_items(model),
        commands=_commands(model),
        events=_events(model),
        faults=_faults(model),
        data_products=_data_products(model),
        packets=_packets(model),
    )


def _telemetry_items(model: MissionModel) -> tuple[GroundTelemetryItem, ...]:
    return tuple(
        GroundTelemetryItem(
            model_id=item.id,
            name=item.name,
            value_type=item.type,
            unit=item.unit,
            source=item.source,
            sampling=item.sampling,
            criticality=item.criticality,
            persistence=item.persistence,
            downlink_priority=item.downlink_priority,
            limits=_clean_model_dump(item.limits),
            enum_values=tuple(item.enum or ()),
            quality=_clean_model_dump(item.quality),
            description=item.description,
        )
        for item in sorted(model.telemetry, key=lambda item: item.id)
    )


def _commands(model: MissionModel) -> tuple[GroundCommand, ...]:
    return tuple(
        GroundCommand(
            model_id=command.id,
            target=command.target,
            description=command.description,
            arguments=_command_arguments(command),
            allowed_modes=tuple(command.allowed_modes),
            preconditions=_clean_value(command.preconditions),
            requires_ack=command.requires_ack,
            timeout_ms=command.timeout_ms,
            risk=command.risk,
            emits=tuple(command.emits),
            expected_effects=_clean_dict(command.expected_effects),
        )
        for command in sorted(model.commands, key=lambda item: item.id)
    )


def _command_arguments(command: Command) -> tuple[GroundCommandArgument, ...]:
    return tuple(
        GroundCommandArgument(
            name=argument.name,
            value_type=argument.type,
            minimum=argument.min,
            maximum=argument.max,
            enum_values=tuple(argument.enum or ()),
            default=argument.default,
            description=argument.description,
        )
        for argument in command.arguments
    )


def _events(model: MissionModel) -> tuple[GroundEvent, ...]:
    return tuple(
        GroundEvent(
            model_id=event.id,
            source=event.source,
            severity=event.severity,
            description=event.description,
            downlink_priority=event.downlink_priority,
            persistence=event.persistence,
        )
        for event in sorted(model.events, key=lambda item: item.id)
    )


def _faults(model: MissionModel) -> tuple[GroundFault, ...]:
    return tuple(
        GroundFault(
            model_id=fault.id,
            source=fault.source,
            severity=fault.severity,
            description=fault.description,
            condition=_clean_model_dump(fault.condition),
            emits=tuple(fault.emits),
            recovery=_clean_model_dump(fault.recovery),
        )
        for fault in sorted(model.faults, key=lambda item: item.id)
    )


def _data_products(model: MissionModel) -> tuple[GroundDataProduct, ...]:
    return tuple(
        GroundDataProduct(
            model_id=data_product.id,
            producer=data_product.producer,
            producer_type=data_product.producer_type,
            type=data_product.type,
            estimated_size_bytes=data_product.estimated_size_bytes,
            priority=data_product.priority,
            payload=data_product.payload,
            storage=_clean_model_dump(data_product.storage),
            downlink=_clean_model_dump(data_product.downlink),
            description=data_product.description,
        )
        for data_product in sorted(model.data_products, key=lambda item: item.id)
    )


def _packets(model: MissionModel) -> tuple[GroundPacket, ...]:
    return tuple(
        GroundPacket(
            model_id=packet.id,
            name=packet.name,
            type=packet.type,
            max_payload_bytes=packet.max_payload_bytes,
            period=packet.period,
            telemetry=tuple(packet.telemetry),
            description=packet.description,
        )
        for packet in sorted(model.packets, key=lambda item: item.id)
    )


def _clean_model_dump(value: BaseModel | None) -> dict[str, Any]:
    if value is None:
        return {}

    dumped = value.model_dump(by_alias=True)
    return _clean_dict(dumped)


def _clean_dict(value: dict[str, Any]) -> dict[str, Any]:
    cleaned = _clean_value(value)
    if isinstance(cleaned, dict):
        return cleaned
    return {}


def _clean_value(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return _clean_model_dump(value)

    if isinstance(value, dict):
        return {
            key: cleaned
            for key, item in value.items()
            if (cleaned := _clean_value(item)) is not None
        }

    if isinstance(value, list):
        return [_clean_value(item) for item in value]

    if isinstance(value, tuple):
        return tuple(_clean_value(item) for item in value)

    return value
