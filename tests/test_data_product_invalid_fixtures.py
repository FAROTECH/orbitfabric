from __future__ import annotations

from pathlib import Path

import pytest

from orbitfabric.lint.engine import LintEngine
from orbitfabric.model.errors import MissionModelError
from orbitfabric.model.loader import MissionModelLoader

DEMO_MISSION = Path("examples/demo-3u/mission")

VALID_DATA_PRODUCTS = """data_products:
  - id: payload.radiation_histogram
    producer: demo_iod_payload
    producer_type: payload
    type: histogram
    estimated_size_bytes: 4096
    priority: high
    storage:
      class: science
      retention: 7d
      overflow_policy: drop_oldest
    downlink:
      policy: next_available_contact
"""


def copy_demo_mission(tmp_path: Path) -> Path:
    mission_dir = tmp_path / "mission"
    mission_dir.mkdir()

    for source_file in DEMO_MISSION.glob("*.yaml"):
        (mission_dir / source_file.name).write_text(
            source_file.read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    return mission_dir


def load_with_data_products(tmp_path: Path, data_products_yaml: str):
    mission_dir = copy_demo_mission(tmp_path)
    (mission_dir / "data_products.yaml").write_text(
        data_products_yaml,
        encoding="utf-8",
    )

    return MissionModelLoader().load(mission_dir)


def assert_structural_failure(tmp_path: Path, data_products_yaml: str) -> None:
    with pytest.raises(MissionModelError) as exc_info:
        load_with_data_products(tmp_path, data_products_yaml)

    codes = {diagnostic.code for diagnostic in exc_info.value.diagnostics}
    assert "OF-STR-003" in codes


def test_valid_data_product_fixture_loads_and_lints_cleanly(tmp_path: Path) -> None:
    model = load_with_data_products(tmp_path, VALID_DATA_PRODUCTS)
    report = LintEngine().run(model)

    assert model.data_product_ids == {"payload.radiation_histogram"}
    assert report.error_count == 0
    assert report.warning_count == 0


def test_duplicate_data_product_id_fixture_fails(tmp_path: Path) -> None:
    model_yaml = """data_products:
  - id: payload.radiation_histogram
    producer: demo_iod_payload
    producer_type: payload
    type: histogram
    estimated_size_bytes: 4096
    priority: high
  - id: payload.radiation_histogram
    producer: demo_iod_payload
    producer_type: payload
    type: histogram
    estimated_size_bytes: 4096
    priority: high
"""

    with pytest.raises(MissionModelError) as exc_info:
        load_with_data_products(tmp_path, model_yaml)

    assert any(
        diagnostic.code == "OF-ID-001"
        and diagnostic.file == "data_products.yaml"
        and diagnostic.domain == "data_products"
        for diagnostic in exc_info.value.diagnostics
    )


def test_missing_producer_fixture_fails_structural_validation(tmp_path: Path) -> None:
    model_yaml = """data_products:
  - id: payload.radiation_histogram
    producer_type: payload
    type: histogram
    estimated_size_bytes: 4096
    priority: high
"""

    assert_structural_failure(tmp_path, model_yaml)


def test_unknown_payload_producer_fixture_fails_lint(tmp_path: Path) -> None:
    model_yaml = """data_products:
  - id: payload.radiation_histogram
    producer: missing_payload
    producer_type: payload
    type: histogram
    estimated_size_bytes: 4096
    priority: high
    storage:
      class: science
      retention: 7d
      overflow_policy: drop_oldest
    downlink:
      policy: next_available_contact
"""

    model = load_with_data_products(tmp_path, model_yaml)
    report = LintEngine().run(model)

    codes = {finding.code for finding in report.findings}
    assert "OF-DP-002" in codes
    assert report.has_errors


def test_unknown_subsystem_producer_fixture_fails_lint(tmp_path: Path) -> None:
    model_yaml = """data_products:
  - id: payload.radiation_histogram
    producer: missing_subsystem
    producer_type: subsystem
    type: histogram
    estimated_size_bytes: 4096
    priority: high
    storage:
      class: science
      retention: 7d
      overflow_policy: drop_oldest
    downlink:
      policy: next_available_contact
"""

    model = load_with_data_products(tmp_path, model_yaml)
    report = LintEngine().run(model)

    codes = {finding.code for finding in report.findings}
    assert "OF-DP-002" in codes
    assert report.has_errors


def test_unknown_payload_reference_fixture_fails_lint(tmp_path: Path) -> None:
    model_yaml = """data_products:
  - id: payload.radiation_histogram
    producer: demo_iod_payload
    producer_type: payload
    payload: missing_payload
    type: histogram
    estimated_size_bytes: 4096
    priority: high
    storage:
      class: science
      retention: 7d
      overflow_policy: drop_oldest
    downlink:
      policy: next_available_contact
"""

    model = load_with_data_products(tmp_path, model_yaml)
    report = LintEngine().run(model)

    codes = {finding.code for finding in report.findings}
    assert "OF-DP-003" in codes
    assert report.has_errors


def test_non_positive_estimated_size_fixture_fails_structural_validation(
    tmp_path: Path,
) -> None:
    model_yaml = """data_products:
  - id: payload.radiation_histogram
    producer: demo_iod_payload
    producer_type: payload
    type: histogram
    estimated_size_bytes: 0
    priority: high
"""

    assert_structural_failure(tmp_path, model_yaml)


def test_unknown_priority_fixture_fails_structural_validation(tmp_path: Path) -> None:
    model_yaml = """data_products:
  - id: payload.radiation_histogram
    producer: demo_iod_payload
    producer_type: payload
    type: histogram
    estimated_size_bytes: 4096
    priority: urgent
"""

    assert_structural_failure(tmp_path, model_yaml)


def test_malformed_storage_fixture_fails_structural_validation(tmp_path: Path) -> None:
    model_yaml = """data_products:
  - id: payload.radiation_histogram
    producer: demo_iod_payload
    producer_type: payload
    type: histogram
    estimated_size_bytes: 4096
    priority: high
    storage: science
"""

    assert_structural_failure(tmp_path, model_yaml)


def test_unknown_storage_class_fixture_fails_structural_validation(tmp_path: Path) -> None:
    model_yaml = """data_products:
  - id: payload.radiation_histogram
    producer: demo_iod_payload
    producer_type: payload
    type: histogram
    estimated_size_bytes: 4096
    priority: high
    storage:
      class: archive
      retention: 7d
      overflow_policy: drop_oldest
"""

    assert_structural_failure(tmp_path, model_yaml)


def test_missing_retention_fixture_emits_lint_warning(tmp_path: Path) -> None:
    model_yaml = """data_products:
  - id: payload.radiation_histogram
    producer: demo_iod_payload
    producer_type: payload
    type: histogram
    estimated_size_bytes: 4096
    priority: medium
    storage:
      class: science
      overflow_policy: drop_oldest
"""

    model = load_with_data_products(tmp_path, model_yaml)
    report = LintEngine().run(model)

    codes = {finding.code for finding in report.findings}
    assert "OF-DP-006" in codes
    assert report.warning_count >= 1


def test_unknown_overflow_policy_fixture_fails_structural_validation(
    tmp_path: Path,
) -> None:
    model_yaml = """data_products:
  - id: payload.radiation_histogram
    producer: demo_iod_payload
    producer_type: payload
    type: histogram
    estimated_size_bytes: 4096
    priority: high
    storage:
      class: science
      retention: 7d
      overflow_policy: erase_random
"""

    assert_structural_failure(tmp_path, model_yaml)


def test_malformed_downlink_fixture_fails_structural_validation(tmp_path: Path) -> None:
    model_yaml = """data_products:
  - id: payload.radiation_histogram
    producer: demo_iod_payload
    producer_type: payload
    type: histogram
    estimated_size_bytes: 4096
    priority: high
    downlink: next_available_contact
"""

    assert_structural_failure(tmp_path, model_yaml)


def test_unknown_downlink_policy_fixture_fails_structural_validation(
    tmp_path: Path,
) -> None:
    model_yaml = """data_products:
  - id: payload.radiation_histogram
    producer: demo_iod_payload
    producer_type: payload
    type: histogram
    estimated_size_bytes: 4096
    priority: high
    downlink:
      policy: immediate_rf_dump
"""

    assert_structural_failure(tmp_path, model_yaml)


def test_high_priority_without_downlink_fixture_emits_lint_warning(
    tmp_path: Path,
) -> None:
    model_yaml = """data_products:
  - id: payload.radiation_histogram
    producer: demo_iod_payload
    producer_type: payload
    type: histogram
    estimated_size_bytes: 4096
    priority: high
    storage:
      class: science
      retention: 7d
      overflow_policy: drop_oldest
"""

    model = load_with_data_products(tmp_path, model_yaml)
    report = LintEngine().run(model)

    codes = {finding.code for finding in report.findings}
    assert "OF-DP-008" in codes
    assert report.warning_count >= 1
