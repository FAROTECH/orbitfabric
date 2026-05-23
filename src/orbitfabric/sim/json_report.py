from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from orbitfabric import __version__
from orbitfabric.sim.state import (
    SimDataFlowEvidenceRecord,
    SimExpectationRecord,
    SimulationResult,
)


def simulation_result_to_dict(result: SimulationResult) -> dict[str, Any]:
    """Convert a simulation result to a stable JSON-serializable dictionary."""
    return {
        "tool": "orbitfabric-sim",
        "version": __version__,
        "mission": result.mission_id,
        "scenario": result.scenario_id,
        "result": _json_result_label(result),
        "summary": {
            "events": len(result.state.events),
            "commands": len(result.state.commands),
            "mode_transitions": len(result.state.mode_transitions),
            "data_flow_evidence": len(result.state.data_flow_evidence),
            "expectations": len(result.state.expectations),
            "passed_expectations": _expectation_count(result, "passed"),
            "failed_expectations": len(result.state.failed_expectations),
        },
        "timeline": [
            {
                "t": entry.t,
                "time": entry.format()[1:6],
                "message": entry.message,
                "rendered": entry.format(),
            }
            for entry in result.state.logs
        ],
        "events": [
            {
                "t": event.t,
                "event_id": event.event_id,
                "severity": event.severity,
            }
            for event in result.state.events
        ],
        "commands": [
            {
                "t": command.t,
                "command_id": command.command_id,
                "status": command.status,
                "dispatch": command.dispatch,
            }
            for command in result.state.commands
        ],
        "mode_transitions": [
            {
                "t": transition.t,
                "from": transition.from_mode,
                "to": transition.to_mode,
                "reason": transition.reason,
            }
            for transition in result.state.mode_transitions
        ],
        "data_flow_evidence": [
            _data_flow_evidence_to_dict(evidence)
            for evidence in result.state.data_flow_evidence
        ],
        "expectations": {
            "total": len(result.state.expectations),
            "passed": _expectation_count(result, "passed"),
            "failed": _expectation_count(result, "failed"),
            "records": [
                _expectation_to_dict(expectation)
                for expectation in result.state.expectations
            ],
        },
        "final_state": {
            "mode": result.state.current_mode,
            "telemetry": result.state.telemetry,
        },
        "failed_expectations": list(result.state.failed_expectations),
    }


def write_simulation_report_json(
    result: SimulationResult,
    output_path: Path,
) -> None:
    """Write a simulation report JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = simulation_result_to_dict(result)

    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _data_flow_evidence_to_dict(
    evidence: SimDataFlowEvidenceRecord,
) -> dict[str, Any]:
    return {
        "t": evidence.t,
        "data_product_id": evidence.data_product_id,
        "producer": evidence.producer,
        "producer_type": evidence.producer_type,
        "triggered_by_command": evidence.command_id,
        "storage_intent": evidence.storage_intent,
        "downlink_intent": evidence.downlink_intent,
        "eligible_downlink_flows": evidence.eligible_downlink_flows,
        "contact_windows": evidence.contact_windows,
    }


def _expectation_to_dict(expectation: SimExpectationRecord) -> dict[str, Any]:
    return {
        "t": expectation.t,
        "expectation_type": expectation.expectation_type,
        "target": expectation.target,
        "expected": expectation.expected,
        "actual": expectation.actual,
        "result": expectation.result,
        "message": expectation.message,
    }


def _expectation_count(result: SimulationResult, label: str) -> int:
    return sum(1 for item in result.state.expectations if item.result == label)


def _json_result_label(result: SimulationResult) -> str:
    return "passed" if result.passed else "failed"
