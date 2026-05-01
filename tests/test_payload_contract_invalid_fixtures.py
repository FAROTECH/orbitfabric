from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
import yaml

from orbitfabric.lint.engine import LintEngine
from orbitfabric.model.errors import MissionModelError
from orbitfabric.model.loader import MissionModelLoader

DEMO_MISSION = Path("examples/demo-3u/mission")
MissionMutator = Callable[[Path], None]


def test_valid_payload_fixture_passes() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    report = LintEngine().run(model)

    assert report.result_label == "PASSED"
    assert report.error_count == 0


@pytest.mark.parametrize(
    ("mutator", "expected_code"),
    [
        (lambda mission_dir: _set_payload_field(mission_dir, "subsystem", "missing"), "OF-PAY-001"),
        (lambda mission_dir: _set_payload_field(mission_dir, "subsystem", "eps"), "OF-PAY-002"),
        (lambda mission_dir: _remove_payload_initial_state(mission_dir), "OF-STR-003"),
        (
            lambda mission_dir: _set_payload_lifecycle_initial_state(
                mission_dir,
                "UNKNOWN",
            ),
            "OF-PAY-004",
        ),
        (
            lambda mission_dir: _append_payload_reference(
                mission_dir,
                "telemetry",
                "produced",
                "payload.unknown.telemetry",
            ),
            "OF-PAY-005",
        ),
        (
            lambda mission_dir: _append_payload_reference(
                mission_dir,
                "commands",
                "accepted",
                "payload.unknown_command",
            ),
            "OF-PAY-006",
        ),
        (
            lambda mission_dir: _append_payload_reference(
                mission_dir,
                "events",
                "generated",
                "payload.unknown_event",
            ),
            "OF-PAY-007",
        ),
        (
            lambda mission_dir: _append_payload_reference(
                mission_dir,
                "faults",
                "possible",
                "payload.unknown_fault",
            ),
            "OF-PAY-008",
        ),
        (
            lambda mission_dir: _set_payload_lifecycle_command_reference(
                mission_dir,
                "preconditions",
                "UNKNOWN",
            ),
            "OF-PAY-009",
        ),
        (
            lambda mission_dir: _set_payload_lifecycle_command_reference(
                mission_dir,
                "expected_effects",
                "UNKNOWN",
            ),
            "OF-PAY-010",
        ),
    ],
)
def test_invalid_payload_contract_fixture_fails_for_expected_reason(
    tmp_path: Path,
    mutator: MissionMutator,
    expected_code: str,
) -> None:
    mission_dir = _copy_demo_mission(tmp_path)
    mutator(mission_dir)

    if expected_code == "OF-STR-003":
        with pytest.raises(MissionModelError) as exc_info:
            MissionModelLoader().load(mission_dir)

        codes = {diagnostic.code for diagnostic in exc_info.value.diagnostics}
        assert expected_code in codes
        return

    model = MissionModelLoader().load(mission_dir)
    report = LintEngine().run(model)

    codes = {finding.code for finding in report.findings}
    assert expected_code in codes
    assert report.has_errors


def _copy_demo_mission(tmp_path: Path) -> Path:
    mission_dir = tmp_path / "mission"
    mission_dir.mkdir()

    for source_file in DEMO_MISSION.glob("*.yaml"):
        (mission_dir / source_file.name).write_text(
            source_file.read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    return mission_dir


def _read_yaml(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def _set_payload_field(mission_dir: Path, field: str, value: Any) -> None:
    payloads_path = mission_dir / "payloads.yaml"
    data = _read_yaml(payloads_path)
    data["payloads"][0][field] = value
    _write_yaml(payloads_path, data)


def _remove_payload_initial_state(mission_dir: Path) -> None:
    payloads_path = mission_dir / "payloads.yaml"
    data = _read_yaml(payloads_path)
    del data["payloads"][0]["lifecycle"]["initial_state"]
    _write_yaml(payloads_path, data)


def _set_payload_lifecycle_initial_state(mission_dir: Path, state: str) -> None:
    payloads_path = mission_dir / "payloads.yaml"
    data = _read_yaml(payloads_path)
    data["payloads"][0]["lifecycle"]["initial_state"] = state
    _write_yaml(payloads_path, data)


def _append_payload_reference(
    mission_dir: Path,
    group: str,
    field: str,
    value: str,
) -> None:
    payloads_path = mission_dir / "payloads.yaml"
    data = _read_yaml(payloads_path)
    data["payloads"][0][group][field].append(value)
    _write_yaml(payloads_path, data)


def _set_payload_lifecycle_command_reference(
    mission_dir: Path,
    container: str,
    state: str,
) -> None:
    commands_path = mission_dir / "commands.yaml"
    data = _read_yaml(commands_path)
    data["commands"][0][container]["payload_lifecycle"]["state"] = state
    _write_yaml(commands_path, data)
