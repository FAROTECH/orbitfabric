from __future__ import annotations

from typing import Any

from orbitfabric.lint.finding import LintFinding
from orbitfabric.model.mission import Command, MissionModel

RISKY_COMMAND_LEVELS = {"medium", "high", "critical"}


def check_commands(model: MissionModel) -> list[LintFinding]:
    """Check command engineering consistency."""
    findings = []

    for command in model.commands:
        findings.extend(_check_timeout(command))
        findings.extend(_check_expected_effects(command))
        findings.extend(_check_expected_effect_data_products(model, command))
        findings.extend(_check_safe_mode_risk(command))

    return findings


def _check_timeout(command: Command) -> list[LintFinding]:
    if command.timeout_ms is not None:
        return []

    return [
        LintFinding(
            severity="WARNING",
            code="OF-CMD-005",
            file="commands.yaml",
            domain="commands",
            object_id=command.id,
            message="command should define timeout_ms",
            suggestion="Add timeout_ms to make command behavior testable.",
        )
    ]


def _check_expected_effects(command: Command) -> list[LintFinding]:
    if command.expected_effects:
        return []

    return [
        LintFinding(
            severity="WARNING",
            code="OF-CMD-006",
            file="commands.yaml",
            domain="commands",
            object_id=command.id,
            message="command should define expected effects",
            suggestion="Add expected_effects or explicitly justify no expected effects.",
        )
    ]


def _check_expected_effect_data_products(
    model: MissionModel,
    command: Command,
) -> list[LintFinding]:
    data_products = command.expected_effects.get("data_products")
    if data_products is None:
        return []

    if not isinstance(data_products, list):
        return [
            LintFinding(
                severity="ERROR",
                code="OF-CMD-008",
                file="commands.yaml",
                domain="commands",
                object_id=command.id,
                message="command expected_effects.data_products must be a list",
                suggestion=(
                    "Set expected_effects.data_products to a list of data product "
                    "IDs declared in data_products.yaml."
                ),
            )
        ]

    findings: list[LintFinding] = []
    for data_product_id in data_products:
        if not isinstance(data_product_id, str):
            findings.append(_invalid_data_product_effect(command, data_product_id))
            continue

        if data_product_id in model.data_product_ids:
            continue

        findings.append(_unknown_data_product_effect(command, data_product_id))

    return findings


def _invalid_data_product_effect(
    command: Command,
    value: Any,
) -> LintFinding:
    return LintFinding(
        severity="ERROR",
        code="OF-CMD-008",
        file="commands.yaml",
        domain="commands",
        object_id=command.id,
        message=(
            "command expected_effects.data_products contains a non-string "
            f"entry '{value}'"
        ),
        suggestion=(
            "Use only data product IDs declared in data_products.yaml under "
            "expected_effects.data_products."
        ),
    )


def _unknown_data_product_effect(
    command: Command,
    data_product_id: str,
) -> LintFinding:
    return LintFinding(
        severity="ERROR",
        code="OF-CMD-009",
        file="commands.yaml",
        domain="commands",
        object_id=command.id,
        message=(
            "command expected_effects references unknown data product "
            f"'{data_product_id}'"
        ),
        suggestion=(
            "Add the data product to data_products.yaml or fix "
            "expected_effects.data_products."
        ),
    )


def _check_safe_mode_risk(command: Command) -> list[LintFinding]:
    if command.risk not in RISKY_COMMAND_LEVELS:
        return []

    if "SAFE" not in command.allowed_modes:
        return []

    return [
        LintFinding(
            severity="ERROR",
            code="OF-CMD-007",
            file="commands.yaml",
            domain="commands",
            object_id=command.id,
            message="medium/high/critical-risk command is allowed in SAFE mode",
            suggestion="Remove SAFE from allowed_modes or lower the command risk.",
        )
    ]