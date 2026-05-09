from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from orbitfabric.gen.runtime.contract import RuntimeContract


def runtime_contract_manifest(contract: RuntimeContract) -> dict[str, Any]:
    """Return a deterministic JSON-serializable RuntimeContract manifest."""
    return {
        "manifest_version": "0.1",
        "kind": "orbitfabric.runtime_contract_manifest",
        "mission": {
            "id": contract.mission_id,
            "name": contract.mission_name,
            "model_version": contract.model_version,
        },
        "generation": {
            "profile": contract.generation_profile,
            "generated_artifacts_are_disposable": True,
            "contains_flight_runtime": False,
        },
        "counts": {
            "modes": len(contract.modes),
            "telemetry": len(contract.telemetry),
            "commands": len(contract.commands),
            "events": len(contract.events),
            "faults": len(contract.faults),
            "packets": len(contract.packets),
            "payloads": len(contract.payloads),
            "data_products": len(contract.data_products),
            "storage_policies": len(contract.storage_policies),
            "downlink_policies": len(contract.downlink_policies),
        },
        "contract": asdict(contract),
    }


def write_runtime_contract_manifest(
    contract: RuntimeContract,
    output_file: Path,
) -> Path:
    """Write a deterministic RuntimeContract manifest JSON file."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    manifest = runtime_contract_manifest(contract)
    output_file.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output_file
