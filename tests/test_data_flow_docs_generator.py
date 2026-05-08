from __future__ import annotations

from pathlib import Path

from orbitfabric.gen.data_flow import generate_data_flow_markdown_doc
from orbitfabric.model.loader import MissionModelLoader

DEMO_MISSION = Path("examples/demo-3u/mission")


def test_generate_data_flow_markdown_doc(tmp_path: Path) -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    output_file = tmp_path / "data_flow.md"

    generated_file = generate_data_flow_markdown_doc(model, output_file)

    assert generated_file == output_file
    assert output_file.exists()

    content = output_file.read_text(encoding="utf-8")

    assert "# Mission Data Flow Evidence Reference" in content
    assert "Mission: `demo-3u`" in content
    assert "Declared data-flow paths: `1`" in content
    assert "Data products with command effects: `1`" in content
    assert "Downlink flows involved: `1`" in content
    assert "Contact windows involved: `1`" in content
    assert "This document is generated from declared Mission Model contracts." in content
    assert "It does not imply real payload file generation" in content
    assert "`payload.start_acquisition`" in content
    assert "`payload.radiation_histogram`" in content
    assert "`demo_iod_payload` (`payload`)" in content
    assert "class `science`" in content
    assert "retention `7d`" in content
    assert "overflow `drop_oldest`" in content
    assert "policy `next_available_contact`" in content
    assert "`science_next_available_contact`" in content
    assert "`demo_contact_001`" in content


def test_generate_data_flow_markdown_doc_without_command_effects(tmp_path: Path) -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    for command in model.commands:
        command.expected_effects.pop("data_products", None)

    output_file = tmp_path / "data_flow.md"

    generate_data_flow_markdown_doc(model, output_file)

    content = output_file.read_text(encoding="utf-8")

    assert "Declared data-flow paths: `0`" in content
    assert "No command-declared data-flow paths found." in content
