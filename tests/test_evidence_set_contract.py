from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from orbitfabric.conformance.evidence_set import (
    EvidenceSetContractError,
    validate_manifest,
    verify_bundle,
)

SHA_A = "a" * 64
SHA_B = "b" * 64


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _record(
    *,
    record_id: str,
    path: str,
    sha256: str,
    content_kind: str = "runtime_excerpt",
    producer_id: str = "test-harness",
    subjects: list[dict[str, str]] | None = None,
) -> dict[str, object]:
    return {
        "id": record_id,
        "content": {
            "kind": content_kind,
            "producer": {"id": producer_id},
            "reference": {
                "path": path,
                "sha256": sha256,
            },
        },
        "subjects": subjects
        or [
            {
                "type": "scenario_source",
                "scenario_id": "payload_stop_acquisition_verification",
                "scenario_sha256": SHA_A,
            }
        ],
    }


def _manifest(records: list[dict[str, object]]) -> dict[str, object]:
    return {
        "kind": "orbitfabric.evidence_set_manifest",
        "manifest_version": "0.1-candidate",
        "evidence_set": {"id": "r1-retained-evidence"},
        "curator": {"id": "orbitfabric-reference-mission"},
        "records": records,
    }


def test_valid_manifest_and_bundle_accept_plain_text_and_json(tmp_path: Path) -> None:
    evidence_dir = tmp_path / "evidence"
    evidence_dir.mkdir()
    text_file = evidence_dir / "runtime.txt"
    json_file = evidence_dir / "live-proof.json"
    text_file.write_text("native runtime evidence\n", encoding="utf-8")
    json_file.write_text('{"status":"producer-owned"}\n', encoding="utf-8")

    manifest = _manifest(
        [
            _record(
                record_id="native-runtime",
                path="evidence/runtime.txt",
                sha256=_sha256(text_file),
            ),
            _record(
                record_id="live-proof",
                path="evidence/live-proof.json",
                sha256=_sha256(json_file),
                content_kind="live_proof",
                producer_id="reference-mission-harness",
                subjects=[
                    {
                        "type": "scenario_atom",
                        "scenario_sha256": SHA_A,
                        "atom_id": "atom-0007",
                    },
                    {
                        "type": "integration_result",
                        "result_sha256": SHA_B,
                    },
                ],
            ),
        ]
    )

    validate_manifest(manifest)
    resolved = verify_bundle(manifest, tmp_path)

    assert set(resolved) == {"native-runtime", "live-proof"}
    assert resolved["native-runtime"] == text_file.resolve()
    assert resolved["live-proof"] == json_file.resolve()


def test_optional_product_and_content_metadata_are_not_required() -> None:
    manifest = _manifest(
        [
            _record(
                record_id="evidence-1",
                path="evidence/runtime.txt",
                sha256=SHA_A,
            )
        ]
    )

    validate_manifest(manifest)


def test_record_ids_must_be_unique_within_one_set() -> None:
    manifest = _manifest(
        [
            _record(record_id="same", path="a.txt", sha256=SHA_A),
            _record(record_id="same", path="b.txt", sha256=SHA_B),
        ]
    )

    with pytest.raises(EvidenceSetContractError, match="record ids must be unique"):
        validate_manifest(manifest)


@pytest.mark.parametrize(
    "path",
    [
        "../outside.txt",
        "a/../outside.txt",
        "/absolute.txt",
        "a//b.txt",
        "C:/absolute.txt",
    ],
)
def test_content_path_must_be_normalized_and_bundle_relative(path: str) -> None:
    manifest = _manifest(
        [_record(record_id="evidence-1", path=path, sha256=SHA_A)]
    )

    with pytest.raises(
        EvidenceSetContractError,
        match="bundle-relative|normalized contained",
    ):
        validate_manifest(manifest)


def test_backslash_path_is_rejected_by_wire_schema() -> None:
    manifest = _manifest(
        [_record(record_id="evidence-1", path="evidence\\runtime.txt", sha256=SHA_A)]
    )

    with pytest.raises(EvidenceSetContractError, match="not conformant"):
        validate_manifest(manifest)


def test_sha256_shape_is_lowercase_exact_hex() -> None:
    manifest = _manifest(
        [_record(record_id="evidence-1", path="evidence/runtime.txt", sha256="A" * 64)]
    )

    with pytest.raises(EvidenceSetContractError, match="not conformant"):
        validate_manifest(manifest)


def test_subject_identity_shape_fails_closed() -> None:
    record = _record(
        record_id="evidence-1",
        path="evidence/runtime.txt",
        sha256=SHA_A,
        subjects=[
            {
                "type": "scenario_atom",
                "scenario_sha256": SHA_A,
            }
        ],
    )
    manifest = _manifest([record])

    with pytest.raises(EvidenceSetContractError, match="not conformant"):
        validate_manifest(manifest)


def test_target_specific_generic_subject_field_is_rejected() -> None:
    record = _record(
        record_id="evidence-1",
        path="evidence/runtime.txt",
        sha256=SHA_A,
        subjects=[
            {
                "type": "integration_artifact",
                "result_sha256": SHA_B,
                "artifact_id": "procedure",
                "cosmos_target": "FPRIME",
            }
        ],
    )
    manifest = _manifest([record])

    with pytest.raises(EvidenceSetContractError, match="not conformant"):
        validate_manifest(manifest)


def test_digest_mismatch_is_bundle_integrity_failure(tmp_path: Path) -> None:
    evidence_file = tmp_path / "runtime.txt"
    evidence_file.write_text("retained bytes\n", encoding="utf-8")
    manifest = _manifest(
        [_record(record_id="runtime", path="runtime.txt", sha256=SHA_A)]
    )

    with pytest.raises(EvidenceSetContractError, match="SHA-256 mismatch"):
        verify_bundle(manifest, tmp_path)


def test_missing_retained_content_is_bundle_integrity_failure(tmp_path: Path) -> None:
    manifest = _manifest(
        [_record(record_id="runtime", path="missing.txt", sha256=SHA_A)]
    )

    with pytest.raises(EvidenceSetContractError, match="content does not exist"):
        verify_bundle(manifest, tmp_path)
