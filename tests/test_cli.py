from __future__ import annotations

from typer.testing import CliRunner

from orbitfabric.cli import app

runner = CliRunner()


def test_version() -> None:
    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert "orbitfabric 0.1.0" in result.output


def test_help() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Mission Data Fabric" in result.output


def test_lint_loads_demo_mission() -> None:
    result = runner.invoke(app, ["lint", "examples/demo-3u/mission"])

    assert result.exit_code == 0
    assert "OrbitFabric Mission Lint v0.1" in result.output
    assert "Mission: demo-3u" in result.output
    assert "No findings." in result.output
    assert "Result: PASSED" in result.output