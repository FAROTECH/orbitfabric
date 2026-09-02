from __future__ import annotations

import json
import os
import shutil
import subprocess
import uuid
from collections.abc import Mapping
from pathlib import Path

from orbitfabric.conformance.integration_contracts import (
    ContractError,
    load_json,
    validate_bindings,
    validate_manifest,
    validate_result,
)

from .acceptance import evaluate_development_explicit_source
from .backends import InstallationBackend, PythonWheelManagedEnvironmentBackend
from .errors import (
    AcceptanceError,
    AdapterManagerError,
    ExecutionError,
    InstallationError,
    VerificationError,
)
from .hashing import sha256_file
from .inventory import InstalledAdapterInventory
from .models import (
    AdapterExecutionReport,
    AdapterReleaseDescriptor,
    AdapterSourceCoordinate,
    AdapterVerificationReport,
    BackendInstallReceipt,
    InstalledAdapterRecord,
    ResolvedAdapterRelease,
    VerificationDimension,
)
from .sources import ExplicitReleaseSource
from .state import default_state_root


class AdapterManager:
    """Core-owned Adapter Manager lifecycle orchestrator."""

    def __init__(
        self,
        state_root: str | Path | None = None,
        *,
        source: ExplicitReleaseSource | None = None,
        backends: list[InstallationBackend] | None = None,
    ) -> None:
        self.state_root = default_state_root(state_root)
        self.instances_root = self.state_root / "instances"
        self.inventory = InstalledAdapterInventory(self.state_root)
        self.source = source or ExplicitReleaseSource()
        selected_backends = backends or [PythonWheelManagedEnvironmentBackend()]
        self.backends = {backend.backend_id: backend for backend in selected_backends}

    def install(
        self,
        descriptor_path: str | Path,
        artifact_path: str | Path,
        *,
        artifact_id: str | None = None,
        expected_descriptor_sha256: str | None = None,
    ) -> InstalledAdapterRecord:
        release = self.source.resolve(
            descriptor_path,
            artifact_path,
            artifact_id=artifact_id,
            expected_descriptor_sha256=expected_descriptor_sha256,
        )
        return self.install_resolved(release)

    def install_resolved(
        self,
        release: ResolvedAdapterRelease,
        *,
        expected_backend_id: str | None = None,
    ) -> InstalledAdapterRecord:
        """Install one already-resolved exact release through the shared lifecycle transaction."""
        acceptance = evaluate_development_explicit_source(release.trust_evidence)
        if not acceptance.accepted:
            raise AcceptanceError(
                "Adapter release was rejected by development explicit-source policy: "
                + ", ".join(acceptance.failures)
            )

        backend = self._select_backend(release.artifact.artifact_type)
        if expected_backend_id is not None and backend.backend_id != expected_backend_id:
            raise InstallationError(
                "Selected installation backend does not satisfy expected backend id: "
                f"expected {expected_backend_id!r}, selected {backend.backend_id!r}"
            )

        instance_id = uuid.uuid4().hex
        receipt = backend.install(release, instance_id, self.instances_root)
        descriptor_copy = receipt.install_root / "release_descriptor.json"
        record = self._build_record(
            instance_id,
            receipt,
            descriptor_copy,
            release.descriptor.source_coordinate,
            release.descriptor.release_version,
            release.descriptor_sha256,
            release.artifact.id,
            release.artifact.sha256,
            acceptance.policy,
            acceptance.warnings,
        )

        try:
            shutil.copyfile(release.descriptor_path, descriptor_copy)
            if sha256_file(descriptor_copy) != release.descriptor_sha256:
                raise InstallationError(
                    "Installed release descriptor copy failed integrity verification"
                )

            report = self._verify_record(record)
            if not report.passed:
                details = self._failed_verification_details(report)
                raise VerificationError(
                    "Installed adapter failed post-install verification: " + "; ".join(details)
                )

            self.inventory.add(record)
            return record
        except Exception:
            try:
                backend.remove(record)
            except AdapterManagerError:
                pass
            raise

    def list(self) -> list[InstalledAdapterRecord]:
        return self.inventory.list()

    def inspect(self, instance_id: str) -> InstalledAdapterRecord:
        return self.inventory.get(instance_id)

    def verify(self, instance_id: str) -> AdapterVerificationReport:
        return self._verify_record(self.inventory.get(instance_id))

    def execute(
        self,
        instance_id: str,
        *,
        operation: str,
        input_set_manifest: str | Path,
        profile: str | Path,
        output_dir: str | Path,
        operation_inputs: Mapping[str, str | Path] | None = None,
    ) -> AdapterExecutionReport:
        record = self.inventory.get(instance_id)
        verification = self._verify_record(record)
        if not verification.passed:
            raise VerificationError(
                "Installed adapter is not executable: "
                + "; ".join(self._failed_verification_details(verification))
            )

        manifest = load_json(record.manifest_path)
        bindings = dict(operation_inputs or {})
        try:
            validate_bindings(manifest, operation, list(bindings))
        except ContractError as exc:
            raise ExecutionError(str(exc)) from exc

        input_manifest_path = Path(input_set_manifest).expanduser().resolve()
        profile_path = Path(profile).expanduser().resolve()
        output_path = Path(output_dir).expanduser().resolve()
        if not input_manifest_path.is_file():
            raise ExecutionError(
                f"Core Integration Input Set manifest does not exist: {input_manifest_path}"
            )
        if not profile_path.is_file():
            raise ExecutionError(f"Projection Profile does not exist: {profile_path}")
        for role, value in bindings.items():
            path = Path(value).expanduser().resolve()
            if not path.is_file():
                raise ExecutionError(f"Operation input {role!r} does not exist: {path}")
            bindings[role] = path

        output_path.parent.mkdir(parents=True, exist_ok=True)
        argv = [
            *record.execution_argv_prefix,
            "run",
            "--operation",
            operation,
            "--input-set-manifest",
            str(input_manifest_path),
            "--profile",
            str(profile_path),
        ]
        for role, value in bindings.items():
            argv.extend(["--operation-input", role, str(value)])
        argv.extend(["--output-dir", str(output_path)])

        completed = subprocess.run(argv, capture_output=True, text=True, check=False)
        result_path = output_path / "integration_result.json"
        if not result_path.is_file():
            detail = (completed.stderr or completed.stdout or "").strip()
            raise ExecutionError(
                "Adapter execution did not produce integration_result.json"
                + (f": {detail}" if detail else "")
            )

        try:
            result = load_json(result_path)
            validate_result(manifest, result)
        except ContractError as exc:
            raise ExecutionError(
                f"Adapter produced a non-conformant Integration Result: {exc}"
            ) from exc

        return AdapterExecutionReport(
            instance_id=instance_id,
            operation=operation,
            argv=argv,
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
            result_path=result_path,
            result=result,
        )

    def remove(self, instance_id: str) -> InstalledAdapterRecord:
        record = self.inventory.get(instance_id)
        backend = self._backend_for_record(record)
        backend.remove(record)
        if Path(record.install_root).exists():
            raise InstallationError(
                f"Adapter backend did not remove installation root: {record.install_root}"
            )
        return self.inventory.remove(instance_id)

    def _verify_record(self, record: InstalledAdapterRecord) -> AdapterVerificationReport:
        descriptor_dimension = self._verify_release_descriptor(record)
        manifest_integrity = self._verify_manifest_integrity(record)
        manifest_conformance = self._verify_manifest_conformance(record)
        execution_binding = self._verify_execution_binding(record)
        backend = self._backend_for_record(record)
        backend_materialization = backend.verify(record)
        return AdapterVerificationReport(
            instance_id=record.instance_id,
            release_descriptor_integrity=descriptor_dimension,
            manifest_integrity=manifest_integrity,
            manifest_conformance=manifest_conformance,
            execution_binding=execution_binding,
            backend_materialization=backend_materialization,
        )

    @staticmethod
    def _verify_release_descriptor(record: InstalledAdapterRecord) -> VerificationDimension:
        path = Path(record.release_descriptor_path)
        if not path.is_file():
            return VerificationDimension(
                status="FAIL",
                detail=f"Installed release descriptor is missing: {path}",
            )
        if sha256_file(path) != record.release_descriptor_sha256:
            return VerificationDimension(
                status="FAIL",
                detail="Installed release descriptor SHA-256 drift detected",
            )
        try:
            AdapterReleaseDescriptor.model_validate_json(path.read_bytes())
        except (OSError, ValueError) as exc:
            return VerificationDimension(
                status="FAIL",
                detail=f"Installed release descriptor is invalid: {exc}",
            )
        return VerificationDimension(status="PASS")

    @staticmethod
    def _verify_manifest_integrity(record: InstalledAdapterRecord) -> VerificationDimension:
        path = Path(record.manifest_path)
        if not path.is_file():
            return VerificationDimension(
                status="FAIL",
                detail=f"Installed Integration Package Manifest is missing: {path}",
            )
        if sha256_file(path) != record.manifest_sha256:
            return VerificationDimension(
                status="FAIL",
                detail="Installed Integration Package Manifest SHA-256 drift detected",
            )
        return VerificationDimension(status="PASS")

    @staticmethod
    def _verify_manifest_conformance(record: InstalledAdapterRecord) -> VerificationDimension:
        try:
            manifest = json.loads(Path(record.manifest_path).read_text(encoding="utf-8"))
            validate_manifest(manifest)
        except (OSError, json.JSONDecodeError, ContractError) as exc:
            return VerificationDimension(
                status="FAIL",
                detail=f"Integration Package Manifest conformance failure: {exc}",
            )
        return VerificationDimension(status="PASS")

    @staticmethod
    def _verify_execution_binding(record: InstalledAdapterRecord) -> VerificationDimension:
        if not record.execution_argv_prefix:
            return VerificationDimension(status="FAIL", detail="Execution binding is empty")
        executable = Path(record.execution_argv_prefix[0])
        if not executable.is_absolute():
            return VerificationDimension(
                status="FAIL",
                detail=f"Execution endpoint is not absolute: {executable}",
            )
        if not executable.is_file():
            return VerificationDimension(
                status="FAIL",
                detail=f"Execution endpoint is missing: {executable}",
            )
        if os.name != "nt" and not os.access(executable, os.X_OK):
            return VerificationDimension(
                status="FAIL",
                detail=f"Execution endpoint is not executable: {executable}",
            )
        return VerificationDimension(status="PASS")

    def _select_backend(self, artifact_type: str) -> InstallationBackend:
        supported = [
            backend
            for backend in self.backends.values()
            if artifact_type == getattr(backend, "artifact_type", None)
        ]
        if len(supported) != 1:
            raise InstallationError(
                f"Expected exactly one installation backend for artifact type {artifact_type!r}; "
                f"found {len(supported)}"
            )
        return supported[0]

    def _backend_for_record(self, record: InstalledAdapterRecord) -> InstallationBackend:
        backend = self.backends.get(record.backend_id)
        if backend is None:
            raise InstallationError(
                f"Installation backend is unavailable for installed record: {record.backend_id}"
            )
        return backend

    @staticmethod
    def _build_record(
        instance_id: str,
        receipt: BackendInstallReceipt,
        descriptor_copy: Path,
        source_coordinate: AdapterSourceCoordinate,
        release_version: str,
        descriptor_sha256: str,
        artifact_id: str,
        artifact_sha256: str,
        acceptance_policy: str,
        acceptance_warnings: list[str],
    ) -> InstalledAdapterRecord:
        return InstalledAdapterRecord(
            instance_id=instance_id,
            source_coordinate=source_coordinate,
            release_version=release_version,
            release_descriptor_path=descriptor_copy,
            release_descriptor_sha256=descriptor_sha256,
            artifact_id=artifact_id,
            artifact_sha256=artifact_sha256,
            backend_id=receipt.backend_id,
            install_root=receipt.install_root,
            manifest_path=receipt.manifest_path,
            manifest_sha256=receipt.manifest_sha256,
            execution_argv_prefix=receipt.execution_argv_prefix,
            acceptance_policy=acceptance_policy,
            acceptance_warnings=acceptance_warnings,
        )

    @staticmethod
    def _failed_verification_details(report: AdapterVerificationReport) -> list[str]:
        dimensions = {
            "release_descriptor_integrity": report.release_descriptor_integrity,
            "manifest_integrity": report.manifest_integrity,
            "manifest_conformance": report.manifest_conformance,
            "execution_binding": report.execution_binding,
            "backend_materialization": report.backend_materialization,
        }
        return [
            f"{name}: {dimension.detail or dimension.status}"
            for name, dimension in dimensions.items()
            if dimension.status != "PASS"
        ]
