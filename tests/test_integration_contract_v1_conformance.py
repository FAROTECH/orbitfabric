from __future__ import annotations

import copy
from pathlib import Path

import pytest

from orbitfabric.conformance.integration_contracts import (
    ContractError,
    load_json,
    validate_bindings,
    validate_manifest,
    validate_result,
)

FIXTURES = Path(__file__).parents[1] / "conformance" / "fixtures" / "integration-v1"


def fixture(group: str, name: str):
    return load_json(FIXTURES / group / name)


def test_valid_zero_input_pair() -> None:
    manifest = fixture("valid", "manifest-zero-input.json")
    validate_manifest(manifest)
    validate_bindings(manifest, "project", [])
    validate_result(manifest, fixture("valid", "result-zero-input.json"))


def test_valid_scenario_pair_and_failed_provenance() -> None:
    manifest = fixture("valid", "manifest-scenario.json")
    validate_bindings(manifest, "verification_projection", ["scenario"])
    validate_result(manifest, fixture("valid", "result-scenario.json"))
    validate_result(manifest, fixture("valid", "result-scenario-unavailable.json"))


@pytest.mark.parametrize("roles", [[], ["other"], ["scenario", "scenario"]])
def test_required_scenario_bindings_fail_closed(roles: list[str]) -> None:
    manifest = fixture("valid", "manifest-scenario.json")
    with pytest.raises(ContractError):
        validate_bindings(manifest, "verification_projection", roles)


def test_zero_input_operation_rejects_fake_scenario() -> None:
    manifest = fixture("valid", "manifest-zero-input.json")
    with pytest.raises(ContractError):
        validate_bindings(manifest, "project", ["scenario"])


def test_missing_requirements_is_invalid() -> None:
    with pytest.raises(ContractError):
        validate_manifest(fixture("invalid", "manifest-missing-requirements.json"))


def test_optional_multi_and_unknown_roles_are_not_advertised() -> None:
    manifest = fixture("valid", "manifest-scenario.json")
    operation = manifest["operations"][0]
    operation["input_requirements"] = [{"role": "scenario"}, {"role": "scenario"}]
    with pytest.raises(ContractError):
        validate_manifest(manifest)
    operation["input_requirements"] = [{"role": "adapter_private"}]
    with pytest.raises(ContractError):
        validate_manifest(manifest)


def test_success_result_requires_exact_available_provenance() -> None:
    manifest = fixture("valid", "manifest-scenario.json")
    result = fixture("valid", "result-scenario.json")
    result["inputs"]["operation_inputs"] = []
    with pytest.raises(ContractError):
        validate_result(manifest, result)
    result = fixture("valid", "result-scenario-unavailable.json")
    result["result"] = "succeeded"
    with pytest.raises(ContractError):
        validate_result(manifest, result)


def test_mixed_version_triples_are_rejected() -> None:
    manifest = fixture("valid", "manifest-zero-input.json")
    for field, value in [
        ("manifest_version", "0.1-candidate"),
    ]:
        changed = copy.deepcopy(manifest)
        changed[field] = value
        with pytest.raises(ContractError):
            validate_manifest(changed)
    changed = copy.deepcopy(manifest)
    changed["execution"]["protocol"] = "orbitfabric.adapter_cli.v0"
    with pytest.raises(ContractError):
        validate_manifest(changed)

