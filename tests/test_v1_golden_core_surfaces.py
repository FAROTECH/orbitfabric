from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from orbitfabric.export.entity_index import entity_index_to_dict
from orbitfabric.export.model_summary import model_summary_to_dict
from orbitfabric.export.relationship_manifest import relationship_manifest_to_dict
from orbitfabric.model.loader import MissionModelLoader

DEMO_MISSION = Path("examples/demo-3u/mission")
GOLDEN_DIR = Path("tests/golden/demo_3u_core_surfaces")


def _load_expected(file_name: str) -> dict[str, Any]:
    golden = json.loads((GOLDEN_DIR / file_name).read_text(encoding="utf-8"))
    return golden["expected"]


def _select_model_summary_contract_fields(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "summary_version": summary["summary_version"],
        "kind": summary["kind"],
        "mission": summary["mission"],
        "boundaries": summary["boundaries"],
        "counts": summary["counts"],
        "domains": sorted(
            [
                {
                    "id": domain["id"],
                    "required": domain["required"],
                    "present": domain["present"],
                    "source_file": domain["source_file"],
                    "count": domain["count"],
                }
                for domain in summary["domains"]
            ],
            key=lambda item: item["id"],
        ),
    }


def _select_entity_index_contract_fields(index: dict[str, Any]) -> dict[str, Any]:
    return {
        "index_version": index["index_version"],
        "kind": index["kind"],
        "mission": index["mission"],
        "boundaries": index["boundaries"],
        "counts": index["counts"],
        "domains": sorted(
            [
                {
                    "id": domain["id"],
                    "source_file": domain["source_file"],
                    "indexed": domain["indexed"],
                    "model_count": domain["model_count"],
                    "entity_count": domain["entity_count"],
                }
                for domain in index["domains"]
            ],
            key=lambda item: item["id"],
        ),
        "entities": sorted(
            [
                {
                    "domain": entity["domain"],
                    "id": entity["id"],
                    "entity_type": entity["entity_type"],
                    "source_file": entity["source_file"],
                }
                for entity in index["entities"]
            ],
            key=lambda item: (item["domain"], item["id"]),
        ),
    }


def _select_relationship_manifest_contract_fields(
    manifest: dict[str, Any],
    selected_relationship_ids: list[str],
) -> dict[str, Any]:
    emitted_relationship_ids = {
        relationship["relationship_id"] for relationship in manifest["relationships"]
    }

    return {
        "manifest_version": manifest["manifest_version"],
        "kind": manifest["kind"],
        "status": manifest["status"],
        "mission": manifest["mission"],
        "boundaries": manifest["boundaries"],
        "derivation_policy": manifest["derivation_policy"],
        "counts": manifest["counts"],
        "relationship_types": manifest["relationship_types"],
        "selected_relationship_ids": [
            relationship_id
            for relationship_id in selected_relationship_ids
            if relationship_id in emitted_relationship_ids
        ],
    }


def test_demo_3u_model_summary_matches_golden_contract_signature() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    summary = model_summary_to_dict(model, DEMO_MISSION)

    actual = _select_model_summary_contract_fields(summary)

    assert actual == _load_expected("model_summary_contract_signature.json")


def test_demo_3u_entity_index_matches_golden_contract_signature() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    index = entity_index_to_dict(model, DEMO_MISSION)

    actual = _select_entity_index_contract_fields(index)

    assert actual == _load_expected("entity_index_contract_signature.json")


def test_demo_3u_relationship_manifest_matches_golden_contract_signature() -> None:
    expected = _load_expected("relationship_manifest_contract_signature.json")
    model = MissionModelLoader().load(DEMO_MISSION)
    manifest = relationship_manifest_to_dict(model, DEMO_MISSION)

    actual = _select_relationship_manifest_contract_fields(
        manifest,
        selected_relationship_ids=expected["selected_relationship_ids"],
    )

    assert actual == expected
