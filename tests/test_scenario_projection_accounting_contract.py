from __future__ import annotations

import copy
import hashlib
import json
from contextlib import contextmanager
from pathlib import Path

import pytest

from orbitfabric.conformance.scenario_projection_accounting import (
    ACCOUNTING_KIND,
    ScenarioProjectionAccountingError,
    validate_accounting,
    validate_parent,
    validate_scenario,
    verify_bundle,
)

ROOT = Path(__file__).parents[1]
FIXTURES = ROOT / "conformance" / "fixtures" / "scenario-projection-accounting"
VALID = FIXTURES / "valid"
INVALID = FIXTURES / "invalid"


def load(name: str) -> dict:
    return json.loads((VALID / name).read_text(encoding="utf-8"))


@contextmanager
def asserted_code(code: str):
    with pytest.raises(ScenarioProjectionAccountingError, match=".") as caught:
        yield
    assert caught.value.code == code


def test_complete_r1_verifies_exact_identity_and_all_eight_atoms() -> None:
    result_path = VALID / "r1-result.json"
    outcome = verify_bundle(
        result_path,
        "scenario-accounting",
        VALID / "r1-scenario-declaration.json",
        expected_result_sha256=hashlib.sha256(result_path.read_bytes()).hexdigest(),
    )
    assert outcome == {
        "identity": {
            "result_sha256": "446c23be71e1aa2d62d64cbb0ed1651b10f14e11cbe185e95092ed400eb89a21",
            "artifact_id": "scenario-accounting",
            "artifact_sha256": "b587991aed9d61cc20aa9e969996f1f5e3ce283705b4f25edf7a35c2917716cb",
        },
        "completeness": "complete",
        "unaccounted_atom_ids": [],
    }


def test_r1_keeps_metadata_and_same_entity_counterexample_explicit() -> None:
    records = {record["atom_id"]: record for record in load("r1-accounting.json")["records"]}
    assert records["atom-0001"]["disposition"] == "projected"
    assert records["atom-0001"]["mapping_ids"] == []
    assert records["atom-0003"]["disposition"] == "not_projected"
    assert records["atom-0003"]["mapping_ids"] == []
    assert records["atom-0006"]["disposition"] == "projected"
    assert records["atom-0006"]["mapping_ids"] == ["mapping.op-0002"]


def test_partial_omission_is_reported_without_inventing_disposition() -> None:
    value = load("partial-unsupported.json")
    declaration = load("r1-scenario-declaration.json")
    assert validate_scenario(value, declaration) == (
        "atom-0001", "atom-0002", "atom-0003", "atom-0004",
        "atom-0005", "atom-0007", "atom-0008",
    )


@pytest.mark.parametrize(
    ("mutation", "code"),
    [
        (lambda x: x["records"].append(copy.deepcopy(x["records"][0])), "sidecar.duplicate_atom"),
        (lambda x: x.update(accounting_version="0.2-candidate"), "surface.unsupported_version"),
        (lambda x: x.update(completeness="partial", reason=""), "sidecar.schema"),
        (lambda x: x.update(completeness="partial") or x.pop("reason", None), "sidecar.schema"),
        (lambda x: x["records"][0].update(disposition="blocked"), "sidecar.schema"),
        (lambda x: x["records"][2].update(mapping_ids=["mapping.op-0002"]), "sidecar.schema"),
        (lambda x: x["records"][2].pop("reason"), "sidecar.schema"),
        (lambda x: x.update(result_sha256="a" * 64), "sidecar.schema"),
    ],
)
def test_sidecar_shape_fails_closed(mutation, code: str) -> None:
    value = load("r1-accounting.json")
    mutation(value)
    with asserted_code(code):
        validate_accounting(value)


def test_projected_supports_zero_one_and_multiple_parent_mappings() -> None:
    value = load("r1-accounting.json")
    value["records"][0]["mapping_ids"] = []
    value["records"][3]["mapping_ids"] = ["mapping.op-0001", "mapping.op-0002"]
    parent = load("r1-result.json")
    parent["artifacts"][0]["derived_from_mappings"] = ["mapping.op-0001", "mapping.op-0002"]
    validate_parent(value, parent, "scenario-accounting")


@pytest.mark.parametrize(
    ("mutation", "code"),
    [
        (lambda x: x["scenario"].update(sha256="a" * 64), "scenario.identity"),
        (lambda x: x["scenario"].update(id="other"), "scenario.identity"),
        (lambda x: x["records"][0].update(atom_id="atom-9999"), "scenario.unknown_atom"),
        (lambda x: x["records"].pop(), "scenario.missing_atom"),
    ],
)
def test_exact_scenario_binding_fails_closed(mutation, code: str) -> None:
    value = load("r1-accounting.json")
    mutation(value)
    with asserted_code(code):
        validate_scenario(value, load("r1-scenario-declaration.json"))


@pytest.mark.parametrize(
    ("mutation", "code"),
    [
        (lambda p: p["inputs"].update(operation_inputs=[]), "parent.scenario_input"),
        (
            lambda p: p["inputs"]["operation_inputs"][0].update(sha256="a" * 64),
            "parent.scenario_identity",
        ),
        (lambda p: p["mappings"].pop(), "parent.unknown_mapping"),
        (
            lambda p: p["mappings"].append(copy.deepcopy(p["mappings"][0])),
            "parent.duplicate_mapping",
        ),
        (lambda p: p["artifacts"][0].update(derived_from_mappings=[]), "parent.artifact_mappings"),
        (lambda p: p["artifacts"][0].update(kind="cosmos.private"), "parent.artifact_contract"),
        (lambda p: p["artifacts"][0].update(path="../outside.json"), "parent.artifact_path"),
    ],
)
def test_parent_binding_fails_closed(mutation, code: str) -> None:
    parent = load("r1-result.json")
    mutation(parent)
    with asserted_code(code):
        validate_parent(load("r1-accounting.json"), parent, "scenario-accounting")


def test_scenario_free_fprime_style_parent_cannot_claim_accounting() -> None:
    parent = load("r1-result.json")
    parent["inputs"]["operation_inputs"] = []
    with asserted_code("parent.scenario_input"):
        validate_parent(load("r1-accounting.json"), parent, "scenario-accounting")


def test_integrity_rejects_artifact_and_result_digest_changes(tmp_path: Path) -> None:
    for source in VALID.iterdir():
        if source.is_file():
            (tmp_path / source.name).write_bytes(source.read_bytes())
    accounting_path = tmp_path / "r1-accounting.json"
    accounting_path.write_bytes(accounting_path.read_bytes() + b" ")
    with asserted_code("integrity.artifact_digest"):
        verify_bundle(
            tmp_path / "r1-result.json",
            "scenario-accounting",
            tmp_path / "r1-scenario-declaration.json",
        )
    with asserted_code("integrity.result_digest"):
        verify_bundle(
            VALID / "r1-result.json",
            "scenario-accounting",
            VALID / "r1-scenario-declaration.json",
            expected_result_sha256="a" * 64,
        )


def test_reserved_kind_is_generic() -> None:
    assert ACCOUNTING_KIND == "orbitfabric.scenario_projection_accounting"
    assert "cosmos" not in ACCOUNTING_KIND
    assert "fprime" not in ACCOUNTING_KIND


@pytest.mark.parametrize(
    ("name", "stage", "code"),
    [
        ("unknown-atom.json", "scenario", "scenario.unknown_atom"),
        ("wrong-scenario-sha.json", "scenario", "scenario.identity"),
        ("duplicate-atom.json", "sidecar", "sidecar.duplicate_atom"),
        ("missing-atom-complete.json", "scenario", "scenario.missing_atom"),
        ("negative-with-mapping.json", "sidecar", "sidecar.schema"),
        ("partial-missing-reason.json", "sidecar", "sidecar.schema"),
    ],
)
def test_published_negative_fixtures(name: str, stage: str, code: str) -> None:
    accounting = json.loads((INVALID / name).read_text(encoding="utf-8"))
    with asserted_code(code):
        if stage == "scenario":
            validate_scenario(accounting, load("r1-scenario-declaration.json"))
        else:
            validate_accounting(accounting)
