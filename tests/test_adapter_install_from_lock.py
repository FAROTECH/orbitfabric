from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

import orbitfabric.adapter_commands as adapter_commands
from orbitfabric.adapter_manager import AdapterManager, ProjectLockInstallService
from orbitfabric.adapter_manager.errors import InstallationError, ProjectLockError, ReleaseResolutionError
from orbitfabric.adapter_manager.hashing import sha256_file
from orbitfabric.adapter_manager.models import (
    AdapterSourceCoordinate,
    BackendInstallReceipt,
    InstalledAdapterRecord,
    ResolvedAdapterRelease,
    VerificationDimension,
)
from orbitfabric.entrypoint import app

ROOT = Path(__file__).resolve().parents[1]
VALID = ROOT / "conformance" / "fixtures" / "integration-v1" / "valid"
MANIFEST_ZERO = VALID / "manifest-zero-input.json"
RESULT_ZERO = VALID / "result-zero-input.json"


class CountingInstallationBackend:
    backend_id = "fake-managed-backend"
    artifact_type = "test-artifact"

    def __init__(self) -> None:
        self.install_calls = 0
        self.result_payload = json.loads(RESULT_ZERO.read_text(encoding="utf-8"))

    def supports(self, release: ResolvedAdapterRelease) -> bool:
        return release.artifact.artifact_type == self.artifact_type

    def install(
        self,
        release: ResolvedAdapterRelease,
        instance_id: str,
        instances_root: Path,
    ) -> BackendInstallReceipt:
        self.install_calls += 1
        instance_root = instances_root / instance_id
        instance_root.mkdir(parents=True)
        manifest_path = instance_root / "integration_package.json"
        shutil.copyfile(MANIFEST_ZERO, manifest_path)
        runner = instance_root / "fake_adapter.py"
        runner.write_text(
            "import json\n"
            "from pathlib import Path\n"
            "import sys\n"
            f"PAYLOAD = {self.result_payload!r}\n"
            "args = sys.argv[1:]\n"
            "out = Path(args[args.index('--output-dir') + 1])\n"
            "out.mkdir(parents=True, exist_ok=True)\n"
            "(out / 'integration_result.json').write_text("
            "json.dumps(PAYLOAD, indent=2) + '\\n', encoding='utf-8')\n",
            encoding="utf-8",
        )
        return BackendInstallReceipt(
            backend_id=self.backend_id,
            install_root=instance_root,
            manifest_path=manifest_path,
            manifest_sha256=sha256_file(manifest_path),
            execution_argv_prefix=[sys.executable, str(runner)],
        )

    def verify(self, record: InstalledAdapterRecord) -> VerificationDimension:
        if Path(record.install_root).is_dir():
            return VerificationDimension(status="PASS")
        return VerificationDimension(status="FAIL", detail="fake install root missing")

    def remove(self, record: InstalledAdapterRecord) -> None:
        shutil.rmtree(record.install_root, ignore_errors=False)


class FailingInstallationBackend(CountingInstallationBackend):
    backend_id = "failing-backend"

    def install(
        self,
        release: ResolvedAdapterRelease,
        instance_id: str,
        instances_root: Path,
    ) -> BackendInstallReceipt:
        self.install_calls += 1
        raise InstallationError("intentional install-from-lock backend failure")


def _coordinate(name: str = "adapter") -> AdapterSourceCoordinate:
    return AdapterSourceCoordinate(
        authority="test.local",
        publisher="fixture",
        name=name,
    )


def _write_release(
    directory: Path,
    *,
    coordinate: AdapterSourceCoordinate | None = None,
    release_version: str = "1.0.0",
    artifact_bytes: bytes = b"exact adapter bytes",
) -> tuple[Path, Path]:
    directory.mkdir(parents=True, exist_ok=True)
    selected_coordinate = coordinate or _coordinate()
    artifact = directory / "adapter.bin"
    artifact.write_bytes(artifact_bytes)
    descriptor = {
        "kind": "orbitfabric.adapter_release",
        "descriptor_version": "0.1-candidate",
        "source_coordinate": selected_coordinate.model_dump(mode="json"),
        "release_version": release_version,
        "source_provenance": {"commit": "fixture"},
        "artifacts": [
            {
                "id": "fixture-artifact",
                "artifact_type": "test-artifact",
                "filename": artifact.name,
                "sha256": sha256_file(artifact),
                "size": artifact.stat().st_size,
                "selectors": {},
            }
        ],
        "integration_package": {"sha256": sha256_file(MANIFEST_ZERO)},
    }
    descriptor_path = directory / "release.json"
    descriptor_path.write_text(json.dumps(descriptor, indent=2) + "\n", encoding="utf-8")
    return descriptor_path, artifact


def _write_lock(
    path: Path,
    descriptor_path: Path,
    artifact_path: Path,
    *,
    coordinate: AdapterSourceCoordinate | None = None,
    release_version: str = "1.0.0",
    backend_id: str = "fake-managed-backend",
    descriptor_sha256: str | None = None,
    artifact_sha256: str | None = None,
) -> Path:
    payload = {
        "kind": "orbitfabric.adapter_project_lock",
        "lock_version": "0.1-candidate",
        "adapters": [
            {
                "source_coordinate": (coordinate or _coordinate()).model_dump(mode="json"),
                "release_version": release_version,
                "release_descriptor": {
                    "sha256": descriptor_sha256 or sha256_file(descriptor_path)
                },
                "artifact": {
                    "id": "fixture-artifact",
                    "sha256": artifact_sha256 or sha256_file(artifact_path),
                },
                "installation_backend": {"id": backend_id},
            }
        ],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def _manager(tmp_path: Path, backend: CountingInstallationBackend) -> AdapterManager:
    return AdapterManager(
        state_root=tmp_path / "state",
        backends=[backend],
    )


def test_missing_entry_installs_exact_release_and_becomes_match(tmp_path: Path) -> None:
    backend = CountingInstallationBackend()
    manager = _manager(tmp_path, backend)
    descriptor, artifact = _write_release(tmp_path / "release")
    lock = _write_lock(tmp_path / "adapter.lock.json", descriptor, artifact)

    report = ProjectLockInstallService(manager).install_entry(
        lock,
        _coordinate(),
        descriptor,
        artifact,
    )

    assert report.before_status == "MISSING"
    assert report.action == "INSTALLED"
    assert report.after_status == "MATCH"
    assert report.installed_instance_id is not None
    assert backend.install_calls == 1
    assert len(manager.list()) == 1


def test_exact_match_is_idempotent_noop(tmp_path: Path) -> None:
    backend = CountingInstallationBackend()
    manager = _manager(tmp_path, backend)
    descriptor, artifact = _write_release(tmp_path / "release")
    lock = _write_lock(tmp_path / "adapter.lock.json", descriptor, artifact)
    service = ProjectLockInstallService(manager)

    first = service.install_entry(lock, _coordinate(), descriptor, artifact)
    second = service.install_entry(lock, _coordinate(), descriptor, artifact)

    assert first.action == "INSTALLED"
    assert second.before_status == "MATCH"
    assert second.action == "NOOP"
    assert second.after_status == "MATCH"
    assert backend.install_calls == 1
    assert len(manager.list()) == 1


def test_mismatch_installs_exact_release_side_by_side(tmp_path: Path) -> None:
    backend = CountingInstallationBackend()
    manager = _manager(tmp_path, backend)
    old_descriptor, old_artifact = _write_release(
        tmp_path / "old",
        release_version="0.9.0",
        artifact_bytes=b"old adapter bytes",
    )
    manager.install(old_descriptor, old_artifact)

    descriptor, artifact = _write_release(
        tmp_path / "exact",
        release_version="1.0.0",
        artifact_bytes=b"exact adapter bytes",
    )
    lock = _write_lock(tmp_path / "adapter.lock.json", descriptor, artifact)

    report = ProjectLockInstallService(manager).install_entry(
        lock,
        _coordinate(),
        descriptor,
        artifact,
    )

    assert report.before_status == "MISMATCH"
    assert report.action == "INSTALLED"
    assert report.after_status == "MATCH"
    assert backend.install_calls == 2
    assert sorted(record.release_version for record in manager.list()) == ["0.9.0", "1.0.0"]


def test_wrong_locked_artifact_digest_fails_before_materialization(tmp_path: Path) -> None:
    backend = CountingInstallationBackend()
    manager = _manager(tmp_path, backend)
    descriptor, artifact = _write_release(tmp_path / "release")
    lock = _write_lock(
        tmp_path / "adapter.lock.json",
        descriptor,
        artifact,
        artifact_sha256="0" * 64,
    )

    with pytest.raises(ProjectLockError, match="artifact_sha256"):
        ProjectLockInstallService(manager).install_entry(
            lock,
            _coordinate(),
            descriptor,
            artifact,
        )

    assert backend.install_calls == 0
    assert manager.list() == []


def test_wrong_locked_descriptor_digest_fails_before_materialization(tmp_path: Path) -> None:
    backend = CountingInstallationBackend()
    manager = _manager(tmp_path, backend)
    descriptor, artifact = _write_release(tmp_path / "release")
    lock = _write_lock(
        tmp_path / "adapter.lock.json",
        descriptor,
        artifact,
        descriptor_sha256="0" * 64,
    )

    with pytest.raises(ReleaseResolutionError, match="Descriptor SHA-256"):
        ProjectLockInstallService(manager).install_entry(
            lock,
            _coordinate(),
            descriptor,
            artifact,
        )

    assert backend.install_calls == 0
    assert manager.list() == []


def test_wrong_source_coordinate_fails_before_materialization(tmp_path: Path) -> None:
    backend = CountingInstallationBackend()
    manager = _manager(tmp_path, backend)
    descriptor, artifact = _write_release(tmp_path / "release", coordinate=_coordinate("actual"))
    lock_coordinate = _coordinate("locked")
    lock = _write_lock(
        tmp_path / "adapter.lock.json",
        descriptor,
        artifact,
        coordinate=lock_coordinate,
    )

    with pytest.raises(ProjectLockError, match="source_coordinate"):
        ProjectLockInstallService(manager).install_entry(
            lock,
            lock_coordinate,
            descriptor,
            artifact,
        )

    assert backend.install_calls == 0
    assert manager.list() == []


def test_locked_backend_mismatch_fails_before_materialization(tmp_path: Path) -> None:
    backend = CountingInstallationBackend()
    manager = _manager(tmp_path, backend)
    descriptor, artifact = _write_release(tmp_path / "release")
    lock = _write_lock(
        tmp_path / "adapter.lock.json",
        descriptor,
        artifact,
        backend_id="different-backend",
    )

    with pytest.raises(InstallationError, match="expected backend id"):
        ProjectLockInstallService(manager).install_entry(
            lock,
            _coordinate(),
            descriptor,
            artifact,
        )

    assert backend.install_calls == 0
    assert manager.list() == []


def test_backend_failure_does_not_publish_inventory(tmp_path: Path) -> None:
    backend = FailingInstallationBackend()
    manager = _manager(tmp_path, backend)
    descriptor, artifact = _write_release(tmp_path / "release")
    lock = _write_lock(
        tmp_path / "adapter.lock.json",
        descriptor,
        artifact,
        backend_id=backend.backend_id,
    )

    with pytest.raises(InstallationError, match="intentional install-from-lock backend failure"):
        ProjectLockInstallService(manager).install_entry(
            lock,
            _coordinate(),
            descriptor,
            artifact,
        )

    assert backend.install_calls == 1
    assert manager.list() == []


def test_lock_install_cli_json_report(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    backend = CountingInstallationBackend()
    manager = _manager(tmp_path, backend)
    descriptor, artifact = _write_release(tmp_path / "release")
    lock = _write_lock(tmp_path / "adapter.lock.json", descriptor, artifact)
    monkeypatch.setattr(adapter_commands, "_manager", lambda: manager)

    result = CliRunner().invoke(
        app,
        [
            "adapter",
            "lock",
            "install",
            str(lock),
            "--source-coordinate",
            _coordinate().display(),
            "--release-descriptor",
            str(descriptor),
            "--artifact",
            str(artifact),
            "--json",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["before_status"] == "MISSING"
    assert payload["action"] == "INSTALLED"
    assert payload["after_status"] == "MATCH"
    assert backend.install_calls == 1
