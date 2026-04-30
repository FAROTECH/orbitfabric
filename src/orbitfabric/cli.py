from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from orbitfabric import __version__
from orbitfabric.gen.docs import generate_markdown_docs
from orbitfabric.lint.engine import LintEngine
from orbitfabric.lint.finding import LintReport
from orbitfabric.lint.json_report import write_lint_report_json
from orbitfabric.model.errors import MissionModelError
from orbitfabric.model.loader import MissionModelLoader
from orbitfabric.model.mission import MissionModel
from orbitfabric.model.scenario_loader import ScenarioLoader
from orbitfabric.sim.json_report import write_simulation_report_json
from orbitfabric.sim.log_writer import write_simulation_log
from orbitfabric.sim.runner import ScenarioRunner

app = typer.Typer(
    name="orbitfabric",
    help="OrbitFabric: a model-first Mission Data Fabric for small spacecraft.",
    no_args_is_help=True,
    invoke_without_command=True,
)

gen_app = typer.Typer(help="Generate artifacts from a Mission Model.")
app.add_typer(gen_app, name="gen")


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            help="Show OrbitFabric version and exit.",
        ),
    ] = False,
) -> None:
    if version:
        typer.echo(f"orbitfabric {__version__}")
        raise typer.Exit()


@app.command()
def lint(
    mission_dir: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
            help="Mission Model directory to lint.",
        ),
    ],
    json_output: Annotated[
        Path | None,
        typer.Option(
            "--json",
            help="Write a machine-readable lint report to this JSON file.",
        ),
    ] = None,
) -> None:
    """Validate and semantically lint a Mission Model."""
    typer.echo("OrbitFabric Mission Lint v0.1")

    try:
        model = MissionModelLoader().load(mission_dir)
    except MissionModelError as exc:
        _print_model_error(exc)
        raise typer.Exit(code=1) from exc

    report = LintEngine().run(model)

    _print_loaded_model_summary(model)
    _print_lint_report(report)

    if json_output is not None:
        write_lint_report_json(model, report, json_output)
        typer.echo(f"\nJSON report written to: {json_output}")

    if report.has_errors:
        raise typer.Exit(code=1)


@gen_app.command("docs")
def gen_docs(
    mission_dir: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
            help="Mission Model directory used to generate documentation.",
        ),
    ],
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output-dir",
            help="Directory where generated Markdown documentation will be written.",
        ),
    ] = Path("generated/docs"),
) -> None:
    """Generate Markdown documentation from a Mission Model."""
    typer.echo("OrbitFabric Docs Generator v0.1")

    try:
        model = MissionModelLoader().load(mission_dir)
    except MissionModelError as exc:
        _print_model_error(exc)
        raise typer.Exit(code=1) from exc

    report = LintEngine().run(model)
    if report.has_errors:
        _print_loaded_model_summary(model)
        _print_lint_report(report)
        typer.echo("\nDocumentation generation aborted because lint errors exist.")
        raise typer.Exit(code=1)

    generated_files = generate_markdown_docs(model, output_dir)

    typer.echo(f"\nMission: {model.spacecraft.id}")
    typer.echo(f"Model version: {model.spacecraft.model_version}")
    typer.echo(f"Output directory: {output_dir}")
    typer.echo("\nGenerated files:")
    for path in generated_files:
        typer.echo(f"  {path}")

    typer.echo("\nResult: PASSED")


@app.command()
def sim(
    scenario_file: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            help="Scenario YAML file to execute.",
        ),
    ],
    json_output: Annotated[
        Path | None,
        typer.Option(
            "--json",
            help="Write a machine-readable simulation report to this JSON file.",
        ),
    ] = None,
    log_output: Annotated[
        Path | None,
        typer.Option(
            "--log",
            help="Write a plain-text simulation timeline log to this file.",
        ),
    ] = None,
) -> None:
    """Run a scenario against a Mission Model."""
    typer.echo("OrbitFabric Scenario Simulator v0.1")

    try:
        loaded = ScenarioLoader().load(scenario_file)
    except MissionModelError as exc:
        _print_model_error(exc)
        raise typer.Exit(code=1) from exc

    result = ScenarioRunner().run(loaded)

    typer.echo(f"\nScenario: {result.scenario_id}")
    typer.echo(f"Mission: {result.mission_id}")
    typer.echo("\nTimeline:")
    for entry in result.state.logs:
        typer.echo(f"  {entry.format()}")

    typer.echo(f"\nResult: {result.result_label}")

    if json_output is not None:
        write_simulation_report_json(result, json_output)
        typer.echo(f"\nJSON report written to: {json_output}")

    if log_output is not None:
        write_simulation_log(result, log_output)
        typer.echo(f"Log written to: {log_output}")

    if not result.passed:
        raise typer.Exit(code=1)


def _print_model_error(exc: MissionModelError) -> None:
    typer.echo("\nFindings:")
    for diagnostic in exc.diagnostics:
        typer.echo(f"  {diagnostic.format()}")
    typer.echo("\nResult: FAILED")


def _print_loaded_model_summary(model: MissionModel) -> None:
    typer.echo(f"\nMission: {model.spacecraft.id}")
    typer.echo(f"Model version: {model.spacecraft.model_version}")
    typer.echo("\nLoaded:")
    typer.echo("  spacecraft: 1")
    typer.echo(f"  subsystems: {len(model.subsystems)}")
    typer.echo(f"  modes: {len(model.modes)}")
    typer.echo(f"  mode transitions: {len(model.mode_transitions)}")
    typer.echo(f"  telemetry: {len(model.telemetry)}")
    typer.echo(f"  commands: {len(model.commands)}")
    typer.echo(f"  events: {len(model.events)}")
    typer.echo(f"  faults: {len(model.faults)}")
    typer.echo(f"  packets: {len(model.packets)}")


def _print_lint_report(report: LintReport) -> None:
    typer.echo("\nFindings:")
    if report.findings:
        for finding in report.findings:
            typer.echo(f"  {finding.format()}")
    else:
        typer.echo("  No findings.")

    typer.echo("\nSummary:")
    typer.echo(f"  errors: {report.error_count}")
    typer.echo(f"  warnings: {report.warning_count}")
    typer.echo(f"  info: {report.info_count}")

    typer.echo(f"\nResult: {report.result_label}")