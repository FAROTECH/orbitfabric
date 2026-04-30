from __future__ import annotations

from pathlib import Path

from orbitfabric.sim.state import SimulationResult


def simulation_result_to_log_text(result: SimulationResult) -> str:
    """Render a simulation result as a stable plain-text log."""
    lines: list[str] = []

    lines.append("OrbitFabric Scenario Log v0.1")
    lines.append("")
    lines.append(f"Mission: {result.mission_id}")
    lines.append(f"Scenario: {result.scenario_id}")
    lines.append(f"Result: {result.result_label}")
    lines.append("")
    lines.append("Timeline:")

    for entry in result.state.logs:
        lines.append(entry.format())

    lines.append("")
    lines.append("Summary:")
    lines.append(f"Events: {len(result.state.events)}")
    lines.append(f"Commands: {len(result.state.commands)}")
    lines.append(f"Mode transitions: {len(result.state.mode_transitions)}")
    lines.append(f"Failed expectations: {len(result.state.failed_expectations)}")
    lines.append("")

    return "\n".join(lines)


def write_simulation_log(result: SimulationResult, output_path: Path) -> None:
    """Write a simulation timeline log file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(simulation_result_to_log_text(result), encoding="utf-8")