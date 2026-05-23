from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from orbitfabric import __version__
from orbitfabric.export.entity_index import entity_index_to_dict
from orbitfabric.export.model_summary import model_summary_to_dict
from orbitfabric.export.relationship_manifest import relationship_manifest_to_dict
from orbitfabric.lint.finding import LintReport
from orbitfabric.model.mission import MissionModel


def dashboard_summary_to_dict(
    model: MissionModel,
    mission_dir: Path,
    lint_report: LintReport,
) -> dict[str, Any]:
    """Return a deterministic read-only dashboard foundation summary.

    This report intentionally aggregates existing Core-owned facts without
    introducing coverage metrics. Coverage remains unavailable until Core emits
    a dedicated coverage summary surface.
    """
    mission_dir = mission_dir.resolve()
    model_summary = model_summary_to_dict(model, mission_dir)
    entity_index = entity_index_to_dict(model, mission_dir)
    relationship_manifest = relationship_manifest_to_dict(model, mission_dir)

    domains = model_summary["domains"]

    return {
        "dashboard_version": "0.1-candidate",
        "kind": "orbitfabric.dashboard_summary",
        "orbitfabric_version": __version__,
        "mission": model_summary["mission"],
        "source": {
            "mission_dir": str(mission_dir),
            "model_summary_kind": model_summary["kind"],
            "model_summary_version": model_summary["summary_version"],
            "entity_index_kind": entity_index["kind"],
            "entity_index_version": entity_index["index_version"],
            "relationship_manifest_kind": relationship_manifest["kind"],
            "relationship_manifest_version": relationship_manifest[
                "manifest_version"
            ],
        },
        "boundaries": {
            "source_of_truth": "mission_model",
            "core_derived_report": True,
            "read_only": True,
            "contains_dashboard_summary": True,
            "contains_coverage_metrics": False,
            "contains_health_score": False,
            "contains_scenario_run_index": False,
            "contains_expectation_accounting": False,
            "contains_relationship_graph": False,
            "contains_dependency_graph": False,
            "contains_yaml_ast": False,
            "contains_source_locations": False,
            "contains_plugin_api": False,
            "contains_studio_api": False,
            "contains_runtime_behavior": False,
            "contains_ground_behavior": False,
        },
        "validation": {
            "tool": "orbitfabric-lint",
            "result": _lint_result_label(lint_report),
            "errors": lint_report.error_count,
            "warnings": lint_report.warning_count,
            "info": lint_report.info_count,
        },
        "model_domains": {
            "required": _domain_presence_summary(domains, required=True),
            "optional": _domain_presence_summary(domains, required=False),
            "counts": model_summary["counts"],
            "domains": [
                {
                    "id": domain["id"],
                    "display_name": domain["display_name"],
                    "source_file": domain["source_file"],
                    "required": domain["required"],
                    "present": domain["present"],
                    "count": domain["count"],
                }
                for domain in domains
            ],
        },
        "entity_inventory": {
            "total_entities": entity_index["counts"]["total_entities"],
            "domains": entity_index["counts"]["domains"],
        },
        "relationship_inventory": {
            "total_relationships": relationship_manifest["counts"][
                "total_relationships"
            ],
            "relationship_types": relationship_manifest["counts"][
                "relationship_types"
            ],
        },
        "coverage": {
            "status": "not_available",
            "reason": (
                "Coverage metrics are not emitted by OrbitFabric Core "
                "in this report version."
            ),
            "requires_core_output": "coverage_summary.json",
        },
    }


def write_dashboard_summary(
    model: MissionModel,
    mission_dir: Path,
    lint_report: LintReport,
    output_file: Path,
) -> Path:
    """Write a deterministic dashboard summary JSON file."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(
        json.dumps(
            dashboard_summary_to_dict(model, mission_dir, lint_report),
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return output_file


def _domain_presence_summary(
    domains: list[dict[str, Any]],
    *,
    required: bool,
) -> dict[str, int]:
    selected = [domain for domain in domains if domain["required"] is required]
    present = [domain for domain in selected if domain["present"]]

    return {
        "total": len(selected),
        "present": len(present),
        "missing": len(selected) - len(present),
    }


def _lint_result_label(report: LintReport) -> str:
    if report.error_count > 0:
        return "failed"
    if report.warning_count > 0:
        return "passed_with_warnings"
    return "passed"
