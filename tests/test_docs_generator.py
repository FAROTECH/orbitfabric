from __future__ import annotations

from pathlib import Path

from orbitfabric.gen.docs import generate_markdown_docs
from orbitfabric.model.loader import MissionModelLoader

DEMO_MISSION = Path("examples/demo-3u/mission")


def test_generate_payload_contract_docs(tmp_path: Path) -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    generated_files = generate_markdown_docs(model, tmp_path)

    payloads_path = tmp_path / "payloads.md"
    generated_names = {path.name for path in generated_files}

    assert "payloads.md" in generated_names
    assert payloads_path.exists()

    content = payloads_path.read_text(encoding="utf-8")

    assert "# Payload Contract Reference" in content
    assert "`demo_iod_payload`" in content
    assert "`payload` - Demo Payload" in content
    assert "`iod`" in content
    assert "`READY`" in content
    assert "`ACQUIRING`" in content
    assert "`payload.acquisition.active`" in content
    assert "`payload.start_acquisition`" in content
    assert "`payload.acquisition_started`" in content


def test_payload_contract_docs_are_skipped_without_payloads(tmp_path: Path) -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    model.payloads = []

    generated_files = generate_markdown_docs(model, tmp_path)
    generated_names = {path.name for path in generated_files}

    assert "payloads.md" not in generated_names
    assert not (tmp_path / "payloads.md").exists()
