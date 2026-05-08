from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from orbitfabric.model.mission import (
    Command,
    DataProductContract,
    DownlinkFlowContract,
    MissionModel,
)


@dataclass(frozen=True)
class DataFlowDocRecord:
    command: Command
    data_product: DataProductContract
    downlink_flows: list[DownlinkFlowContract]
    contact_windows: list[str]


def generate_data_flow_markdown_doc(
    model: MissionModel,
    output_file: Path,
) -> Path:
    """Generate a Markdown data-flow evidence reference from a Mission Model."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(_render_data_flow_doc(model), encoding="utf-8")
    return output_file


def _render_data_flow_doc(model: MissionModel) -> str:
    records = _data_flow_records(model)
    data_product_ids = {record.data_product.id for record in records}
    downlink_flow_ids = {
        flow.id for record in records for flow in record.downlink_flows
    }
    contact_window_ids = {
        window_id for record in records for window_id in record.contact_windows
    }

    lines = [_header("Mission Data Flow Evidence Reference", model)]

    lines.append("## Summary\n\n")
    lines.append(f"- Declared data-flow paths: `{len(records)}`\n")
    lines.append(f"- Data products with command effects: `{len(data_product_ids)}`\n")
    lines.append(f"- Downlink flows involved: `{len(downlink_flow_ids)}`\n")
    lines.append(f"- Contact windows involved: `{len(contact_window_ids)}`\n\n")
    lines.append(
        "This document is generated from declared Mission Model contracts. "
        "It traces command expected effects to data products, storage intent, "
        "downlink intent, eligible downlink flows and matching contact windows. "
        "It does not imply real payload file generation, onboard storage writes, "
        "queue execution, contact scheduling, RF behavior or ground integration.\n\n"
    )

    lines.append("## Declared data-flow paths\n\n")

    if not records:
        lines.append("No command-declared data-flow paths found.\n")
        return "".join(lines)

    lines.append(
        "| Command | Data Product | Producer | Storage Intent | Downlink Intent | "
        "Eligible Downlink Flows | Matching Contact Windows |\n"
    )
    lines.append("|---|---|---|---|---|---|---|\n")

    for record in records:
        lines.append(_render_record_row(model, record))

    return "".join(lines)


def _data_flow_records(model: MissionModel) -> list[DataFlowDocRecord]:
    data_products = {data_product.id: data_product for data_product in model.data_products}
    records: list[DataFlowDocRecord] = []

    for command in sorted(model.commands, key=lambda item: item.id):
        data_product_ids = command.expected_effects.get("data_products")
        if not isinstance(data_product_ids, list):
            continue

        for data_product_id in data_product_ids:
            if not isinstance(data_product_id, str):
                continue

            data_product = data_products.get(data_product_id)
            if data_product is None:
                continue

            flows = _eligible_downlink_flows(model, data_product.id)
            records.append(
                DataFlowDocRecord(
                    command=command,
                    data_product=data_product,
                    downlink_flows=flows,
                    contact_windows=_matching_contact_windows(model, flows),
                )
            )

    return records


def _eligible_downlink_flows(
    model: MissionModel,
    data_product_id: str,
) -> list[DownlinkFlowContract]:
    return [
        flow
        for flow in sorted(model.contacts.downlink_flows, key=lambda item: item.id)
        if data_product_id in flow.eligible_data_products
    ]


def _matching_contact_windows(
    model: MissionModel,
    flows: list[DownlinkFlowContract],
) -> list[str]:
    windows: set[str] = set()

    for flow in flows:
        for window in model.contacts.contact_windows:
            if window.contact_profile != flow.contact_profile:
                continue
            if window.link_profile != flow.link_profile:
                continue
            windows.add(window.id)

    return sorted(windows)


def _render_record_row(model: MissionModel, record: DataFlowDocRecord) -> str:
    return (
        f"| {_code(record.command.id)} "
        f"| {_code(record.data_product.id)} "
        f"| {_producer_heading(model, record.data_product)} "
        f"| {_format_storage_intent(record.data_product)} "
        f"| {_format_downlink_intent(record.data_product)} "
        f"| {_format_list([flow.id for flow in record.downlink_flows])} "
        f"| {_format_list(record.contact_windows)} |\n"
    )


def _header(title: str, model: MissionModel) -> str:
    return (
        f"# {title}\n\n"
        f"Mission: `{model.spacecraft.id}`  \n"
        f"Model version: `{model.spacecraft.model_version}`  \n"
        "Generated by OrbitFabric. Do not edit manually.\n\n"
        "This page is generated from the validated Mission Model.\n\n"
    )


def _producer_heading(model: MissionModel, data_product: DataProductContract) -> str:
    if data_product.producer_type != "subsystem":
        return f"{_code(data_product.producer)} ({_code(data_product.producer_type)})"

    subsystems = {subsystem.id: subsystem for subsystem in model.subsystems}
    subsystem = subsystems.get(data_product.producer)
    if subsystem is None:
        return _code(data_product.producer)

    return f"{_code(data_product.producer)} - {_text(subsystem.name)}"


def _format_storage_intent(data_product: DataProductContract) -> str:
    storage = data_product.storage
    if storage is None:
        return "-"

    lines = [f"class {_code(storage.storage_class)}"]

    if storage.retention is not None:
        lines.append(f"retention {_code(storage.retention)}")

    if storage.overflow_policy is not None:
        lines.append(f"overflow {_code(storage.overflow_policy)}")

    return _line_break_join(lines)


def _format_downlink_intent(data_product: DataProductContract) -> str:
    downlink = data_product.downlink
    if downlink is None or downlink.policy is None:
        return "-"

    return f"policy {_code(downlink.policy)}"


def _format_list(values: list[str]) -> str:
    if not values:
        return "-"

    return ", ".join(_code(value) for value in values)


def _line_break_join(values: list[str]) -> str:
    items = [value for value in values if value]
    if not items:
        return "-"

    return "<br>".join(items)


def _code(value: Any) -> str:
    return f"`{_text(_format_plain_value(value))}`"


def _format_plain_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    return str(value)


def _text(value: str) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")
