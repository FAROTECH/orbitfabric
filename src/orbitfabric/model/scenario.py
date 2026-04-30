from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from orbitfabric.model.mission import MissionModel

CommandStatus = Literal["ACCEPTED", "REJECTED", "AUTO_DISPATCHED", "TIMEOUT", "FAILED"]
CommandDispatch = Literal["GROUND", "AUTO"]
ScenarioStatus = Literal["PASSED", "FAILED"]


class StrictScenarioModel(BaseModel):
    """Base model for OrbitFabric scenario objects."""

    model_config = ConfigDict(extra="forbid")


class ScenarioMetadata(StrictScenarioModel):
    id: str
    name: str
    description: str | None = None


class ScenarioMissionRef(StrictScenarioModel):
    path: Path


class ScenarioInitialState(StrictScenarioModel):
    mode: str
    telemetry: dict[str, Any] = Field(default_factory=dict)


class ScenarioInject(StrictScenarioModel):
    telemetry: str
    value: Any


class ScenarioExpectedCommand(StrictScenarioModel):
    id: str
    dispatch: CommandDispatch = "GROUND"


class ScenarioStep(StrictScenarioModel):
    t: int | float

    command: str | None = None
    args: dict[str, Any] = Field(default_factory=dict)
    inject: ScenarioInject | None = None

    expect_event: str | None = None
    expect_mode: str | None = None
    expect_command: ScenarioExpectedCommand | None = None
    expect_telemetry: dict[str, Any] | None = None
    expect: dict[str, Any] | None = None

    @model_validator(mode="after")
    def validate_step_has_action(self) -> ScenarioStep:
        actions = [
            self.command is not None,
            self.inject is not None,
            self.expect_event is not None,
            self.expect_mode is not None,
            self.expect_command is not None,
            self.expect_telemetry is not None,
            self.expect is not None,
        ]

        if not any(actions):
            raise ValueError("scenario step must define at least one action or expectation")

        return self


class ScenarioModel(StrictScenarioModel):
    scenario: ScenarioMetadata
    mission: ScenarioMissionRef
    initial_state: ScenarioInitialState
    steps: list[ScenarioStep]


class LoadedScenario(StrictScenarioModel):
    scenario: ScenarioModel
    mission_model: MissionModel
    scenario_file: Path
    mission_path: Path