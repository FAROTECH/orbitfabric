from __future__ import annotations

from pathlib import Path

import pytest

from orbitfabric.model.errors import MissionModelError
from orbitfabric.model.loader import MissionModelLoader

DEMO_MISSION = Path("examples/demo-3u/mission")


def test_load_demo_mission() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    assert model.spacecraft.id == "demo-3u"
    assert model.spacecraft.model_version == "0.1.0"
    assert len(model.subsystems) == 4
    assert len(model.modes) == 6
    assert len(model.telemetry) >= 5
    assert len(model.commands) >= 4
    assert len(model.events) >= 8
    assert len(model.faults) == 2
    assert len(model.packets) >= 3


def test_load_demo_payload_contract() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    assert len(model.payloads) == 1
    payload = model.payloads[0]

    assert payload.id == "demo_iod_payload"
    assert payload.subsystem == "payload"
    assert payload.profile == "iod"
    assert payload.lifecycle.initial_state == "READY"
    assert payload.lifecycle.states == ["OFF", "READY", "ACQUIRING", "FAULT"]
    assert payload.telemetry.produced == ["payload.acquisition.active"]
    assert payload.commands.accepted == [
        "payload.start_acquisition",
        "payload.stop_acquisition",
    ]
    assert payload.events.generated == [
        "payload.acquisition_started",
        "payload.acquisition_stopped",
    ]
    assert payload.faults.possible == []


def test_optional_payloads_file_can_be_absent(tmp_path: Path) -> None:
    mission_dir = tmp_path / "mission"
    mission_dir.mkdir()

    for source_file in DEMO_MISSION.glob("*.yaml"):
        if source_file.name == "payloads.yaml":
            continue
        (mission_dir / source_file.name).write_text(
            source_file.read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    model = MissionModelLoader().load(mission_dir)

    assert model.payloads == []


def test_invalid_payloads_top_level_key_fails(tmp_path: Path) -> None:
    mission_dir = tmp_path / "mission"
    mission_dir.mkdir()

    for source_file in DEMO_MISSION.glob("*.yaml"):
        (mission_dir / source_file.name).write_text(
            source_file.read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    (mission_dir / "payloads.yaml").write_text(
        "payload_contracts: []\n",
        encoding="utf-8",
    )

    with pytest.raises(MissionModelError) as exc_info:
        MissionModelLoader().load(mission_dir)

    codes = {diagnostic.code for diagnostic in exc_info.value.diagnostics}
    assert "OF-STR-001" in codes
    assert "OF-STR-002" in codes


def test_missing_mission_directory_fails() -> None:
    with pytest.raises(MissionModelError) as exc_info:
        MissionModelLoader().load(Path("does-not-exist"))

    assert exc_info.value.diagnostics[0].code == "OF-SYN-001"

    assert exc_info.value.diagnostics[0].suggestion == (
        "Pass an existing Mission Model directory."
    )


def test_missing_required_file_fails(tmp_path: Path) -> None:
    mission_dir = tmp_path / "mission"
    mission_dir.mkdir()

    with pytest.raises(MissionModelError) as exc_info:
        MissionModelLoader().load(mission_dir)

    codes = {diagnostic.code for diagnostic in exc_info.value.diagnostics}
    assert "OF-SYN-002" in codes

    suggestions = {
        diagnostic.suggestion
        for diagnostic in exc_info.value.diagnostics
        if diagnostic.code == "OF-SYN-002"
    }

    assert suggestions
    assert all(suggestion is not None for suggestion in suggestions)