from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

MANIFEST_VERSION = "0.2-candidate"
PROTOCOL = "orbitfabric.adapter_cli.v1"
RESULT_VERSION = "0.2-candidate"


class ContractError(ValueError):
    """Raised when an Integration Package boundary is not conformant."""


def _schema_path(name: str) -> Path:
    return Path(__file__).resolve().parents[1] / "contracts" / "integration" / name


def load_json(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"Cannot read JSON {source}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ContractError(f"Expected a JSON object in {source}")
    return payload


def _validate_schema(payload: dict[str, Any], schema_name: str, label: str) -> None:
    schema = load_json(_schema_path(schema_name))
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda item: list(item.absolute_path))
    if not errors:
        return
    details = []
    for error in errors:
        location = ".".join(str(item) for item in error.absolute_path) or "$"
        details.append(f"{location}: {error.message}")
    raise ContractError(f"{label} is not conformant: " + "; ".join(details))


def validate_manifest(manifest: dict[str, Any]) -> None:
    _validate_schema(
        manifest,
        "integration-package-manifest-0.2-candidate.schema.json",
        "Integration Package Manifest",
    )
    operation_ids = [item["id"] for item in manifest["operations"]]
    if len(operation_ids) != len(set(operation_ids)):
        raise ContractError("Integration Package operation ids must be unique")


def operation_requirements(manifest: dict[str, Any], operation_id: str) -> tuple[str, ...]:
    validate_manifest(manifest)
    for operation in manifest["operations"]:
        if operation["id"] == operation_id:
            return tuple(item["role"] for item in operation["input_requirements"])
    raise ContractError(f"Unknown operation: {operation_id}")


def validate_bindings(
    manifest: dict[str, Any], operation_id: str, bound_roles: list[str] | tuple[str, ...]
) -> None:
    expected = operation_requirements(manifest, operation_id)
    actual = tuple(bound_roles)
    if len(actual) != len(set(actual)):
        raise ContractError("Operation input roles must not be bound more than once")
    missing = sorted(set(expected) - set(actual))
    unexpected = sorted(set(actual) - set(expected))
    if missing or unexpected:
        details = []
        if missing:
            details.append("missing required roles: " + ", ".join(missing))
        if unexpected:
            details.append("unexpected roles: " + ", ".join(unexpected))
        raise ContractError("Operation input binding mismatch: " + "; ".join(details))


def validate_result(manifest: dict[str, Any], result: dict[str, Any]) -> None:
    validate_manifest(manifest)
    _validate_schema(
        result,
        "integration-result-0.2-candidate.schema.json",
        "Integration Result",
    )
    if result["result_version"] not in manifest["result_compatibility"]["result_versions"]:
        raise ContractError("Result version is not declared compatible by the package")
    operation_id = result["operation"]["id"]
    expected = operation_requirements(manifest, operation_id)
    records = result["inputs"]["operation_inputs"]
    actual = tuple(item["role"] for item in records)
    if len(actual) != len(set(actual)):
        raise ContractError("Result operation input roles must be unique")
    if set(actual) != set(expected):
        raise ContractError("Result operation input roles do not match manifest requirements")
    if result["result"] == "succeeded" and any(
        item["status"] != "available" for item in records
    ):
        raise ContractError("Successful Results require available provenance for every role")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="orbitfabric-integration-conformance")
    subparsers = parser.add_subparsers(dest="command", required=True)
    manifest = subparsers.add_parser("manifest")
    manifest.add_argument("manifest")
    bindings = subparsers.add_parser("bindings")
    bindings.add_argument("manifest")
    bindings.add_argument("operation")
    bindings.add_argument("--role", action="append", default=[])
    result = subparsers.add_parser("result")
    result.add_argument("manifest")
    result.add_argument("result")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        manifest = load_json(args.manifest)
        if args.command == "manifest":
            validate_manifest(manifest)
        elif args.command == "bindings":
            validate_bindings(manifest, args.operation, args.role)
        else:
            validate_result(manifest, load_json(args.result))
    except ContractError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

