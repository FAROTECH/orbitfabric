from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from orbitfabric import __version__
from orbitfabric.cli import app

runner = CliRunner()


def test_export_relationship_manifest_writes_candidate_json_report(tmp_path: Path) -> None:
    output_file = tmp_path / "relationship_manifest.json"

    result = runner.invoke(
        app,
        [
            "export",
            "relationship-manifest",
            "examples/demo-3u/mission",
            "--json",
            str(output_file),
        ],
    )

    assert result.exit_code == 0
    assert f"OrbitFabric Relationship Manifest Export {__version__}" in result.output
    assert "Mission: demo-3u" in result.output
    assert "Model version: 0.1.0" in result.output
    assert "Status: candidate" in result.output
    assert "Relationships emitted: 38" in result.output
    assert f"JSON report written to: {output_file}" in result.output
    assert "Result: PASSED" in result.output
    assert output_file.exists()

    manifest = json.loads(output_file.read_text(encoding="utf-8"))
    assert manifest["kind"] == "orbitfabric.relationship_manifest"
    assert manifest["manifest_version"] == "0.1-candidate"
    assert manifest["status"] == "candidate"
    assert manifest["mission"]["id"] == "demo-3u"
    assert manifest["counts"]["total_relationships"] == 38
    assert manifest["counts"]["relationship_types"] == {
        "command_emits_event": 4,
        "command_targets_subsystem": 4,
        "data_product_produced_by_payload": 1,
        "downlink_flow_includes_data_product": 1,
        "event_sourced_from_subsystem": 8,
        "fault_emits_event": 2,
        "fault_sourced_from_subsystem": 2,
        "packet_includes_telemetry": 5,
        "payload_accepts_command": 2,
        "payload_belongs_to_subsystem": 1,
        "payload_generates_event": 2,
        "payload_produces_telemetry": 1,
        "telemetry_sourced_from_subsystem": 5,
    }
    assert len(manifest["relationship_types"]) == 13
    assert len(manifest["relationships"]) == 38
    assert manifest["boundaries"]["contains_relationship_manifest"] is True
    assert manifest["boundaries"]["contains_relationship_graph"] is False
    assert manifest["boundaries"]["contains_plugin_api"] is False
    assert manifest["boundaries"]["contains_studio_api"] is False


def test_export_relationship_manifest_rejects_invalid_mission(tmp_path: Path) -> None:
    mission_dir = tmp_path / "mission"
    mission_dir.mkdir()
    output_file = tmp_path / "relationship_manifest.json"

    result = runner.invoke(
        app,
        [
            "export",
            "relationship-manifest",
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
