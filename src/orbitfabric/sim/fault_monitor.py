from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from orbitfabric.model.mission import Fault, MissionModel
from orbitfabric.sim.telemetry_registry import TelemetryRegistry


@dataclass(frozen=True)
class FaultTrigger:
    fault_id: str
    emitted_events: list[str]
    mode_transition: str | None
    auto_commands: list[str]


class FaultMonitor:
    """Evaluates model-defined faults during simulation."""

    def __init__(self, model: MissionModel, telemetry: TelemetryRegistry) -> None:
        self._faults = model.faults
        self._telemetry = telemetry
        self._counters: dict[str, int] = {fault.id: 0 for fault in self._faults}
        self._triggered: set[str] = set()

    def evaluate(self) -> list[FaultTrigger]:
        triggers: list[FaultTrigger] = []

        for fault in self._faults:
            if fault.id in self._triggered:
                continue

            if self._condition_is_true(fault):
                self._counters[fault.id] += 1
            else:
                self._counters[fault.id] = 0

            debounce = fault.condition.debounce_samples or 1
            if self._counters[fault.id] >= debounce:
                self._triggered.add(fault.id)
                triggers.append(self._build_trigger(fault))

        return triggers

    def _build_trigger(self, fault: Fault) -> FaultTrigger:
        mode_transition = None
        auto_commands: list[str] = []

        if fault.recovery is not None:
            mode_transition = fault.recovery.mode_transition
            auto_commands = list(fault.recovery.auto_commands)

        return FaultTrigger(
            fault_id=fault.id,
            emitted_events=list(fault.emits),
            mode_transition=mode_transition,
            auto_commands=auto_commands,
        )

    def _condition_is_true(self, fault: Fault) -> bool:
        condition = fault.condition

        if condition.telemetry is None:
            return False

        actual = self._telemetry.get(condition.telemetry)
        expected = condition.value
        operator = condition.operator

        if actual is None or operator is None:
            return False

        return _compare(actual=actual, operator=operator, expected=expected)


def _compare(actual: Any, operator: str, expected: Any) -> bool:
    if operator == "<":
        return actual < expected
    if operator == "<=":
        return actual <= expected
    if operator == ">":
        return actual > expected
    if operator == ">=":
        return actual >= expected
    if operator == "==":
        return actual == expected
    if operator == "!=":
        return actual != expected
    return False