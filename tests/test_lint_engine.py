from __future__ import annotations

from pathlib import Path

from orbitfabric.lint.engine import LintEngine
from orbitfabric.model.loader import MissionModelLoader

DEMO_MISSION = Path("examples/demo-3u/mission")


def test_demo_mission_has_no_semantic_lint_findings() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    report = LintEngine().run(model)

    assert report.error_count == 0
    assert report.warning_count == 0
    assert report.info_count == 0
    assert report.result_label == "PASSED"


def test_unknown_telemetry_source_is_reported() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    model.telemetry[0].source = "missing_subsystem"

    report = LintEngine().run(model)

    codes = {finding.code for finding in report.findings}
    assert "OF-REF-001" in codes
    assert report.has_errors


def test_unknown_command_emitted_event_is_reported() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    model.commands[0].emits.append("missing.event")

    report = LintEngine().run(model)

    codes = {finding.code for finding in report.findings}
    assert "OF-REF-006" in codes
    assert report.has_errors


def test_missing_initial_mode_is_reported() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    for mode in model.modes.values():
        mode.initial = False

    report = LintEngine().run(model)

    codes = {finding.code for finding in report.findings}
    assert "OF-MODE-001" in codes
    assert report.has_errors