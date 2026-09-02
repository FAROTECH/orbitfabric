from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

DESCRIPTOR_VERSION = "0.1-candidate"


class AdapterReleaseContractError(ValueError):
    """Raised when an Adapter Release Descriptor is not conformant."""


def _schema_path() -> Path:
    return (
        Path(__file__).resolve().parents[1]
        / "contracts"
        / "adapter_management"
        / "adapter-release-descriptor-0.1-candidate.schema.json"
    )


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AdapterReleaseContractError(f"Cannot read JSON {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise AdapterReleaseContractError(f"Expected a JSON object in {path}")
    return payload


def validate_release_descriptor(payload: dict[str, Any]) -> None:
    """Validate the public Adapter Release Descriptor candidate contract."""
    schema = _load_json(_schema_path())
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda item: list(item.absolute_path))
    if errors:
        details = []
        for error in errors:
            location = ".".join(str(item) for item in error.absolute_path) or "$"
            details.append(f"{location}: {error.message}")
        raise AdapterReleaseContractError(
            "Adapter Release Descriptor is not conformant: " + "; ".join(details)
        )

    artifact_ids = [artifact["id"] for artifact in payload["artifacts"]]
    if len(artifact_ids) != len(set(artifact_ids)):
        raise AdapterReleaseContractError(
            "Adapter Release Descriptor artifact ids must be unique"
        )


def load_release_descriptor(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    payload = _load_json(source)
    validate_release_descriptor(payload)
    return payload


__all__ = [
    "AdapterReleaseContractError",
    "DESCRIPTOR_VERSION",
    "load_release_descriptor",
    "validate_release_descriptor",
]
