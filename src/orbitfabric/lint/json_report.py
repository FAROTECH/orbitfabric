from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from orbitfabric import __version__
from orbitfabric.lint.finding import LintFinding, LintReport
from orbitfabric.model.mission import MissionModel


def lint_report_to_dict(model: MissionModel, report: LintReport) -> dict[str, Any]:
    """Convert a lint report to a stable JSON-serializable dictionary."""
    return {
        "tool": "orbitfabric-lint",
        "version": __version__,
        "mission": report.mission_id,
        "model_version": report.model_version,
        "result": _json_result_label(report),
        "loaded": {
            "spacecraft": 1,
            "subsystems": len(model.subsystems),
            "modes": len(model.modes),
            "mode_transitions": len(model.mode_transitions),
            "telemetry": len(model.telemetry),
            "commands": len(model.commands),
            "events": len(model.events),
            "faults": len(model.faults),
            "packets": len(model.packets),
        },
        "summary": {
            "errors": report.error_count,
            "warnings": report.warning_count,
            "info": report.info_count,
        },
        "findings": [_finding_to_dict(finding) for finding in report.findings],
    }


def write_lint_report_json(
    model: MissionModel,
    report: LintReport,
    output_path: Path,
) -> None:
    """Write a lint report JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = lint_report_to_dict(model, report)

    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _finding_to_dict(finding: LintFinding) -> dict[str, str | None]:
    return {
        "severity": finding.severity,
        "code": finding.code,
        "file": finding.file,
        "domain": finding.domain,
        "object_id": finding.object_id,
        "message": finding.message,
        "suggestion": finding.suggestion,
    }


def _json_result_label(report: LintReport) -> str:
    if report.error_count > 0:
        return "failed"
    if report.warning_count > 0:
        return "passed_with_warnings"
    return "passed"