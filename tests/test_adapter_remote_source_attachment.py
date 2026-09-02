from __future__ import annotations

import json
from pathlib import Path

from orbitfabric.adapter_manager import ProjectLockInstallService
from orbitfabric.adapter_manager.models import (
    AdapterReleaseDescriptor,
    AdapterSourceCoordinate,
    InstalledAdapterRecord,
    ReleaseArtifact,
    ReleaseTrustEvidence,
    ResolvedAdapterRelease,
)


class FakeSource:
    def __init__(self, release: ResolvedAdapterRelease) -> None:
        self.release = release
        self.resolve_calls = 0

    def resolve(self, *args: object, **kwargs: object) -> ResolvedAdapterRelease:
        self.resolve_calls += 1
        return self.release


class FakeManager:
    def __init__(self, release: ResolvedAdapterRelease) -> None:
        self.source = FakeSource(release)
        self.records: list[InstalledAdapterRecord] = []
        self.install_calls = 0

    def list(self) -> list[InstalledAdapterRecord]:
        return list(self.records)

    def install_resolved(
        self,
        release: ResolvedAdapterRelease,
        *,
        expected_backend_id: str | None = None,
    ) -> InstalledAdapterRecord:
        self.install_calls += 1
        backend_id = expected_backend_id or "fake-managed-backend"
        record = _installed_record(release, backend_id=backend_id)
        self.records.append(record)
        return record

    def remove(self, instance_id: str) -> InstalledAdapterRecord:
        record = next(record for record in self.records if record.instance_id == instance_id)
        self.records.remove(record)
        return record


def _coordinate() -> AdapterSourceCoordinate:
    return AdapterSourceCoordinate(
        authority="test.local",
        publisher="fixture",
        name="remote-source",
    )


def _release(tmp_path: Path) -> ResolvedAdapterRelease:
    descriptor_path = tmp_path / "release.json"
    artifact_path = tmp_path / "adapter.bin"
    descriptor_path.write_text("{}\n", encoding="utf-8")
    artifact_path.write_bytes(b"remote adapter bytes")
    descriptor_sha = "1" * 64
    artifact_sha = "2" * 64
    descriptor = AdapterReleaseDescriptor(
        kind="orbitfabric.adapter_release",
        descriptor_version="0.1-candidate",
        source_coordinate=_coordinate(),
        release_version="1.0.0",
        source_provenance={"proof": "remote-source-attachment"},
        artifacts=[
            ReleaseArtifact(
                id="remote-artifact",
                artifact_type="test-artifact",
                filename=artifact_path.name,
                sha256=artifact_sha,
                size=artifact_path.stat().st_size,
            )
        ],
        integration_package={"sha256": "3" * 64},
    )
    return ResolvedAdapterRelease(
        descriptor=descriptor,
        descriptor_path=descriptor_path,
        descriptor_sha256=descriptor_sha,
        artifact=descriptor.artifacts[0],
        artifact_path=artifact_path,
        trust_evidence=ReleaseTrustEvidence(
            release_descriptor_integrity="PASS",
            artifact_integrity="PASS",
            operational_state="allowed-lab",
        ),
    )


def _write_lock(path: Path, release: ResolvedAdapterRelease) -> Path:
    path.write_text(
        json.dumps(
            {
                "kind": "orbitfabric.adapter_project_lock",
                "lock_version": "0.1-candidate",
                "adapters": [
                    {
                        "source_coordinate": _coordinate().model_dump(mode="json"),
                        "release_version": release.descriptor.release_version,
                        "release_descriptor": {"sha256": release.descriptor_sha256},
                        "artifact": {
                            "id": release.artifact.id,
                            "sha256": release.artifact.sha256,
                        },
                        "installation_backend": {"id": "fake-managed-backend"},
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return path


def _installed_record(
    release: ResolvedAdapterRelease,
    *,
    backend_id: str,
) -> InstalledAdapterRecord:
    return InstalledAdapterRecord(
        instance_id="resolved-source-instance",
        source_coordinate=release.descriptor.source_coordinate,
        release_version=release.descriptor.release_version,
        release_descriptor_path=Path("/installed/release_descriptor.json"),
        release_descriptor_sha256=release.descriptor_sha256,
        artifact_id=release.artifact.id,
        artifact_sha256=release.artifact.sha256,
        backend_id=backend_id,
        install_root=Path("/installed"),
        manifest_path=Path("/installed/integration_package.json"),
        manifest_sha256="3" * 64,
        execution_argv_prefix=["/installed/bin/adapter"],
        acceptance_policy="development-explicit-source",
    )


def test_already_resolved_release_satisfies_missing_lock_entry(tmp_path: Path) -> None:
    release = _release(tmp_path)
    lock = _write_lock(tmp_path / "adapter.lock.json", release)
    manager = FakeManager(release)

    report = ProjectLockInstallService(manager).install_resolved_entry(
        lock,
        _coordinate(),
        release,
    )

    assert report.before_status == "MISSING"
    assert report.action == "INSTALLED"
    assert report.after_status == "MATCH"
    assert manager.install_calls == 1
    assert manager.source.resolve_calls == 0


def test_explicit_wrapper_does_not_resolve_source_when_lock_already_matches(
    tmp_path: Path,
) -> None:
    release = _release(tmp_path)
    lock = _write_lock(tmp_path / "adapter.lock.json", release)
    manager = FakeManager(release)
    manager.records.append(_installed_record(release, backend_id="fake-managed-backend"))

    report = ProjectLockInstallService(manager, source=manager.source).install_entry(
        lock,
        _coordinate(),
        tmp_path / "unused-release.json",
        tmp_path / "unused-artifact.bin",
    )

    assert report.before_status == "MATCH"
    assert report.action == "NOOP"
    assert report.after_status == "MATCH"
    assert manager.source.resolve_calls == 0
    assert manager.install_calls == 0
