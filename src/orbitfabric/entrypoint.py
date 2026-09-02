from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer

from orbitfabric import __version__
from orbitfabric.adapter_commands import adapter_app
from orbitfabric.cli import _mission_workspace_default_path, app, export_app
from orbitfabric.export.integration_input_set import write_integration_input_set

app.add_typer(adapter_app, name="adapter")


@export_app.command("integration-input-set")
def export_integration_input_set(
    mission_dir: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
            help="Mission Model directory used to export a coherent integration input set.",
        ),
    ],
    output_dir: Annotated[
        Path | None,
        typer.Option(
            "--output-dir",
            help="Directory where the coherent integration input set will be written.",
        ),
    ] = None,
) -> None:
    """Export one coherent Core Integration Input Set from one load/lint operation."""
    typer.echo(f"OrbitFabric Integration Input Set Export {__version__}")

    output_dir = _mission_workspace_default_path(
        mission_dir,
        output_dir,
        "generated/reports/integration_input",
    )

    try:
        result = write_integration_input_set(mission_dir, output_dir)
    except OSError as exc:
        typer.echo(f"\nError: {exc}")
        typer.echo("\nResult: FAILED")
        raise typer.Exit(code=1) from exc

    manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))

    typer.echo(f"\nLoad result: {manifest['load_result']}")
    typer.echo(f"Lint result: {manifest['lint_result']}")
    typer.echo("Surfaces:")
    for surface in manifest["surfaces"]:
        typer.echo(
            f"  {surface['role']}: {surface['status']}"
            + (
                f" ({surface['unavailable_reason']})"
                if surface["status"] == "unavailable"
                else ""
            )
        )
    typer.echo(f"Manifest: {result.manifest_path}")

    if not result.succeeded:
        typer.echo("\nResult: FAILED")
        raise typer.Exit(code=1)

    typer.echo("\nResult: PASSED")


__all__ = ["app"]
