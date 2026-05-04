from __future__ import annotations

from collections.abc import Iterable

from orbitfabric.lint.finding import LintFinding
from orbitfabric.model.mission import ContactWindow, DownlinkFlowContract, MissionModel


def check_contacts(model: MissionModel) -> list[LintFinding]:
    """Check Contact Windows and Downlink Flow Contract consistency."""
    findings: list[LintFinding] = []

    for contact_window in model.contacts.contact_windows:
        findings.extend(_check_contact_window_references(model, contact_window))

    for downlink_flow in model.contacts.downlink_flows:
        findings.extend(_check_downlink_flow_references(model, downlink_flow))

    if _has_contact_domain_content(model):
        findings.extend(_check_high_priority_products_are_eligible(model))
        findings.extend(_check_declared_contact_capacity(model))

    return findings


def _check_contact_window_references(
    model: MissionModel,
    contact_window: ContactWindow,
) -> list[LintFinding]:
    findings: list[LintFinding] = []

    if contact_window.contact_profile not in model.contact_profile_ids:
        findings.append(
            LintFinding(
                severity="ERROR",
                code="OF-CON-001",
                file="contacts.yaml",
                domain="contact_windows",
                object_id=contact_window.id,
                message=(
                    "contact window references unknown contact profile "
                    f"'{contact_window.contact_profile}'"
                ),
                suggestion="Add the contact profile or fix contact_window.contact_profile.",
            )
        )

    if contact_window.link_profile not in model.link_profile_ids:
        findings.append(
            LintFinding(
                severity="ERROR",
                code="OF-CON-002",
                file="contacts.yaml",
                domain="contact_windows",
                object_id=contact_window.id,
                message=(
                    "contact window references unknown link profile "
                    f"'{contact_window.link_profile}'"
                ),
                suggestion="Add the link profile or fix contact_window.link_profile.",
            )
        )

    return findings


def _check_downlink_flow_references(
    model: MissionModel,
    downlink_flow: DownlinkFlowContract,
) -> list[LintFinding]:
    findings: list[LintFinding] = []

    if downlink_flow.contact_profile not in model.contact_profile_ids:
        findings.append(
            LintFinding(
                severity="ERROR",
                code="OF-DL-001",
                file="contacts.yaml",
                domain="downlink_flows",
                object_id=downlink_flow.id,
                message=(
                    "downlink flow references unknown contact profile "
                    f"'{downlink_flow.contact_profile}'"
                ),
                suggestion="Add the contact profile or fix downlink_flow.contact_profile.",
            )
        )

    if downlink_flow.link_profile not in model.link_profile_ids:
        findings.append(
            LintFinding(
                severity="ERROR",
                code="OF-DL-002",
                file="contacts.yaml",
                domain="downlink_flows",
                object_id=downlink_flow.id,
                message=(
                    "downlink flow references unknown link profile "
                    f"'{downlink_flow.link_profile}'"
                ),
                suggestion="Add the link profile or fix downlink_flow.link_profile.",
            )
        )

    for data_product_id in downlink_flow.eligible_data_products:
        if data_product_id in model.data_product_ids:
            continue

        findings.append(
            LintFinding(
                severity="ERROR",
                code="OF-DL-003",
                file="contacts.yaml",
                domain="downlink_flows",
                object_id=downlink_flow.id,
                message=(
                    "downlink flow references unknown eligible data product "
                    f"'{data_product_id}'"
                ),
                suggestion="Add the data product or fix downlink_flow.eligible_data_products.",
            )
        )

    return findings


def _check_high_priority_products_are_eligible(model: MissionModel) -> list[LintFinding]:
    eligible_ids = _eligible_data_product_ids(model.contacts.downlink_flows)
    findings: list[LintFinding] = []

    for data_product in model.data_products:
        if data_product.priority not in {"high", "critical"}:
            continue

        if data_product.downlink is None or data_product.downlink.policy in {None, "none"}:
            continue

        if data_product.id in eligible_ids:
            continue

        findings.append(
            LintFinding(
                severity="WARNING",
                code="OF-DL-004",
                file="data_products.yaml",
                domain="data_products",
                object_id=data_product.id,
                message=(
                    "high-priority data product has downlink intent but is not "
                    "eligible in any downlink flow"
                ),
                suggestion=(
                    "Add the data product to a downlink flow eligible_data_products "
                    "list, or revise its downlink intent."
                ),
            )
        )

    return findings


def _check_declared_contact_capacity(model: MissionModel) -> list[LintFinding]:
    findings: list[LintFinding] = []
    data_product_sizes = {
        data_product.id: data_product.estimated_size_bytes
        for data_product in model.data_products
    }

    for downlink_flow in model.contacts.downlink_flows:
        estimated_size = sum(
            data_product_sizes[data_product_id]
            for data_product_id in downlink_flow.eligible_data_products
            if data_product_id in data_product_sizes
        )
        if estimated_size == 0:
            continue

        declared_capacity = _declared_capacity_for_flow(model, downlink_flow)
        if declared_capacity is None or estimated_size <= declared_capacity:
            continue

        findings.append(
            LintFinding(
                severity="WARNING",
                code="OF-DL-005",
                file="contacts.yaml",
                domain="downlink_flows",
                object_id=downlink_flow.id,
                message=(
                    "estimated eligible data product volume may exceed declared "
                    "contact capacity"
                ),
                suggestion=(
                    "Increase declared contact capacity, reduce eligible data volume, "
                    "or split the flow across multiple contacts."
                ),
            )
        )

    return findings


def _declared_capacity_for_flow(
    model: MissionModel,
    downlink_flow: DownlinkFlowContract,
) -> int | None:
    capacities = [
        contact_window.assumed_capacity_bytes
        for contact_window in model.contacts.contact_windows
        if contact_window.contact_profile == downlink_flow.contact_profile
        and contact_window.link_profile == downlink_flow.link_profile
        and contact_window.assumed_capacity_bytes is not None
    ]

    if not capacities:
        return None

    return sum(capacities)


def _eligible_data_product_ids(
    downlink_flows: Iterable[DownlinkFlowContract],
) -> set[str]:
    eligible_ids: set[str] = set()

    for downlink_flow in downlink_flows:
        eligible_ids.update(downlink_flow.eligible_data_products)

    return eligible_ids


def _has_contact_domain_content(model: MissionModel) -> bool:
    return any(
        (
            model.contacts.contact_profiles,
            model.contacts.link_profiles,
            model.contacts.contact_windows,
            model.contacts.downlink_flows,
        )
    )
