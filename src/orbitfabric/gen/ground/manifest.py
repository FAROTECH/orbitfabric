from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from orbitfabric.gen.ground.contract import GroundContract
from orbitfabric.gen.ground.json_safe import json_safe


def ground_contract_manifest(contract: GroundContract) -> dict[str, Any]:
    """Return a deterministic JSON-serializable GroundContract manifest."""
    return {
        "manifest_version": "0.1",
        "kind": "orbitfabric.ground_contract_manifest",
        "mission": {
            "id": contract.mission_id,
            "name": contract.mission_name,
            "model_version": contract.model_version,
        },
        "generation": {
            "profile": contract.generation_profile,
            "generated_artifacts_are_disposable": True,
            "contains_ground_runtime": False,
            "contains_operator_console": False,
            "contains_transport": False,
            "contains_database": False,
            "claims_yamcs_compatibility": False,
            "claims_openc3_compatibility": False,
            "claims_xtce_compliance": False,
        },
        "counts": {
            "telemetry": len(contract.telemetry),
            "commands": len(contract.commands),
            "events": len(contract.events),
            "faults": len(contract.faults),
            "data_products": len(contract.data_products),
            "packets": len(contract.packets),
        },
        "contract": json_safe(asdict(contract)),
    }


def write_ground_contract_manifest(
    contract: GroundContract,
    output_file: Path,
) -> Path:
    """Write a deterministic GroundContract manifest JSON file."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(
        json.dumps(ground_contract_manifest(contract), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output_file
