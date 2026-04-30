from __future__ import annotations

from orbitfabric.model.mission import Event, MissionModel
from orbitfabric.sim.state import SimEventRecord, SimulationState


class EventBus:
    """Records emitted events during simulation."""

    def __init__(self, model: MissionModel, state: SimulationState) -> None:
        self._events_by_id = {event.id: event for event in model.events}
        self._state = state

    def emit(self, event_id: str, t: float) -> None:
        event = self._events_by_id[event_id]
        self._state.events.append(
            SimEventRecord(t=t, event_id=event.id, severity=event.severity)
        )
        self._state.log(t, f"EVENT {event.id} severity={event.severity.upper()}")

    def has_event(self, event_id: str) -> bool:
        return any(record.event_id == event_id for record in self._state.events)

    def get_event_definition(self, event_id: str) -> Event:
        return self._events_by_id[event_id]