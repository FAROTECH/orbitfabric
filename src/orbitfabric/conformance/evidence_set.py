from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

MANIFEST_KIND = "orbitfabric.evidence_set_manifest"
MANIFEST_VERSION = "0.1-candidate"


class EvidenceSetContractError(ValueError):
    """Raised when an Evidence Set Manifest or retained bundle is not conformant."""


def _schema_path() -> Path:
    return (
        Path(__file__).resolve().parents[1]
        / "contracts"
        / "evidence"
        / "evidence-set-manifest-0.1-candidate.schema.json"
    )


def load_json(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvidenceSetContractError(f"Cannot read JSON {source}: {exc}") from exc
    if not isinstance(payload, dict):
        raise EvidenceSetContractError(f"Expected a JSON object in {source}")
    return payload


def validate_manifest(manifest: dict[str, Any]) -> None:
    """Validate the generic Evidence Set wire contract and local semantic constraints."""
    schema = load_json(_schema_path())
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    errors = sorted(
        validator.iter_errors(manifest),
        key=lambda item: list(item.absolute_path),
    )
    if errors:
        details = []
        for error in errors:
            location = ".".join(str(item) for item in error.absolute_path) or "$"
            details.append(f"{location}: {error.message}")
        raise EvidenceSetContractError(
            "Evidence Set Manifest is not conformant: " + "; ".join(details)
        )

    record_ids = [record["id"] for record in manifest["records"]]
    if len(record_ids) != len(set(record_ids)):
        raise EvidenceSetContractError("Evidence Set record ids must be unique within the set")

    for record in manifest["records"]:
        _validate_bundle_relative_path(record["content"]["reference"]["path"])


def verify_bundle(manifest: dict[str, Any], bundle_root: str | Path) -> dict[str, Path]:
    """Verify retained evidence paths and exact bytes under one local bundle root."""
    validate_manifest(manifest)

    root = Path(bundle_root).resolve()
    if not root.exists() or not root.is_dir():
        raise EvidenceSetContractError(
            f"Evidence Set bundle root does not exist or is not a directory: {root}"
        )

    resolved: dict[str, Path] = {}
    for record in manifest["records"]:
        record_id = record["id"]
        reference = record["content"]["reference"]
        relative_path = reference["path"]
        candidate = (root / relative_path).resolve()

        if not candidate.is_relative_to(root):
            raise EvidenceSetContractError(
                f"Evidence record {record_id!r} resolves outside the bundle root"
            )
        if not candidate.exists() or not candidate.is_file():
            raise EvidenceSetContractError(
                f"Evidence record {record_id!r} content does not exist: {relative_path}"
            )

        try:
            actual_sha256 = hashlib.sha256(candidate.read_bytes()).hexdigest()
        except OSError as exc:
            raise EvidenceSetContractError(
                f"Cannot read evidence record {record_id!r} content: {exc}"
            ) from exc

        expected_sha256 = reference["sha256"]
        if actual_sha256 != expected_sha256:
            raise EvidenceSetContractError(
                f"Evidence record {record_id!r} SHA-256 mismatch: "
                f"expected {expected_sha256}, got {actual_sha256}"
            )
        resolved[record_id] = candidate

    return resolved


def _validate_bundle_relative_path(value: str) -> None:
    if value.startswith("/") or _looks_like_windows_absolute_path(value):
        raise EvidenceSetContractError(
            f"Evidence content path must be bundle-relative: {value!r}"
        )

    parts = value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise EvidenceSetContractError(
            f"Evidence content path must be a normalized contained path: {value!r}"
        )


def _looks_like_windows_absolute_path(value: str) -> bool:
    return len(value) >= 2 and value[0].isalpha() and value[1] == ":"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="orbitfabric-evidence-set-conformance")
    subparsers = parser.add_subparsers(dest="command", required=True)

    manifest_parser = subparsers.add_parser("manifest")
    manifest_parser.add_argument("manifest")

    bundle_parser = subparsers.add_parser("bundle")
    bundle_parser.add_argument("manifest")
    bundle_parser.add_argument("bundle_root")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        manifest = load_json(args.manifest)
        if args.command == "manifest":
            validate_manifest(manifest)
        else:
            verify_bundle(manifest, args.bundle_root)
    except EvidenceSetContractError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
