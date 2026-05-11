from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from orbitfabric import __version__
from orbitfabric.gen.data_flow import generate_data_flow_markdown_doc
from orbitfabric.gen.docs import generate_markdown_docs
from orbitfabric.gen.ground import (
    build_ground_contract,
    write_ground_contract_manifest,
    write_ground_dictionary_csv_files,
    write_ground_dictionary_json_files,
)
from orbitfabric.gen.runtime import (
    build_runtime_contract,
    generate_cpp17_runtime_files,
    write_runtime_contract_manifest,
)
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

validate_app = typer.Typer(help="Validate OrbitFabric inputs without executing them.")
app.add_typer(validate_app, name="validate")

inspect_app = typer.Typer(help="Inspect OrbitFabric models and inputs.")
app.add_typer(inspect_app, name="inspect")


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
    warnings_as_errors: Annotated[
        bool,
        typer.Option(
            "--warnings-as-errors",
            help="Fail lint when warning-level findings are present.",
        ),
    ] = False,
) -> None:
    """Validate and semantically lint a Mission Model."""
    typer.echo(f"OrbitFabric Mission Lint {__version__}")

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

    if warnings_as_errors and report.warning_count > 0:
        typer.echo("\nWarnings are treated as errors.")
        raise typer.Exit(code=1)

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
    typer.echo(f"OrbitFabric Docs Generator {__version__}")

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
    generated_files.append(
        generate_data_flow_markdown_doc(model, output_dir / "data_flow.md")
    )

    typer.echo(f"\nMission: {model.spacecraft.id}")
    typer.echo(f"Model version: {model.spacecraft.model_version}")
    typer.echo(f"Output directory: {output_dir}")
    typer.echo("\nGenerated files:")
    for path in generated_files:
        typer.echo(f"  {path}")

    typer.echo("\nResult: PASSED")


@gen_app.command("data-flow")
def gen_data_flow(
    mission_dir: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
            help="Mission Model directory used to generate data-flow documentation.",
        ),
    ],
    output_file: Annotated[
        Path,
        typer.Option(
            "--output-file",
            help="Markdown file where data-flow documentation will be written.",
        ),
    ] = Path("generated/docs/data_flow.md"),
) -> None:
    """Generate Markdown data-flow documentation from a Mission Model."""
    typer.echo(f"OrbitFabric Data Flow Docs Generator {__version__}")

    try:
        model = MissionModelLoader().load(mission_dir)
    except MissionModelError as exc:
        _print_model_error(exc)
        raise typer.Exit(code=1) from exc

    report = LintEngine().run(model)
    if report.has_errors:
        _print_loaded_model_summary(model)
        _print_lint_report(report)
        typer.echo("\nData-flow documentation generation aborted because lint errors exist.")
        raise typer.Exit(code=1)

    generated_file = generate_data_flow_markdown_doc(model, output_file)

    typer.echo(f"\nMission: {model.spacecraft.id}")
    typer.echo(f"Model version: {model.spacecraft.model_version}")
    typer.echo(f"Generated file: {generated_file}")
    typer.echo("\nResult: PASSED")


@gen_app.command("runtime")
def gen_runtime(
    mission_dir: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
            help="Mission Model directory used to generate runtime-facing artifacts.",
        ),
    ],
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output-dir",
            help="Directory where runtime generation artifacts will be written.",
        ),
    ] = Path("generated/runtime"),
    profile: Annotated[
        str,
        typer.Option(
            "--profile",
            help="Runtime generation profile. Currently only 'cpp17' is supported.",
        ),
    ] = "cpp17",
) -> None:
    """Generate runtime-facing contract artifacts from a Mission Model."""
    typer.echo(f"OrbitFabric Runtime Generator {__version__}")

    if profile != "cpp17":
        typer.echo(f"\nUnsupported runtime generation profile: {profile}")
        typer.echo("Supported profiles: cpp17")
        raise typer.Exit(code=1)

    try:
        model = MissionModelLoader().load(mission_dir)
    except MissionModelError as exc:
        _print_model_error(exc)
        raise typer.Exit(code=1) from exc

    report = LintEngine().run(model)
    if report.has_errors:
        _print_loaded_model_summary(model)
        _print_lint_report(report)
        typer.echo("\nRuntime generation aborted because lint errors exist.")
        raise typer.Exit(code=1)

    contract = build_runtime_contract(model, generation_profile=profile)
    manifest_file = output_dir / profile / "runtime_contract_manifest.json"
    generated_files = [write_runtime_contract_manifest(contract, manifest_file)]
    generated_files.extend(generate_cpp17_runtime_files(contract, output_dir))

    typer.echo(f"\nMission: {model.spacecraft.id}")
    typer.echo(f"Model version: {model.spacecraft.model_version}")
    typer.echo(f"Profile: {profile}")
    typer.echo("\nGenerated files:")
    for path in generated_files:
        typer.echo(f"  {path}")
    typer.echo("\nRuntime contract counts:")
    typer.echo(f"  modes: {len(contract.modes)}")
    typer.echo(f"  telemetry: {len(contract.telemetry)}")
    typer.echo(f"  commands: {len(contract.commands)}")
    typer.echo(f"  events: {len(contract.events)}")
    typer.echo(f"  faults: {len(contract.faults)}")
    typer.echo(f"  packets: {len(contract.packets)}")
    typer.echo(f"  payloads: {len(contract.payloads)}")
    typer.echo(f"  data products: {len(contract.data_products)}")
    typer.echo("\nResult: PASSED")


@gen_app.command("ground")
def gen_ground(
    mission_dir: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
            help="Mission Model directory used to generate ground-facing artifacts.",
        ),
    ],
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output-dir",
            help="Directory where ground generation artifacts will be written.",
        ),
    ] = Path("generated/ground"),
    profile: Annotated[
        str,
        typer.Option(
            "--profile",
            help="Ground generation profile. Currently only 'generic' is supported.",
        ),
    ] = "generic",
) -> None:
    """Generate ground-facing contract artifacts from a Mission Model."""
    typer.echo(f"OrbitFabric Ground Generator {__version__}")

    if profile != "generic":
        typer.echo(f"\nUnsupported ground generation profile: {profile}")
        typer.echo("Supported profiles: generic")
        raise typer.Exit(code=1)

    try:
        model = MissionModelLoader().load(mission_dir)
    except MissionModelError as exc:
        _print_model_error(exc)
        raise typer.Exit(code=1) from exc

    report = LintEngine().run(model)
    if report.has_errors:
        _print_loaded_model_summary(model)
        _print_lint_report(report)
        typer.echo("\nGround generation aborted because lint errors exist.")
        raise typer.Exit(code=1)

    contract = build_ground_contract(model, generation_profile=profile)
    profile_output_dir = output_dir / profile
    manifest_file = profile_output_dir / "ground_contract_manifest.json"
    generated_files = [write_ground_contract_manifest(contract, manifest_file)]
    generated_files.extend(write_ground_dictionary_json_files(contract, profile_output_dir))
    generated_files.extend(write_ground_dictionary_csv_files(contract, profile_output_dir))

    typer.echo(f"\nMission: {model.spacecraft.id}")
    typer.echo(f"Model version: {model.spacecraft.model_version}")
    typer.echo(f"Profile: {profile}")
    typer.echo("\nGenerated files:")
    for path in generated_files:
        typer.echo(f"  {path}")
    typer.echo("\nGround contract counts:")
    typer.echo(f"  telemetry: {len(contract.telemetry)}")
    typer.echo(f"  commands: {len(contract.commands)}")
    typer.echo(f"  events: {len(contract.events)}")
    typer.echo(f"  faults: {len(contract.faults)}")
    typer.echo(f"  data products: {len(contract.data_products)}")
    typer.echo(f"  packets: {len(contract.packets)}")
    typer.echo("\nResult: PASSED")


@inspect_app.command("mission")
def inspect_mission(
    mission_dir: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
            help="Mission Model directory to inspect.",
        ),
    ],
) -> None:
    """Inspect a Mission Model without linting or generating artifacts."""
    typer.echo(f"OrbitFabric Mission Inspection {__version__}")

    try:
        model = MissionModelLoader().load(mission_dir)
    except MissionModelError as exc:
        _print_model_error(exc)
        raise typer.Exit(code=1) from exc

    _print_loaded_model_summary(model)

    typer.echo("\nResult: PASSED")


@validate_app.command("scenario")
def validate_scenario(
    scenario_file: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            help="Scenario YAML file to validate.",
        ),
    ],
) -> None:
    """Validate a scenario without executing it."""
    typer.echo(f"OrbitFabric Scenario Validation {__version__}")

    try:
        loaded = ScenarioLoader().load(scenario_file)
    except MissionModelError as exc:
        _print_model_error(exc)
        raise typer.Exit(code=1) from exc

    typer.echo(f"\nScenario: {loaded.scenario.scenario.id}")
    typer.echo(f"Mission: {loaded.mission_model.spacecraft.id}")
    typer.echo(f"Model version: {loaded.mission_model.spacecraft.model_version}")
    typer.echo(f"Initial mode: {loaded.scenario.initial_state.mode}")
    typer.echo(f"Steps: {len(loaded.scenario.steps)}")

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
    typer.echo(f"OrbitFabric Scenario Simulator {__version__}")

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
    typer.echo(f"  payloads: {len(model.payloads)}")
    typer.echo(f"  data products: {len(model.data_products)}")


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