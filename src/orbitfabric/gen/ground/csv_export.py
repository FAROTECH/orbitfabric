from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from orbitfabric.gen.ground.contract import GroundContract
from orbitfabric.gen.ground.json_export import ground_dictionary_documents

CSV_DICTIONARY_HEADERS: dict[str, tuple[str, ...]] = {
    "telemetry_dictionary": (
        "model_id",
        "name",
        "value_type",
        "unit",
        "source",
        "sampling",
        "criticality",
        "persistence",
        "downlink_priority",
        "limits",
        "enum_values",
        "quality",
        "description",
    ),
    "command_dictionary": (
        "model_id",
        "target",
        "description",
        "arguments",
        "allowed_modes",
        "preconditions",
        "requires_ack",
        "timeout_ms",
        "risk",
        "emits",
        "expected_effects",
    ),
    "event_dictionary": (
        "model_id",
        "source",
        "severity",
        "description",
        "downlink_priority",
        "persistence",
    ),
    "fault_dictionary": (
        "model_id",
        "source",
        "severity",
        "description",
        "condition",
        "emits",
        "recovery",
    ),
    "data_product_dictionary": (
        "model_id",
        "producer",
        "producer_type",
        "type",
        "estimated_size_bytes",
        "priority",
        "payload",
        "storage",
        "downlink",
        "description",
    ),
    "packet_dictionary": (
        "model_id",
        "name",
        "type",
        "max_payload_bytes",
        "period",
        "telemetry",
        "description",
    ),
}


def write_ground_dictionary_csv_files(
    contract: GroundContract,
    output_dir: Path,
) -> list[Path]:
    """Write deterministic CSV dictionary files for a GroundContract."""
    csv_dir = output_dir / "csv"
    csv_dir.mkdir(parents=True, exist_ok=True)

    written_files: list[Path] = []
    documents = ground_dictionary_documents(contract)
    for name, rows in documents.items():
        output_file = csv_dir / f"{name}.csv"
        _write_dictionary_csv(output_file, CSV_DICTIONARY_HEADERS[name], rows)
        written_files.append(output_file)

    return written_files


def _write_dictionary_csv(
    output_file: Path,
    headers: tuple[str, ...],
    rows: list[dict[str, Any]],
) -> None:
    with output_file.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({header: _csv_cell(row.get(header)) for header in headers})


def _csv_cell(value: Any) -> str | int | float | bool | None:
    if isinstance(value, dict | list):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))

    return value
