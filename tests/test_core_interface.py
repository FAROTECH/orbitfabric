from __future__ import annotations

import hashlib
import json

import pytest
import rfc8785
from typer.testing import CliRunner

import orbitfabric.export.core_interface as core_interface
from orbitfabric.entrypoint import app
from orbitfabric.export.core_interface import (
    CORE_CAPABILITIES,
    CORE_INTERFACE_KIND,
    CORE_INTERFACE_VERSION,
    CoreCapability,
    core_interface_to_dict,
)


def _fingerprint_payload(manifest: dict[str, object]) -> dict[str, object]:
    return {
        "kind": manifest["kind"],
        "interface_version": manifest["interface_version"],
        "capabilities": manifest["capabilities"],
    }


def test_manifest_schema_and_expected_capabilities() -> None:
    manifest = core_interface_to_dict()

    assert set(manifest) == {
        "kind",
        "interface_version",
        "orbitfabric_version",
        "interface_sha256",
        "capabilities",
    }
    assert manifest["kind"] == CORE_INTERFACE_KIND
    assert manifest["interface_version"] == CORE_INTERFACE_VERSION
    assert manifest["orbitfabric_version"] == "1.3.0"
    assert len(manifest["interface_sha256"]) == 64
    assert all(
        set(capability) == {"id", "contract_kind", "contract_version"}
        for capability in manifest["capabilities"]
    )

    capabilities = {item["id"]: item for item in manifest["capabilities"]}
    assert capabilities["scenario_declaration"] == {
        "id": "scenario_declaration",
        "contract_kind": "orbitfabric.scenario_declaration",
        "contract_version": "0.1-candidate",
    }
    assert set(capabilities) == {item.id for item in CORE_CAPABILITIES}


def test_capabilities_and_fingerprint_are_order_independent() -> None:
    forward = core_interface_to_dict(CORE_CAPABILITIES)
    reverse = core_interface_to_dict(reversed(CORE_CAPABILITIES))

    assert [item["id"] for item in forward["capabilities"]] == sorted(
        item.id for item in CORE_CAPABILITIES
    )
    assert reverse == forward
    assert forward["interface_sha256"] == hashlib.sha256(
        rfc8785.dumps(_fingerprint_payload(forward))
    ).hexdigest()


@pytest.mark.parametrize(
    "changed_capabilities",
    [
        CORE_CAPABILITIES[:-1],
        CORE_CAPABILITIES
        + (CoreCapability("additional_surface", "orbitfabric.additional", "0.1"),),
        tuple(
            CoreCapability(item.id, item.contract_kind, "changed")
            if item.id == "scenario_declaration"
            else item
            for item in CORE_CAPABILITIES
        ),
    ],
)
def test_interface_change_changes_fingerprint(
    changed_capabilities: tuple[CoreCapability, ...],
) -> None:
    assert (
        core_interface_to_dict(changed_capabilities)["interface_sha256"]
        != core_interface_to_dict()["interface_sha256"]
    )


def test_product_version_is_provenance_not_interface_identity(monkeypatch: pytest.MonkeyPatch) -> None:
    original = core_interface_to_dict()
    monkeypatch.setattr(core_interface, "__version__", "9.9.9")
    changed_product = core_interface_to_dict()

    assert changed_product["orbitfabric_version"] == "9.9.9"
    assert changed_product["interface_sha256"] == original["interface_sha256"]


@pytest.mark.parametrize(
    "capabilities",
    [
        (CoreCapability("", "orbitfabric.invalid", "0.1"),),
        (CoreCapability("Invalid-Id", "orbitfabric.invalid", "0.1"),),
        (CoreCapability("invalid", "", "0.1"),),
        (CoreCapability("invalid", "orbitfabric.invalid", " 0.1"),),
        (
            CoreCapability("duplicate", "orbitfabric.one", "0.1"),
            CoreCapability("duplicate", "orbitfabric.two", "0.2"),
        ),
        ({"id": "not-a-declaration"},),
    ],
)
def test_malformed_internal_declarations_fail_closed(capabilities: object) -> None:
    with pytest.raises(ValueError):
        core_interface_to_dict(capabilities)  # type: ignore[arg-type]


def test_cli_exports_manifest_without_mission_input(tmp_path) -> None:
    output_file = tmp_path / "core_interface.json"
    result = CliRunner().invoke(
        app, ["export", "core-interface", "--json", str(output_file)]
    )

    assert result.exit_code == 0, result.output
    manifest = json.loads(output_file.read_text(encoding="utf-8"))
    assert manifest == core_interface_to_dict()
    assert "Interface SHA-256:" in result.output
    assert "Result: PASSED" in result.output
