from __future__ import annotations

from pathlib import Path

from orbitfabric.gen.docs import generate_markdown_docs
from orbitfabric.model.loader import MissionModelLoader
from orbitfabric.model.mission import (
    DataProductContract,
    DataProductDownlinkIntent,
    DataProductStorageIntent,
)

DEMO_MISSION = Path("examples/demo-3u/mission")


def make_valid_data_product() -> DataProductContract:
    return DataProductContract(
        id="payload.synthetic_histogram",
        producer="demo_iod_payload",
        producer_type="payload",
        type="histogram",
        estimated_size_bytes=2048,
        priority="medium",
        storage=DataProductStorageIntent(
            **{
                "class": "science",
                "retention": "3d",
                "overflow_policy": "drop_oldest",
            }
        ),
        downlink=DataProductDownlinkIntent(policy="priority_based"),
        description="Synthetic payload histogram data product.",
    )


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


def test_generate_demo_data_product_contract_docs(tmp_path: Path) -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    generated_files = generate_markdown_docs(model, tmp_path)

    data_products_path = tmp_path / "data_products.md"
    generated_names = {path.name for path in generated_files}

    assert "data_products.md" in generated_names
    assert data_products_path.exists()

    content = data_products_path.read_text(encoding="utf-8")

    assert "# Data Product Contract Reference" in content
    assert "Storage and downlink fields describe contract intent only." in content
    assert "`payload.radiation_histogram`" in content
    assert "`demo_iod_payload` (`payload`)" in content
    assert "`histogram`" in content
    assert "4096" in content
    assert "`high`" in content
    assert "class `science`" in content
    assert "retention `7d`" in content
    assert "overflow `drop_oldest`" in content
    assert "policy `next_available_contact`" in content
    assert "Synthetic payload histogram data product used to demonstrate" in content


def test_generate_data_product_contract_docs_from_model_object(tmp_path: Path) -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    model.data_products = [make_valid_data_product()]

    generated_files = generate_markdown_docs(model, tmp_path)

    data_products_path = tmp_path / "data_products.md"
    generated_names = {path.name for path in generated_files}

    assert "data_products.md" in generated_names
    assert data_products_path.exists()

    content = data_products_path.read_text(encoding="utf-8")

    assert "`payload.synthetic_histogram`" in content
    assert "2048" in content
    assert "`medium`" in content
    assert "retention `3d`" in content
    assert "policy `priority_based`" in content


def test_data_product_contract_docs_are_skipped_without_data_products(
    tmp_path: Path,
) -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    model.data_products = []

    generated_files = generate_markdown_docs(model, tmp_path)
    generated_names = {path.name for path in generated_files}

    assert "data_products.md" not in generated_names
    assert not (tmp_path / "data_products.md").exists()
