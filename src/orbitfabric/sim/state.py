from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

CommandDispatchKind = Literal["GROUND", "AUTO"]
CommandStatus = Literal["ACCEPTED", "REJECTED", "AUTO_DISPATCHED", "FAILED"]


@dataclass(frozen=True)
class SimLogEntry:
    t: float
    message: str

    def format(self) -> str:
        return f"[{format_sim_time(self.t)}] {self.message}"


@dataclass(frozen=True)
class SimEventRecord:
    t: float
    event_id: str
    severity: str


@dataclass(frozen=True)
class SimCommandRecord:
    t: float
    command_id: str
    status: CommandStatus
    dispatch: CommandDispatchKind


@dataclass(frozen=True)
class SimModeTransitionRecord:
    t: float
    from_mode: str
    to_mode: str
    reason: str


@dataclass
class SimulationState:
    current_time: float
    current_mode: str
    telemetry: dict[str, Any] = field(default_factory=dict)
    logs: list[SimLogEntry] = field(default_factory=list)
    events: list[SimEventRecord] = field(default_factory=list)
    commands: list[SimCommandRecord] = field(default_factory=list)
    mode_transitions: list[SimModeTransitionRecord] = field(default_factory=list)
    failed_expectations: list[str] = field(default_factory=list)

    def log(self, t: float, message: str) -> None:
        self.logs.append(SimLogEntry(t=t, message=message))

    def fail_expectation(self, t: float, message: str) -> None:
        self.failed_expectations.append(message)
        self.log(t, f"EXPECTATION FAILED {message}")

    @property
    def passed(self) -> bool:
        return not self.failed_expectations


@dataclass(frozen=True)
class SimulationResult:
    scenario_id: str
    mission_id: str
    state: SimulationState

    @property
    def passed(self) -> bool:
        return self.state.passed

    @property
    def result_label(self) -> str:
        return "PASSED" if self.passed else "FAILED"


def format_sim_time(t: float) -> str:
    seconds = int(t)
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes:02d}:{remaining_seconds:02d}"