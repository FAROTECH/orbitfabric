from __future__ import annotations

from pathlib import Path
from typing import Any

from orbitfabric.gen.ground.contract import GroundContract


def write_ground_markdown_review_artifacts(
    contract: GroundContract,
    output_dir: Path,
) -> list[Path]:
    """Write human-reviewable Markdown artifacts for a GroundContract."""
    output_dir.mkdir(parents=True, exist_ok=True)

    readme_file = output_dir / "README.md"
    dictionaries_file = output_dir / "ground_dictionaries.md"

    readme_file.write_text(_render_readme(contract), encoding="utf-8")
    dictionaries_file.write_text(_render_ground_dictionaries(contract), encoding="utf-8")

    return [readme_file, dictionaries_file]


def _render_readme(contract: GroundContract) -> str:
    lines = [
        "# OrbitFabric Ground Integration Artifacts",
        "",
        (
            "This directory contains generated ground-facing artifacts derived from "
            "the OrbitFabric Mission Model."
        ),
        "",
        (
            "These files are intended to help ground software engineers, mission "
            "operators and integration teams review what the spacecraft contract "
            "exposes to the ground side."
        ),
        "",
        (
            "The Mission Model remains the source of truth. These artifacts are "
            "generated outputs and can be deleted and regenerated at any time."
        ),
        "",
        "## Mission",
        "",
        f"- Mission ID: `{contract.mission_id}`",
        f"- Mission name: {contract.mission_name}",
        f"- Model version: `{contract.model_version}`",
        f"- Ground profile: `{contract.generation_profile}`",
        "",
        "## Generated files",
        "",
        "| Path | Purpose | Primary audience |",
        "| --- | --- | --- |",
        (
            "| `ground_contract_manifest.json` | Machine-readable manifest and "
            "boundary declaration. | Tooling and integration checks |"
        ),
        (
            "| `dictionaries/*.json` | Machine-readable ground dictionaries. | "
            "Ground tooling, scripts and automated checks |"
        ),
        (
            "| `csv/*.csv` | Review-friendly tabular dictionaries. | "
            "Engineers and reviewers |"
        ),
        (
            "| `ground_dictionaries.md` | Human-readable review document. | "
            "Engineers, operators and reviewers |"
        ),
        (
            "| `README.md` | This generated orientation file. | Everyone "
            "opening the artifact directory |"
        ),
        "",
        "## Contract coverage",
        "",
        "| Domain | Count |",
        "| --- | ---: |",
        f"| Telemetry | {len(contract.telemetry)} |",
        f"| Commands | {len(contract.commands)} |",
        f"| Events | {len(contract.events)} |",
        f"| Faults | {len(contract.faults)} |",
        f"| Data products | {len(contract.data_products)} |",
        f"| Packets | {len(contract.packets)} |",
        "",
        "## Boundary",
        "",
        (
            "These artifacts do not implement a ground system. They do not contain "
            "runtime behavior, transport behavior, database behavior, decoder logic "
            "or command uplink logic."
        ),
        "",
        (
            "They also do not claim compatibility with Yamcs, OpenC3, XTCE, CCSDS, "
            "PUS or CFDP. They provide generic, tool-neutral mission contract "
            "evidence that other tools can consume or map later."
        ),
        "",
        "## Recommended review flow",
        "",
        (
            "1. Start from `ground_contract_manifest.json` to verify the mission "
            "identity, generation profile and declared boundary."
        ),
        (
            "2. Read `ground_dictionaries.md` to review the contract as a coherent "
            "engineering document."
        ),
        "3. Use `csv/*.csv` for spreadsheet-style inspection and review comments.",
        (
            "4. Use `dictionaries/*.json` for scripts, tooling and deterministic "
            "integration checks."
        ),
        "",
    ]
    return "\n".join(lines)


def _render_ground_dictionaries(contract: GroundContract) -> str:
    lines = [
        "# Ground Dictionaries Review",
        "",
        f"Mission: `{contract.mission_id}`",
        "",
        f"Model version: `{contract.model_version}`",
        "",
        f"Ground generation profile: `{contract.generation_profile}`",
        "",
        (
            "This document is generated from the OrbitFabric `GroundContract` and "
            "is intended for human review."
        ),
        "",
        (
            "It summarizes the ground-facing telemetry, commands, events, faults, "
            "data products and packets exposed by the Mission Model."
        ),
        "",
        "## Review boundary",
        "",
        (
            "This document is not a ground runtime specification. It does not "
            "define binary packet decoding, transport protocols, database schemas, "
            "command uplink execution or operator console behavior."
        ),
        "",
        "It is a tool-neutral review layer over the mission data contract.",
        "",
        "## Summary",
        "",
        "| Domain | Count | Review focus |",
        "| --- | ---: | --- |",
        f"| Telemetry | {len(contract.telemetry)} | Values expected from the spacecraft |",
        f"| Commands | {len(contract.commands)} | Ground-callable command contract |",
        f"| Events | {len(contract.events)} | Operational event vocabulary |",
        f"| Faults | {len(contract.faults)} | Fault vocabulary and recovery hints |",
        (
            f"| Data products | {len(contract.data_products)} | Products to store, "
            "downlink or process |"
        ),
        f"| Packets | {len(contract.packets)} | Logical packet membership |",
        "",
    ]

    lines.extend(_render_telemetry(contract))
    lines.extend(_render_commands(contract))
    lines.extend(_render_events(contract))
    lines.extend(_render_faults(contract))
    lines.extend(_render_data_products(contract))
    lines.extend(_render_packets(contract))

    return "\n".join(lines)


def _render_telemetry(contract: GroundContract) -> list[str]:
    lines = [
        "## Telemetry dictionary",
        "",
        (
            "Telemetry entries describe values expected by the ground side. Limits "
            "and quality metadata are shown where available."
        ),
        "",
        (
            "| Model ID | Name | Type | Unit | Source | Sampling | Criticality | "
            "Persistence | Downlink | Limits | Quality |"
        ),
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in contract.telemetry:
        lines.append(
            "| "
            + " | ".join(
                [
                    _code(item.model_id),
                    _text(item.name),
                    _code(item.value_type),
                    _text(item.unit),
                    _code(item.source),
                    _text(item.sampling),
                    _text(item.criticality),
                    _text(item.persistence),
                    _text(item.downlink_priority),
                    _compact(item.limits),
                    _compact(item.quality),
                ]
            )
            + " |"
        )
    lines.append("")
    return lines


def _render_commands(contract: GroundContract) -> list[str]:
    lines = [
        "## Command dictionary",
        "",
        (
            "Command entries describe the callable contract visible to the ground "
            "side. This is not a command encoder or uplink implementation."
        ),
        "",
        (
            "| Model ID | Target | Modes | Ack | Timeout ms | Risk | Arguments | "
            "Emits | Expected effects | Preconditions |"
        ),
        "| --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |",
    ]
    for item in contract.commands:
        lines.append(
            "| "
            + " | ".join(
                [
                    _code(item.model_id),
                    _code(item.target),
                    _list(item.allowed_modes),
                    _bool(item.requires_ack),
                    _text(item.timeout_ms),
                    _text(item.risk),
                    _arguments(item.arguments),
                    _list(item.emits),
                    _compact(item.expected_effects),
                    _compact(item.preconditions),
                ]
            )
            + " |"
        )
    lines.append("")
    return lines


def _render_events(contract: GroundContract) -> list[str]:
    lines = [
        "## Event dictionary",
        "",
        "Events define the operational vocabulary emitted by the spacecraft contract.",
        "",
        "| Model ID | Source | Severity | Downlink | Persistence | Description |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in contract.events:
        lines.append(
            "| "
            + " | ".join(
                [
                    _code(item.model_id),
                    _code(item.source),
                    _text(item.severity),
                    _text(item.downlink_priority),
                    _text(item.persistence),
                    _text(item.description),
                ]
            )
            + " |"
        )
    lines.append("")
    return lines


def _render_faults(contract: GroundContract) -> list[str]:
    lines = [
        "## Fault dictionary",
        "",
        (
            "Fault entries summarize fault identifiers, severity and recovery "
            "hints. They do not implement onboard or ground fault handling."
        ),
        "",
        "| Model ID | Source | Severity | Condition | Emits | Recovery | Description |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in contract.faults:
        lines.append(
            "| "
            + " | ".join(
                [
                    _code(item.model_id),
                    _code(item.source),
                    _text(item.severity),
                    _compact(item.condition),
                    _list(item.emits),
                    _compact(item.recovery),
                    _text(item.description),
                ]
            )
            + " |"
        )
    lines.append("")
    return lines


def _render_data_products(contract: GroundContract) -> list[str]:
    lines = [
        "## Data product dictionary",
        "",
        (
            "Data products describe files or logical products expected to be "
            "stored, downlinked or processed by the ground side."
        ),
        "",
        (
            "| Model ID | Producer | Type | Size bytes | Priority | Storage | "
            "Downlink | Description |"
        ),
        "| --- | --- | --- | ---: | --- | --- | --- | --- |",
    ]
    for item in contract.data_products:
        lines.append(
            "| "
            + " | ".join(
                [
                    _code(item.model_id),
                    _code(item.producer),
                    _text(item.type),
                    _text(item.estimated_size_bytes),
                    _text(item.priority),
                    _compact(item.storage),
                    _compact(item.downlink),
                    _text(item.description),
                ]
            )
            + " |"
        )
    lines.append("")
    return lines


def _render_packets(contract: GroundContract) -> list[str]:
    lines = [
        "## Packet dictionary",
        "",
        (
            "Packets describe logical membership of model fields. They do not "
            "define binary layout, offsets, framing or transport."
        ),
        "",
        (
            "| Model ID | Name | Type | Max payload bytes | Period | Telemetry "
            "membership | Description |"
        ),
        "| --- | --- | --- | ---: | --- | --- | --- |",
    ]
    for item in contract.packets:
        lines.append(
            "| "
            + " | ".join(
                [
                    _code(item.model_id),
                    _text(item.name),
                    _text(item.type),
                    _text(item.max_payload_bytes),
                    _text(item.period),
                    _list(item.telemetry),
                    _text(item.description),
                ]
            )
            + " |"
        )
    lines.append("")
    return lines


def _arguments(arguments: tuple[Any, ...]) -> str:
    if not arguments:
        return ""

    rendered = []
    for argument in arguments:
        metadata = _argument_metadata(argument)
        if metadata:
            rendered.append(f"`{argument.name}` ({argument.value_type}, {metadata})")
        else:
            rendered.append(f"`{argument.name}` ({argument.value_type})")
    return "; ".join(rendered)


def _argument_metadata(argument: Any) -> str:
    metadata: list[str] = []

    if argument.minimum is not None:
        metadata.append(f"min: {_text(argument.minimum)}")
    if argument.maximum is not None:
        metadata.append(f"max: {_text(argument.maximum)}")
    if argument.enum_values:
        metadata.append(f"enum: {_list(argument.enum_values)}")
    if argument.default is not None:
        metadata.append(f"default: {_text(argument.default)}")
    if argument.description:
        metadata.append(f"description: {_text(argument.description)}")

    return "; ".join(metadata)


def _list(values: tuple[str, ...] | list[str] | None) -> str:
    if not values:
        return ""
    return ", ".join(_code(value) for value in values)


def _compact(value: Any) -> str:
    if value in (None, {}, [], ()):
        return ""

    if isinstance(value, dict):
        return "; ".join(
            _compact_key_value(key, item) for key, item in value.items()
        )

    if isinstance(value, list | tuple):
        return ", ".join(_compact(item) for item in value)

    return _text(value)


def _compact_key_value(key: Any, value: Any) -> str:
    if isinstance(value, dict | list | tuple):
        rendered_value = _compact(value)
    else:
        rendered_value = _text(value)

    return f"{_text(key)}: {rendered_value}"


def _bool(value: bool) -> str:
    return "yes" if value else "no"


def _code(value: Any) -> str:
    if value in (None, ""):
        return ""
    return f"`{_escape_markdown(str(value))}`"


def _text(value: Any) -> str:
    if value is None:
        return ""
    return _escape_markdown(str(value))


def _escape_markdown(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")
