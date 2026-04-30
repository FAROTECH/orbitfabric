from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class LintFinding:
    """A semantic lint finding emitted by the OrbitFabric lint engine."""

    severity: str
    code: str
    message: str
    file: str | None = None
    domain: str | None = None
    object_id: str | None = None
    suggestion: str | None = None

    def format(self) -> str:
        parts = [self.severity, self.code]

        if self.file:
            parts.append(self.file)

        if self.object_id:
            parts.append(self.object_id)

        parts.append(self.message)

        if self.suggestion:
            parts.append(f"Suggestion: {self.suggestion}")

        return " ".join(parts)


@dataclass(frozen=True)
class LintReport:
    """Result of running semantic lint rules against a Mission Model."""

    mission_id: str
    model_version: str
    findings: list[LintFinding] = field(default_factory=list)

    @property
    def error_count(self) -> int:
        return sum(1 for finding in self.findings if finding.severity == "ERROR")

    @property
    def warning_count(self) -> int:
        return sum(1 for finding in self.findings if finding.severity == "WARNING")

    @property
    def info_count(self) -> int:
        return sum(1 for finding in self.findings if finding.severity == "INFO")

    @property
    def has_errors(self) -> bool:
        return self.error_count > 0

    @property
    def result_label(self) -> str:
        if self.error_count > 0:
            return "FAILED"
        if self.warning_count > 0:
            return "PASSED WITH WARNINGS"
        return "PASSED"