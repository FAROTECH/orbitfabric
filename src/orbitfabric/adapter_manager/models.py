from __future__ import annotations

from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

Sha256 = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{64}$")]
EvidenceStatus = Literal["PASS", "FAIL", "UNKNOWN"]
ProjectAdapterState = Literal["MATCH", "MISSING", "MISMATCH"]
ProjectOverallState = Literal["MATCH", "NOT_SATISFIED"]
ProjectInstallAction = Literal["NOOP", "INSTALLED"]
ProjectMismatchDimension = Literal[
    "release_version",
    "release_descriptor_sha256",
    "artifact_id",
    "artifact_sha256",
    "backend_id",
]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class AdapterSourceCoordinate(StrictModel):
    authority: str = Field(min_length=1)
    publisher: str = Field(min_length=1)
    name: str = Field(min_length=1)

    def display(self) -> str:
        return f"{self.authority}:{self.publisher}/{self.name}"


class ReleaseArtifact(StrictModel):
    id: str = Field(min_length=1)
    artifact_type: str = Field(min_length=1)
    filename: str | None = Field(default=None, min_length=1)
    sha256: Sha256
    size: int | None = Field(default=None, ge=0)
    selectors: dict[str, str] = Field(default_factory=dict)


class IntegrationPackageBinding(StrictModel):
    sha256: Sha256


class AdapterReleaseDescriptor(StrictModel):
    kind: Literal["orbitfabric.adapter_release"]
    descriptor_version: Literal["0.1-candidate"]
    source_coordinate: AdapterSourceCoordinate
    release_version: str = Field(min_length=1)
    source_provenance: dict[str, str] = Field(default_factory=dict)
    artifacts: list[ReleaseArtifact] = Field(min_length=1)
    integration_package: IntegrationPackageBinding

    @model_validator(mode="after")
    def validate_artifact_ids(self) -> AdapterReleaseDescriptor:
        ids = [artifact.id for artifact in self.artifacts]
        if len(ids) != len(set(ids)):
            raise ValueError("Adapter Release artifact ids must be unique")
        return self


class ReleaseTrustEvidence(StrictModel):
    source_authority_recognition: EvidenceStatus = "UNKNOWN"
    publisher_namespace_binding: EvidenceStatus = "UNKNOWN"
    publication_authentication: EvidenceStatus = "UNKNOWN"
    closed_release_immutability: EvidenceStatus = "UNKNOWN"
    release_descriptor_integrity: EvidenceStatus = "UNKNOWN"
    artifact_integrity: EvidenceStatus = "UNKNOWN"
    source_build_provenance: EvidenceStatus = "UNKNOWN"
    signature_attestation_verification: EvidenceStatus = "UNKNOWN"
    orbitfabric_conformance: EvidenceStatus = "UNKNOWN"
    policy_freshness: EvidenceStatus = "UNKNOWN"
    operational_state: str = "unknown"


class AcceptanceResult(StrictModel):
    policy: str = Field(min_length=1)
    accepted: bool
    failures: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class ResolvedAdapterRelease(StrictModel):
    descriptor: AdapterReleaseDescriptor
    descriptor_path: Path
    descriptor_sha256: Sha256
    artifact: ReleaseArtifact
    artifact_path: Path
    trust_evidence: ReleaseTrustEvidence


class BackendInstallReceipt(StrictModel):
    backend_id: str = Field(min_length=1)
    install_root: Path
    manifest_path: Path
    manifest_sha256: Sha256
    execution_argv_prefix: list[str] = Field(min_length=1)


class InstalledAdapterRecord(StrictModel):
    instance_id: str = Field(min_length=1)
    source_coordinate: AdapterSourceCoordinate
    release_version: str = Field(min_length=1)
    release_descriptor_path: Path
    release_descriptor_sha256: Sha256
    artifact_id: str = Field(min_length=1)
    artifact_sha256: Sha256
    backend_id: str = Field(min_length=1)
    install_root: Path
    manifest_path: Path
    manifest_sha256: Sha256
    execution_argv_prefix: list[str] = Field(min_length=1)
    acceptance_policy: str = Field(min_length=1)
    acceptance_warnings: list[str] = Field(default_factory=list)


class ProjectLockDigestBinding(StrictModel):
    sha256: Sha256


class ProjectLockArtifactBinding(StrictModel):
    id: str = Field(min_length=1)
    sha256: Sha256


class ProjectLockInstallationBackend(StrictModel):
    id: str = Field(min_length=1)


class BackendResolutionBinding(StrictModel):
    kind: str = Field(min_length=1)
    reference: str = Field(min_length=1)
    sha256: Sha256


class AdapterProjectLockEntry(StrictModel):
    source_coordinate: AdapterSourceCoordinate
    release_version: str = Field(min_length=1)
    release_descriptor: ProjectLockDigestBinding
    artifact: ProjectLockArtifactBinding
    installation_backend: ProjectLockInstallationBackend
    backend_resolution: BackendResolutionBinding | None = None


class AdapterProjectLock(StrictModel):
    kind: Literal["orbitfabric.adapter_project_lock"]
    lock_version: Literal["0.1-candidate"]
    adapters: list[AdapterProjectLockEntry] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_source_coordinates(self) -> AdapterProjectLock:
        coordinates = [
            (
                entry.source_coordinate.authority,
                entry.source_coordinate.publisher,
                entry.source_coordinate.name,
            )
            for entry in self.adapters
        ]
        if len(coordinates) != len(set(coordinates)):
            raise ValueError("Adapter Project Lock Source Coordinates must be unique")
        return self


class ProjectLockCandidateMismatch(StrictModel):
    instance_id: str = Field(min_length=1)
    dimensions: list[ProjectMismatchDimension] = Field(min_length=1)


class ProjectAdapterStateReport(StrictModel):
    source_coordinate: AdapterSourceCoordinate
    release_version: str = Field(min_length=1)
    status: ProjectAdapterState
    matching_instance_ids: list[str] = Field(default_factory=list)
    candidate_instance_ids: list[str] = Field(default_factory=list)
    candidate_mismatches: list[ProjectLockCandidateMismatch] = Field(default_factory=list)


class ProjectLockCheckReport(StrictModel):
    lock_path: Path
    lock_version: str = Field(min_length=1)
    status: ProjectOverallState
    adapters: list[ProjectAdapterStateReport] = Field(min_length=1)

    @property
    def passed(self) -> bool:
        return self.status == "MATCH"


class ProjectLockInstallReport(StrictModel):
    lock_path: Path
    source_coordinate: AdapterSourceCoordinate
    before_status: ProjectAdapterState
    action: ProjectInstallAction
    installed_instance_id: str | None = None
    after_status: ProjectAdapterState
    matching_instance_ids: list[str] = Field(default_factory=list)


class VerificationDimension(StrictModel):
    status: EvidenceStatus
    detail: str | None = None


class AdapterVerificationReport(StrictModel):
    instance_id: str
    release_descriptor_integrity: VerificationDimension
    manifest_integrity: VerificationDimension
    manifest_conformance: VerificationDimension
    execution_binding: VerificationDimension
    backend_materialization: VerificationDimension

    @property
    def passed(self) -> bool:
        return all(
            dimension.status == "PASS"
            for dimension in (
                self.release_descriptor_integrity,
                self.manifest_integrity,
                self.manifest_conformance,
                self.execution_binding,
                self.backend_materialization,
            )
        )


class AdapterExecutionReport(StrictModel):
    instance_id: str
    operation: str
    argv: list[str]
    returncode: int
    stdout: str
    stderr: str
    result_path: Path
    result: dict[str, Any]
