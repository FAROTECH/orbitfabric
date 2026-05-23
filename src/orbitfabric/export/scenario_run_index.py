from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from orbitfabric import __version__


def scenario_run_index_to_dict(simulation_reports_dir: Path) -> dict[str, Any]:
    """Return a deterministic index of Core simulation JSON reports.

    The index reads only JSON files produced by `orbitfabric-sim`.
    Plain-text logs and non-simulation JSON files are intentionally ignored.
    """
    reports_dir = simulation_reports_dir.resolve()
    runs = _load_simulation_runs(reports_dir)

    return {
        "index_version": "0.1-candidate",
        "kind": "orbitfabric.scenario_run_index",
        "orbitfabric_version": __version__,
        "source": {
            "simulation_reports_dir": str(reports_dir),
            "input_report_tool": "orbitfabric-sim",
        },
        "boundaries": {
            "source_of_truth": "simulation_json_reports",
            "core_derived_report": True,
            "read_only": True,
            "contains_scenario_run_index": True,
            "contains_coverage_metrics": False,
            "contains_health_score": False,
            "contains_expectation_accounting": False,
            "contains_relationship_graph": False,
            "contains_dependency_graph": False,
            "contains_yaml_ast": False,
            "contains_source_locations": False,
            "contains_plugin_api": False,
            "contains_studio_api": False,
            "contains_runtime_behavior": False,
            "contains_ground_behavior": False,
            "derived_from_simulation_json": True,
            "derived_from_logs": False,
        },
        "summary": _summary(runs),
        "runs": runs,
    }


def write_scenario_run_index(
    simulation_reports_dir: Path,
    output_file: Path,
) -> Path:
    """Write a deterministic scenario run index JSON file."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(
        json.dumps(
            scenario_run_index_to_dict(simulation_reports_dir),
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return output_file


def _load_simulation_runs(reports_dir: Path) -> list[dict[str, Any]]:
    runs = []

    for report_file in sorted(reports_dir.glob("*.json")):
        payload = _read_json(report_file)
        if payload.get("tool") != "orbitfabric-sim":
            continue

        runs.append(_run_record(report_file, payload))

    return sorted(
        runs,
        key=lambda run: (
            run["mission"],
            run["scenario"],
            run["report_file"],
        ),
    )


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON report: {path}") from exc

    if not isinstance(payload, dict):
        raise ValueError(f"JSON report must be an object: {path}")

    return payload


def _run_record(report_file: Path, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "report_file": report_file.name,
        "report_path": str(report_file.resolve()),
        "mission": _required_string(payload, "mission", report_file),
        "scenario": _required_string(payload, "scenario", report_file),
        "result": _required_string(payload, "result", report_file),
        "summary": _summary_object(payload, report_file),
    }


def _required_string(
    payload: dict[str, Any],
    field: str,
    report_file: Path,
) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value:
        raise ValueError(f"simulation report {report_file} must contain string field {field}")
    return value


def _summary_object(payload: dict[str, Any], report_file: Path) -> dict[str, Any]:
    summary = payload.get("summary")
    if not isinstance(summary, dict):
        raise ValueError(f"simulation report {report_file} must contain summary object")

    return {
        key: summary[key]
        for key in sorted(summary)
        if isinstance(summary[key], int)
    }


def _summary(runs: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(1 for run in runs if run["result"] == "passed")
    failed = sum(1 for run in runs if run["result"] == "failed")

    return {
        "total": len(runs),
        "passed": passed,
        "failed": failed,
    }
