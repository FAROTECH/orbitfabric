from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer

from orbitfabric import __version__
from orbitfabric.adapter_commands import adapter_app
from orbitfabric.cli import _mission_workspace_default_path, app, export_app
from orbitfabric.export.integration_input_set import write_integration_input_set
from orbitfabric.export.scenario_declaration import write_scenario_declaration

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


@export_app.command("scenario-declaration")
def export_scenario_declaration(
    scenario_file: Annotated[
        Path,
        typer.Argument(
            help="Scenario YAML file used to export the Core-normalized declaration.",
        ),
    ],
    json_output: Annotated[
        Path,
        typer.Option(
            "--json",
            help="Write the candidate declared Scenario surface to this JSON file.",
        ),
    ],
) -> None:
    """Export one Core-owned candidate declared Scenario surface."""
    typer.echo(f"OrbitFabric Scenario Declaration Export {__version__}")

    try:
        written_file = write_scenario_declaration(scenario_file, json_output)
    except OSError as exc:
        typer.echo(f"\nError: unable to write Scenario declaration: {exc}")
        typer.echo("\nResult: FAILED")
        raise typer.Exit(code=1) from exc

    payload = json.loads(written_file.read_text(encoding="utf-8"))

    if payload["result"] == "failed":
        _print_structured_diagnostics(payload["diagnostics"])
        typer.echo("Status: candidate")
        typer.echo(f"JSON report written to: {written_file}")
        typer.echo("\nResult: FAILED")
        raise typer.Exit(code=1)

    typer.echo(f"\nScenario: {payload['scenario']['id']}")
    typer.echo(f"Mission: {payload['mission']['id']}")
    typer.echo(f"Model version: {payload['mission']['model_version']}")
    typer.echo(f"Declared atoms: {payload['atom_count']}")
    typer.echo("Status: candidate")
    typer.echo(f"JSON report written to: {written_file}")
    typer.echo("\nResult: PASSED")


def _print_structured_diagnostics(diagnostics: list[dict[str, object]]) -> None:
    if not diagnostics:
        return
    typer.echo("\nFindings:")
    for diagnostic in diagnostics:
        parts = [str(diagnostic.get("severity") or "ERROR"), str(diagnostic.get("code") or "")]
        for field in ("file", "object_id"):
            value = diagnostic.get(field)
            if value:
                parts.append(str(value))
        message = diagnostic.get("message")
        if message:
            parts.append(str(message))
        suggestion = diagnostic.get("suggestion")
        if suggestion:
            parts.append(f"Suggestion: {suggestion}")
        typer.echo(f"  {' '.join(part for part in parts if part)}")


__all__ = ["app"]
