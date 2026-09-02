from __future__ import annotations

from .models import AcceptanceResult, ReleaseTrustEvidence

DEVELOPMENT_EXPLICIT_SOURCE_POLICY = "development-explicit-source"


def evaluate_development_explicit_source(
    evidence: ReleaseTrustEvidence,
) -> AcceptanceResult:
    failures: list[str] = []
    warnings: list[str] = []

    if evidence.artifact_integrity != "PASS":
        failures.append("artifact_integrity_not_pass")

    warning_dimensions = {
        "release_descriptor_integrity": evidence.release_descriptor_integrity,
        "closed_release_immutability": evidence.closed_release_immutability,
        "publisher_namespace_binding": evidence.publisher_namespace_binding,
        "publication_authentication": evidence.publication_authentication,
        "source_build_provenance": evidence.source_build_provenance,
        "signature_attestation_verification": evidence.signature_attestation_verification,
        "orbitfabric_conformance": evidence.orbitfabric_conformance,
        "policy_freshness": evidence.policy_freshness,
    }
    for name, status in warning_dimensions.items():
        if status != "PASS":
            warnings.append(f"{name.lower()}_{status.lower()}")

    if evidence.operational_state not in {"unknown", "allowed", "allowed-lab"}:
        failures.append(f"operational_state_{evidence.operational_state}")

    return AcceptanceResult(
        policy=DEVELOPMENT_EXPLICIT_SOURCE_POLICY,
        accepted=not failures,
        failures=failures,
        warnings=warnings,
    )
