from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Any

import typer

from orbitfabric.adapter_manager import AdapterManager, AdapterManagerError

adapter_app = typer.Typer(
    help="Manage installed OrbitFabric adapters.",
    no_args_is_help=True,
)


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
        typer.Option("--artifact-id", help="Release-local artifact id when multiple artifacts exist."),
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
    """Install one exact adapter release through the M0 explicit-source lane."""
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
    typer.echo(
        "Release: "
        f"{record.source_coordinate.display()}@{record.release_version}"
    )
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


__all__ = ["adapter_app"]
