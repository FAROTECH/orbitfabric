from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

LOCK_VERSION = "0.1-candidate"


class AdapterProjectLockContractError(ValueError):
    """Raised when an Adapter Project Lock is not conformant."""


def _schema_path() -> Path:
    return (
        Path(__file__).resolve().parents[1]
        / "contracts"
        / "adapter_management"
        / "adapter-project-lock-0.1-candidate.schema.json"
    )


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AdapterProjectLockContractError(f"Cannot read JSON {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise AdapterProjectLockContractError(f"Expected a JSON object in {path}")
    return payload


def validate_project_lock(payload: dict[str, Any]) -> None:
    """Validate the public Adapter Project Lock candidate contract."""
    schema = _load_json(_schema_path())
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda item: list(item.absolute_path))
    if errors:
        details = []
        for error in errors:
            location = ".".join(str(item) for item in error.absolute_path) or "$"
            details.append(f"{location}: {error.message}")
        raise AdapterProjectLockContractError(
            "Adapter Project Lock is not conformant: " + "; ".join(details)
        )

    coordinates = [
        (
            item["source_coordinate"]["authority"],
            item["source_coordinate"]["publisher"],
            item["source_coordinate"]["name"],
        )
        for item in payload["adapters"]
    ]
    if len(coordinates) != len(set(coordinates)):
        raise AdapterProjectLockContractError(
            "Adapter Project Lock Source Coordinates must be unique"
        )


def load_project_lock(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    payload = _load_json(source)
    validate_project_lock(payload)
    return payload


__all__ = [
    "AdapterProjectLockContractError",
    "LOCK_VERSION",
    "load_project_lock",
    "validate_project_lock",
]
