from __future__ import annotations

from orbitfabric.lint.finding import LintFinding
from orbitfabric.model.mission import DataProductContract, MissionModel


def check_data_products(model: MissionModel) -> list[LintFinding]:
    """Check Data Product and Storage Contract consistency."""
    findings: list[LintFinding] = []

    for data_product in model.data_products:
        findings.extend(_check_producer_reference(model, data_product))
        findings.extend(_check_payload_reference(model, data_product))
        findings.extend(_check_storage_intent(data_product))
        findings.extend(_check_downlink_intent(data_product))

    return findings


def _check_producer_reference(
    model: MissionModel,
    data_product: DataProductContract,
) -> list[LintFinding]:
    if data_product.producer_type == "payload":
        if data_product.producer in model.payload_ids:
            return []

        return [
            LintFinding(
                severity="ERROR",
                code="OF-DP-002",
                file="data_products.yaml",
                domain="data_products",
                object_id=data_product.id,
                message=(
                    f"data product producer '{data_product.producer}' does not reference "
                    "an existing payload contract"
                ),
                suggestion="Add the payload to payloads.yaml or fix data_product.producer.",
            )
        ]

    if data_product.producer_type == "subsystem":
        if data_product.producer in model.subsystem_ids:
            return []

        return [
            LintFinding(
                severity="ERROR",
                code="OF-DP-002",
                file="data_products.yaml",
                domain="data_products",
                object_id=data_product.id,
                message=(
                    f"data product producer '{data_product.producer}' does not reference "
                    "an existing subsystem"
                ),
                suggestion="Add the subsystem to subsystems.yaml or fix data_product.producer.",
            )
        ]

    return []


def _check_payload_reference(
    model: MissionModel,
    data_product: DataProductContract,
) -> list[LintFinding]:
    if data_product.payload is None:
        return []

    if data_product.payload in model.payload_ids:
        return []

    return [
        LintFinding(
            severity="ERROR",
            code="OF-DP-003",
            file="data_products.yaml",
            domain="data_products",
            object_id=data_product.id,
            message=(
                f"data product payload reference '{data_product.payload}' does not reference "
                "an existing payload contract"
            ),
            suggestion="Add the payload to payloads.yaml or fix data_product.payload.",
        )
    ]


def _check_storage_intent(data_product: DataProductContract) -> list[LintFinding]:
    findings: list[LintFinding] = []

    if data_product.storage is None:
        return findings

    if data_product.storage.retention is None:
        findings.append(
            LintFinding(
                severity="WARNING",
                code="OF-DP-006",
                file="data_products.yaml",
                domain="data_products",
                object_id=data_product.id,
                message="data product storage intent should define retention",
                suggestion="Set storage.retention or remove storage intent if the product is not retained.",
            )
        )

    if data_product.storage.overflow_policy is None:
        findings.append(
            LintFinding(
                severity="WARNING",
                code="OF-DP-007",
                file="data_products.yaml",
                domain="data_products",
                object_id=data_product.id,
                message="data product storage intent should define overflow_policy",
                suggestion="Set storage.overflow_policy for retained data products.",
            )
        )

    return findings


def _check_downlink_intent(data_product: DataProductContract) -> list[LintFinding]:
    if data_product.priority not in {"high", "critical"}:
        return []

    if data_product.downlink is not None and data_product.downlink.policy not in {None, "none"}:
        return []

    return [
        LintFinding(
            severity="WARNING",
            code="OF-DP-008",
            file="data_products.yaml",
            domain="data_products",
            object_id=data_product.id,
            message="high-priority data product should define downlink intent",
            suggestion="Set downlink.policy for high or critical data products.",
        )
    ]
