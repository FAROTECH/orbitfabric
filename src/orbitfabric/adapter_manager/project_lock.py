from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from pydantic import ValidationError

from orbitfabric.conformance.adapter_project_lock import (
    AdapterProjectLockContractError,
    load_project_lock,
)

from .errors import ProjectLockError
from .models import (
    AdapterProjectLock,
    AdapterProjectLockEntry,
    InstalledAdapterRecord,
    ProjectAdapterStateReport,
    ProjectLockCandidateMismatch,
    ProjectLockCheckReport,
    ProjectMismatchDimension,
)


class ProjectLockService:
    """Load and compare project-scoped exact adapter desired state."""

    def load(self, lock_path: str | Path) -> AdapterProjectLock:
        path = Path(lock_path).expanduser().resolve()
        try:
            payload = load_project_lock(path)
            return AdapterProjectLock.model_validate(payload)
        except (AdapterProjectLockContractError, ValidationError) as exc:
            raise ProjectLockError(str(exc)) from exc

    def check(
        self,
        lock_path: str | Path,
        installed_records: Iterable[InstalledAdapterRecord],
    ) -> ProjectLockCheckReport:
        path = Path(lock_path).expanduser().resolve()
        lock = self.load(path)
        records = sorted(installed_records, key=lambda item: item.instance_id)
        reports = [self._check_entry(entry, records) for entry in lock.adapters]
        overall = (
            "MATCH"
            if all(report.status == "MATCH" for report in reports)
            else "NOT_SATISFIED"
        )
        return ProjectLockCheckReport(
            lock_path=path,
            lock_version=lock.lock_version,
            status=overall,
            adapters=reports,
        )

    def _check_entry(
        self,
        entry: AdapterProjectLockEntry,
        installed_records: list[InstalledAdapterRecord],
    ) -> ProjectAdapterStateReport:
        candidates = [
            record
            for record in installed_records
            if record.source_coordinate == entry.source_coordinate
        ]
        if not candidates:
            return ProjectAdapterStateReport(
                source_coordinate=entry.source_coordinate,
                release_version=entry.release_version,
                status="MISSING",
            )

        exact_matches = [
            record for record in candidates if not self._mismatch_dimensions(entry, record)
        ]
        if exact_matches:
            return ProjectAdapterStateReport(
                source_coordinate=entry.source_coordinate,
                release_version=entry.release_version,
                status="MATCH",
                matching_instance_ids=[record.instance_id for record in exact_matches],
                candidate_instance_ids=[record.instance_id for record in candidates],
            )

        mismatches = [
            ProjectLockCandidateMismatch(
                instance_id=record.instance_id,
                dimensions=self._mismatch_dimensions(entry, record),
            )
            for record in candidates
        ]
        return ProjectAdapterStateReport(
            source_coordinate=entry.source_coordinate,
            release_version=entry.release_version,
            status="MISMATCH",
            candidate_instance_ids=[record.instance_id for record in candidates],
            candidate_mismatches=mismatches,
        )

    @staticmethod
    def _mismatch_dimensions(
        entry: AdapterProjectLockEntry,
        record: InstalledAdapterRecord,
    ) -> list[ProjectMismatchDimension]:
        mismatches: list[ProjectMismatchDimension] = []
        if record.release_version != entry.release_version:
            mismatches.append("release_version")
        if record.release_descriptor_sha256 != entry.release_descriptor.sha256:
            mismatches.append("release_descriptor_sha256")
        if record.artifact_id != entry.artifact.id:
            mismatches.append("artifact_id")
        if record.artifact_sha256 != entry.artifact.sha256:
            mismatches.append("artifact_sha256")
        if record.backend_id != entry.installation_backend.id:
            mismatches.append("backend_id")
        return mismatches


__all__ = ["ProjectLockService"]
