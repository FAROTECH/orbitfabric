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


def test_payload_subsystem_reference_must_exist() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    model.payloads[0].subsystem = "missing_subsystem"

    report = LintEngine().run(model)

    codes = {finding.code for finding in report.findings}
    assert "OF-PAY-001" in codes
    assert report.has_errors


def test_payload_subsystem_type_must_be_payload() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    model.payloads[0].subsystem = "eps"

    report = LintEngine().run(model)

    codes = {finding.code for finding in report.findings}
    assert "OF-PAY-002" in codes
    assert report.has_errors


def test_payload_lifecycle_initial_state_must_exist_in_states() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    model.payloads[0].lifecycle.initial_state = "UNKNOWN"

    report = LintEngine().run(model)

    codes = {finding.code for finding in report.findings}
    assert "OF-PAY-004" in codes
    assert report.has_errors


def test_payload_telemetry_references_must_exist() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    model.payloads[0].telemetry.produced.append("payload.unknown.telemetry")

    report = LintEngine().run(model)

    codes = {finding.code for finding in report.findings}
    assert "OF-PAY-005" in codes
    assert report.has_errors


def test_payload_command_references_must_exist() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    model.payloads[0].commands.accepted.append("payload.unknown_command")

    report = LintEngine().run(model)

    codes = {finding.code for finding in report.findings}
    assert "OF-PAY-006" in codes
    assert report.has_errors


def test_payload_event_references_must_exist() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    model.payloads[0].events.generated.append("payload.unknown_event")

    report = LintEngine().run(model)

    codes = {finding.code for finding in report.findings}
    assert "OF-PAY-007" in codes
    assert report.has_errors


def test_payload_fault_references_must_exist() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    model.payloads[0].faults.possible.append("payload.unknown_fault")

    report = LintEngine().run(model)

    codes = {finding.code for finding in report.findings}
    assert "OF-PAY-008" in codes
    assert report.has_errors


def test_command_precondition_payload_lifecycle_state_must_exist() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    model.commands[0].preconditions = {
        "payload_lifecycle": {
            "payload": "demo_iod_payload",
            "state": "UNKNOWN",
        }
    }

    report = LintEngine().run(model)

    codes = {finding.code for finding in report.findings}
    assert "OF-PAY-009" in codes
    assert report.has_errors


def test_command_expected_effect_payload_lifecycle_state_must_exist() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    model.commands[0].expected_effects = {
        "payload_lifecycle": {
            "payload": "demo_iod_payload",
            "state": "UNKNOWN",
        }
    }

    report = LintEngine().run(model)

    codes = {finding.code for finding in report.findings}
    assert "OF-PAY-010" in codes
    assert report.has_errors