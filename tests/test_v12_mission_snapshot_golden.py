from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from orbitfabric.export.mission_snapshot import mission_snapshot_from_dir

DEMO_MISSION = Path("examples/demo-3u/mission")
GOLDEN_FILE = Path(
    "tests/golden/demo_3u_core_surfaces/mission_snapshot_contract_signature.json"
)

REQUIRED_MODEL_FIELDS = {
    "spacecraft",
    "subsystems",
    "modes",
    "mode_transitions",
    "telemetry",
    "commands",
    "events",
    "faults",
    "packets",
    "policies",
    "payloads",
    "data_products",
    "contacts",
    "commandability",
}
SELECTED_TELEMETRY_IDS = {
    "obc.mode",
    "eps.battery.voltage",
    "payload.acquisition.active",
}


def _load_expected() -> dict[str, Any]:
    return json.loads(GOLDEN_FILE.read_text(encoding="utf-8"))["expected"]


def _select_mission_snapshot_contract_fields(snapshot: dict[str, Any]) -> dict[str, Any]:
    model = snapshot["model"]
    telemetry_ids = {item["id"] for item in model["telemetry"]}

    return {
        "snapshot_version": snapshot["snapshot_version"],
        "kind": snapshot["kind"],
        "result": snapshot["result"],
        "mission": snapshot["mission"],
        "boundaries": snapshot["boundaries"],
        "model_contract": {
            "required_top_level_fields_present": sorted(
                field for field in REQUIRED_MODEL_FIELDS if field in model
            ),
            "spacecraft_class_alias": {
                "class_present": "class" in model["spacecraft"],
                "spacecraft_class_absent": "spacecraft_class" not in model["spacecraft"],
            },
            "selected_telemetry_ids": sorted(
                telemetry_id
                for telemetry_id in SELECTED_TELEMETRY_IDS
                if telemetry_id in telemetry_ids
            ),
        },
    }


def test_demo_3u_mission_snapshot_matches_v12_golden_contract_signature() -> None:
    snapshot = mission_snapshot_from_dir(DEMO_MISSION)

    actual = _select_mission_snapshot_contract_fields(snapshot)

    assert actual == _load_expected()
