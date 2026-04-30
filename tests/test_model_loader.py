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


def test_missing_mission_directory_fails() -> None:
    with pytest.raises(MissionModelError) as exc_info:
        MissionModelLoader().load(Path("does-not-exist"))

    assert exc_info.value.diagnostics[0].code == "OF-SYN-001"


def test_missing_required_file_fails(tmp_path: Path) -> None:
    mission_dir = tmp_path / "mission"
    mission_dir.mkdir()

    with pytest.raises(MissionModelError) as exc_info:
        MissionModelLoader().load(mission_dir)

    codes = {diagnostic.code for diagnostic in exc_info.value.diagnostics}
    assert "OF-SYN-002" in codes