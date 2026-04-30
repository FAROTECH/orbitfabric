from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from orbitfabric.lint.finding import LintFinding
from orbitfabric.model.errors import MissionModelError, ModelDiagnostic
from orbitfabric.model.loader import MissionModelLoader
from orbitfabric.model.scenario import LoadedScenario, ScenarioModel

REQUIRED_SCENARIO_KEYS = ("scenario", "mission", "initial_state", "steps")


class ScenarioLoader:
    """Loads an OrbitFabric scenario and the Mission Model it references."""

    def load(self, scenario_file: Path) -> LoadedScenario:
        scenario_file = scenario_file.resolve()

        diagnostics: list[ModelDiagnostic] = []

        if not scenario_file.exists() or not scenario_file.is_file():
            raise MissionModelError(
                [
                    ModelDiagnostic(
                        severity="ERROR",
                        code="OF-SCN-000",
                        file=str(scenario_file),
                        message="scenario path does not exist or is not a file",
                    )
                ]
            )

        raw = self._load_yaml_file(scenario_file, diagnostics)
        if diagnostics:
            raise MissionModelError(diagnostics)

        self._validate_top_level_keys(raw, diagnostics)
        if diagnostics:
            raise MissionModelError(diagnostics)

        try:
            scenario = ScenarioModel.model_validate(raw)
        except ValidationError as exc:
            raise MissionModelError(self._pydantic_diagnostics(exc)) from exc

        mission_path = self._resolve_mission_path(scenario_file, scenario.mission.path)
        mission_model = MissionModelLoader().load(mission_path)

        reference_findings = self.validate_references(scenario, mission_model)
        if reference_findings:
            raise MissionModelError(
                [
                    ModelDiagnostic(
                        severity=finding.severity,
                        code=finding.code,
                        file=finding.file,
                        domain=finding.domain,
                        object_id=finding.object_id,
                        message=finding.message,
                        suggestion=finding.suggestion,
                    )
                    for finding in reference_findings
                ]
            )

        return LoadedScenario(
            scenario=scenario,
            mission_model=mission_model,
            scenario_file=scenario_file,
            mission_path=mission_path,
        )

    def validate_references(
        self,
        scenario: ScenarioModel,
        mission_model: Any,
    ) -> list[LintFinding]:
        """Validate scenario references against a loaded Mission Model."""
        findings: list[LintFinding] = []

        mode_ids = mission_model.mode_ids
        telemetry_ids = mission_model.telemetry_ids
        command_ids = mission_model.command_ids
        event_ids = mission_model.event_ids

        if scenario.initial_state.mode not in mode_ids:
            findings.append(
                LintFinding(
                    severity="ERROR",
                    code="OF-SCN-006",
                    file="scenario.yaml",
                    domain="scenario",
                    object_id=scenario.scenario.id,
                    message=(
                        "scenario initial mode references unknown mode "
                        f"'{scenario.initial_state.mode}'"
                    ),
                    suggestion="Use a mode defined in modes.yaml.",
                )
            )

        for telemetry_id in scenario.initial_state.telemetry:
            if telemetry_id not in telemetry_ids:
                findings.append(
                    LintFinding(
                        severity="ERROR",
                        code="OF-SCN-007",
                        file="scenario.yaml",
                        domain="scenario",
                        object_id=scenario.scenario.id,
                        message=(
                            "scenario initial telemetry references unknown telemetry "
                            f"'{telemetry_id}'"
                        ),
                        suggestion="Use telemetry defined in telemetry.yaml.",
                    )
                )

        previous_t: int | float | None = None
        for step in scenario.steps:
            if previous_t is not None and step.t < previous_t:
                findings.append(
                    LintFinding(
                        severity="ERROR",
                        code="OF-SCN-005",
                        file="scenario.yaml",
                        domain="scenario",
                        object_id=scenario.scenario.id,
                        message="scenario timeline must be monotonic",
                        suggestion="Sort scenario steps by non-decreasing time.",
                    )
                )
            previous_t = step.t

            if step.command is not None and step.command not in command_ids:
                findings.append(
                    LintFinding(
                        severity="ERROR",
                        code="OF-SCN-001",
                        file="scenario.yaml",
                        domain="scenario",
                        object_id=scenario.scenario.id,
                        message=f"scenario command references unknown command '{step.command}'",
                        suggestion="Use a command defined in commands.yaml.",
                    )
                )

            if step.inject is not None and step.inject.telemetry not in telemetry_ids:
                findings.append(
                    LintFinding(
                        severity="ERROR",
                        code="OF-SCN-004",
                        file="scenario.yaml",
                        domain="scenario",
                        object_id=scenario.scenario.id,
                        message=(
                            "scenario telemetry injection references unknown telemetry "
                            f"'{step.inject.telemetry}'"
                        ),
                        suggestion="Use telemetry defined in telemetry.yaml.",
                    )
                )

            if step.expect_event is not None and step.expect_event not in event_ids:
                findings.append(
                    LintFinding(
                        severity="ERROR",
                        code="OF-SCN-002",
                        file="scenario.yaml",
                        domain="scenario",
                        object_id=scenario.scenario.id,
                        message=(
                            "scenario event expectation references unknown event "
                            f"'{step.expect_event}'"
                        ),
                        suggestion="Use an event defined in events.yaml.",
                    )
                )

            if step.expect_mode is not None and step.expect_mode not in mode_ids:
                findings.append(
                    LintFinding(
                        severity="ERROR",
                        code="OF-SCN-003",
                        file="scenario.yaml",
                        domain="scenario",
                        object_id=scenario.scenario.id,
                        message=(
                            "scenario mode expectation references unknown mode "
                            f"'{step.expect_mode}'"
                        ),
                        suggestion="Use a mode defined in modes.yaml.",
                    )
                )

            if step.expect_command is not None and step.expect_command.id not in command_ids:
                findings.append(
                    LintFinding(
                        severity="ERROR",
                        code="OF-SCN-001",
                        file="scenario.yaml",
                        domain="scenario",
                        object_id=scenario.scenario.id,
                        message=(
                            "scenario command expectation references unknown command "
                            f"'{step.expect_command.id}'"
                        ),
                        suggestion="Use a command defined in commands.yaml.",
                    )
                )

            if step.expect_telemetry is not None:
                for telemetry_id in step.expect_telemetry:
                    if telemetry_id not in telemetry_ids:
                        findings.append(
                            LintFinding(
                                severity="ERROR",
                                code="OF-SCN-004",
                                file="scenario.yaml",
                                domain="scenario",
                                object_id=scenario.scenario.id,
                                message=(
                                    "scenario telemetry expectation references "
                                    f"unknown telemetry '{telemetry_id}'"
                                ),
                                suggestion="Use telemetry defined in telemetry.yaml.",
                            )
                        )

        return findings

    def _load_yaml_file(
        self,
        scenario_file: Path,
        diagnostics: list[ModelDiagnostic],
    ) -> dict[str, Any]:
        try:
            with scenario_file.open("r", encoding="utf-8") as handle:
                loaded = yaml.safe_load(handle)
        except yaml.YAMLError as exc:
            diagnostics.append(
                ModelDiagnostic(
                    severity="ERROR",
                    code="OF-SCN-008",
                    file=str(scenario_file),
                    message=f"invalid scenario YAML: {exc}",
                )
            )
            return {}

        if loaded is None:
            diagnostics.append(
                ModelDiagnostic(
                    severity="ERROR",
                    code="OF-SCN-009",
                    file=str(scenario_file),
                    message="scenario YAML file is empty",
                )
            )
            return {}

        if not isinstance(loaded, dict):
            diagnostics.append(
                ModelDiagnostic(
                    severity="ERROR",
                    code="OF-SCN-010",
                    file=str(scenario_file),
                    message="scenario YAML file must contain a top-level mapping",
                )
            )
            return {}

        return loaded

    def _validate_top_level_keys(
        self,
        loaded: dict[str, Any],
        diagnostics: list[ModelDiagnostic],
    ) -> None:
        for key in REQUIRED_SCENARIO_KEYS:
            if key not in loaded:
                diagnostics.append(
                    ModelDiagnostic(
                        severity="ERROR",
                        code="OF-SCN-011",
                        domain="scenario",
                        message=f"missing required top-level key '{key}'",
                    )
                )

        for key in loaded:
            if key not in REQUIRED_SCENARIO_KEYS:
                diagnostics.append(
                    ModelDiagnostic(
                        severity="ERROR",
                        code="OF-SCN-012",
                        domain="scenario",
                        message=f"unexpected top-level key '{key}'",
                    )
                )

    def _pydantic_diagnostics(self, exc: ValidationError) -> list[ModelDiagnostic]:
        diagnostics: list[ModelDiagnostic] = []

        for error in exc.errors():
            location = ".".join(str(part) for part in error.get("loc", ()))
            message = error.get("msg", "scenario validation error")
            diagnostics.append(
                ModelDiagnostic(
                    severity="ERROR",
                    code="OF-SCN-013",
                    domain=location or None,
                    message=message,
                )
            )

        return diagnostics

    def _resolve_mission_path(self, scenario_file: Path, mission_path: Path) -> Path:
        if mission_path.is_absolute():
            return mission_path.resolve()

        return (scenario_file.parent / mission_path).resolve()