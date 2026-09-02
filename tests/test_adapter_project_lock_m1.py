from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from orbitfabric.adapter_manager import ProjectLockService
from orbitfabric.adapter_manager.inventory import InstalledAdapterInventory
from orbitfabric.adapter_manager.models import AdapterSourceCoordinate, InstalledAdapterRecord
from orbitfabric.conformance.adapter_project_lock import (
    AdapterProjectLockContractError,
    load_project_lock,
)
from orbitfabric.entrypoint import app

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "conformance" / "fixtures" / "adapter-project-lock"
VALID = FIXTURES / "valid" / "basic.json"
DUPLICATE = FIXTURES / "invalid" / "duplicate-source-coordinate.json"
BAD_DIGEST = FIXTURES / "invalid" / "bad-artifact-digest.json"

DESCRIPTOR_SHA = "1" * 64
ARTIFACT_SHA = "2" * 64


def _source() -> AdapterSourceCoordinate:
    return AdapterSourceCoordinate(
        authority="test.local",
        publisher="fixture",
        name="adapter-a",
    )


def _record(
    tmp_path: Path,
    instance_id: str,
    *,
    release_version: str = "1.0.0",
    descriptor_sha: str = DESCRIPTOR_SHA,
    artifact_id: str = "python-wheel",
    artifact_sha: str = ARTIFACT_SHA,
    backend_id: str = "python-wheel-managed-env",
) -> InstalledAdapterRecord:
    root = tmp_path / instance_id
    return InstalledAdapterRecord(
        instance_id=instance_id,
        source_coordinate=_source(),
        release_version=release_version,
        release_descriptor_path=root / "release_descriptor.json",
        release_descriptor_sha256=descriptor_sha,
        artifact_id=artifact_id,
        artifact_sha256=artifact_sha,
        backend_id=backend_id,
        install_root=root,
        manifest_path=root / "integration_package.json",
        manifest_sha256="3" * 64,
        execution_argv_prefix=[str(root / "adapter")],
        acceptance_policy="fixture",
        acceptance_warnings=[],
    )


def _write_lock(tmp_path: Path, payload: dict) -> Path:
    path = tmp_path / "adapter-lock.json"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def test_project_lock_contract_accepts_valid_fixture() -> None:
    payload = load_project_lock(VALID)
    assert payload["kind"] == "orbitfabric.adapter_project_lock"
    assert payload["lock_version"] == "0.1-candidate"
    assert len(payload["adapters"]) == 1


def test_project_lock_contract_rejects_duplicate_source_coordinate() -> None:
    with pytest.raises(AdapterProjectLockContractError, match="Source Coordinates must be unique"):
        load_project_lock(DUPLICATE)


def test_project_lock_contract_rejects_invalid_digest() -> None:
    with pytest.raises(AdapterProjectLockContractError, match="not-a-sha256"):
        load_project_lock(BAD_DIGEST)


def test_project_lock_check_reports_match(tmp_path: Path) -> None:
    report = ProjectLockService().check(VALID, [_record(tmp_path, "exact")])

    assert report.status == "MATCH"
    assert report.passed
    assert report.adapters[0].status == "MATCH"
    assert report.adapters[0].matching_instance_ids == ["exact"]


def test_project_lock_check_reports_missing(tmp_path: Path) -> None:
    report = ProjectLockService().check(VALID, [])

    assert report.status == "NOT_SATISFIED"
    assert not report.passed
    assert report.adapters[0].status == "MISSING"
    assert report.adapters[0].candidate_instance_ids == []


def test_project_lock_check_reports_mismatch_dimensions(tmp_path: Path) -> None:
    candidate = _record(
        tmp_path,
        "different",
        release_version="0.9.0",
        descriptor_sha="4" * 64,
        artifact_id="other-artifact",
        artifact_sha="5" * 64,
        backend_id="other-backend",
    )

    report = ProjectLockService().check(VALID, [candidate])

    assert report.status == "NOT_SATISFIED"
    adapter = report.adapters[0]
    assert adapter.status == "MISMATCH"
    assert adapter.candidate_instance_ids == ["different"]
    assert adapter.candidate_mismatches[0].dimensions == [
        "release_version",
        "release_descriptor_sha256",
        "artifact_id",
        "artifact_sha256",
        "backend_id",
    ]


def test_extra_installed_version_does_not_break_exact_match(tmp_path: Path) -> None:
    records = [
        _record(tmp_path, "old", release_version="0.9.0"),
        _record(tmp_path, "exact"),
    ]

    report = ProjectLockService().check(VALID, records)

    adapter = report.adapters[0]
    assert report.status == "MATCH"
    assert adapter.status == "MATCH"
    assert adapter.matching_instance_ids == ["exact"]
    assert adapter.candidate_instance_ids == ["exact", "old"]


def test_multiple_exact_instances_still_satisfy_project(tmp_path: Path) -> None:
    records = [
        _record(tmp_path, "exact-b"),
        _record(tmp_path, "exact-a"),
    ]

    report = ProjectLockService().check(VALID, records)

    assert report.status == "MATCH"
    assert report.adapters[0].matching_instance_ids == ["exact-a", "exact-b"]


def test_project_lock_with_multiple_sources_reports_independently(tmp_path: Path) -> None:
    payload = json.loads(VALID.read_text(encoding="utf-8"))
    second = json.loads(json.dumps(payload["adapters"][0]))
    second["source_coordinate"]["name"] = "adapter-b"
    second["release_version"] = "2.0.0"
    second["release_descriptor"]["sha256"] = "6" * 64
    second["artifact"]["sha256"] = "7" * 64
    payload["adapters"].append(second)
    lock_path = _write_lock(tmp_path, payload)

    report = ProjectLockService().check(lock_path, [_record(tmp_path, "adapter-a")])

    assert report.status == "NOT_SATISFIED"
    assert [entry.status for entry in report.adapters] == ["MATCH", "MISSING"]


def test_project_lock_cli_validate_and_check_json(tmp_path: Path) -> None:
    state_root = tmp_path / "state"
    inventory = InstalledAdapterInventory(state_root)
    inventory.add(_record(tmp_path, "exact"))
    runner = CliRunner()
    env = {"ORBITFABRIC_STATE_DIR": str(state_root)}

    validate_result = runner.invoke(
        app,
        ["adapter", "lock", "validate", str(VALID), "--json"],
        env=env,
    )
    assert validate_result.exit_code == 0
    assert json.loads(validate_result.stdout)["lock_version"] == "0.1-candidate"

    check_result = runner.invoke(
        app,
        ["adapter", "lock", "check", str(VALID), "--json"],
        env=env,
    )
    assert check_result.exit_code == 0
    payload = json.loads(check_result.stdout)
    assert payload["status"] == "MATCH"
    assert payload["adapters"][0]["matching_instance_ids"] == ["exact"]


def test_project_lock_cli_human_output_and_unsatisfied_exit(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        app,
        ["adapter", "lock", "check", str(VALID)],
        env={"ORBITFABRIC_STATE_DIR": str(tmp_path / "empty-state")},
    )

    assert result.exit_code == 1
    assert "test.local:fixture/adapter-a@1.0.0: MISSING" in result.stdout
    assert "Project state: NOT_SATISFIED" in result.stdout
