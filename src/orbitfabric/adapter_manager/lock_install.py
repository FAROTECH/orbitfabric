from __future__ import annotations

from pathlib import Path

from .errors import AdapterManagerError, ProjectLockError
from .manager import AdapterManager
from .models import (
    AdapterProjectLock,
    AdapterProjectLockEntry,
    AdapterSourceCoordinate,
    ProjectAdapterStateReport,
    ProjectLockCheckReport,
    ProjectLockInstallReport,
    ResolvedAdapterRelease,
)
from .project_lock import ProjectLockService
from .sources import ExplicitReleaseSource


class ProjectLockInstallService:
    """Satisfy one exact Project Lock entry through a resolved adapter release."""

    def __init__(
        self,
        manager: AdapterManager | None = None,
        *,
        project_locks: ProjectLockService | None = None,
        source: ExplicitReleaseSource | None = None,
    ) -> None:
        self.manager = manager or AdapterManager()
        self.project_locks = project_locks or ProjectLockService()
        self.source = source or self.manager.source

    def install_entry(
        self,
        lock_path: str | Path,
        source_coordinate: AdapterSourceCoordinate,
        descriptor_path: str | Path,
        artifact_path: str | Path,
    ) -> ProjectLockInstallReport:
        """Satisfy one lock entry through the existing explicit Release Source."""
        path, entry, before = self._prepare_entry(lock_path, source_coordinate)
        if before.status == "MATCH":
            return self._noop_report(path, source_coordinate, before)

        release = self.source.resolve(
            descriptor_path,
            artifact_path,
            artifact_id=entry.artifact.id,
            expected_descriptor_sha256=entry.release_descriptor.sha256,
        )
        return self._install_selected_entry(
            path,
            source_coordinate,
            entry,
            before,
            release,
        )

    def install_resolved_entry(
        self,
        lock_path: str | Path,
        source_coordinate: AdapterSourceCoordinate,
        release: ResolvedAdapterRelease,
    ) -> ProjectLockInstallReport:
        """Satisfy one lock entry from an already-resolved exact release."""
        path, entry, before = self._prepare_entry(lock_path, source_coordinate)
        if before.status == "MATCH":
            return self._noop_report(path, source_coordinate, before)

        return self._install_selected_entry(
            path,
            source_coordinate,
            entry,
            before,
            release,
        )

    def _prepare_entry(
        self,
        lock_path: str | Path,
        source_coordinate: AdapterSourceCoordinate,
    ) -> tuple[Path, AdapterProjectLockEntry, ProjectAdapterStateReport]:
        path = Path(lock_path).expanduser().resolve()
        lock = self.project_locks.load(path)
        entry = self._find_entry(lock, source_coordinate)
        before = self._find_report(
            self.project_locks.check(path, self.manager.list()), source_coordinate
        )
        return path, entry, before

    def _install_selected_entry(
        self,
        path: Path,
        source_coordinate: AdapterSourceCoordinate,
        entry: AdapterProjectLockEntry,
        before: ProjectAdapterStateReport,
        release: ResolvedAdapterRelease,
    ) -> ProjectLockInstallReport:
        self._verify_release_satisfies_entry(entry, release)

        record = self.manager.install_resolved(
            release,
            expected_backend_id=entry.installation_backend.id,
        )

        try:
            after = self._find_report(
                self.project_locks.check(path, self.manager.list()), source_coordinate
            )
            if after.status != "MATCH":
                raise ProjectLockError(
                    "Installed release did not satisfy the Adapter Project Lock entry"
                )
            return ProjectLockInstallReport(
                lock_path=path,
                source_coordinate=source_coordinate,
                before_status=before.status,
                action="INSTALLED",
                installed_instance_id=record.instance_id,
                after_status=after.status,
                matching_instance_ids=after.matching_instance_ids,
            )
        except Exception:
            try:
                self.manager.remove(record.instance_id)
            except AdapterManagerError:
                pass
            raise

    @staticmethod
    def _noop_report(
        path: Path,
        source_coordinate: AdapterSourceCoordinate,
        before: ProjectAdapterStateReport,
    ) -> ProjectLockInstallReport:
        return ProjectLockInstallReport(
            lock_path=path,
            source_coordinate=source_coordinate,
            before_status=before.status,
            action="NOOP",
            after_status="MATCH",
            matching_instance_ids=before.matching_instance_ids,
        )

    @staticmethod
    def _find_entry(
        lock: AdapterProjectLock,
        source_coordinate: AdapterSourceCoordinate,
    ) -> AdapterProjectLockEntry:
        matches = [
            entry for entry in lock.adapters if entry.source_coordinate == source_coordinate
        ]
        if len(matches) != 1:
            raise ProjectLockError(
                "Adapter Project Lock does not contain exactly one requested "
                f"Source Coordinate: {source_coordinate.display()}"
            )
        return matches[0]

    @staticmethod
    def _find_report(
        report: ProjectLockCheckReport,
        source_coordinate: AdapterSourceCoordinate,
    ) -> ProjectAdapterStateReport:
        matches = [
            item for item in report.adapters if item.source_coordinate == source_coordinate
        ]
        if len(matches) != 1:
            raise ProjectLockError(
                "Project Lock check report does not contain exactly one requested "
                f"Source Coordinate: {source_coordinate.display()}"
            )
        return matches[0]

    @staticmethod
    def _verify_release_satisfies_entry(
        entry: AdapterProjectLockEntry,
        release: ResolvedAdapterRelease,
    ) -> None:
        mismatches: list[str] = []
        if release.descriptor.source_coordinate != entry.source_coordinate:
            mismatches.append("source_coordinate")
        if release.descriptor.release_version != entry.release_version:
            mismatches.append("release_version")
        if release.descriptor_sha256 != entry.release_descriptor.sha256:
            mismatches.append("release_descriptor_sha256")
        if release.artifact.id != entry.artifact.id:
            mismatches.append("artifact_id")
        if release.artifact.sha256 != entry.artifact.sha256:
            mismatches.append("artifact_sha256")
        if mismatches:
            raise ProjectLockError(
                "Resolved adapter release does not satisfy Project Lock entry: "
                + ", ".join(mismatches)
            )


__all__ = ["ProjectLockInstallService"]