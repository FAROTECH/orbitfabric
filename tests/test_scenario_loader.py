from __future__ import annotations

import shutil
from collections.abc import Callable
from pathlib import Path

import pytest
from typer.testing import CliRunner

from orbitfabric import __version__
from orbitfabric.cli import app
from orbitfabric.model.errors import MissionModelError
from orbitfabric.model.scenario_loader import ScenarioLoader

DEMO_SCENARIO = Path("examples/demo-3u/scenarios/battery_low_during_payload.yaml")
PAYLOAD_SCENARIO = Path("examples/demo-3u/scenarios/nominal_payload_acquisition.yaml")
DATA_FLOW_SCENARIO = Path("examples/demo-3u/scenarios/payload_data_flow_evidence.yaml")
runner = CliRunner()


def test_load_demo_scenario() -> None:
    loaded = ScenarioLoader().load(DEMO_SCENARIO)

    assert loaded.scenario.scenario.id == "battery_low_during_payload"
    assert loaded.mission_model.spacecraft.id == "demo-3u"
    assert loaded.scenario.initial_state.mode == "NOMINAL"
    assert len(loaded.scenario.steps) == 13


def test_load_payload_scenario() -> None:
    loaded = ScenarioLoader().load(PAYLOAD_SCENARIO)

    assert loaded.scenario.scenario.id == "nominal_payload_acquisition"
    assert len(loaded.scenario.steps) == 11


def test_load_data_flow_evidence_scenario() -> None:
    loaded = ScenarioLoader().load(DATA_FLOW_SCENARIO)

    assert loaded.scenario.scenario.id == "payload_data_flow_evidence"
    assert len(loaded.scenario.steps) == 12


def test_sim_cli_loads_demo_scenario() -> None:
    result = runner.invoke(app, ["sim", str(DEMO_SCENARIO)])

    assert result.exit_code == 0
    assert f"OrbitFabric Scenario Simulator {__version__}" in result.output
    assert "Scenario: battery_low_during_payload" in result.output
    assert "Mission: demo-3u" in result.output
    assert "Result: PASSED" in result.output


def test_scenario_loader_rejects_missing_file() -> None:
    with pytest.raises(MissionModelError) as exc_info:
        ScenarioLoader().load(Path("missing-scenario.yaml"))

    assert exc_info.value.diagnostics[0].code == "OF-SCN-000"


def test_validate_scenario_cli_loads_demo_scenario() -> None:
    result = runner.invoke(app, ["validate", "scenario", str(DEMO_SCENARIO)])

    assert result.exit_code == 0
    assert f"OrbitFabric Scenario Validation {__version__}" in result.output
    assert "Scenario: battery_low_during_payload" in result.output
    assert "Mission: demo-3u" in result.output
    assert "Initial mode: NOMINAL" in result.output
    assert "Steps: 13" in result.output
    assert "Result: PASSED" in result.output
    assert "Timeline:" not in result.output
    assert "COMMAND payload.start_acquisition" not in result.output


def test_validate_scenario_cli_loads_data_flow_evidence_scenario() -> None:
    result = runner.invoke(app, ["validate", "scenario", str(DATA_FLOW_SCENARIO)])

    assert result.exit_code == 0
    assert f"OrbitFabric Scenario Validation {__version__}" in result.output
    assert "Scenario: payload_data_flow_evidence" in result.output
    assert "Mission: demo-3u" in result.output
    assert "Steps: 12" in result.output
    assert "Result: PASSED" in result.output
    assert "Timeline:" not in result.output


def test_validate_scenario_cli_rejects_unknown_command(tmp_path: Path) -> None:
    scenario_path = _copy_demo_scenario_with_replacement(
        tmp_path,
        "command: payload.start_acquisition",
        "command: payload.unknown_command",
    )

    result = runner.invoke(app, ["validate", "scenario", str(scenario_path)])

    assert result.exit_code == 1
    assert "OF-SCN-001" in result.output
    assert "unknown command" in result.output
    assert "Suggestion: Use a command defined in commands.yaml." in result.output
    assert "Result: FAILED" in result.output


@pytest.mark.parametrize(
    ("mutate", "expected_code"),
    [
        (
            lambda text: text.replace(
                "expect_event: payload.acquisition_started",
                "expect_event: payload.unknown_event",
                1,
            ),
            "OF-SCN-002",
        ),
        (
            lambda text: text.replace(
                "expect_mode: PAYLOAD_ACTIVE",
                "expect_mode: UNKNOWN_MODE",
                1,
            ),
            "OF-SCN-003",
        ),
        (
            lambda text: text.replace(
                "telemetry: eps.battery.voltage",
                "telemetry: eps.battery.unknown",
                1,
            ),
            "OF-SCN-004",
        ),
        (
            lambda text: text.replace(
                "  - t: 31",
                "  - t: 29",
                1,
            ),
            "OF-SCN-005",
        ),
        (
            lambda text: text.replace(
                "  mode: NOMINAL",
                "  mode: UNKNOWN_MODE",
                1,
            ),
            "OF-SCN-006",
        ),
        (
            lambda text: text.replace(
                "    obc.mode: NOMINAL",
                "    obc.unknown: NOMINAL",
                1,
            ),
            "OF-SCN-007",
        ),
    ],
)
def test_scenario_loader_rejects_invalid_references(
    tmp_path: Path,
    mutate: Callable[[str], str],
    expected_code: str,
) -> None:
    scenario_path = _copy_demo_scenario_with_mutation(tmp_path, mutate)

    with pytest.raises(MissionModelError) as exc_info:
        ScenarioLoader().load(scenario_path)

    codes = {diagnostic.code for diagnostic in exc_info.value.diagnostics}

    assert expected_code in codes
    assert any(diagnostic.suggestion for diagnostic in exc_info.value.diagnostics)


@pytest.mark.parametrize(
    ("old", "new", "expected_code"),
    [
        (
            "data_product: payload.radiation_histogram",
            "data_product: payload.unknown_product",
            "OF-SCN-014",
        ),
        (
            "triggered_by_command: payload.start_acquisition",
            "triggered_by_command: payload.unknown_command",
            "OF-SCN-015",
        ),
        (
            "eligible_downlink_flow: science_next_available_contact",
            "eligible_downlink_flow: unknown_flow",
            "OF-SCN-016",
        ),
        (
            "contact_window: demo_contact_001",
            "contact_window: unknown_contact_window",
            "OF-SCN-017",
        ),
    ],
)
def test_scenario_loader_rejects_invalid_data_flow_references(
    tmp_path: Path,
    old: str,
    new: str,
    expected_code: str,
) -> None:
    scenario_path = _copy_data_flow_scenario_with_replacement(tmp_path, old, new)

    with pytest.raises(MissionModelError) as exc_info:
        ScenarioLoader().load(scenario_path)

    codes = {diagnostic.code for diagnostic in exc_info.value.diagnostics}

    assert expected_code in codes
    assert any(diagnostic.suggestion for diagnostic in exc_info.value.diagnostics)


def test_scenario_loader_rejects_missing_required_top_level_key(tmp_path: Path) -> None:
    scenario_path = tmp_path / "missing-steps.yaml"
    scenario_path.write_text(
        """scenario:
  id: missing_steps
  name: Missing steps
mission:
  path: ../mission
initial_state:
  mode: NOMINAL
""",
        encoding="utf-8",
    )

    with pytest.raises(MissionModelError) as exc_info:
        ScenarioLoader().load(scenario_path)

    assert exc_info.value.diagnostics[0].code == "OF-SCN-011"

    assert exc_info.value.diagnostics[0].suggestion == (
        "Add the required scenario top-level key 'steps'."
    )


def test_scenario_loader_rejects_unexpected_top_level_key(tmp_path: Path) -> None:
    scenario_path = tmp_path / "unexpected-key.yaml"
    scenario_path.write_text(
        """scenario:
  id: unexpected_key
  name: Unexpected key
mission:
  path: ../mission
initial_state:
  mode: NOMINAL
steps: []
unexpected: true
""",
        encoding="utf-8",
    )

    with pytest.raises(MissionModelError) as exc_info:
        ScenarioLoader().load(scenario_path)

    assert exc_info.value.diagnostics[0].code == "OF-SCN-012"

    assert exc_info.value.diagnostics[0].suggestion == (
        "Remove or rename the unexpected scenario top-level key 'unexpected'."
    )


def _copy_demo_scenario_with_replacement(
    tmp_path: Path,
    old: str,
    new: str,
) -> Path:
    return _copy_demo_scenario_with_mutation(
        tmp_path,
        lambda text: text.replace(old, new, 1),
    )


def _copy_demo_scenario_with_mutation(
    tmp_path: Path,
    mutate: Callable[[str], str],
) -> Path:
    source = Path("examples/demo-3u")
    demo_dir = tmp_path / "demo-3u"
    shutil.copytree(source, demo_dir)

    scenario_path = demo_dir / "scenarios" / "battery_low_during_payload.yaml"
    scenario = scenario_path.read_text(encoding="utf-8")
    scenario_path.write_text(mutate(scenario), encoding="utf-8")

    return scenario_path


def _copy_data_flow_scenario_with_replacement(
    tmp_path: Path,
    old: str,
    new: str,
) -> Path:
    source = Path("examples/demo-3u")
    demo_dir = tmp_path / "demo-3u"
    shutil.copytree(source, demo_dir)

    scenario_path = demo_dir / "scenarios" / "payload_data_flow_evidence.yaml"
    scenario = scenario_path.read_text(encoding="utf-8")
    scenario_path.write_text(scenario.replace(old, new, 1), encoding="utf-8")

    return scenario_path
