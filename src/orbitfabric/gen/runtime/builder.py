from __future__ import annotations

from collections.abc import Iterable

from orbitfabric.gen.runtime.contract import (
    RuntimeArgument,
    RuntimeCommand,
    RuntimeContract,
    RuntimeElement,
)
from orbitfabric.gen.runtime.naming import to_pascal_case
from orbitfabric.model.mission import (
    Command,
    DataProductContract,
    MissionModel,
)


def build_runtime_contract(
    model: MissionModel,
    *,
    generation_profile: str = "cpp17",
) -> RuntimeContract:
    """Build the runtime-facing contract surface from a validated Mission Model."""
    return RuntimeContract(
        mission_id=model.spacecraft.id,
        mission_name=model.spacecraft.name,
        model_version=model.spacecraft.model_version,
        generation_profile=generation_profile,
        modes=_mode_elements(model),
        telemetry=_telemetry_elements(model),
        commands=_command_elements(model),
        events=_event_elements(model),
        faults=_fault_elements(model),
        packets=_packet_elements(model),
        payloads=_payload_elements(model),
        data_products=_data_product_elements(model),
        storage_policies=_storage_policy_elements(model.data_products),
        downlink_policies=_downlink_policy_elements(model.data_products),
    )


def _mode_elements(model: MissionModel) -> tuple[RuntimeElement, ...]:
    return tuple(
        RuntimeElement(
            model_id=mode_id,
            symbol_name=to_pascal_case(mode_id),
            numeric_id=index,
            description=mode.description,
            metadata={"initial": mode.initial},
        )
        for index, (mode_id, mode) in enumerate(sorted(model.modes.items()), start=1)
    )


def _telemetry_elements(model: MissionModel) -> tuple[RuntimeElement, ...]:
    return tuple(
        RuntimeElement(
            model_id=item.id,
            symbol_name=to_pascal_case(item.id),
            numeric_id=index,
            description=item.description,
            metadata={
                "type": item.type,
                "unit": item.unit,
                "source": item.source,
                "criticality": item.criticality,
                "persistence": item.persistence,
                "downlink_priority": item.downlink_priority,
            },
        )
        for index, item in enumerate(sorted(model.telemetry, key=lambda item: item.id), start=1)
    )


def _command_elements(model: MissionModel) -> tuple[RuntimeCommand, ...]:
    return tuple(
        RuntimeCommand(
            model_id=command.id,
            symbol_name=to_pascal_case(command.id),
            numeric_id=index,
            description=command.description,
            metadata={
                "target": command.target,
                "allowed_modes": tuple(command.allowed_modes),
                "requires_ack": command.requires_ack,
                "timeout_ms": command.timeout_ms,
                "risk": command.risk,
                "emits": tuple(command.emits),
            },
            arguments=_runtime_arguments(command),
        )
        for index, command in enumerate(sorted(model.commands, key=lambda item: item.id), start=1)
    )


def _runtime_arguments(command: Command) -> tuple[RuntimeArgument, ...]:
    return tuple(
        RuntimeArgument(
            model_id=argument.name,
            symbol_name=to_pascal_case(argument.name),
            value_type=argument.type,
            minimum=argument.min,
            maximum=argument.max,
            enum_values=tuple(argument.enum or ()),
            default=argument.default,
            description=argument.description,
        )
        for argument in command.arguments
    )


def _event_elements(model: MissionModel) -> tuple[RuntimeElement, ...]:
    return tuple(
        RuntimeElement(
            model_id=event.id,
            symbol_name=to_pascal_case(event.id),
            numeric_id=index,
            description=event.description,
            metadata={
                "source": event.source,
                "severity": event.severity,
                "downlink_priority": event.downlink_priority,
                "persistence": event.persistence,
            },
        )
        for index, event in enumerate(sorted(model.events, key=lambda item: item.id), start=1)
    )


def _fault_elements(model: MissionModel) -> tuple[RuntimeElement, ...]:
    return tuple(
        RuntimeElement(
            model_id=fault.id,
            symbol_name=to_pascal_case(fault.id),
            numeric_id=index,
            description=fault.description,
            metadata={
                "source": fault.source,
                "severity": fault.severity,
                "emits": tuple(fault.emits),
            },
        )
        for index, fault in enumerate(sorted(model.faults, key=lambda item: item.id), start=1)
    )


def _packet_elements(model: MissionModel) -> tuple[RuntimeElement, ...]:
    return tuple(
        RuntimeElement(
            model_id=packet.id,
            symbol_name=to_pascal_case(packet.id),
            numeric_id=index,
            description=packet.description,
            metadata={
                "name": packet.name,
                "type": packet.type,
                "max_payload_bytes": packet.max_payload_bytes,
                "period": packet.period,
                "telemetry": tuple(packet.telemetry),
            },
        )
        for index, packet in enumerate(sorted(model.packets, key=lambda item: item.id), start=1)
    )


def _payload_elements(model: MissionModel) -> tuple[RuntimeElement, ...]:
    return tuple(
        RuntimeElement(
            model_id=payload.id,
            symbol_name=to_pascal_case(payload.id),
            numeric_id=index,
            description=payload.description,
            metadata={
                "subsystem": payload.subsystem,
                "profile": payload.profile,
                "initial_state": payload.lifecycle.initial_state,
                "states": tuple(payload.lifecycle.states),
            },
        )
        for index, payload in enumerate(sorted(model.payloads, key=lambda item: item.id), start=1)
    )


def _data_product_elements(model: MissionModel) -> tuple[RuntimeElement, ...]:
    return tuple(
        RuntimeElement(
            model_id=data_product.id,
            symbol_name=to_pascal_case(data_product.id),
            numeric_id=index,
            description=data_product.description,
            metadata={
                "producer": data_product.producer,
                "producer_type": data_product.producer_type,
                "type": data_product.type,
                "estimated_size_bytes": data_product.estimated_size_bytes,
                "priority": data_product.priority,
                "payload": data_product.payload,
                "storage_policy": _storage_policy_id(data_product),
                "downlink_policy": _downlink_policy_id(data_product),
            },
        )
        for index, data_product in enumerate(
            sorted(model.data_products, key=lambda item: item.id),
            start=1,
        )
    )


def _storage_policy_elements(
    data_products: Iterable[DataProductContract],
) -> tuple[RuntimeElement, ...]:
    policy_ids = sorted(
        {
            policy_id
            for data_product in data_products
            if (policy_id := _storage_policy_id(data_product)) is not None
        }
    )
    return _policy_elements(policy_ids)


def _downlink_policy_elements(
    data_products: Iterable[DataProductContract],
) -> tuple[RuntimeElement, ...]:
    policy_ids = sorted(
        {
            policy_id
            for data_product in data_products
            if (policy_id := _downlink_policy_id(data_product)) is not None
        }
    )
    return _policy_elements(policy_ids)


def _policy_elements(policy_ids: list[str]) -> tuple[RuntimeElement, ...]:
    return tuple(
        RuntimeElement(
            model_id=policy_id,
            symbol_name=to_pascal_case(policy_id),
            numeric_id=index,
        )
        for index, policy_id in enumerate(policy_ids, start=1)
    )


def _storage_policy_id(data_product: DataProductContract) -> str | None:
    if data_product.storage is None:
        return None

    return data_product.storage.storage_class


def _downlink_policy_id(data_product: DataProductContract) -> str | None:
    if data_product.downlink is None or data_product.downlink.policy is None:
        return None

    return data_product.downlink.policy
