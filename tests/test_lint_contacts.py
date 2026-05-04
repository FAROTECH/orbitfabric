from __future__ import annotations

from pathlib import Path

from orbitfabric.lint.engine import LintEngine
from orbitfabric.model.loader import MissionModelLoader
from orbitfabric.model.mission import (
    ContactContracts,
    ContactProfile,
    ContactWindow,
    DownlinkFlowContract,
    LinkProfile,
)

DEMO_MISSION = Path("examples/demo-3u/mission")


def _model_with_valid_contacts():
    model = MissionModelLoader().load(DEMO_MISSION)
    model.contacts = ContactContracts(
        contact_profiles=[
            ContactProfile(
                id="primary_ground_contact",
                target="synthetic_ground_station",
            )
        ],
        link_profiles=[
            LinkProfile(
                id="uhf_downlink_nominal",
                direction="downlink",
                assumed_rate_bps=9600,
            )
        ],
        contact_windows=[
            ContactWindow(
                id="demo_contact_001",
                contact_profile="primary_ground_contact",
                link_profile="uhf_downlink_nominal",
                start="2026-01-01T00:00:00Z",
                duration_seconds=600,
                assumed_capacity_bytes=8192,
            )
        ],
        downlink_flows=[
            DownlinkFlowContract(
                id="science_next_available_contact",
                contact_profile="primary_ground_contact",
                link_profile="uhf_downlink_nominal",
                queue_policy="priority_then_age",
                eligible_data_products=["payload.radiation_histogram"],
            )
        ],
    )
    return model


def _codes_for(model) -> set[str]:
    report = LintEngine().run(model)
    return {finding.code for finding in report.findings}


def test_demo_mission_without_contacts_still_has_no_findings() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)

    assert _codes_for(model) == set()


def test_valid_contact_downlink_contracts_have_no_findings() -> None:
    model = _model_with_valid_contacts()

    assert _codes_for(model) == set()


def test_contact_window_unknown_contact_profile_is_reported() -> None:
    model = _model_with_valid_contacts()
    model.contacts.contact_windows[0].contact_profile = "missing_contact_profile"

    report = LintEngine().run(model)

    assert "OF-CON-001" in {finding.code for finding in report.findings}
    assert report.has_errors


def test_contact_window_unknown_link_profile_is_reported() -> None:
    model = _model_with_valid_contacts()
    model.contacts.contact_windows[0].link_profile = "missing_link_profile"

    report = LintEngine().run(model)

    assert "OF-CON-002" in {finding.code for finding in report.findings}
    assert report.has_errors


def test_downlink_flow_unknown_contact_profile_is_reported() -> None:
    model = _model_with_valid_contacts()
    model.contacts.downlink_flows[0].contact_profile = "missing_contact_profile"

    report = LintEngine().run(model)

    assert "OF-DL-001" in {finding.code for finding in report.findings}
    assert report.has_errors


def test_downlink_flow_unknown_link_profile_is_reported() -> None:
    model = _model_with_valid_contacts()
    model.contacts.downlink_flows[0].link_profile = "missing_link_profile"

    report = LintEngine().run(model)

    assert "OF-DL-002" in {finding.code for finding in report.findings}
    assert report.has_errors


def test_downlink_flow_unknown_data_product_is_reported() -> None:
    model = _model_with_valid_contacts()
    model.contacts.downlink_flows[0].eligible_data_products = ["payload.missing_product"]

    report = LintEngine().run(model)

    assert "OF-DL-003" in {finding.code for finding in report.findings}
    assert report.has_errors


def test_contact_domain_without_downlink_flows_warns_about_high_priority_product() -> None:
    model = _model_with_valid_contacts()
    model.contacts.downlink_flows = []

    report = LintEngine().run(model)

    assert "OF-DL-004" in {finding.code for finding in report.findings}
    assert report.warning_count == 1


def test_downlink_flow_capacity_warning_is_reported() -> None:
    model = _model_with_valid_contacts()
    model.contacts.contact_windows[0].assumed_capacity_bytes = 1024

    report = LintEngine().run(model)

    assert "OF-DL-005" in {finding.code for finding in report.findings}
    assert report.warning_count == 1
