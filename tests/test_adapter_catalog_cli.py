from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from typer.testing import CliRunner

from orbitfabric.entrypoint import app

DESCRIPTOR_SHA = "724eb67299150887167dfce8aa3ea117a163c79b6fcaff6ab105dfd35daf7464"
SOURCE_COORDINATE = "github.com/FAROTECH:orbitfabric/fprime"


def _catalog_payload() -> dict[str, object]:
    return {
        "kind": "orbitfabric.adapter_catalog",
        "catalog_version": "0.1-candidate",
        "adapters": [
            {
                "source_coordinate": {
                    "authority": "github.com/FAROTECH",
                    "publisher": "orbitfabric",
                    "name": "fprime",
                },
                "releases": [
                    {
                        "version": "0.1.1",
                        "release_descriptor_digest": {
                            "algorithm": "sha256",
                            "value": DESCRIPTOR_SHA,
                        },
                        "sources": [
                            {
                                "binding": "github-fprime",
                                "release_ref": "v0.1.1",
                            }
                        ],
                    }
                ],
            }
        ],
        "source_bindings": [
            {
                "id": "github-fprime",
                "provider": "github-release",
                "config": {"repository": "FAROTECH/orbitfabric-fprime-adapter"},
            }
        ],
    }


def _write_catalog(tmp_path: Path, payload: dict[str, object] | None = None) -> Path:
    path = tmp_path / "catalog.json"
    path.write_text(
        json.dumps(payload if payload is not None else _catalog_payload(), indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def test_adapter_help_exposes_catalog_group() -> None:
    result = CliRunner().invoke(app, ["adapter", "--help"])

    assert result.exit_code == 0
    assert "catalog" in result.stdout
    assert "Inspect and select exact adapter releases" in result.stdout


def test_catalog_validate_human_output(tmp_path: Path) -> None:
    catalog = _write_catalog(tmp_path)

    result = CliRunner().invoke(app, ["adapter", "catalog", "validate", str(catalog)])

    assert result.exit_code == 0
    assert "Version: 0.1-candidate" in result.stdout
    assert "Adapters: 1" in result.stdout
    assert "Releases: 1" in result.stdout
    assert "Source bindings: 1" in result.stdout
    assert "Result: CONFORMANT" in result.stdout


def test_catalog_validate_json_returns_core_model(tmp_path: Path) -> None:
    catalog = _write_catalog(tmp_path)

    result = CliRunner().invoke(
        app,
        ["adapter", "catalog", "validate", str(catalog), "--json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["kind"] == "orbitfabric.adapter_catalog"
    assert payload["catalog_version"] == "0.1-candidate"
    assert payload["adapters"][0]["source_coordinate"]["name"] == "fprime"


def test_catalog_list_reports_exact_release_identity(tmp_path: Path) -> None:
    catalog = _write_catalog(tmp_path)

    result = CliRunner().invoke(app, ["adapter", "catalog", "list", str(catalog)])

    assert result.exit_code == 0
    assert f"{SOURCE_COORDINATE}@0.1.1" in result.stdout


def test_catalog_select_exact_release_json(tmp_path: Path) -> None:
    catalog = _write_catalog(tmp_path)

    result = CliRunner().invoke(
        app,
        [
            "adapter",
            "catalog",
            "select",
            str(catalog),
            SOURCE_COORDINATE,
            "--version",
            "0.1.1",
            "--json",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["source_coordinate"] == {
        "authority": "github.com/FAROTECH",
        "publisher": "orbitfabric",
        "name": "fprime",
    }
    assert payload["release_version"] == "0.1.1"
    assert payload["release_descriptor_digest"] == {
        "algorithm": "sha256",
        "value": DESCRIPTOR_SHA,
    }
    assert payload["sources"][0]["binding"]["provider"] == "github-release"
    assert payload["sources"][0]["release_ref"] == "v0.1.1"


def test_catalog_select_unknown_coordinate_fails_closed(tmp_path: Path) -> None:
    catalog = _write_catalog(tmp_path)

    result = CliRunner().invoke(
        app,
        [
            "adapter",
            "catalog",
            "select",
            str(catalog),
            "github.com/FAROTECH:orbitfabric/missing",
            "--version",
            "0.1.1",
        ],
    )

    assert result.exit_code == 1
    assert "Expected one Catalog adapter" in result.stderr


def test_catalog_select_unknown_exact_version_fails_closed(tmp_path: Path) -> None:
    catalog = _write_catalog(tmp_path)

    result = CliRunner().invoke(
        app,
        [
            "adapter",
            "catalog",
            "select",
            str(catalog),
            SOURCE_COORDINATE,
            "--version",
            "v0.1.1",
        ],
    )

    assert result.exit_code == 1
    assert "Expected one exact Catalog release" in result.stderr


def test_catalog_select_rejects_malformed_source_coordinate(tmp_path: Path) -> None:
    catalog = _write_catalog(tmp_path)

    result = CliRunner().invoke(
        app,
        [
            "adapter",
            "catalog",
            "select",
            str(catalog),
            "orbitfabric/fprime",
            "--version",
            "0.1.1",
        ],
    )

    assert result.exit_code == 1
    assert "AUTHORITY:PUBLISHER/NAME" in result.stderr


def test_catalog_validation_fails_closed_on_unresolved_binding(tmp_path: Path) -> None:
    payload = deepcopy(_catalog_payload())
    adapters = payload["adapters"]
    assert isinstance(adapters, list)
    adapters[0]["releases"][0]["sources"][0]["binding"] = "missing-binding"
    catalog = _write_catalog(tmp_path, payload)

    result = CliRunner().invoke(app, ["adapter", "catalog", "validate", str(catalog)])

    assert result.exit_code == 1
    assert "source binding reference is unresolved" in result.stderr
