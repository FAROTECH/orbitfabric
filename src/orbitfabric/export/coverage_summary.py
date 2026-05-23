from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from orbitfabric import __version__

SUPPORTED_ENTITY_DOMAINS = ("commands", "events", "data_products")
SUPPORTED_RELATIONSHIP_TYPES = (
    "data_product_produced_by_payload",
    "data_product_produced_by_subsystem",
    "downlink_flow_includes_data_product",
)


def coverage_summary_to_dict(
    mission_dir: Path,
    entity_index_file: Path,
    relationship_manifest_file: Path,
    scenario_run_index_file: Path,
) -> dict[str, Any]:
    """Return a deterministic Core-owned coverage summary.

    Coverage is derived from structured Core outputs only:

    - entity_index.json;
    - relationship_manifest.json;
    - scenario_run_index.json;
    - simulation JSON reports referenced by the scenario run index.

    Plain-text logs, raw YAML scanning and downstream UI state are intentionally
    excluded from the derivation path.
    """
    entity_index = _load_json_object(entity_index_file)
    relationship_manifest = _load_json_object(relationship_manifest_file)
    scenario_run_index = _load_json_object(scenario_run_index_file)

    _require_kind(entity_index, "orbitfabric.entity_index", entity_index_file)
    _require_kind(
        relationship_manifest,
        "orbitfabric.relationship_manifest",
        relationship_manifest_file,
    )
    _require_kind(
        scenario_run_index,
        "orbitfabric.scenario_run_index",
        scenario_run_index_file,
    )

    reports = _load_simulation_reports(scenario_run_index)
    observations = _observations_from_reports(reports)

    relationships = relationship_manifest.get("relationships", [])
    if not isinstance(relationships, list):
        raise ValueError("relationship_manifest.json must contain relationships array")

    return {
        "coverage_version": "0.1-candidate",
        "kind": "orbitfabric.coverage_summary",
        "orbitfabric_version": __version__,
        "mission": entity_index["mission"],
        "source": {
            "mission_dir": str(mission_dir.resolve()),
            "entity_index": str(entity_index_file.resolve()),
            "entity_index_kind": entity_index["kind"],
            "entity_index_version": entity_index["index_version"],
            "relationship_manifest": str(relationship_manifest_file.resolve()),
            "relationship_manifest_kind": relationship_manifest["kind"],
            "relationship_manifest_version": relationship_manifest["manifest_version"],
            "scenario_run_index": str(scenario_run_index_file.resolve()),
            "scenario_run_index_kind": scenario_run_index["kind"],
            "scenario_run_index_version": scenario_run_index["index_version"],
        },
        "boundaries": {
            "source_of_truth": "core_structured_outputs",
            "core_derived_report": True,
            "read_only": True,
            "contains_coverage_metrics": True,
            "contains_health_score": False,
            "contains_model_completeness_score": False,
            "contains_relationship_graph": False,
            "contains_dependency_graph": False,
            "contains_yaml_ast": False,
            "contains_source_locations": False,
            "contains_plugin_api": False,
            "contains_studio_api": False,
            "contains_runtime_behavior": False,
            "contains_ground_behavior": False,
            "coverage_derived_from_entity_index": True,
            "coverage_derived_from_relationship_manifest": True,
            "coverage_derived_from_scenario_run_index": True,
            "coverage_derived_from_simulation_json": True,
            "coverage_derived_from_logs": False,
        },
        "scenario_runs": scenario_run_index["summary"],
        "entity_coverage": _entity_coverage(entity_index, observations),
        "expectation_coverage": _expectation_coverage(observations),
        "relationship_coverage": _relationship_coverage(relationships, observations),
        "unsupported": _unsupported(relationships),
    }


def write_coverage_summary(
    mission_dir: Path,
    entity_index_file: Path,
    relationship_manifest_file: Path,
    scenario_run_index_file: Path,
    output_file: Path,
) -> Path:
    """Write a deterministic coverage summary JSON file."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(
        json.dumps(
            coverage_summary_to_dict(
                mission_dir,
                entity_index_file,
                relationship_manifest_file,
                scenario_run_index_file,
            ),
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return output_file


def _entity_coverage(
    entity_index: dict[str, Any],
    observations: dict[str, Any],
) -> dict[str, Any]:
    entities = entity_index.get("entities", [])
    if not isinstance(entities, list):
        raise ValueError("entity_index.json must contain entities array")

    declared_by_domain = {
        domain: sorted(
            entity["id"]
            for entity in entities
            if entity.get("domain") == domain and isinstance(entity.get("id"), str)
        )
        for domain in SUPPORTED_ENTITY_DOMAINS
    }

    observed_by_domain = {
        "commands": observations["commands"],
        "events": observations["events"],
        "data_products": observations["data_products"],
    }

    return {
        domain: _coverage_record(
            declared_ids=declared_by_domain[domain],
            covered_ids=observed_by_domain[domain],
        )
        for domain in SUPPORTED_ENTITY_DOMAINS
    }


def _expectation_coverage(observations: dict[str, Any]) -> dict[str, Any]:
    records = observations["expectations"]
    by_type: dict[str, dict[str, int | float | None]] = {}

    for record in records:
        expectation_type = record.get("expectation_type")
        if not isinstance(expectation_type, str):
            continue

        bucket = by_type.setdefault(
            expectation_type,
            {"total": 0, "passed": 0, "failed": 0, "pass_ratio": None},
        )
        bucket["total"] += 1
        if record.get("result") == "passed":
            bucket["passed"] += 1
        elif record.get("result") == "failed":
            bucket["failed"] += 1

    for bucket in by_type.values():
        bucket["pass_ratio"] = _ratio(bucket["passed"], bucket["total"])

    total = len(records)
    passed = sum(1 for record in records if record.get("result") == "passed")
    failed = sum(1 for record in records if record.get("result") == "failed")

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_ratio": _ratio(passed, total),
        "by_type": dict(sorted(by_type.items())),
    }


def _relationship_coverage(
    relationships: list[dict[str, Any]],
    observations: dict[str, Any],
) -> dict[str, Any]:
    supported = [
        relationship
        for relationship in relationships
        if relationship.get("relationship_type") in SUPPORTED_RELATIONSHIP_TYPES
    ]
    covered_ids = {
        relationship["relationship_id"]
        for relationship in supported
        if _relationship_is_covered(relationship, observations)
    }
    declared_ids = sorted(
        relationship["relationship_id"]
        for relationship in supported
        if isinstance(relationship.get("relationship_id"), str)
    )

    by_type = {
        relationship_type: _coverage_record(
            declared_ids=[
                relationship["relationship_id"]
                for relationship in supported
                if relationship.get("relationship_type") == relationship_type
            ],
            covered_ids=covered_ids,
        )
        for relationship_type in SUPPORTED_RELATIONSHIP_TYPES
    }

    aggregate = _coverage_record(
        declared_ids=declared_ids,
        covered_ids=covered_ids,
    )

    return {
        "supported_relationship_types": list(SUPPORTED_RELATIONSHIP_TYPES),
        "total_supported_relationships": aggregate["total"],
        "covered_supported_relationships": aggregate["covered"],
        "uncovered_supported_relationships": aggregate["uncovered"],
        "coverage_ratio": aggregate["coverage_ratio"],
        "covered_relationship_ids": aggregate["covered_ids"],
        "uncovered_relationship_ids": aggregate["uncovered_ids"],
        "by_type": by_type,
    }


def _unsupported(relationships: list[dict[str, Any]]) -> dict[str, Any]:
    relationship_types = sorted(
        {
            relationship["relationship_type"]
            for relationship in relationships
            if isinstance(relationship.get("relationship_type"), str)
        }
        - set(SUPPORTED_RELATIONSHIP_TYPES)
    )

    return {
        "entity_domains": [
            "spacecraft",
            "subsystems",
            "modes",
            "telemetry",
            "faults",
            "packets",
            "payloads",
            "contact_profiles",
            "link_profiles",
            "contact_windows",
            "downlink_flows",
            "command_sources",
            "commandability_rules",
            "autonomous_actions",
            "recovery_intents",
        ],
        "relationship_types": relationship_types,
        "reason": (
            "Coverage is emitted only for domains and relationship families "
            "with direct evidence in current simulation JSON reports."
        ),
    }


def _relationship_is_covered(
    relationship: dict[str, Any],
    observations: dict[str, Any],
) -> bool:
    relationship_type = relationship.get("relationship_type")
    source = relationship.get("from", {})
    target = relationship.get("to", {})

    if not isinstance(source, dict) or not isinstance(target, dict):
        return False

    source_id = source.get("id")
    target_id = target.get("id")

    if relationship_type in {
        "data_product_produced_by_payload",
        "data_product_produced_by_subsystem",
    }:
        return source_id in observations["data_products"]

    if relationship_type == "downlink_flow_includes_data_product":
        return (source_id, target_id) in observations["downlink_flow_data_products"]

    return False


def _coverage_record(
    declared_ids: list[str],
    covered_ids: set[str],
) -> dict[str, Any]:
    declared = sorted(set(declared_ids))
    covered = sorted(item for item in declared if item in covered_ids)
    uncovered = sorted(item for item in declared if item not in covered_ids)

    return {
        "total": len(declared),
        "covered": len(covered),
        "uncovered": len(uncovered),
        "coverage_ratio": _ratio(len(covered), len(declared)),
        "covered_ids": covered,
        "uncovered_ids": uncovered,
    }


def _observations_from_reports(reports: list[dict[str, Any]]) -> dict[str, Any]:
    commands: set[str] = set()
    events: set[str] = set()
    data_products: set[str] = set()
    downlink_flow_data_products: set[tuple[str, str]] = set()
    expectations: list[dict[str, Any]] = []

    for report in reports:
        for command in _list_field(report, "commands"):
            command_id = command.get("command_id")
            if isinstance(command_id, str):
                commands.add(command_id)

        for event in _list_field(report, "events"):
            event_id = event.get("event_id")
            if isinstance(event_id, str):
                events.add(event_id)

        for evidence in _list_field(report, "data_flow_evidence"):
            data_product_id = evidence.get("data_product_id")
            if isinstance(data_product_id, str):
                data_products.add(data_product_id)

                for flow_id in evidence.get("eligible_downlink_flows", []):
                    if isinstance(flow_id, str):
                        downlink_flow_data_products.add((flow_id, data_product_id))

        expectation_section = report.get("expectations", {})
        if isinstance(expectation_section, dict):
            for record in expectation_section.get("records", []):
                if isinstance(record, dict):
                    expectations.append(record)

    return {
        "commands": commands,
        "events": events,
        "data_products": data_products,
        "downlink_flow_data_products": downlink_flow_data_products,
        "expectations": expectations,
    }


def _load_simulation_reports(
    scenario_run_index: dict[str, Any],
) -> list[dict[str, Any]]:
    runs = scenario_run_index.get("runs")
    if not isinstance(runs, list):
        raise ValueError("scenario_run_index.json must contain runs array")

    reports = []
    for run in runs:
        if not isinstance(run, dict):
            continue

        report_path = run.get("report_path")
        if not isinstance(report_path, str):
            raise ValueError("scenario run must contain report_path")

        report_file = Path(report_path)
        report = _load_json_object(report_file)
        if report.get("tool") != "orbitfabric-sim":
            raise ValueError(f"not a simulation JSON report: {report_file}")
        reports.append(report)

    return reports


def _load_json_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON file: {path}") from exc

    if not isinstance(payload, dict):
        raise ValueError(f"JSON file must contain an object: {path}")

    return payload


def _require_kind(payload: dict[str, Any], expected_kind: str, path: Path) -> None:
    if payload.get("kind") != expected_kind:
        raise ValueError(f"{path} must have kind {expected_kind}")


def _list_field(payload: dict[str, Any], field: str) -> list[dict[str, Any]]:
    values = payload.get(field, [])
    if not isinstance(values, list):
        return []

    return [item for item in values if isinstance(item, dict)]


def _ratio(part: int, total: int) -> float | None:
    if total == 0:
        return None
    return round(part / total, 6)
