from __future__ import annotations

import json
import shutil
from pathlib import Path

from typer.testing import CliRunner

from orbitfabric import __version__
from orbitfabric.cli import app

runner = CliRunner()


def test_version() -> None:
    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert f"orbitfabric {__version__}" in result.output


def test_help() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Mission Data Fabric" in result.output


def test_lint_loads_demo_mission() -> None:
    result = runner.invoke(app, ["lint", "examples/demo-3u/mission"])

    assert result.exit_code == 0
    assert f"OrbitFabric Mission Lint {__version__}" in result.output
    assert "Mission: demo-3u" in result.output
    assert "No findings." in result.output
    assert "Result: PASSED" in result.output


def test_gen_docs_includes_data_flow_reference(tmp_path: Path) -> None:
    output_dir = tmp_path / "docs"

    result = runner.invoke(
        app,
        [
            "gen",
            "docs",
            "examples/demo-3u/mission",
            "--output-dir",
            str(output_dir),
        ],
    )

    assert result.exit_code == 0
    assert f"OrbitFabric Docs Generator {__version__}" in result.output
    assert "Mission: demo-3u" in result.output
    assert f"Output directory: {output_dir}" in result.output
    assert f"  {output_dir / 'data_flow.md'}" in result.output
    assert "Result: PASSED" in result.output

    data_flow_path = output_dir / "data_flow.md"
    assert data_flow_path.exists()

    content = data_flow_path.read_text(encoding="utf-8")
    assert "# Mission Data Flow Evidence Reference" in content
    assert "`payload.start_acquisition`" in content
    assert "`payload.radiation_histogram`" in content
    assert "`science_next_available_contact`" in content
    assert "`demo_contact_001`" in content


def test_gen_data_flow_docs_writes_markdown(tmp_path: Path) -> None:
    output_file = tmp_path / "data_flow.md"

    result = runner.invoke(
        app,
        [
            "gen",
            "data-flow",
            "examples/demo-3u/mission",
            "--output-file",
            str(output_file),
        ],
    )

    assert result.exit_code == 0
    assert f"OrbitFabric Data Flow Docs Generator {__version__}" in result.output
    assert "Mission: demo-3u" in result.output
    assert f"Generated file: {output_file}" in result.output
    assert "Result: PASSED" in result.output
    assert output_file.exists()

    content = output_file.read_text(encoding="utf-8")
    assert "# Mission Data Flow Evidence Reference" in content
    assert "`payload.start_acquisition`" in content
    assert "`payload.radiation_histogram`" in content
    assert "`science_next_available_contact`" in content
    assert "`demo_contact_001`" in content


def test_gen_runtime_writes_manifest(tmp_path: Path) -> None:
    output_dir = tmp_path / "runtime"

    result = runner.invoke(
        app,
        [
            "gen",
            "runtime",
            "examples/demo-3u/mission",
            "--output-dir",
            str(output_dir),
        ],
    )

    output_file = output_dir / "cpp17" / "runtime_contract_manifest.json"

    assert result.exit_code == 0
    assert f"OrbitFabric Runtime Generator {__version__}" in result.output
    assert "Mission: demo-3u" in result.output
    assert "Profile: cpp17" in result.output
    assert f"Generated file: {output_file}" in result.output
    assert "Runtime contract counts:" in result.output
    assert "Result: PASSED" in result.output
    assert output_file.exists()

    manifest = json.loads(output_file.read_text(encoding="utf-8"))
    assert manifest["kind"] == "orbitfabric.runtime_contract_manifest"
    assert manifest["generation"]["profile"] == "cpp17"
    assert manifest["generation"]["contains_flight_runtime"] is False
    assert manifest["contract"]["mission_id"] == "demo-3u"


def test_gen_runtime_rejects_unsupported_profile(tmp_path: Path) -> None:
    output_dir = tmp_path / "runtime"

    result = runner.invoke(
        app,
        [
            "gen",
            "runtime",
            "examples/demo-3u/mission",
            "--output-dir",
            str(output_dir),
            "--profile",
            "c99",
        ],
    )

    assert result.exit_code == 1
    assert "Unsupported runtime generation profile: c99" in result.output
    assert "Supported profiles: cpp17" in result.output
    assert not output_dir.exists()


def test_inspect_mission_loads_demo_mission() -> None:
    result = runner.invoke(app, ["inspect", "mission", "examples/demo-3u/mission"])

    assert result.exit_code == 0
    assert f"OrbitFabric Mission Inspection {__version__}" in result.output
    assert "Mission: demo-3u" in result.output
    assert "Model version: 0.1.0" in result.output
    assert "subsystems: 4" in result.output
    assert "modes: 6" in result.output
    assert "telemetry:" in result.output
    assert "commands:" in result.output
    assert "events:" in result.output
    assert "faults:" in result.output
    assert "packets:" in result.output
    assert "payloads:" in result.output
    assert "data products:" in result.output
    assert "Result: PASSED" in result.output
    assert "Findings:" not in result.output


def test_inspect_mission_rejects_invalid_mission(tmp_path: Path) -> None:
    mission_dir = _copy_demo_mission_missing_required_file(tmp_path)

    result = runner.invoke(app, ["inspect", "mission", str(mission_dir)])

    assert result.exit_code == 1
    assert "OF-SYN-002" in result.output
    assert "required Mission Model file is missing" in result.output
    assert "Result: FAILED" in result.output


def test_lint_with_warnings_passes_by_default(tmp_path: Path) -> None:
    mission_dir = _copy_demo_mission_with_warning(tmp_path)

    result = runner.invoke(app, ["lint", str(mission_dir)])

    assert result.exit_code == 0
    assert "OF-CMD-005" in result.output
    assert "warnings: 1" in result.output
    assert "Result: PASSED WITH WARNINGS" in result.output


def test_lint_with_warnings_as_errors_fails(tmp_path: Path) -> None:
    mission_dir = _copy_demo_mission_with_warning(tmp_path)

    result = runner.invoke(
        app,
        [
            "lint",
            str(mission_dir),
            "--warnings-as-errors",
        ],
    )

    assert result.exit_code == 1
    assert "OF-CMD-005" in result.output
    assert "warnings: 1" in result.output
    assert "Warnings are treated as errors." in result.output


def _copy_demo_mission_with_warning(tmp_path: Path) -> Path:
    source = Path("examples/demo-3u/mission")
    mission_dir = tmp_path / "mission"
    shutil.copytree(source, mission_dir)

    commands_path = mission_dir / "commands.yaml"
    commands = commands_path.read_text(encoding="utf-8")
    commands = commands.replace("    timeout_ms: 1000\n", "", 1)
    commands_path.write_text(commands, encoding="utf-8")

    return mission_dir


def _copy_demo_mission_missing_required_file(tmp_path: Path) -> Path:
    source = Path("examples/demo-3u/mission")
    mission_dir = tmp_path / "mission"
    shutil.copytree(source, mission_dir)

    (mission_dir / "telemetry.yaml").unlink()

    return mission_dir
