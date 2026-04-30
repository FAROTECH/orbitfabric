from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelDiagnostic:
    """Diagnostic emitted while loading or validating a Mission Model."""

    severity: str
    code: str
    message: str
    file: str | None = None
    domain: str | None = None
    object_id: str | None = None

    def format(self) -> str:
        parts = [self.severity, self.code]

        if self.file:
            parts.append(self.file)

        if self.object_id:
            parts.append(self.object_id)

        parts.append(self.message)
        return " ".join(parts)


class MissionModelError(Exception):
    """Raised when a Mission Model cannot be loaded or validated."""

    def __init__(self, diagnostics: list[ModelDiagnostic]) -> None:
        self.diagnostics = diagnostics
        message = "Mission Model validation failed"
        if diagnostics:
            message = diagnostics[0].format()
        super().__init__(message)