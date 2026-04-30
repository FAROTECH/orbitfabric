from __future__ import annotations

from pathlib import Path

from orbitfabric.lint.engine import LintEngine
from orbitfabric.model.loader import MissionModelLoader

DEMO_MISSION = Path("examples/demo-3u/mission")


def _codes_for_demo_model() -> tuple[set[str], object]:
    model = MissionModelLoader().load(DEMO_MISSION)
    report = LintEngine().run(model)
    return {finding.code for finding in report.findings}, model


def test_demo_mission_still_has_no_findings() -> None:
    codes, _model = _codes_for_demo_model()

    assert codes == set()


def test_high_criticality_numeric_telemetry_without_limits_is_reported() -> None:
    _codes, model = _codes_for_demo_model()
    telemetry = next(item for item in model.telemetry if item.id == "eps.battery.voltage")
    telemetry.limits = None

    report = LintEngine().run(model)

    assert "OF-TLM-001" in {finding.code for finding in report.findings}
    assert report.has_errors


def test_enum_telemetry_without_enum_values_is_reported() -> None:
    _codes, model = _codes_for_demo_model()
    telemetry = next(item for item in model.telemetry if item.id == "obc.mode")
    telemetry.enum = None

    report = LintEngine().run(model)

    assert "OF-TLM-006" in {finding.code for finding in report.findings}
    assert report.has_errors


def test_telemetry_without_quality_policy_is_reported_as_warning() -> None:
    _codes, model = _codes_for_demo_model()
    telemetry = next(item for item in model.telemetry if item.id == "eps.battery.current")
    telemetry.quality = None

    report = LintEngine().run(model)

    assert "OF-TLM-007" in {finding.code for finding in report.findings}
    assert report.warning_count == 1


def test_command_without_timeout_is_reported_as_warning() -> None:
    _codes, model = _codes_for_demo_model()
    command = next(item for item in model.commands if item.id == "payload.start_acquisition")
    command.timeout_ms = None

    report = LintEngine().run(model)

    assert "OF-CMD-005" in {finding.code for finding in report.findings}
    assert report.warning_count == 1


def test_risky_command_allowed_in_safe_mode_is_reported() -> None:
    _codes, model = _codes_for_demo_model()
    command = next(item for item in model.commands if item.id == "payload.start_acquisition")
    command.allowed_modes.append("SAFE")

    report = LintEngine().run(model)

    assert "OF-CMD-007" in {finding.code for finding in report.findings}
    assert report.has_errors


def test_event_without_downlink_priority_is_reported_as_warning() -> None:
    _codes, model = _codes_for_demo_model()
    event = next(item for item in model.events if item.id == "eps.battery_low")
    event.downlink_priority = None

    report = LintEngine().run(model)

    assert "OF-EVT-002" in {finding.code for finding in report.findings}
    assert report.warning_count == 1


def test_fault_without_emitted_event_is_reported() -> None:
    _codes, model = _codes_for_demo_model()
    fault = next(item for item in model.faults if item.id == "eps.battery_low_fault")
    fault.emits = []

    report = LintEngine().run(model)

    assert "OF-FLT-003" in {finding.code for finding in report.findings}
    assert report.has_errors


def test_empty_packet_is_reported() -> None:
    _codes, model = _codes_for_demo_model()
    packet = next(item for item in model.packets if item.id == "hk_fast")
    packet.telemetry = []

    report = LintEngine().run(model)

    assert "OF-PKT-002" in {finding.code for finding in report.findings}
    assert report.has_errors


def test_packet_with_non_positive_size_is_reported() -> None:
    _codes, model = _codes_for_demo_model()
    packet = next(item for item in model.packets if item.id == "hk_fast")
    packet.max_payload_bytes = 0

    report = LintEngine().run(model)

    assert "OF-PKT-003" in {finding.code for finding in report.findings}
    assert report.has_errors