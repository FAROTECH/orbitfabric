from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from orbitfabric.model.errors import MissionModelError, ModelDiagnostic
from orbitfabric.model.mission import MissionModel

REQUIRED_FILES: dict[str, tuple[str, ...]] = {
    "spacecraft.yaml": ("spacecraft",),
    "subsystems.yaml": ("subsystems",),
    "modes.yaml": ("modes", "mode_transitions"),
    "telemetry.yaml": ("telemetry",),
    "commands.yaml": ("commands",),
    "events.yaml": ("events",),
    "faults.yaml": ("faults",),
    "packets.yaml": ("packets",),
    "policies.yaml": ("policies",),
}


class MissionModelLoader:
    """Loads a Mission Model from a canonical OrbitFabric mission directory."""

    def load(self, mission_dir: Path) -> MissionModel:
        diagnostics: list[ModelDiagnostic] = []
        data: dict[str, Any] = {}

        mission_dir = mission_dir.resolve()

        if not mission_dir.exists() or not mission_dir.is_dir():
            raise MissionModelError(
                [
                    ModelDiagnostic(
                        severity="ERROR",
                        code="OF-SYN-001",
                        file=str(mission_dir),
                        message="mission path does not exist or is not a directory",
                        suggestion="Pass an existing Mission Model directory.",
                    )
                ]
            )

        for filename, expected_keys in REQUIRED_FILES.items():
            file_path = mission_dir / filename

            if not file_path.exists():
                diagnostics.append(
                    ModelDiagnostic(
                        severity="ERROR",
                        code="OF-SYN-002",
                        file=filename,
                        message="required Mission Model file is missing",
                        suggestion=f"Add the required Mission Model file '{filename}'.",
                    )
                )
                continue

            loaded = self._load_yaml_file(file_path, filename, diagnostics)
            if loaded is None:
                continue

            self._validate_expected_keys(filename, loaded, expected_keys, diagnostics)

            for key in expected_keys:
                if key in loaded:
                    data[key] = loaded[key]

        if diagnostics:
            raise MissionModelError(diagnostics)

        try:
            model = MissionModel.model_validate(data)
        except ValidationError as exc:
            raise MissionModelError(self._pydantic_diagnostics(exc)) from exc

        duplicate_diagnostics = self._check_duplicate_ids(model)
        if duplicate_diagnostics:
            raise MissionModelError(duplicate_diagnostics)

        return model

    def _load_yaml_file(
        self,
        file_path: Path,
        display_name: str,
        diagnostics: list[ModelDiagnostic],
    ) -> dict[str, Any] | None:
        try:
            with file_path.open("r", encoding="utf-8") as handle:
                loaded = yaml.safe_load(handle)
        except yaml.YAMLError as exc:
            diagnostics.append(
                ModelDiagnostic(
                    severity="ERROR",
                    code="OF-SYN-003",
                    file=display_name,
                    message=f"invalid YAML: {exc}",
                    suggestion="Fix YAML syntax.",
                )
            )
            return None

        if loaded is None:
            diagnostics.append(
                ModelDiagnostic(
                    severity="ERROR",
                    code="OF-SYN-004",
                    file=display_name,
                    message="YAML file is empty",
                    suggestion="Add the required top-level YAML mapping.",
                )
            )
            return None

        if not isinstance(loaded, dict):
            diagnostics.append(
                ModelDiagnostic(
                    severity="ERROR",
                    code="OF-SYN-005",
                    file=display_name,
                    message="YAML file must contain a mapping at the top level",
                    suggestion="Use a YAML mapping at the top level.",
                )
            )
            return None

        return loaded

    def _validate_expected_keys(
        self,
        filename: str,
        loaded: dict[str, Any],
        expected_keys: tuple[str, ...],
        diagnostics: list[ModelDiagnostic],
    ) -> None:
        for key in expected_keys:
            if key not in loaded:
                diagnostics.append(
                    ModelDiagnostic(
                        severity="ERROR",
                        code="OF-STR-001",
                        file=filename,
                        domain=key,
                        message=f"missing required top-level key '{key}'",
                        suggestion=f"Add the required top-level key '{key}'.",
                    )
                )

        for key in loaded:
            if key not in expected_keys:
                diagnostics.append(
                    ModelDiagnostic(
                        severity="ERROR",
                        code="OF-STR-002",
                        file=filename,
                        domain=key,
                        message=f"unexpected top-level key '{key}'",
                        suggestion=f"Remove or rename the unexpected top-level key '{key}'.",
                    )
                )

    def _pydantic_diagnostics(self, exc: ValidationError) -> list[ModelDiagnostic]:
        diagnostics: list[ModelDiagnostic] = []

        for error in exc.errors():
            location = ".".join(str(part) for part in error.get("loc", ()))
            message = error.get("msg", "validation error")
            diagnostics.append(
                ModelDiagnostic(
                    severity="ERROR",
                    code="OF-STR-003",
                    domain=location or None,
                    message=message,
                    suggestion="Fix the invalid Mission Model field.",
                )
            )

        return diagnostics

    def _check_duplicate_ids(self, model: MissionModel) -> list[ModelDiagnostic]:
        diagnostics: list[ModelDiagnostic] = []

        diagnostics.extend(
            self._duplicates(
                domain="subsystems",
                file="subsystems.yaml",
                values=[item.id for item in model.subsystems],
            )
        )
        diagnostics.extend(
            self._duplicates(
                domain="telemetry",
                file="telemetry.yaml",
                values=[item.id for item in model.telemetry],
            )
        )
        diagnostics.extend(
            self._duplicates(
                domain="commands",
                file="commands.yaml",
                values=[item.id for item in model.commands],
            )
        )
        diagnostics.extend(
            self._duplicates(
                domain="events",
                file="events.yaml",
                values=[item.id for item in model.events],
            )
        )
        diagnostics.extend(
            self._duplicates(
                domain="faults",
                file="faults.yaml",
                values=[item.id for item in model.faults],
            )
        )
        diagnostics.extend(
            self._duplicates(
                domain="packets",
                file="packets.yaml",
                values=[item.id for item in model.packets],
            )
        )
        diagnostics.extend(
            self._duplicates(
                domain="modes",
                file="modes.yaml",
                values=model.modes.keys(),
            )
        )

        return diagnostics

    def _duplicates(
        self,
        domain: str,
        file: str,
        values: Iterable[str],
    ) -> list[ModelDiagnostic]:
        diagnostics: list[ModelDiagnostic] = []
        seen: set[str] = set()

        for value in values:
            if value in seen:
                diagnostics.append(
                    ModelDiagnostic(
                        severity="ERROR",
                        code="OF-ID-001",
                        file=file,
                        domain=domain,
                        object_id=value,
                        message="duplicate ID is not allowed within a domain",
                        suggestion=f"Rename or remove duplicate ID '{value}'.",
                    )
                )
            seen.add(value)

        return diagnostics