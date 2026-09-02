from __future__ import annotations

import json
from pathlib import Path
import shutil
import sys

import pytest
from typer.testing import CliRunner

from orbitfabric.adapter_manager import AdapterManager
from orbitfabric.adapter_manager.errors import InstallationError, ReleaseResolutionError
from orbitfabric.adapter_manager.hashing import sha256_file
from orbitfabric.adapter_manager.models import (
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


class FakeInstallationBackend:
    backend_id = "fake-managed-backend"
    artifact_type = "test-artifact"

    def __init__(self, result_payload: dict) -> None:
        self.result_payload = result_payload

    def supports(self, release: ResolvedAdapterRelease) -> bool:
        return release.artifact.artifact_type == self.artifact_type

    def install(
        self,
        release: ResolvedAdapterRelease,
        instance_id: str,
        instances_root: Path,
    ) -> BackendInstallReceipt:
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


class FailingInstallationBackend(FakeInstallationBackend):
    backend_id = "failing-backend"

    def install(
        self,
        release: ResolvedAdapterRelease,
        instance_id: str,
        instances_root: Path,
    ) -> BackendInstallReceipt:
        raise InstallationError("intentional backend failure")


def _write_release(tmp_path: Path, *, artifact_sha256: str | None = None) -> tuple[Path, Path]:
    artifact = tmp_path / "adapter.bin"
    artifact.write_bytes(b"exact adapter bytes")
    digest = sha256_file(artifact)
    descriptor = {
        "kind": "orbitfabric.adapter_release",
        "descriptor_version": "0.1-candidate",
        "source_coordinate": {
            "authority": "test.local",
            "publisher": "fixture",
            "name": "zero-input",
        },
        "release_version": "1.0.0",
        "source_provenance": {"commit": "fixture"},
        "artifacts": [
            {
                "id": "fixture-artifact",
                "artifact_type": "test-artifact",
                "filename": artifact.name,
                "sha256": artifact_sha256 or digest,
                "size": artifact.stat().st_size,
                "selectors": {},
            }
        ],
        "integration_package": {"sha256": sha256_file(MANIFEST_ZERO)},
    }
    descriptor_path = tmp_path / "release.json"
    descriptor_path.write_text(json.dumps(descriptor, indent=2) + "\n", encoding="utf-8")
    return descriptor_path, artifact


def _manager(tmp_path: Path) -> AdapterManager:
    result_payload = json.loads(RESULT_ZERO.read_text(encoding="utf-8"))
    return AdapterManager(
        state_root=tmp_path / "state",
        backends=[FakeInstallationBackend(result_payload)],
    )


def test_m0_install_verify_execute_remove_lifecycle(tmp_path: Path) -> None:
    manager = _manager(tmp_path)
    descriptor_path, artifact = _write_release(tmp_path)

    record = manager.install(descriptor_path, artifact)

    assert manager.inspect(record.instance_id) == record
    assert manager.list() == [record]
    assert Path(record.release_descriptor_path).is_file()
    assert Path(record.execution_argv_prefix[0]).is_absolute()

    verification = manager.verify(record.instance_id)
    assert verification.passed

    input_manifest = tmp_path / "input-set.json"
    profile = tmp_path / "profile.yaml"
    input_manifest.write_text("{}\n", encoding="utf-8")
    profile.write_text("kind: fixture\n", encoding="utf-8")
    execution = manager.execute(
        record.instance_id,
        operation="project",
        input_set_manifest=input_manifest,
        profile=profile,
        output_dir=tmp_path / "output",
    )

    assert execution.returncode == 0
    assert execution.result["result"] == "succeeded"
    assert execution.result_path.is_file()

    removed = manager.remove(record.instance_id)
    assert removed.instance_id == record.instance_id
    assert manager.list() == []
    assert not Path(record.install_root).exists()


def test_verify_detects_installed_manifest_drift(tmp_path: Path) -> None:
    manager = _manager(tmp_path)
    descriptor_path, artifact = _write_release(tmp_path)
    record = manager.install(descriptor_path, artifact)

    Path(record.manifest_path).write_text("{}\n", encoding="utf-8")

    report = manager.verify(record.instance_id)
    assert report.manifest_integrity.status == "FAIL"
    assert report.manifest_conformance.status == "FAIL"
    assert not report.passed


def test_bad_artifact_digest_never_publishes_inventory(tmp_path: Path) -> None:
    manager = _manager(tmp_path)
    descriptor_path, artifact = _write_release(tmp_path, artifact_sha256="0" * 64)

    with pytest.raises(ReleaseResolutionError):
        manager.install(descriptor_path, artifact)

    assert manager.list() == []


def test_backend_failure_never_publishes_inventory(tmp_path: Path) -> None:
    result_payload = json.loads(RESULT_ZERO.read_text(encoding="utf-8"))
    manager = AdapterManager(
        state_root=tmp_path / "state",
        backends=[FailingInstallationBackend(result_payload)],
    )
    descriptor_path, artifact = _write_release(tmp_path)

    with pytest.raises(InstallationError, match="intentional backend failure"):
        manager.install(descriptor_path, artifact)

    assert manager.list() == []


def test_adapter_cli_group_is_registered(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        app,
        ["adapter", "list", "--json"],
        env={"ORBITFABRIC_STATE_DIR": str(tmp_path / "state")},
    )

    assert result.exit_code == 0
    assert json.loads(result.stdout) == []
