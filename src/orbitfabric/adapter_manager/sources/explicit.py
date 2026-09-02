from __future__ import annotations

from pathlib import Path

from pydantic import ValidationError

from ..errors import ReleaseResolutionError
from ..hashing import sha256_bytes, sha256_file
from ..models import (
    AdapterReleaseDescriptor,
    ReleaseArtifact,
    ReleaseTrustEvidence,
    ResolvedAdapterRelease,
)


class ExplicitReleaseSource:
    """Resolve one exact release from an explicit descriptor and artifact path."""

    source_id = "explicit-release"

    def resolve(
        self,
        descriptor_path: str | Path,
        artifact_path: str | Path,
        *,
        artifact_id: str | None = None,
        expected_descriptor_sha256: str | None = None,
    ) -> ResolvedAdapterRelease:
        descriptor_file = Path(descriptor_path).expanduser().resolve()
        artifact_file = Path(artifact_path).expanduser().resolve()

        try:
            descriptor_bytes = descriptor_file.read_bytes()
        except OSError as exc:
            raise ReleaseResolutionError(
                f"Cannot read Adapter Release Descriptor {descriptor_file}: {exc}"
            ) from exc

        try:
            descriptor = AdapterReleaseDescriptor.model_validate_json(descriptor_bytes)
        except ValidationError as exc:
            raise ReleaseResolutionError(
                f"Adapter Release Descriptor is invalid: {exc}"
            ) from exc

        descriptor_digest = sha256_bytes(descriptor_bytes)
        descriptor_integrity = "UNKNOWN"
        if expected_descriptor_sha256 is not None:
            if descriptor_digest != expected_descriptor_sha256:
                raise ReleaseResolutionError(
                    "Adapter Release Descriptor SHA-256 does not match the expected digest"
                )
            descriptor_integrity = "PASS"

        artifact = self._select_artifact(descriptor, artifact_file, artifact_id)
        if not artifact_file.is_file():
            raise ReleaseResolutionError(f"Adapter artifact does not exist: {artifact_file}")

        if artifact.size is not None and artifact_file.stat().st_size != artifact.size:
            raise ReleaseResolutionError(
                f"Adapter artifact size does not match descriptor for {artifact.id}"
            )

        artifact_digest = sha256_file(artifact_file)
        if artifact_digest != artifact.sha256:
            raise ReleaseResolutionError(
                f"Adapter artifact SHA-256 does not match descriptor for {artifact.id}"
            )

        evidence = ReleaseTrustEvidence(
            release_descriptor_integrity=descriptor_integrity,
            artifact_integrity="PASS",
            operational_state="allowed-lab",
        )
        return ResolvedAdapterRelease(
            descriptor=descriptor,
            descriptor_path=descriptor_file,
            descriptor_sha256=descriptor_digest,
            artifact=artifact,
            artifact_path=artifact_file,
            trust_evidence=evidence,
        )

    @staticmethod
    def _select_artifact(
        descriptor: AdapterReleaseDescriptor,
        artifact_path: Path,
        artifact_id: str | None,
    ) -> ReleaseArtifact:
        if artifact_id is not None:
            matches = [artifact for artifact in descriptor.artifacts if artifact.id == artifact_id]
            if len(matches) != 1:
                raise ReleaseResolutionError(f"Unknown Adapter Release artifact id: {artifact_id}")
            return matches[0]

        if len(descriptor.artifacts) == 1:
            return descriptor.artifacts[0]

        filename_matches = [
            artifact
            for artifact in descriptor.artifacts
            if artifact.filename is not None and artifact.filename == artifact_path.name
        ]
        if len(filename_matches) == 1:
            return filename_matches[0]

        raise ReleaseResolutionError(
            "Adapter Release contains multiple artifacts; select one explicitly with artifact id"
        )
