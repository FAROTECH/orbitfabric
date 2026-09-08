from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from orbitfabric import __version__
from orbitfabric.entrypoint import app

runner = CliRunner()
BATTERY_SCENARIO = Path("examples/demo-3u/scenarios/battery_low_during_payload.yaml")


def test_export_scenario_declaration_writes_loaded_candidate_surface(tmp_path: Path) -> None:
    output_file = tmp_path / "scenario_declaration.json"

    result = runner.invoke(
        app,
        [
            "export",
            "scenario-declaration",
            str(BATTERY_SCENARIO),
            "--json",
            str(output_file),
        ],
    )

    assert result.exit_code == 0, result.output
    assert f"OrbitFabric Scenario Declaration Export {__version__}" in result.output
    assert "Scenario: battery_low_during_payload" in result.output
    assert "Mission: demo-3u" in result.output
    assert "Declared atoms:" in result.output
    assert "Status: candidate" in result.output
    assert f"JSON report written to: {output_file}" in result.output
    assert "Result: PASSED" in result.output

    payload = json.loads(output_file.read_text(encoding="utf-8"))
    assert payload["kind"] == "orbitfabric.scenario_declaration"
    assert payload["declaration_version"] == "0.1-candidate"
    assert payload["result"] == "loaded"
    assert payload["scenario"]["id"] == "battery_low_during_payload"
    assert payload["atoms"]


def test_export_scenario_declaration_writes_failure_before_nonzero_exit(tmp_path: Path) -> None:
    scenario_file = tmp_path / "missing-scenario.yaml"
    output_file = tmp_path / "scenario_declaration.json"

    result = runner.invoke(
        app,
        [
            "export",
            "scenario-declaration",
            str(scenario_file),
            "--json",
            str(output_file),
        ],
    )

    assert result.exit_code == 1
    assert "OF-SCN-000" in result.output
    assert f"JSON report written to: {output_file}" in result.output
    assert "Result: FAILED" in result.output

    payload = json.loads(output_file.read_text(encoding="utf-8"))
    assert payload["kind"] == "orbitfabric.scenario_declaration"
    assert payload["result"] == "failed"
    assert payload["scenario"] is None
    assert payload["mission"] is None
    assert payload["atoms"] is None
    assert payload["diagnostics"][0]["code"] == "OF-SCN-000"
