from __future__ import annotations

import json
import os
from collections.abc import Callable
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import rfc8785

from orbitfabric import __version__
from orbitfabric.export.entity_index import entity_index_to_dict
from orbitfabric.export.mission_snapshot import (
    failed_mission_snapshot_to_dict,
    mission_snapshot_to_dict,
)
from orbitfabric.export.model_summary import model_summary_to_dict
from orbitfabric.export.relationship_manifest import relationship_manifest_to_dict
from orbitfabric.lint.engine import LintEngine
from orbitfabric.lint.json_report import lint_report_to_dict
from orbitfabric.model.errors import MissionModelError, ModelDiagnostic
from orbitfabric.model.loader import MissionModelLoader
from orbitfabric.model.mission import MissionModel

INPUT_SET_KIND = "orbitfabric.integration_input_set"
INPUT_SET_VERSION = "0.1-candidate"
MANIFEST_FILENAME = "integration_input_manifest.json"


@dataclass(frozen=True)
class SurfaceSpec:
    role: str
    requirement: str
    kind: str
    format_version: str
    filename: str


SURFACE_SPECS: tuple[SurfaceSpec, ...] = tuple(
    sorted(
        (
            SurfaceSpec(
                role="entity_index",
                requirement="required",
                kind="orbitfabric.entity_index",
                format_version="0.1",
                filename="entity_index.json",
            ),
            SurfaceSpec(
                role="lint_report",
                requirement="required",
                kind="orbitfabric-lint",
                format_version="v1",
                filename="lint_report.json",
            ),
            SurfaceSpec(
                role="mission_snapshot",
                requirement="required",
                kind="orbitfabric.mission_snapshot",
                format_version="0.1-candidate",
                filename="mission_snapshot.json",
            ),
            SurfaceSpec(
                role="model_summary",
                requirement="companion",
                kind="orbitfabric.model_summary",
                format_version="0.1",
                filename="model_summary.json",
            ),
            SurfaceSpec(
                role="relationship_manifest",
                requirement="required",
                kind="orbitfabric.relationship_manifest",
                format_version="0.1-candidate",
                filename="relationship_manifest.json",
            ),
        ),
        key=lambda spec: spec.role,
    )
)


@dataclass(frozen=True)
class IntegrationInputSetResult:
    manifest_path: Path
    load_result: str
    lint_result: str
    generation_failed: bool

    @property
    def succeeded(self) -> bool:
        return (
            self.load_result == "loaded"
            and self.lint_result in {"passed", "passed_with_warnings"}
            and not self.generation_failed
        )


def write_integration_input_set(
    mission_dir: Path,
    output_dir: Path,
) -> IntegrationInputSetResult:
    """Produce one coherent Core Integration Input Set from one load/lint operation.

    Generation occurs in a sibling staging directory. Any previously published
    manifest is invalidated before generation starts, and the new manifest is
    published only after every surface publication decision has completed.
    Therefore, an interrupted regeneration cannot leave a stale manifest that
    falsely describes a partially replaced input set.
    """
    mission_dir = mission_dir.resolve()
    output_dir = output_dir.resolve()
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    published_manifest = output_dir / MANIFEST_FILENAME
    published_manifest.unlink(missing_ok=True)

    with TemporaryDirectory(
        dir=output_dir.parent,
        prefix=f".{output_dir.name}.staging-",
    ) as temporary_directory:
        staging_dir = Path(temporary_directory)

        try:
            model = MissionModelLoader().load(mission_dir)
        except MissionModelError as exc:
            return _write_load_failure_set(
                mission_dir=mission_dir,
                output_dir=output_dir,
                staging_dir=staging_dir,
                diagnostics=exc.diagnostics,
            )

        report = LintEngine().run(model)
        lint_payload = lint_report_to_dict(model, report)
        lint_result = str(lint_payload["result"])

        producers: dict[str, Callable[[], dict[str, Any]]] = {
            "entity_index": lambda: entity_index_to_dict(model, mission_dir),
            "lint_report": lambda: lint_payload,
            "mission_snapshot": lambda: mission_snapshot_to_dict(model, mission_dir),
            "model_summary": lambda: model_summary_to_dict(model, mission_dir),
            "relationship_manifest": lambda: relationship_manifest_to_dict(
                model, mission_dir
            ),
        }

        surface_records: list[dict[str, Any]] = []
        generation_failed = False
        for spec in SURFACE_SPECS:
            record, failed = _produce_surface(staging_dir, spec, producers[spec.role])
            surface_records.append(record)
            generation_failed = generation_failed or failed

        manifest = _build_manifest(
            model=model,
            load_result="loaded",
            lint_result=lint_result,
            surface_records=surface_records,
        )
        _write_json(staging_dir / MANIFEST_FILENAME, manifest)
        _publish_staged_set(staging_dir, output_dir, surface_records)

        return IntegrationInputSetResult(
            manifest_path=published_manifest,
            load_result="loaded",
            lint_result=lint_result,
            generation_failed=generation_failed,
        )


def _write_load_failure_set(
    *,
    mission_dir: Path,
    output_dir: Path,
    staging_dir: Path,
    diagnostics: list[ModelDiagnostic],
) -> IntegrationInputSetResult:
    records: list[dict[str, Any]] = []
    generation_failed = False

    for spec in SURFACE_SPECS:
        if spec.role == "mission_snapshot":
            try:
                payload = failed_mission_snapshot_to_dict(mission_dir, diagnostics)
                path = staging_dir / spec.filename
                _write_json(path, payload)
                records.append(_available_record(spec, path))
            except Exception:
                records.append(_unavailable_record(spec, "generation_failed"))
                generation_failed = True
        else:
            records.append(_unavailable_record(spec, "load_failed"))

    manifest = _build_manifest(
        model=None,
        load_result="failed",
        lint_result="not_run",
        surface_records=records,
    )
    _write_json(staging_dir / MANIFEST_FILENAME, manifest)
    _publish_staged_set(staging_dir, output_dir, records)

    return IntegrationInputSetResult(
        manifest_path=output_dir / MANIFEST_FILENAME,
        load_result="failed",
        lint_result="not_run",
        generation_failed=generation_failed,
    )


def _produce_surface(
    staging_dir: Path,
    spec: SurfaceSpec,
    producer: Callable[[], dict[str, Any]],
) -> tuple[dict[str, Any], bool]:
    try:
        payload = producer()
        path = staging_dir / spec.filename
        _write_json(path, payload)
        return _available_record(spec, path), False
    except Exception:
        return _unavailable_record(spec, "generation_failed"), True


def _available_record(spec: SurfaceSpec, path: Path) -> dict[str, Any]:
    return {
        "role": spec.role,
        "requirement": spec.requirement,
        "status": "available",
        "kind": spec.kind,
        "format_version": spec.format_version,
        "path": spec.filename,
        "sha256": _sha256_file(path),
        "unavailable_reason": None,
    }


def _unavailable_record(spec: SurfaceSpec, reason: str) -> dict[str, Any]:
    return {
        "role": spec.role,
        "requirement": spec.requirement,
        "status": "unavailable",
        "kind": spec.kind,
        "format_version": spec.format_version,
        "path": None,
        "sha256": None,
        "unavailable_reason": reason,
    }


def _build_manifest(
    *,
    model: MissionModel | None,
    load_result: str,
    lint_result: str,
    surface_records: list[dict[str, Any]],
) -> dict[str, Any]:
    records = sorted(surface_records, key=lambda record: record["role"])
    mission = None
    if model is not None:
        mission = {
            "id": model.spacecraft.id,
            "model_version": model.spacecraft.model_version,
        }

    manifest: dict[str, Any] = {
        "kind": INPUT_SET_KIND,
        "input_set_version": INPUT_SET_VERSION,
        "orbitfabric_version": __version__,
        "mission": mission,
        "load_result": load_result,
        "lint_result": lint_result,
        "surfaces": records,
    }
    manifest["input_set_sha256"] = _input_set_sha256(manifest)
    return manifest


def _input_set_sha256(manifest: dict[str, Any]) -> str:
    digest_surfaces = []
    for record in sorted(manifest["surfaces"], key=lambda item: item["role"]):
        digest_surfaces.append(
            {
                "role": record["role"],
                "requirement": record["requirement"],
                "status": record["status"],
                "kind": record["kind"],
                "format_version": record["format_version"],
                "sha256": record["sha256"],
                "unavailable_reason": record["unavailable_reason"],
            }
        )

    digest_payload = {
        "kind": manifest["kind"],
        "input_set_version": manifest["input_set_version"],
        "orbitfabric_version": manifest["orbitfabric_version"],
        "mission": manifest["mission"],
        "load_result": manifest["load_result"],
        "lint_result": manifest["lint_result"],
        "surfaces": digest_surfaces,
    }
    canonical_bytes = rfc8785.dumps(digest_payload)
    return sha256(canonical_bytes).hexdigest()


def _publish_staged_set(
    staging_dir: Path,
    output_dir: Path,
    surface_records: list[dict[str, Any]],
) -> None:
    by_role = {record["role"]: record for record in surface_records}

    for spec in SURFACE_SPECS:
        record = by_role[spec.role]
        target = output_dir / spec.filename
        if record["status"] == "available":
            os.replace(staging_dir / spec.filename, target)
        else:
            target.unlink(missing_ok=True)

    # Completeness marker: publish the manifest after all surface decisions.
    os.replace(staging_dir / MANIFEST_FILENAME, output_dir / MANIFEST_FILENAME)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
