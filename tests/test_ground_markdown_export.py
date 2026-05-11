from __future__ import annotations

from pathlib import Path

from orbitfabric.gen.ground import (
    build_ground_contract,
    write_ground_markdown_review_artifacts,
)
from orbitfabric.model.loader import MissionModelLoader

DEMO_MISSION = Path("examples/demo-3u/mission")


def test_write_ground_markdown_review_artifacts(tmp_path: Path) -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    contract = build_ground_contract(model)

    written_files = write_ground_markdown_review_artifacts(contract, tmp_path)

    assert written_files == [
        tmp_path / "README.md",
        tmp_path / "ground_dictionaries.md",
    ]
    assert (tmp_path / "README.md").exists()
    assert (tmp_path / "ground_dictionaries.md").exists()


def test_ground_readme_is_human_reviewable(tmp_path: Path) -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    contract = build_ground_contract(model)

    write_ground_markdown_review_artifacts(contract, tmp_path)

    content = (tmp_path / "README.md").read_text(encoding="utf-8")

    assert content.startswith("# OrbitFabric Ground Integration Artifacts")
    assert "## Mission" in content
    assert "## Generated files" in content
    assert "## Contract coverage" in content
    assert "## Boundary" in content
    assert "## Recommended review flow" in content
    assert "Mission ID: `demo-3u`" in content
    assert "Ground profile: `generic`" in content
    assert "`ground_contract_manifest.json`" in content
    assert "`ground_dictionaries.md`" in content
    assert "The Mission Model remains the source of truth." in content
    assert "They also do not claim compatibility with Yamcs, OpenC3, XTCE, CCSDS, PUS or CFDP." in content


def test_ground_dictionaries_markdown_contains_review_sections(tmp_path: Path) -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    contract = build_ground_contract(model)

    write_ground_markdown_review_artifacts(contract, tmp_path)

    content = (tmp_path / "ground_dictionaries.md").read_text(encoding="utf-8")

    assert content.startswith("# Ground Dictionaries Review")
    assert "## Review boundary" in content
    assert "## Summary" in content
    assert "## Telemetry dictionary" in content
    assert "## Command dictionary" in content
    assert "## Event dictionary" in content
    assert "## Fault dictionary" in content
    assert "## Data product dictionary" in content
    assert "## Packet dictionary" in content
    assert "This document is generated from the OrbitFabric `GroundContract`" in content
    assert "This document is not a ground runtime specification." in content


def test_ground_dictionaries_markdown_contains_domain_content(tmp_path: Path) -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    contract = build_ground_contract(model)

    write_ground_markdown_review_artifacts(contract, tmp_path)

    content = (tmp_path / "ground_dictionaries.md").read_text(encoding="utf-8")

    assert "`eps.battery.voltage`" in content
    assert "Battery Voltage" in content
    assert "warning_low: 6.8" in content
    assert "`payload.start_acquisition`" in content
    assert "`duration_s` (uint16" in content
    assert "`payload.acquisition_started`" in content
    assert "`eps.battery_low`" in content
    assert "`eps.battery_low_fault`" in content
    assert "`payload.radiation_histogram`" in content
    assert "`hk_fast`" in content
