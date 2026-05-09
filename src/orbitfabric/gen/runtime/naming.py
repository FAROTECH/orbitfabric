from __future__ import annotations

import re

_IDENTIFIER_PARTS = re.compile(r"[A-Za-z0-9]+")


def to_pascal_case(model_id: str) -> str:
    """Convert a Mission Model identifier to a deterministic PascalCase symbol."""
    parts = _identifier_parts(model_id)
    if not parts:
        return "Unnamed"

    return "".join(_pascal_part(part) for part in parts)


def to_camel_case(model_id: str) -> str:
    """Convert a Mission Model identifier to a deterministic camelCase symbol."""
    pascal = to_pascal_case(model_id)
    return pascal[:1].lower() + pascal[1:]


def _identifier_parts(model_id: str) -> list[str]:
    return _IDENTIFIER_PARTS.findall(model_id)


def _pascal_part(part: str) -> str:
    if not part:
        return ""

    if part[0].isdigit():
        part = f"N{part}"

    if part.isupper() or part.islower():
        return part[:1].upper() + part[1:].lower()

    return part[:1].upper() + part[1:]
