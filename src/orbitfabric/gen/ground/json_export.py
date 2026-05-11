from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from orbitfabric.gen.ground.contract import GroundContract


def ground_dictionary_documents(contract: GroundContract) -> dict[str, list[dict[str, Any]]]:
    """Return deterministic JSON dictionary documents from a GroundContract."""
    return {
        "telemetry_dictionary": [asdict(item) for item in contract.telemetry],
        "command_dictionary": [asdict(item) for item in contract.commands],
        "event_dictionary": [asdict(item) for item in contract.events],
        "fault_dictionary": [asdict(item) for item in contract.faults],
        "data_product_dictionary": [asdict(item) for item in contract.data_products],
        "packet_dictionary": [asdict(item) for item in contract.packets],
    }


def write_ground_dictionary_json_files(
    contract: GroundContract,
    output_dir: Path,
) -> list[Path]:
    """Write deterministic JSON dictionary files for a GroundContract."""
    dictionaries_dir = output_dir / "dictionaries"
    dictionaries_dir.mkdir(parents=True, exist_ok=True)

    written_files: list[Path] = []
    for name, document in ground_dictionary_documents(contract).items():
        output_file = dictionaries_dir / f"{name}.json"
        output_file.write_text(
            json.dumps(document, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        written_files.append(output_file)

    return written_files
