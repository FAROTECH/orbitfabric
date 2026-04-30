from __future__ import annotations

from orbitfabric.sim.state import SimModeTransitionRecord, SimulationState
from orbitfabric.sim.telemetry_registry import TelemetryRegistry


class ModeManager:
    """Tracks current operational mode during simulation."""

    def __init__(self, state: SimulationState, telemetry: TelemetryRegistry) -> None:
        self._state = state
        self._telemetry = telemetry

    @property
    def current_mode(self) -> str:
        return self._state.current_mode

    def initialize(self, t: float) -> None:
        self._telemetry.set("obc.mode", self.current_mode, t)
        self._state.log(t, f"MODE={self.current_mode}")

    def transition_to(self, target_mode: str, reason: str, t: float) -> None:
        previous_mode = self._state.current_mode
        if previous_mode == target_mode:
            return

        self._state.current_mode = target_mode
        self._telemetry.set("obc.mode", target_mode, t)
        self._state.mode_transitions.append(
            SimModeTransitionRecord(
                t=t,
                from_mode=previous_mode,
                to_mode=target_mode,
                reason=reason,
            )
        )
        self._state.log(
            t,
            f"MODE TRANSITION {previous_mode} -> {target_mode} reason={reason}",
        )