from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ACCOUNTING_KIND = "orbitfabric.scenario_projection_accounting"
ACCOUNTING_VERSION = "0.1-candidate"
RESULT_VERSION = "0.2-candidate"


class ScenarioProjectionAccountingError(ValueError):
    """Raised when Scenario Projection Accounting conformance fails."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def _fail(code: str, message: str) -> None:
    raise ScenarioProjectionAccountingError(code, message)


def _schema_path(name: str) -> Path:
    return Path(__file__).resolve().parents[1] / "contracts" / "integration" / name


def _load_object(path: str | Path, domain: str) -> tuple[dict[str, Any], bytes]:
    source = Path(path)
    try:
        raw = source.read_bytes()
        value = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        _fail(f"{domain}.json", f"Cannot read UTF-8 JSON {source}: {exc}")
    if not isinstance(value, dict):
        _fail(f"{domain}.json", f"Expected a JSON object in {source}")
    return value, raw


def _schema_errors(value: dict[str, Any], schema_name: str) -> list[str]:
    schema, _ = _load_object(_schema_path(schema_name), "schema")
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    return [
        f"{'.'.join(str(part) for part in error.absolute_path) or '$'}: {error.message}"
        for error in sorted(validator.iter_errors(value), key=lambda item: list(item.absolute_path))
    ]


def validate_accounting(accounting: dict[str, Any]) -> None:
    """Validate the independently versioned payload and key uniqueness."""
    if (
        accounting.get("kind") == ACCOUNTING_KIND
        and isinstance(accounting.get("accounting_version"), str)
        and accounting["accounting_version"] != ACCOUNTING_VERSION
    ):
        _fail("surface.unsupported_version", "Unsupported accounting surface version")
    errors = _schema_errors(
        accounting, "scenario-projection-accounting-0.1-candidate.schema.json"
    )
    if errors:
        _fail(
            "sidecar.schema",
            "Scenario Projection Accounting is not conformant: " + "; ".join(errors),
        )
    atom_ids = [record["atom_id"] for record in accounting["records"]]
    if len(atom_ids) != len(set(atom_ids)):
        _fail("sidecar.duplicate_atom", "Each exact atom has at most one accounting record")


def _artifact(parent: dict[str, Any], artifact_id: str) -> dict[str, Any]:
    errors = _schema_errors(parent, "integration-result-0.2-candidate.schema.json")
    if errors:
        _fail("parent.schema", "Integration Result is not conformant: " + "; ".join(errors))
    if parent.get("result_version") != RESULT_VERSION:
        _fail("parent.contract", "Accounting requires Integration Result 0.2-candidate")
    matches = [
        value for value in parent.get("artifacts", [])
        if isinstance(value, dict) and value.get("id") == artifact_id
    ]
    if len(matches) != 1:
        _fail("parent.artifact", "Select exactly one parent-owned artifact id")
    artifact = matches[0]
    if (
        artifact.get("kind") != ACCOUNTING_KIND
        or artifact.get("status") != "generated"
        or artifact.get("media_type") != "application/json"
    ):
        _fail("parent.artifact_contract", "Expected a generated JSON accounting artifact")
    digest = artifact.get("sha256")
    if (
        not isinstance(digest, str)
        or len(digest) != 64
        or any(c not in "0123456789abcdef" for c in digest)
    ):
        _fail("parent.artifact_digest", "Artifact must declare a lowercase SHA-256 digest")
    path = artifact.get("path")
    if not isinstance(path, str) or not path or "\\" in path or ":" in path:
        _fail("parent.artifact_path", "Artifact path must be portable and bundle-relative")
    if any(part in {"", ".", ".."} for part in path.split("/")):
        _fail("parent.artifact_path", "Artifact path must be normalized and bundle-relative")
    return artifact


def validate_parent(
    accounting: dict[str, Any], parent: dict[str, Any], artifact_id: str
) -> dict[str, Any]:
    """Validate ownership and references against the exact parent Result."""
    validate_accounting(accounting)
    artifact = _artifact(parent, artifact_id)
    inputs = parent["inputs"]["operation_inputs"]
    if (
        len(inputs) != 1
        or inputs[0].get("role") != "scenario"
        or inputs[0].get("status") != "available"
    ):
        _fail("parent.scenario_input", "Parent must explicitly consume one available Scenario")
    if (
        inputs[0].get("id") != accounting["scenario"]["id"]
        or inputs[0].get("sha256") != accounting["scenario"]["sha256"]
    ):
        _fail("parent.scenario_identity", "Accounting Scenario differs from parent provenance")
    mappings = parent.get("mappings")
    if not isinstance(mappings, list) or not all(
        isinstance(item, dict) and isinstance(item.get("id"), str) and item["id"]
        for item in mappings
    ):
        _fail("parent.mappings", "Parent must declare explicit mapping identities")
    mapping_ids = [item["id"] for item in mappings]
    if len(mapping_ids) != len(set(mapping_ids)):
        _fail("parent.duplicate_mapping", "Parent mapping identities are ambiguous")
    referenced = {
        mapping_id
        for record in accounting["records"]
        for mapping_id in record["mapping_ids"]
    }
    unknown = sorted(referenced - set(mapping_ids))
    if unknown:
        _fail(
            "parent.unknown_mapping",
            f"Mappings do not belong to parent Result: {', '.join(unknown)}",
        )
    derived = artifact.get("derived_from_mappings")
    if (
        not isinstance(derived, list)
        or len(derived) != len(set(derived))
        or set(derived) != referenced
    ):
        _fail("parent.artifact_mappings", "Artifact mapping list must equal payload mapping union")
    return artifact


def validate_scenario(
    accounting: dict[str, Any], declaration: dict[str, Any]
) -> tuple[str, ...]:
    """Validate exact Scenario source and atom inventory."""
    validate_accounting(accounting)
    if (
        declaration.get("kind") != "orbitfabric.scenario_declaration"
        or declaration.get("declaration_version") != "0.1-candidate"
        or declaration.get("result") != "loaded"
        or not isinstance(declaration.get("atoms"), list)
    ):
        _fail("scenario.contract", "Require a loaded Core Scenario Declaration 0.1-candidate")
    if (
        declaration.get("scenario", {}).get("id") != accounting["scenario"]["id"]
        or declaration.get("source", {}).get("scenario_sha256")
        != accounting["scenario"]["sha256"]
    ):
        _fail("scenario.identity", "Accounting and Declaration identify different Scenario sources")
    atom_ids = [
        atom.get("id") for atom in declaration["atoms"] if isinstance(atom, dict)
    ]
    if (
        any(not isinstance(atom_id, str) or not atom_id for atom_id in atom_ids)
        or len(atom_ids) != len(declaration["atoms"])
        or len(atom_ids) != len(set(atom_ids))
        or declaration.get("atom_count") != len(atom_ids)
    ):
        _fail("scenario.accounting", "Invalid Scenario Declaration atom inventory")
    recorded = {record["atom_id"] for record in accounting["records"]}
    unknown = sorted(recorded - set(atom_ids))
    if unknown:
        _fail("scenario.unknown_atom", f"Unknown Scenario atoms: {', '.join(unknown)}")
    missing = tuple(atom_id for atom_id in atom_ids if atom_id not in recorded)
    if accounting["completeness"] == "complete" and missing:
        _fail("scenario.missing_atom", f"Complete accounting omits: {', '.join(missing)}")
    return missing


def verify_bundle(
    result_path: str | Path,
    artifact_id: str,
    declaration_path: str | Path,
    *,
    expected_result_sha256: str | None = None,
) -> dict[str, Any]:
    """Verify all four conformance domains using exact retained bytes."""
    parent, result_bytes = _load_object(result_path, "parent")
    result_sha256 = hashlib.sha256(result_bytes).hexdigest()
    if expected_result_sha256 is not None and result_sha256 != expected_result_sha256:
        _fail("integrity.result_digest", "Selected Result bytes do not match expected identity")
    artifact = _artifact(parent, artifact_id)
    root = Path(result_path).resolve().parent
    candidate = (root / artifact["path"]).resolve()
    if not candidate.is_relative_to(root):
        _fail("integrity.containment", "Accounting artifact resolves outside Result bundle")
    if not candidate.exists():
        _fail("integrity.missing_file", "Accounting artifact does not exist")
    if not candidate.is_file():
        _fail("integrity.not_file", "Accounting artifact is not a regular file")
    accounting, artifact_bytes = _load_object(candidate, "sidecar")
    if hashlib.sha256(artifact_bytes).hexdigest() != artifact["sha256"]:
        _fail("integrity.artifact_digest", "Accounting artifact digest does not match parent")
    validate_parent(accounting, parent, artifact_id)
    declaration, _ = _load_object(declaration_path, "scenario")
    missing = validate_scenario(accounting, declaration)
    mission = parent.get("mission", {})
    declared_mission = declaration.get("mission", {})
    if (
        mission.get("status") != "available"
        or mission.get("id") != declared_mission.get("id")
        or mission.get("model_version") != declared_mission.get("model_version")
    ):
        _fail("parent.mission", "Parent and Declaration mission binding differs")
    return {
        "identity": {
            "result_sha256": result_sha256,
            "artifact_id": artifact_id,
            "artifact_sha256": artifact["sha256"],
        },
        "completeness": accounting["completeness"],
        "unaccounted_atom_ids": list(missing),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="orbitfabric-scenario-projection-accounting")
    parser.add_argument("result")
    parser.add_argument("artifact_id")
    parser.add_argument("scenario_declaration")
    parser.add_argument("--result-sha256")
    args = parser.parse_args(argv)
    try:
        outcome = verify_bundle(
            args.result,
            args.artifact_id,
            args.scenario_declaration,
            expected_result_sha256=args.result_sha256,
        )
    except ScenarioProjectionAccountingError as exc:
        print(json.dumps({"code": exc.code, "message": str(exc)}), file=sys.stderr)
        return 1
    print(json.dumps(outcome, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
