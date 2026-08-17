from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from orbitfabric import __version__
from orbitfabric.model.errors import MissionModelError, ModelDiagnostic
from orbitfabric.model.loader import MissionModelLoader
from orbitfabric.model.mission import MissionModel

SNAPSHOT_VERSION = "0.1-candidate"
SNAPSHOT_KIND = "orbitfabric.mission_snapshot"


def mission_snapshot_to_dict(
    model: MissionModel,
    mission_dir: Path,
) -> dict[str, Any]:
    """Return a deterministic read-only snapshot of the loaded Mission Model."""
    mission_dir = mission_dir.resolve()

    return {
        "kind": SNAPSHOT_KIND,
        "snapshot_version": SNAPSHOT_VERSION,
        "orbitfabric_version": __version__,
        "result": "loaded",
        "mission": {
            "id": model.spacecraft.id,
            "name": model.spacecraft.name,
            "model_version": model.spacecraft.model_version,
        },
        "source": {
            "mission_dir": str(mission_dir),
        },
        "boundaries": _boundaries(),
        "diagnostics": [],
        "model": model.model_dump(mode="json", by_alias=True),
    }


def failed_mission_snapshot_to_dict(
    mission_dir: Path,
    diagnostics: list[ModelDiagnostic],
) -> dict[str, Any]:
    """Return a structured snapshot failure without exposing a partial model."""
    mission_dir = mission_dir.resolve()

    return {
        "kind": SNAPSHOT_KIND,
        "snapshot_version": SNAPSHOT_VERSION,
        "orbitfabric_version": __version__,
        "result": "failed",
        "mission": None,
        "source": {
            "mission_dir": str(mission_dir),
        },
        "boundaries": _boundaries(),
        "diagnostics": [_diagnostic_to_dict(item) for item in diagnostics],
        "model": None,
    }


def mission_snapshot_from_dir(mission_dir: Path) -> dict[str, Any]:
    """Load a Mission Model and return either a loaded or failed snapshot envelope."""
    mission_dir = mission_dir.resolve()

    try:
        model = MissionModelLoader().load(mission_dir)
    except MissionModelError as exc:
        return failed_mission_snapshot_to_dict(mission_dir, exc.diagnostics)

    return mission_snapshot_to_dict(model, mission_dir)


def write_mission_snapshot(
    mission_dir: Path,
    output_file: Path,
) -> Path:
    """Write a deterministic Mission Model snapshot JSON file.

    Structural load failures are represented inside the JSON envelope rather
    than by omitting the report. Callers can inspect the top-level ``result``
    field to distinguish a loaded model from structured load diagnostics.
    """
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(
        json.dumps(
            mission_snapshot_from_dir(mission_dir),
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return output_file


def _boundaries() -> dict[str, bool | str]:
    return {
        "source_of_truth": "mission_model",
        "core_derived_report": True,
        "read_only": True,
        "contains_full_loaded_model": True,
        "contains_structured_diagnostics": True,
        "contains_yaml_ast": False,
        "contains_source_locations": False,
        "contains_plugin_api": False,
        "contains_studio_api": False,
        "contains_runtime_behavior": False,
        "contains_ground_behavior": False,
    }


def _diagnostic_to_dict(diagnostic: ModelDiagnostic) -> dict[str, Any]:
    return {
        "severity": diagnostic.severity,
        "code": diagnostic.code,
        "file": diagnostic.file,
        "domain": diagnostic.domain,
        "object_id": diagnostic.object_id,
        "message": diagnostic.message,
        "suggestion": diagnostic.suggestion,
    }
