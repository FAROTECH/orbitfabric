from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from orbitfabric.model.mission import Command, MissionModel
from orbitfabric.sim.state import (
    CommandDispatchKind,
    CommandStatus,
    SimCommandRecord,
    SimulationState,
)


@dataclass(frozen=True)
class CommandDispatchResult:
    command: Command | None
    status: CommandStatus
    reason: str | None = None


class CommandRouter:
    """Validates and records command dispatches during simulation."""

    def __init__(self, model: MissionModel, state: SimulationState) -> None:
        self._commands_by_id = {command.id: command for command in model.commands}
        self._state = state

    def dispatch(
        self,
        command_id: str,
        args: dict[str, Any],
        dispatch: CommandDispatchKind,
        t: float,
    ) -> CommandDispatchResult:
        command = self._commands_by_id.get(command_id)
        if command is None:
            self._record(command_id, "FAILED", dispatch, t)
            return CommandDispatchResult(
                command=None,
                status="FAILED",
                reason="unknown command",
            )

        if self._state.current_mode not in command.allowed_modes:
            self._record(command_id, "REJECTED", dispatch, t)
            return CommandDispatchResult(
                command=command,
                status="REJECTED",
                reason=f"command not allowed in mode {self._state.current_mode}",
            )

        validation_error = self._validate_args(command, args)
        if validation_error is not None:
            self._record(command_id, "FAILED", dispatch, t)
            return CommandDispatchResult(
                command=command,
                status="FAILED",
                reason=validation_error,
            )

        status: CommandStatus = "AUTO_DISPATCHED" if dispatch == "AUTO" else "ACCEPTED"
        self._record(command_id, status, dispatch, t)
        return CommandDispatchResult(command=command, status=status)

    def has_command(self, command_id: str, dispatch: CommandDispatchKind | None = None) -> bool:
        for record in self._state.commands:
            if record.command_id != command_id:
                continue
            if dispatch is not None and record.dispatch != dispatch:
                continue
            return True
        return False

    def _record(
        self,
        command_id: str,
        status: CommandStatus,
        dispatch: CommandDispatchKind,
        t: float,
    ) -> None:
        self._state.commands.append(
            SimCommandRecord(
                t=t,
                command_id=command_id,
                status=status,
                dispatch=dispatch,
            )
        )
        self._state.log(t, f"COMMAND {command_id} -> {status}")

    def _validate_args(self, command: Command, args: dict[str, Any]) -> str | None:
        declared_args = {arg.name: arg for arg in command.arguments}

        for arg_name in args:
            if arg_name not in declared_args:
                return f"unknown argument {arg_name}"

        for arg in command.arguments:
            if arg.name not in args:
                return f"missing argument {arg.name}"

            value = args[arg.name]
            if arg.min is not None and value < arg.min:
                return f"argument {arg.name} below minimum"
            if arg.max is not None and value > arg.max:
                return f"argument {arg.name} above maximum"

        return None