from __future__ import annotations

import json
from pathlib import Path

from orbitfabric import __version__
from orbitfabric.export.mission_snapshot import (
    SNAPSHOT_KIND,
    SNAPSHOT_VERSION,
    mission_snapshot_from_dir,
    mission_snapshot_to_dict,
    write_mission_snapshot,
)
from orbitfabric.model.loader import MissionModelLoader

DEMO_MISSION = Path("examples/demo-3u/mission")


def test_mission_snapshot_contains_complete_loaded_model() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    snapshot = mission_snapshot_to_dict(model, DEMO_MISSION)

    assert snapshot["kind"] == SNAPSHOT_KIND
    assert snapshot["snapshot_version"] == SNAPSHOT_VERSION
    assert snapshot["orbitfabric_version"] == __version__
    assert snapshot["result"] == "loaded"
    assert snapshot["mission"] == {
        "id": "demo-3u",
        "name": "Demo 3U Spacecraft",
        "model_version": "0.1.0",
    }
    assert snapshot["source"]["mission_dir"] == str(DEMO_MISSION.resolve())
    assert snapshot["diagnostics"] == []
    assert snapshot["model"] == model.model_dump(mode="json", by_alias=True)


def test_mission_snapshot_serializes_core_field_aliases() -> None:
    snapshot = mission_snapshot_from_dir(DEMO_MISSION)

    assert snapshot["result"] == "loaded"
    assert "class" in snapshot["model"]["spacecraft"]
    assert "spacecraft_class" not in snapshot["model"]["spacecraft"]

    products = snapshot["model"]["data_products"]
    if products and products[0]["storage"] is not None:
        assert "class" in products[0]["storage"]


def test_mission_snapshot_declares_read_only_generic_boundaries() -> None:
    snapshot = mission_snapshot_from_dir(DEMO_MISSION)

    assert snapshot["boundaries"] == {
        "source_of_truth": "mission_model",
        "core_derived_report": True,
        "read_only": True,
        "contains_full_loaded_model": True,
        "contains_structured_diagnostics": True,
        "contains_yaml_ast": False,
        "contains_source_locations": False,
        "contains_plugin_api": False,
        "contains_studio_api": False,
        "contains_runtime_behavior": False,
        "contains_ground_behavior": False,
    }


def test_mission_snapshot_returns_structured_failure_without_partial_model(
    tmp_path: Path,
) -> None:
    mission_dir = tmp_path / "mission"
    mission_dir.mkdir()

    for source_file in DEMO_MISSION.glob("*.yaml"):
        if source_file.name == "telemetry.yaml":
            continue
        (mission_dir / source_file.name).write_text(
            source_file.read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    snapshot = mission_snapshot_from_dir(mission_dir)

    assert snapshot["kind"] == SNAPSHOT_KIND
    assert snapshot["snapshot_version"] == SNAPSHOT_VERSION
    assert snapshot["result"] == "failed"
    assert snapshot["mission"] is None
    assert snapshot["model"] is None
    assert snapshot["source"]["mission_dir"] == str(mission_dir.resolve())
    assert snapshot["diagnostics"]
    assert any(
        diagnostic["code"] == "OF-SYN-002"
        and diagnostic["file"] == "telemetry.yaml"
        for diagnostic in snapshot["diagnostics"]
    )


def test_mission_snapshot_preserves_structured_invalid_yaml_diagnostic(
    tmp_path: Path,
) -> None:
    mission_dir = tmp_path / "mission"
    mission_dir.mkdir()

    for source_file in DEMO_MISSION.glob("*.yaml"):
        content = source_file.read_text(encoding="utf-8")
        if source_file.name == "telemetry.yaml":
            content = "telemetry: [\n"
        (mission_dir / source_file.name).write_text(content, encoding="utf-8")

    snapshot = mission_snapshot_from_dir(mission_dir)

    assert snapshot["result"] == "failed"
    assert snapshot["model"] is None
    assert any(
        diagnostic["code"] == "OF-SYN-003"
        and diagnostic["file"] == "telemetry.yaml"
        for diagnostic in snapshot["diagnostics"]
    )


def test_write_mission_snapshot_writes_loaded_report_deterministically(
    tmp_path: Path,
) -> None:
    output_file = tmp_path / "mission_snapshot.json"

    written = write_mission_snapshot(DEMO_MISSION, output_file)

    assert written == output_file
    content = output_file.read_text(encoding="utf-8")
    assert content.endswith("\n")
    assert json.loads(content) == mission_snapshot_from_dir(DEMO_MISSION)


def test_write_mission_snapshot_writes_failure_report(tmp_path: Path) -> None:
    mission_dir = tmp_path / "missing-mission"
    output_file = tmp_path / "mission_snapshot.json"

    write_mission_snapshot(mission_dir, output_file)

    snapshot = json.loads(output_file.read_text(encoding="utf-8"))
    assert snapshot["result"] == "failed"
    assert snapshot["model"] is None
    assert snapshot["diagnostics"][0]["code"] == "OF-SYN-001"
