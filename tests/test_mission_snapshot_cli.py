from __future__ import annotations

import json
import shutil
from pathlib import Path

from typer.testing import CliRunner

from orbitfabric import __version__
from orbitfabric.cli import app

runner = CliRunner()
DEMO_MISSION = Path("examples/demo-3u/mission")


def test_export_mission_snapshot_writes_loaded_envelope(tmp_path: Path) -> None:
    output_file = tmp_path / "mission_snapshot.json"

    result = runner.invoke(
        app,
        [
            "export",
            "mission-snapshot",
            str(DEMO_MISSION),
            "--json",
            str(output_file),
        ],
    )

    assert result.exit_code == 0
    assert f"OrbitFabric Mission Snapshot Export {__version__}" in result.output
    assert "Mission: demo-3u" in result.output
    assert "Model version: 0.1.0" in result.output
    assert f"JSON report written to: {output_file}" in result.output
    assert "Result: PASSED" in result.output

    payload = json.loads(output_file.read_text(encoding="utf-8"))
    assert payload["kind"] == "orbitfabric.mission_snapshot"
    assert payload["result"] == "loaded"
    assert payload["mission"]["id"] == "demo-3u"
    assert payload["model"]["spacecraft"]["id"] == "demo-3u"


def test_export_mission_snapshot_writes_failed_envelope_and_exits_nonzero(
    tmp_path: Path,
) -> None:
    mission_dir = tmp_path / "mission"
    shutil.copytree(DEMO_MISSION, mission_dir)
    (mission_dir / "telemetry.yaml").unlink()

    output_file = tmp_path / "mission_snapshot.json"
    result = runner.invoke(
        app,
        [
            "export",
            "mission-snapshot",
            str(mission_dir),
            "--json",
            str(output_file),
        ],
    )

    assert result.exit_code == 1
    assert "OF-SYN-002" in result.output
    assert "required Mission Model file is missing" in result.output
    assert f"JSON report written to: {output_file}" in result.output
    assert "Result: FAILED" in result.output

    payload = json.loads(output_file.read_text(encoding="utf-8"))
    assert payload["kind"] == "orbitfabric.mission_snapshot"
    assert payload["result"] == "failed"
    assert payload["mission"] is None
    assert payload["model"] is None
    assert payload["diagnostics"]
    assert payload["diagnostics"][0]["code"] == "OF-SYN-002"
