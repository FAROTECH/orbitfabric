from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Any

import typer

from orbitfabric.adapter_manager import (
    AdapterManager,
    AdapterManagerError,
    ProjectLockInstallService,
    ProjectLockService,
)
from orbitfabric.adapter_manager.models import AdapterSourceCoordinate

adapter_app = typer.Typer(
    help="Manage installed OrbitFabric adapters.",
    no_args_is_help=True,
)
lock_app = typer.Typer(
    help="Validate, compare and satisfy project-scoped exact adapter state.",
    no_args_is_help=True,
)
adapter_app.add_typer(lock_app, name="lock")


def _manager() -> AdapterManager:
    return AdapterManager()


def _json_echo(payload: Any) -> None:
    if hasattr(payload, "model_dump"):
        payload = payload.model_dump(mode="json")
    typer.echo(json.dumps(payload, indent=2, sort_keys=True))


def _fail(exc: Exception) -> None:
    typer.echo(f"Adapter Manager error: {exc}", err=True)
    raise typer.Exit(code=1) from exc


@adapter_app.command("install")
def install_adapter(
    release_descriptor: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            help="Exact Adapter Release Descriptor JSON file.",
        ),
    ],
    artifact: Annotated[
        Path,
        typer.Option(
            "--artifact",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            help="Exact local adapter artifact referenced by the release descriptor.",
        ),
    ],
    artifact_id: Annotated[
        str | None,
        typer.Option(
            "--artifact-id",
            help="Release-local artifact id when multiple artifacts exist.",
        ),
    ] = None,
    descriptor_sha256: Annotated[
        str | None,
        typer.Option(
            "--descriptor-sha256",
            help="Optional expected SHA-256 for the exact Release Descriptor bytes.",
        ),
    ] = None,
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Write the installed record as JSON."),
    ] = False,
) -> None:
    """Install one exact adapter release through the explicit-source lane."""
    try:
        record = _manager().install(
            release_descriptor,
            artifact,
            artifact_id=artifact_id,
            expected_descriptor_sha256=descriptor_sha256,
        )
    except AdapterManagerError as exc:
        _fail(exc)
        return

    if json_output:
        _json_echo(record)
        return
    typer.echo(f"Installed adapter instance: {record.instance_id}")
    typer.echo("Release: " f"{record.source_coordinate.display()}@{record.release_version}")
    typer.echo(f"Backend: {record.backend_id}")
    if record.acceptance_warnings:
        typer.echo("Acceptance warnings:")
        for warning in record.acceptance_warnings:
            typer.echo(f"  - {warning}")


@adapter_app.command("list")
def list_adapters(
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Write installed adapter records as JSON."),
    ] = False,
) -> None:
    """List Core-owned user-scoped installed adapter state."""
    try:
        records = _manager().list()
    except AdapterManagerError as exc:
        _fail(exc)
        return

    if json_output:
        _json_echo([record.model_dump(mode="json") for record in records])
        return
    if not records:
        typer.echo("No adapters installed.")
        return
    for record in records:
        typer.echo(
            f"{record.instance_id}  "
            f"{record.source_coordinate.display()}@{record.release_version}  "
            f"{record.backend_id}"
        )


@adapter_app.command("inspect")
def inspect_adapter(
    instance_id: Annotated[str, typer.Argument(help="Installed adapter instance id.")],
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Write the installed adapter record as JSON."),
    ] = False,
) -> None:
    """Inspect one installed adapter record."""
    try:
        record = _manager().inspect(instance_id)
    except AdapterManagerError as exc:
        _fail(exc)
        return

    if json_output:
        _json_echo(record)
        return
    typer.echo(f"Instance: {record.instance_id}")
    typer.echo(f"Release: {record.source_coordinate.display()}@{record.release_version}")
    typer.echo(f"Artifact: {record.artifact_id} sha256:{record.artifact_sha256}")
    typer.echo(f"Backend: {record.backend_id}")
    typer.echo(f"Manifest: {record.manifest_path}")
    typer.echo(f"Endpoint: {' '.join(record.execution_argv_prefix)}")


@adapter_app.command("verify")
def verify_adapter(
    instance_id: Annotated[str, typer.Argument(help="Installed adapter instance id.")],
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Write the verification report as JSON."),
    ] = False,
) -> None:
    """Verify current installed adapter health and integrity."""
    try:
        report = _manager().verify(instance_id)
    except AdapterManagerError as exc:
        _fail(exc)
        return

    if json_output:
        _json_echo(report)
    else:
        typer.echo(f"Instance: {report.instance_id}")
        for name in (
            "release_descriptor_integrity",
            "manifest_integrity",
            "manifest_conformance",
            "execution_binding",
            "backend_materialization",
        ):
            dimension = getattr(report, name)
            suffix = f" ({dimension.detail})" if dimension.detail else ""
            typer.echo(f"{name}: {dimension.status}{suffix}")
        typer.echo(f"Result: {'PASSED' if report.passed else 'FAILED'}")
    if not report.passed:
        raise typer.Exit(code=1)


@adapter_app.command("execute")
def execute_adapter(
    instance_id: Annotated[str, typer.Argument(help="Installed adapter instance id.")],
    operation: Annotated[
        str,
        typer.Option("--operation", help="Manifest-declared operation id."),
    ],
    input_set_manifest: Annotated[
        Path,
        typer.Option(
            "--input-set-manifest",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            help="Core Integration Input Set manifest.",
        ),
    ],
    profile: Annotated[
        Path,
        typer.Option(
            "--profile",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            help="Projection Profile for the adapter operation.",
        ),
    ],
    output_dir: Annotated[
        Path,
        typer.Option("--output-dir", help="Adapter output directory."),
    ],
    operation_input: Annotated[
        list[str] | None,
        typer.Option(
            "--operation-input",
            help="Repeatable operation binding encoded as ROLE=PATH.",
        ),
    ] = None,
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Write the execution report as JSON."),
    ] = False,
) -> None:
    """Execute one installed adapter through orbitfabric.adapter_cli.v1."""
    try:
        bindings = _parse_operation_inputs(operation_input or [])
        report = _manager().execute(
            instance_id,
            operation=operation,
            input_set_manifest=input_set_manifest,
            profile=profile,
            output_dir=output_dir,
            operation_inputs=bindings,
        )
    except (AdapterManagerError, ValueError) as exc:
        _fail(exc)
        return

    if json_output:
        _json_echo(report)
    else:
        typer.echo(f"Integration Result: {report.result_path}")
        typer.echo(f"Result: {report.result.get('result', 'unknown')}")
        if report.stderr.strip():
            typer.echo(report.stderr.strip(), err=True)
    if report.returncode != 0 or report.result.get("result") != "succeeded":
        raise typer.Exit(code=1)


@adapter_app.command("remove")
def remove_adapter(
    instance_id: Annotated[str, typer.Argument(help="Installed adapter instance id.")],
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Write the removed installed record as JSON."),
    ] = False,
) -> None:
    """Remove one adapter materialization and delete its inventory record last."""
    try:
        record = _manager().remove(instance_id)
    except AdapterManagerError as exc:
        _fail(exc)
        return

    if json_output:
        _json_echo(record)
        return
    typer.echo(f"Removed adapter instance: {record.instance_id}")


@lock_app.command("validate")
def validate_adapter_project_lock(
    lock_path: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            help="Adapter Project Lock JSON file.",
        ),
    ],
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Write the conformant project lock as JSON."),
    ] = False,
) -> None:
    """Validate an Adapter Project Lock against the Core candidate contract."""
    try:
        lock = ProjectLockService().load(lock_path)
    except AdapterManagerError as exc:
        _fail(exc)
        return

    if json_output:
        _json_echo(lock)
        return
    typer.echo(f"Adapter Project Lock: {lock_path}")
    typer.echo(f"Version: {lock.lock_version}")
    typer.echo(f"Adapters: {len(lock.adapters)}")
    typer.echo("Result: CONFORMANT")


@lock_app.command("check")
def check_adapter_project_lock(
    lock_path: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            help="Adapter Project Lock JSON file.",
        ),
    ],
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Write the project adapter-state report as JSON."),
    ] = False,
) -> None:
    """Compare exact project-required adapter state with the installed inventory."""
    try:
        manager = _manager()
        report = ProjectLockService().check(lock_path, manager.list())
    except AdapterManagerError as exc:
        _fail(exc)
        return

    if json_output:
        _json_echo(report)
    else:
        typer.echo(f"Adapter Project Lock: {report.lock_path}")
        for adapter in report.adapters:
            label = f"{adapter.source_coordinate.display()}@{adapter.release_version}"
            typer.echo(f"{label}: {adapter.status}")
            if adapter.matching_instance_ids:
                typer.echo(
                    "  matching instances: " + ", ".join(adapter.matching_instance_ids)
                )
            for mismatch in adapter.candidate_mismatches:
                typer.echo(
                    f"  {mismatch.instance_id}: mismatch "
                    + ", ".join(mismatch.dimensions)
                )
        typer.echo(f"Project state: {report.status}")
    if not report.passed:
        raise typer.Exit(code=1)


@lock_app.command("install")
def install_adapter_project_lock_entry(
    lock_path: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            help="Adapter Project Lock JSON file.",
        ),
    ],
    source_coordinate: Annotated[
        str,
        typer.Option(
            "--source-coordinate",
            help="Exact lock entry as AUTHORITY:PUBLISHER/NAME.",
        ),
    ],
    release_descriptor: Annotated[
        Path,
        typer.Option(
            "--release-descriptor",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            help="Exact Adapter Release Descriptor supplied by the explicit source.",
        ),
    ],
    artifact: Annotated[
        Path,
        typer.Option(
            "--artifact",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            help="Exact adapter artifact supplied by the explicit source.",
        ),
    ],
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Write the install-from-lock report as JSON."),
    ] = False,
) -> None:
    """Satisfy one Project Lock entry through explicit exact source material."""
    try:
        coordinate = _parse_source_coordinate(source_coordinate)
        manager = _manager()
        report = ProjectLockInstallService(manager).install_entry(
            lock_path,
            coordinate,
            release_descriptor,
            artifact,
        )
    except (AdapterManagerError, ValueError) as exc:
        _fail(exc)
        return

    if json_output:
        _json_echo(report)
        return
    typer.echo(f"Adapter Project Lock: {report.lock_path}")
    typer.echo(f"Adapter: {report.source_coordinate.display()}")
    typer.echo(f"Before: {report.before_status}")
    typer.echo(f"Action: {report.action}")
    if report.installed_instance_id:
        typer.echo(f"Installed instance: {report.installed_instance_id}")
    typer.echo(f"After: {report.after_status}")


def _parse_operation_inputs(values: list[str]) -> dict[str, Path]:
    bindings: dict[str, Path] = {}
    for value in values:
        role, separator, path_value = value.partition("=")
        role = role.strip()
        path_value = path_value.strip()
        if not separator or not role or not path_value:
            raise ValueError("Operation inputs must use ROLE=PATH syntax")
        if role in bindings:
            raise ValueError(f"Operation input role is bound more than once: {role}")
        bindings[role] = Path(path_value)
    return bindings


def _parse_source_coordinate(value: str) -> AdapterSourceCoordinate:
    authority, authority_separator, logical = value.partition(":")
    publisher, publisher_separator, name = logical.partition("/")
    if (
        not authority_separator
        or not publisher_separator
        or not authority.strip()
        or not publisher.strip()
        or not name.strip()
    ):
        raise ValueError("Source Coordinate must use AUTHORITY:PUBLISHER/NAME syntax")
    return AdapterSourceCoordinate(
        authority=authority.strip(),
        publisher=publisher.strip(),
        name=name.strip(),
    )


__all__ = ["adapter_app"]
