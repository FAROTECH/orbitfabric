from __future__ import annotations

from typing import Any


def json_safe(value: Any) -> Any:
    """Return a JSON-compatible representation of nested Python values."""
    if isinstance(value, dict):
        return {key: json_safe(item) for key, item in value.items()}

    if isinstance(value, tuple | list):
        return [json_safe(item) for item in value]

    return value
