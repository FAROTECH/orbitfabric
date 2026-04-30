from __future__ import annotations

from typing import Any

from orbitfabric.sim.state import SimulationState


class TelemetryRegistry:
    """Stores current telemetry values during simulation."""

    def __init__(self, state: SimulationState) -> None:
        self._state = state

    def get(self, telemetry_id: str) -> Any:
        return self._state.telemetry.get(telemetry_id)

    def set(self, telemetry_id: str, value: Any, t: float, log: bool = False) -> None:
        self._state.telemetry[telemetry_id] = value
        if log:
            self._state.log(t, f"TELEMETRY {telemetry_id}={_format_value(value)}")

    def inject(self, telemetry_id: str, value: Any, t: float) -> None:
        self._state.telemetry[telemetry_id] = value
        self._state.log(t, f"INJECT {telemetry_id}={_format_value(value)}")


def _format_value(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)