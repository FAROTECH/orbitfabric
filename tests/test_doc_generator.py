from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from orbitfabric import __version__
from orbitfabric.cli import app
from orbitfabric.gen.docs import generate_markdown_docs
from orbitfabric.model.loader import MissionModelLoader

DEMO_MISSION = Path("examples/demo-3u/mission")
runner = CliRunner()


def test_generate_markdown_docs(tmp_path: Path) -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    generated_files = generate_markdown_docs(model, tmp_path)

    generated_names = {path.name for path in generated_files}
    assert generated_names == {
        "telemetry.md",
        "commands.md",
        "events.md",
        "faults.md",
        "modes.md",
        "packets.md",
        "payloads.md",
        "data_products.md",
        "contacts.md",
        "commandability.md",
    }

    telemetry_doc = (tmp_path / "telemetry.md").read_text(encoding="utf-8")
    commands_doc = (tmp_path / "commands.md").read_text(encoding="utf-8")
    payloads_doc = (tmp_path / "payloads.md").read_text(encoding="utf-8")
    data_products_doc = (tmp_path / "data_products.md").read_text(encoding="utf-8")
    commandability_doc = (tmp_path / "commandability.md").read_text(encoding="utf-8")

    assert "Telemetry Reference" in telemetry_doc
    assert "eps.battery.voltage" in telemetry_doc
    assert "Battery Voltage" in telemetry_doc
    assert "Command Reference" in commands_doc
    assert "payload.start_acquisition" in commands_doc
    assert "Payload Contract Reference" in payloads_doc
    assert "demo_iod_payload" in payloads_doc
    assert "Data Product Contract Reference" in data_products_doc
    assert "payload.radiation_histogram" in data_products_doc

    assert "Commandability and Autonomy Contract Reference" in commandability_doc
    assert "ground_operator" in commandability_doc
    assert "onboard_autonomy" in commandability_doc
    assert "payload_start_ground_rule" in commandability_doc
    assert "stop_payload_on_battery_low" in commandability_doc
    assert "payload_battery_critical_recovery" in commandability_doc

    faults_doc = (tmp_path / "faults.md").read_text(encoding="utf-8")

    assert "## Summary" in telemetry_doc
    assert "## Telemetry by subsystem" in telemetry_doc
    assert "### `eps`" in telemetry_doc
    assert "`warning_low` = `6.8`" in telemetry_doc
    assert "`critical_low` = `6.4`" in telemetry_doc

    assert "## Commands by target subsystem" in commands_doc
    assert "### `payload`" in commands_doc
    assert "`duration_s`: `uint16`" in commands_doc
    assert "`payload.acquisition.active` = `true`" in commands_doc
    assert "mode -> `PAYLOAD_ACTIVE`" in commands_doc

    assert "## Faults by source subsystem" in faults_doc
    assert "`eps.battery.voltage` < `6.8`" in faults_doc
    assert "debounce `3` samples" in faults_doc
    assert "mode -> `DEGRADED`" in faults_doc
    assert "auto commands: `payload.stop_acquisition`" in faults_doc


def test_gen_docs_cli_writes_markdown_files(tmp_path: Path) -> None:
    output_dir = tmp_path / "docs"

    result = runner.invoke(
        app,
        [
            "gen",
            "docs",
            "examples/demo-3u/mission",
            "--output-dir",
            str(output_dir),
        ],
    )

    assert result.exit_code == 0
    assert f"OrbitFabric Docs Generator {__version__}" in result.output
    assert "Generated files:" in result.output
    assert "Result: PASSED" in result.output

    assert (output_dir / "telemetry.md").exists()
    assert (output_dir / "commands.md").exists()
    assert (output_dir / "events.md").exists()
    assert (output_dir / "faults.md").exists()
    assert (output_dir / "modes.md").exists()
    assert (output_dir / "packets.md").exists()
    assert (output_dir / "payloads.md").exists()
    assert (output_dir / "data_products.md").exists()
    assert (output_dir / "commandability.md").exists()
