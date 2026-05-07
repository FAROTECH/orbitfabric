from __future__ import annotations

from pathlib import Path

from orbitfabric.lint.engine import LintEngine
from orbitfabric.model.loader import MissionModelLoader

DEMO_MISSION = Path("examples/demo-3u/mission")

VALID_COMMANDABILITY_YAML = """commandability:
  sources:
    - id: ground_operator
      type: ground
      requires_contact: true
      contact_profile: primary_ground_contact
      description: Abstract ground-originated command source.
    - id: onboard_autonomy
      type: autonomous
      requires_contact: false
      description: Abstract onboard autonomous command source.
  rules:
    - id: payload_start_ground_rule
      command: payload.start_acquisition
      sources:
        - ground_operator
      allowed_modes:
        - NOMINAL
      confirmation: required
      expected_events:
        - payload.acquisition_started
      description: Payload acquisition may be commanded from ground in nominal mode.
  autonomous_actions:
    - id: stop_payload_on_battery_warning
      trigger:
        fault: eps.battery_low_fault
      dispatches:
        command: payload.stop_acquisition
        source: onboard_autonomy
      expected_events:
        - payload.acquisition_stopped
      description: Contract-level autonomous recovery assumption for battery warning.
  recovery_intents:
    - id: payload_battery_warning_recovery
      fault: eps.battery_low_fault
      target_mode: DEGRADED
      commands:
        - payload.stop_acquisition
      expected_events:
        - payload.acquisition_stopped
      description: Declared recovery intent for payload activity during battery warning.
"""


def copy_demo_mission(tmp_path: Path) -> Path:
    mission_dir = tmp_path / "mission"
    mission_dir.mkdir()

    for source_file in DEMO_MISSION.glob("*.yaml"):
        (mission_dir / source_file.name).write_text(
            source_file.read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    return mission_dir


def load_model_with_commandability(tmp_path: Path, commandability_yaml: str):
    mission_dir = copy_demo_mission(tmp_path)
    (mission_dir / "commandability.yaml").write_text(commandability_yaml, encoding="utf-8")
    return MissionModelLoader().load(mission_dir)


def lint_codes(commandability_yaml: str, tmp_path: Path) -> set[str]:
    model = load_model_with_commandability(tmp_path, commandability_yaml)
    return {finding.code for finding in LintEngine().run(model).findings}


def test_valid_commandability_contract_has_no_commandability_findings(tmp_path: Path) -> None:
    model = load_model_with_commandability(tmp_path, VALID_COMMANDABILITY_YAML)
    report = LintEngine().run(model)

    commandability_codes = {
        finding.code
        for finding in report.findings
        if finding.file == "commandability.yaml"
    }

    assert commandability_codes == set()


def test_commandability_rule_unknown_command_is_reported(tmp_path: Path) -> None:
    mutated = VALID_COMMANDABILITY_YAML.replace(
        "command: payload.start_acquisition",
        "command: payload.unknown_command",
    )

    assert "OF-CAB-001" in lint_codes(mutated, tmp_path)


def test_commandability_rule_unknown_mode_is_reported(tmp_path: Path) -> None:
    mutated = VALID_COMMANDABILITY_YAML.replace("- NOMINAL", "- UNKNOWN_MODE", 1)

    assert "OF-CAB-002" in lint_codes(mutated, tmp_path)


def test_commandability_rule_unknown_source_is_reported(tmp_path: Path) -> None:
    mutated = VALID_COMMANDABILITY_YAML.replace("- ground_operator", "- missing_source", 1)

    assert "OF-CAB-003" in lint_codes(mutated, tmp_path)


def test_ground_source_requires_contact_without_profile_is_warning(tmp_path: Path) -> None:
    mutated = VALID_COMMANDABILITY_YAML.replace(
        "      contact_profile: primary_ground_contact\n",
        "",
        1,
    )

    assert "OF-CAB-004" in lint_codes(mutated, tmp_path)


def test_ground_source_unknown_contact_profile_is_reported(tmp_path: Path) -> None:
    mutated = VALID_COMMANDABILITY_YAML.replace(
        "contact_profile: primary_ground_contact",
        "contact_profile: missing_contact_profile",
    )

    assert "OF-CAB-005" in lint_codes(mutated, tmp_path)


def test_commandability_rule_unknown_expected_event_is_reported(tmp_path: Path) -> None:
    mutated = VALID_COMMANDABILITY_YAML.replace(
        "- payload.acquisition_started",
        "- payload.unknown_event",
        1,
    )

    assert "OF-CAB-006" in lint_codes(mutated, tmp_path)


def test_risky_command_without_required_confirmation_is_warning(tmp_path: Path) -> None:
    mutated = VALID_COMMANDABILITY_YAML.replace("confirmation: required", "confirmation: hinted")

    assert "OF-CAB-007" in lint_codes(mutated, tmp_path)


def test_autonomous_action_unknown_command_is_reported(tmp_path: Path) -> None:
    mutated = VALID_COMMANDABILITY_YAML.replace(
        "command: payload.stop_acquisition",
        "command: payload.unknown_stop",
    )

    assert "OF-AUT-001" in lint_codes(mutated, tmp_path)


def test_autonomous_action_unknown_source_is_reported(tmp_path: Path) -> None:
    mutated = VALID_COMMANDABILITY_YAML.replace(
        "source: onboard_autonomy",
        "source: missing_source",
    )

    assert "OF-AUT-002" in lint_codes(mutated, tmp_path)


def test_autonomous_action_unknown_trigger_is_reported(tmp_path: Path) -> None:
    mutated = VALID_COMMANDABILITY_YAML.replace(
        "fault: eps.battery_low_fault",
        "fault: eps.unknown_fault",
    )

    assert "OF-AUT-003" in lint_codes(mutated, tmp_path)


def test_autonomous_action_unknown_expected_event_is_reported(tmp_path: Path) -> None:
    mutated = VALID_COMMANDABILITY_YAML.replace(
        "- payload.acquisition_stopped",
        "- payload.unknown_stop_event",
        1,
    )

    assert "OF-AUT-004" in lint_codes(mutated, tmp_path)


def test_autonomous_action_without_expected_evidence_is_warning(tmp_path: Path) -> None:
    mutated = VALID_COMMANDABILITY_YAML.replace(
        "      expected_events:\n        - payload.acquisition_stopped\n",
        "",
        1,
    )

    assert "OF-AUT-005" in lint_codes(mutated, tmp_path)


def test_recovery_intent_unknown_command_is_reported(tmp_path: Path) -> None:
    mutated = VALID_COMMANDABILITY_YAML.replace(
        "- payload.stop_acquisition",
        "- payload.unknown_recovery_command",
        2,
    )

    assert "OF-REC-001" in lint_codes(mutated, tmp_path)


def test_recovery_intent_unknown_reference_is_reported(tmp_path: Path) -> None:
    mutated = VALID_COMMANDABILITY_YAML.replace(
        "fault: eps.battery_low_fault",
        "fault: eps.unknown_recovery_fault",
        2,
    )

    assert "OF-REC-002" in lint_codes(mutated, tmp_path)


def test_recovery_intent_unknown_expected_event_is_reported(tmp_path: Path) -> None:
    mutated = VALID_COMMANDABILITY_YAML.replace(
        "- payload.acquisition_stopped",
        "- payload.unknown_recovery_event",
        2,
    )

    assert "OF-REC-003" in lint_codes(mutated, tmp_path)
