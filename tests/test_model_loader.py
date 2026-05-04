from __future__ import annotations

from pathlib import Path

import pytest

from orbitfabric.model.errors import MissionModelError
from orbitfabric.model.loader import MissionModelLoader

DEMO_MISSION = Path("examples/demo-3u/mission")

VALID_DATA_PRODUCTS_YAML = """data_products:
  - id: payload.synthetic_histogram
    producer: demo_iod_payload
    producer_type: payload
    type: histogram
    estimated_size_bytes: 2048
    priority: medium
    storage:
      class: science
      retention: 3d
      overflow_policy: drop_oldest
    downlink:
      policy: priority_based
    description: Synthetic payload data product used to validate data product contracts.
"""

VALID_CONTACTS_YAML = """contacts:
  contact_profiles:
    - id: primary_ground_contact
      target: synthetic_ground_station
      description: Synthetic primary ground contact used by the demo mission.
  link_profiles:
    - id: uhf_downlink_nominal
      direction: downlink
      assumed_rate_bps: 9600
      description: Abstract nominal downlink assumption.
  contact_windows:
    - id: demo_contact_001
      contact_profile: primary_ground_contact
      link_profile: uhf_downlink_nominal
      start: "2026-01-01T00:00:00Z"
      duration_seconds: 600
      assumed_capacity_bytes: 512000
  downlink_flows:
    - id: science_next_available_contact
      contact_profile: primary_ground_contact
      link_profile: uhf_downlink_nominal
      queue_policy: priority_then_age
      eligible_data_products:
        - payload.radiation_histogram
      description: Synthetic science downlink flow used to validate contact contracts.
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


def test_load_demo_mission() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    assert model.spacecraft.id == "demo-3u"
    assert model.spacecraft.model_version == "0.1.0"
    assert len(model.subsystems) == 4
    assert len(model.modes) == 6
    assert len(model.telemetry) >= 5
    assert len(model.commands) >= 4
    assert len(model.events) >= 8
    assert len(model.faults) == 2
    assert len(model.packets) >= 3
    assert model.contacts.contact_profiles == []
    assert model.contacts.link_profiles == []
    assert model.contacts.contact_windows == []
    assert model.contacts.downlink_flows == []


def test_load_demo_payload_contract() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    assert len(model.payloads) == 1
    payload = model.payloads[0]

    assert payload.id == "demo_iod_payload"
    assert payload.subsystem == "payload"
    assert payload.profile == "iod"
    assert payload.lifecycle.initial_state == "READY"
    assert payload.lifecycle.states == ["OFF", "READY", "ACQUIRING", "FAULT"]
    assert payload.telemetry.produced == ["payload.acquisition.active"]
    assert payload.commands.accepted == [
        "payload.start_acquisition",
        "payload.stop_acquisition",
    ]
    assert payload.events.generated == [
        "payload.acquisition_started",
        "payload.acquisition_stopped",
    ]
    assert payload.faults.possible == []


def test_optional_payloads_file_can_be_absent(tmp_path: Path) -> None:
    mission_dir = tmp_path / "mission"
    mission_dir.mkdir()

    for source_file in DEMO_MISSION.glob("*.yaml"):
        if source_file.name == "payloads.yaml":
            continue
        (mission_dir / source_file.name).write_text(
            source_file.read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    model = MissionModelLoader().load(mission_dir)

    assert model.payloads == []


def test_invalid_payloads_top_level_key_fails(tmp_path: Path) -> None:
    mission_dir = copy_demo_mission(tmp_path)

    (mission_dir / "payloads.yaml").write_text(
        "payload_contracts: []\n",
        encoding="utf-8",
    )

    with pytest.raises(MissionModelError) as exc_info:
        MissionModelLoader().load(mission_dir)

    codes = {diagnostic.code for diagnostic in exc_info.value.diagnostics}
    assert "OF-STR-001" in codes
    assert "OF-STR-002" in codes


def test_load_demo_data_product_contract() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    assert len(model.data_products) == 1
    data_product = model.data_products[0]

    assert data_product.id == "payload.radiation_histogram"
    assert data_product.producer == "demo_iod_payload"
    assert data_product.producer_type == "payload"
    assert data_product.type == "histogram"
    assert data_product.estimated_size_bytes == 4096
    assert data_product.priority == "high"
    assert data_product.storage is not None
    assert data_product.storage.storage_class == "science"
    assert data_product.storage.retention == "7d"
    assert data_product.storage.overflow_policy == "drop_oldest"
    assert data_product.downlink is not None
    assert data_product.downlink.policy == "next_available_contact"
    assert data_product.description is not None
    assert model.data_product_ids == {"payload.radiation_histogram"}


def test_optional_data_products_file_can_be_absent(tmp_path: Path) -> None:
    mission_dir = tmp_path / "mission"
    mission_dir.mkdir()

    for source_file in DEMO_MISSION.glob("*.yaml"):
        if source_file.name == "data_products.yaml":
            continue
        (mission_dir / source_file.name).write_text(
            source_file.read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    model = MissionModelLoader().load(mission_dir)

    assert model.data_products == []


def test_load_valid_data_product_contract(tmp_path: Path) -> None:
    mission_dir = copy_demo_mission(tmp_path)
    (mission_dir / "data_products.yaml").write_text(
        VALID_DATA_PRODUCTS_YAML,
        encoding="utf-8",
    )

    model = MissionModelLoader().load(mission_dir)

    assert len(model.data_products) == 1
    data_product = model.data_products[0]

    assert data_product.id == "payload.synthetic_histogram"
    assert data_product.producer == "demo_iod_payload"
    assert data_product.producer_type == "payload"
    assert data_product.type == "histogram"
    assert data_product.estimated_size_bytes == 2048
    assert data_product.priority == "medium"
    assert data_product.storage is not None
    assert data_product.storage.storage_class == "science"
    assert data_product.storage.retention == "3d"
    assert data_product.storage.overflow_policy == "drop_oldest"
    assert data_product.downlink is not None
    assert data_product.downlink.policy == "priority_based"
    assert data_product.description is not None
    assert model.data_product_ids == {"payload.synthetic_histogram"}


def test_invalid_data_products_top_level_key_fails(tmp_path: Path) -> None:
    mission_dir = copy_demo_mission(tmp_path)
    (mission_dir / "data_products.yaml").write_text(
        "products: []\n",
        encoding="utf-8",
    )

    with pytest.raises(MissionModelError) as exc_info:
        MissionModelLoader().load(mission_dir)

    codes = {diagnostic.code for diagnostic in exc_info.value.diagnostics}
    assert "OF-STR-001" in codes
    assert "OF-STR-002" in codes


def test_duplicate_data_product_id_fails(tmp_path: Path) -> None:
    mission_dir = copy_demo_mission(tmp_path)
    (mission_dir / "data_products.yaml").write_text(
        """data_products:
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
""",
        encoding="utf-8",
    )

    with pytest.raises(MissionModelError) as exc_info:
        MissionModelLoader().load(mission_dir)

    diagnostics = exc_info.value.diagnostics

    assert any(
        diagnostic.code == "OF-ID-001"
        and diagnostic.file == "data_products.yaml"
        and diagnostic.domain == "data_products"
        and diagnostic.object_id == "payload.radiation_histogram"
        for diagnostic in diagnostics
    )


def test_optional_contacts_file_can_be_absent(tmp_path: Path) -> None:
    mission_dir = tmp_path / "mission"
    mission_dir.mkdir()

    for source_file in DEMO_MISSION.glob("*.yaml"):
        if source_file.name == "contacts.yaml":
            continue
        (mission_dir / source_file.name).write_text(
            source_file.read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    model = MissionModelLoader().load(mission_dir)

    assert model.contacts.contact_profiles == []
    assert model.contacts.link_profiles == []
    assert model.contacts.contact_windows == []
    assert model.contacts.downlink_flows == []


def test_load_valid_contact_downlink_contracts(tmp_path: Path) -> None:
    mission_dir = copy_demo_mission(tmp_path)
    (mission_dir / "contacts.yaml").write_text(
        VALID_CONTACTS_YAML,
        encoding="utf-8",
    )

    model = MissionModelLoader().load(mission_dir)

    assert len(model.contacts.contact_profiles) == 1
    assert len(model.contacts.link_profiles) == 1
    assert len(model.contacts.contact_windows) == 1
    assert len(model.contacts.downlink_flows) == 1

    contact_profile = model.contacts.contact_profiles[0]
    link_profile = model.contacts.link_profiles[0]
    contact_window = model.contacts.contact_windows[0]
    downlink_flow = model.contacts.downlink_flows[0]

    assert contact_profile.id == "primary_ground_contact"
    assert contact_profile.target == "synthetic_ground_station"
    assert link_profile.id == "uhf_downlink_nominal"
    assert link_profile.direction == "downlink"
    assert link_profile.assumed_rate_bps == 9600
    assert contact_window.id == "demo_contact_001"
    assert contact_window.contact_profile == "primary_ground_contact"
    assert contact_window.link_profile == "uhf_downlink_nominal"
    assert contact_window.duration_seconds == 600
    assert contact_window.assumed_capacity_bytes == 512000
    assert downlink_flow.id == "science_next_available_contact"
    assert downlink_flow.contact_profile == "primary_ground_contact"
    assert downlink_flow.link_profile == "uhf_downlink_nominal"
    assert downlink_flow.queue_policy == "priority_then_age"
    assert downlink_flow.eligible_data_products == ["payload.radiation_histogram"]

    assert model.contact_profile_ids == {"primary_ground_contact"}
    assert model.link_profile_ids == {"uhf_downlink_nominal"}
    assert model.contact_window_ids == {"demo_contact_001"}
    assert model.downlink_flow_ids == {"science_next_available_contact"}


def test_invalid_contacts_top_level_key_fails(tmp_path: Path) -> None:
    mission_dir = copy_demo_mission(tmp_path)
    (mission_dir / "contacts.yaml").write_text(
        "ground_contacts: []\n",
        encoding="utf-8",
    )

    with pytest.raises(MissionModelError) as exc_info:
        MissionModelLoader().load(mission_dir)

    codes = {diagnostic.code for diagnostic in exc_info.value.diagnostics}
    assert "OF-STR-001" in codes
    assert "OF-STR-002" in codes


def test_duplicate_contact_profile_id_fails(tmp_path: Path) -> None:
    mission_dir = copy_demo_mission(tmp_path)
    (mission_dir / "contacts.yaml").write_text(
        "contacts:\n"
        "  contact_profiles:\n"
        "    - id: primary_ground_contact\n"
        "      target: synthetic_ground_station\n"
        "    - id: primary_ground_contact\n"
        "      target: backup_synthetic_ground_station\n",
        encoding="utf-8",
    )

    with pytest.raises(MissionModelError) as exc_info:
        MissionModelLoader().load(mission_dir)

    diagnostics = exc_info.value.diagnostics

    assert any(
        diagnostic.code == "OF-ID-001"
        and diagnostic.file == "contacts.yaml"
        and diagnostic.domain == "contact_profiles"
        and diagnostic.object_id == "primary_ground_contact"
        for diagnostic in diagnostics
    )


def test_missing_mission_directory_fails() -> None:
    with pytest.raises(MissionModelError) as exc_info:
        MissionModelLoader().load(Path("does-not-exist"))

    assert exc_info.value.diagnostics[0].code == "OF-SYN-001"

    assert exc_info.value.diagnostics[0].suggestion == (
        "Pass an existing Mission Model directory."
    )


def test_missing_required_file_fails(tmp_path: Path) -> None:
    mission_dir = tmp_path / "mission"
    mission_dir.mkdir()

    with pytest.raises(MissionModelError) as exc_info:
        MissionModelLoader().load(mission_dir)

    codes = {diagnostic.code for diagnostic in exc_info.value.diagnostics}
    assert "OF-SYN-002" in codes

    suggestions = {
        diagnostic.suggestion
        for diagnostic in exc_info.value.diagnostics
        if diagnostic.code == "OF-SYN-002"
    }

    assert suggestions
    assert all(suggestion is not None for suggestion in suggestions)