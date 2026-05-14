from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from orbitfabric import __version__
from orbitfabric.cli import app

runner = CliRunner()


def test_export_entity_index_writes_json_report(tmp_path: Path) -> None:
    output_file = tmp_path / "entity_index.json"

    result = runner.invoke(
        app,
        [
            "export",
            "entity-index",
            "examples/demo-3u/mission",
            "--json",
            str(output_file),
        ],
    )

    assert result.exit_code == 0
    assert f"OrbitFabric Entity Index Export {__version__}" in result.output
    assert "Mission: demo-3u" in result.output
    assert "Model version: 0.1.0" in result.output
    assert f"JSON report written to: {output_file}" in result.output
    assert "Result: PASSED" in result.output
    assert output_file.exists()

    index = json.loads(output_file.read_text(encoding="utf-8"))
    assert index["kind"] == "orbitfabric.entity_index"
    assert index["mission"]["id"] == "demo-3u"
    assert index["counts"]["total_entities"] == len(index["entities"])
    assert index["counts"]["domains"]["commands"] == 4
    assert index["counts"]["domains"]["mode_transitions"] == 0
    assert index["counts"]["domains"]["policies"] == 0
    assert index["boundaries"]["contains_entity_index"] is True
    assert index["boundaries"]["contains_entity_records"] is True
    assert index["boundaries"]["contains_relationship_manifest"] is False
    assert index["boundaries"]["contains_plugin_api"] is False


def test_export_entity_index_rejects_invalid_mission(tmp_path: Path) -> None:
    mission_dir = tmp_path / "mission"
    mission_dir.mkdir()
    output_file = tmp_path / "entity_index.json"

    result = runner.invoke(
        app,
        [
            "export",
            "entity-index",
            str(mission_dir),
            "--json",
            str(output_file),
        ],
    )

    assert result.exit_code == 1
    assert "OF-SYN-002" in result.output
    assert "required Mission Model file is missing" in result.output
    assert "Result: FAILED" in result.output
    assert not output_file.exists()
