from __future__ import annotations

import json
import os
from hashlib import sha256
from pathlib import Path

import rfc8785
from typer.testing import CliRunner

from orbitfabric.entrypoint import app
from orbitfabric.export import integration_input_set as integration
from orbitfabric.lint.finding import LintFinding, LintReport

MISSION_DIR = Path("examples/demo-3u/mission")
runner = CliRunner()


def _load_manifest(output_dir: Path) -> dict:
    return json.loads((output_dir / integration.MANIFEST_FILENAME).read_text(encoding="utf-8"))


def _surface(manifest: dict, role: str) -> dict:
    return next(item for item in manifest["surfaces"] if item["role"] == role)


def _recompute_input_set_digest(manifest: dict) -> str:
    surfaces = []
    for record in sorted(manifest["surfaces"], key=lambda item: item["role"]):
        surfaces.append(
            {
                "role": record["role"],
                "requirement": record["requirement"],
                "status": record["status"],
                "kind": record["kind"],
                "format_version": record["format_version"],
                "sha256": record["sha256"],
                "unavailable_reason": record["unavailable_reason"],
            }
        )
    payload = {
        "kind": manifest["kind"],
        "input_set_version": manifest["input_set_version"],
        "orbitfabric_version": manifest["orbitfabric_version"],
        "mission": manifest["mission"],
        "load_result": manifest["load_result"],
        "lint_result": manifest["lint_result"],
        "surfaces": surfaces,
    }
    return sha256(rfc8785.dumps(payload)).hexdigest()


def test_successful_input_set_is_coherent_and_loads_once(tmp_path, monkeypatch) -> None:
    output_dir = tmp_path / "integration_input"
    load_calls = 0
    original_load = integration.MissionModelLoader.load

    def counted_load(self, mission_dir):
        nonlocal load_calls
        load_calls += 1
        return original_load(self, mission_dir)

    monkeypatch.setattr(integration.MissionModelLoader, "load", counted_load)

    result = integration.write_integration_input_set(MISSION_DIR, output_dir)
    manifest = _load_manifest(output_dir)

    assert result.succeeded
    assert load_calls == 1
    assert manifest["kind"] == "orbitfabric.integration_input_set"
    assert manifest["input_set_version"] == "0.1-candidate"
    assert manifest["load_result"] == "loaded"
    assert manifest["lint_result"] in {"passed", "passed_with_warnings"}
    assert [item["role"] for item in manifest["surfaces"]] == sorted(
        item["role"] for item in manifest["surfaces"]
    )

    for record in manifest["surfaces"]:
        assert record["status"] == "available"
        surface_path = output_dir / record["path"]
        assert surface_path.is_file()
        assert sha256(surface_path.read_bytes()).hexdigest() == record["sha256"]

    assert manifest["input_set_sha256"] == _recompute_input_set_digest(manifest)


def test_structural_load_failure_writes_failed_snapshot_and_manifest(tmp_path) -> None:
    mission_dir = tmp_path / "invalid_mission"
    mission_dir.mkdir()
    output_dir = tmp_path / "integration_input"

    result = integration.write_integration_input_set(mission_dir, output_dir)
    manifest = _load_manifest(output_dir)

    assert not result.succeeded
    assert manifest["mission"] is None
    assert manifest["load_result"] == "failed"
    assert manifest["lint_result"] == "not_run"

    snapshot = _surface(manifest, "mission_snapshot")
    assert snapshot["status"] == "available"
    snapshot_payload = json.loads((output_dir / snapshot["path"]).read_text(encoding="utf-8"))
    assert snapshot_payload["result"] == "failed"
    assert snapshot_payload["model"] is None
    assert snapshot_payload["diagnostics"]

    for role in ("entity_index", "lint_report", "model_summary", "relationship_manifest"):
        record = _surface(manifest, role)
        assert record["status"] == "unavailable"
        assert record["unavailable_reason"] == "load_failed"
        assert record["path"] is None
        assert record["sha256"] is None


def test_lint_failure_preserves_all_surfaces_but_returns_failure(tmp_path, monkeypatch) -> None:
    output_dir = tmp_path / "integration_input"

    def failing_lint(self, model):
        return LintReport(
            mission_id=model.spacecraft.id,
            model_version=model.spacecraft.model_version,
            findings=[
                LintFinding(
                    severity="ERROR",
                    code="TEST-ERROR",
                    message="synthetic semantic lint failure",
                )
            ],
        )

    monkeypatch.setattr(integration.LintEngine, "run", failing_lint)

    result = integration.write_integration_input_set(MISSION_DIR, output_dir)
    manifest = _load_manifest(output_dir)

    assert not result.succeeded
    assert not result.generation_failed
    assert manifest["load_result"] == "loaded"
    assert manifest["lint_result"] == "failed"
    assert all(item["status"] == "available" for item in manifest["surfaces"])

    lint_record = _surface(manifest, "lint_report")
    lint_payload = json.loads((output_dir / lint_record["path"]).read_text(encoding="utf-8"))
    assert lint_payload["result"] == "failed"
    assert lint_payload["findings"][0]["code"] == "TEST-ERROR"


def test_required_surface_generation_failure_is_explicit(tmp_path, monkeypatch) -> None:
    output_dir = tmp_path / "integration_input"

    def fail_entity_index(model, mission_dir):
        raise RuntimeError("synthetic entity-index generation failure")

    monkeypatch.setattr(integration, "entity_index_to_dict", fail_entity_index)

    result = integration.write_integration_input_set(MISSION_DIR, output_dir)
    manifest = _load_manifest(output_dir)

    assert not result.succeeded
    assert result.generation_failed
    record = _surface(manifest, "entity_index")
    assert record["requirement"] == "required"
    assert record["status"] == "unavailable"
    assert record["unavailable_reason"] == "generation_failed"
    assert record["path"] is None
    assert not (output_dir / "entity_index.json").exists()


def test_interrupted_publication_cannot_leave_old_manifest(tmp_path, monkeypatch) -> None:
    output_dir = tmp_path / "integration_input"
    first = integration.write_integration_input_set(MISSION_DIR, output_dir)
    assert first.succeeded
    assert (output_dir / integration.MANIFEST_FILENAME).exists()

    original_replace = os.replace
    replace_calls = 0

    def interrupted_replace(source, target):
        nonlocal replace_calls
        replace_calls += 1
        if replace_calls == 1:
            raise OSError("synthetic publication interruption")
        return original_replace(source, target)

    monkeypatch.setattr(integration.os, "replace", interrupted_replace)

    try:
        integration.write_integration_input_set(MISSION_DIR, output_dir)
    except OSError as exc:
        assert "synthetic publication interruption" in str(exc)
    else:
        raise AssertionError("expected publication interruption")

    assert not (output_dir / integration.MANIFEST_FILENAME).exists()


def test_cli_exports_the_frozen_multifile_boundary(tmp_path) -> None:
    output_dir = tmp_path / "integration_input"
    result = runner.invoke(
        app,
        [
            "export",
            "integration-input-set",
            str(MISSION_DIR),
            "--output-dir",
            str(output_dir),
        ],
    )

    assert result.exit_code == 0, result.stdout
    assert "Load result: loaded" in result.stdout
    assert "Manifest:" in result.stdout
    assert "Result: PASSED" in result.stdout
    assert (output_dir / integration.MANIFEST_FILENAME).is_file()
