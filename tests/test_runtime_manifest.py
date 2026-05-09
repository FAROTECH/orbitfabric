from __future__ import annotations

import json
from pathlib import Path

from orbitfabric.gen.runtime import build_runtime_contract, runtime_contract_manifest
from orbitfabric.gen.runtime.manifest import write_runtime_contract_manifest
from orbitfabric.model.loader import MissionModelLoader

DEMO_MISSION = Path("examples/demo-3u/mission")


def test_runtime_contract_manifest_shape() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    contract = build_runtime_contract(model)

    manifest = runtime_contract_manifest(contract)

    assert manifest["manifest_version"] == "0.1"
    assert manifest["kind"] == "orbitfabric.runtime_contract_manifest"
    assert manifest["mission"]["id"] == "demo-3u"
    assert manifest["generation"]["profile"] == "cpp17"
    assert manifest["generation"]["generated_artifacts_are_disposable"] is True
    assert manifest["generation"]["contains_flight_runtime"] is False
    assert manifest["counts"]["commands"] == len(contract.commands)
    assert manifest["contract"]["mission_id"] == "demo-3u"


def test_write_runtime_contract_manifest_is_deterministic(tmp_path: Path) -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    contract = build_runtime_contract(model)

    output_file = tmp_path / "runtime_contract_manifest.json"

    write_runtime_contract_manifest(contract, output_file)
    first_content = output_file.read_text(encoding="utf-8")

    write_runtime_contract_manifest(contract, output_file)
    second_content = output_file.read_text(encoding="utf-8")

    assert first_content == second_content

    parsed = json.loads(first_content)
    assert parsed["mission"]["name"] == "Demo 3U Spacecraft"
    assert parsed["counts"]["data_products"] == 1
