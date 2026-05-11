from __future__ import annotations

import json
from pathlib import Path

from orbitfabric.gen.ground import (
    build_ground_contract,
    ground_contract_manifest,
    write_ground_contract_manifest,
)
from orbitfabric.model.loader import MissionModelLoader

DEMO_MISSION = Path("examples/demo-3u/mission")


def test_ground_contract_manifest_contains_boundary_flags() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    contract = build_ground_contract(model)

    manifest = ground_contract_manifest(contract)

    assert manifest["manifest_version"] == "0.1"
    assert manifest["kind"] == "orbitfabric.ground_contract_manifest"
    assert manifest["mission"]["id"] == "demo-3u"
    assert manifest["mission"]["name"] == "Demo 3U Spacecraft"
    assert manifest["mission"]["model_version"] == "0.1.0"
    assert manifest["generation"]["profile"] == "generic"
    assert manifest["generation"]["generated_artifacts_are_disposable"] is True
    assert manifest["generation"]["contains_ground_runtime"] is False
    assert manifest["generation"]["contains_operator_console"] is False
    assert manifest["generation"]["contains_transport"] is False
    assert manifest["generation"]["contains_database"] is False
    assert manifest["generation"]["claims_yamcs_compatibility"] is False
    assert manifest["generation"]["claims_openc3_compatibility"] is False
    assert manifest["generation"]["claims_xtce_compliance"] is False


def test_ground_contract_manifest_counts_contract_domains() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    contract = build_ground_contract(model)

    manifest = ground_contract_manifest(contract)

    assert manifest["counts"] == {
        "telemetry": len(contract.telemetry),
        "commands": len(contract.commands),
        "events": len(contract.events),
        "faults": len(contract.faults),
        "data_products": len(contract.data_products),
        "packets": len(contract.packets),
    }


def test_write_ground_contract_manifest_is_deterministic_json(tmp_path: Path) -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    contract = build_ground_contract(model)
    output_file = tmp_path / "ground_contract_manifest.json"

    written_file = write_ground_contract_manifest(contract, output_file)

    assert written_file == output_file
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert content.endswith("\n")

    parsed = json.loads(content)
    assert parsed == ground_contract_manifest(contract)
