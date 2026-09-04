from __future__ import annotations

from copy import deepcopy

import pytest
from pydantic import ValidationError

from orbitfabric.adapter_manager.catalog import (
    AdapterCatalog,
    select_exact_release,
    select_exact_release_by_logical_key,
)
from orbitfabric.adapter_manager.errors import ReleaseResolutionError
from orbitfabric.adapter_manager.models import AdapterSourceCoordinate


def _catalog_payload() -> dict[str, object]:
    return {
        "kind": "orbitfabric.adapter_catalog",
        "catalog_version": "0.1-candidate",
        "adapters": [
            {
                "source_coordinate": {
                    "authority": "github.com/FAROTECH",
                    "publisher": "orbitfabric",
                    "name": "openobsw-opensvf",
                },
                "releases": [
                    {
                        "version": "0.1.0",
                        "release_descriptor_digest": {
                            "algorithm": "sha256",
                            "value": (
                                "ef1b568c06a1573b580bbb91308b1311"
                                "b81ba65dca29331fcf1610fc7ee5c016"
                            ),
                        },
                        "sources": [
                            {
                                "binding": "github-openobsw",
                                "release_ref": "v0.1.0",
                            }
                        ],
                    }
                ],
            },
            {
                "source_coordinate": {
                    "authority": "github.com/FAROTECH",
                    "publisher": "orbitfabric",
                    "name": "openc3-cosmos",
                },
                "releases": [
                    {
                        "version": "0.1.0",
                        "release_descriptor_digest": {
                            "algorithm": "sha256",
                            "value": (
                                "2509a1c1c132f647abba0ebe02af4962"
                                "7ebbbed58d62555efd60d7cb30b48d4f"
                            ),
                        },
                        "sources": [
                            {
                                "binding": "github-cosmos",
                                "release_ref": "v0.1.0",
                            }
                        ],
                    }
                ],
            },
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
                            "value": (
                                "724eb67299150887167dfce8aa3ea117"
                                "a163c79b6fcaff6ab105dfd35daf7464"
                            ),
                        },
                        "sources": [
                            {
                                "binding": "github-fprime",
                                "release_ref": "v0.1.1",
                            }
                        ],
                    }
                ],
            },
        ],
        "source_bindings": [
            {
                "id": "github-openobsw",
                "provider": "github-release",
                "config": {
                    "repository": "FAROTECH/orbitfabric-openobsw-opensvf-adapter"
                },
            },
            {
                "id": "github-cosmos",
                "provider": "github-release",
                "config": {
                    "repository": "FAROTECH/orbitfabric-openc3-cosmos-adapter"
                },
            },
            {
                "id": "github-fprime",
                "provider": "github-release",
                "config": {"repository": "FAROTECH/orbitfabric-fprime-adapter"},
            },
        ],
    }


def _catalog() -> AdapterCatalog:
    return AdapterCatalog.model_validate(_catalog_payload())


def _fprime_coordinate() -> AdapterSourceCoordinate:
    return AdapterSourceCoordinate(
        authority="github.com/FAROTECH",
        publisher="orbitfabric",
        name="fprime",
    )


def test_three_canonical_releases_validate_in_one_provider_neutral_catalog() -> None:
    catalog = _catalog()

    assert len(catalog.adapters) == 3
    assert {adapter.source_coordinate.name for adapter in catalog.adapters} == {
        "openobsw-opensvf",
        "openc3-cosmos",
        "fprime",
    }


def test_exact_source_coordinate_and_version_select_one_release() -> None:
    selection = select_exact_release(_catalog(), _fprime_coordinate(), "0.1.1")

    assert selection.source_coordinate == _fprime_coordinate()
    assert selection.release_version == "0.1.1"
    assert selection.release_descriptor_digest.algorithm == "sha256"
    assert (
        selection.release_descriptor_digest.value
        == "724eb67299150887167dfce8aa3ea117a163c79b6fcaff6ab105dfd35daf7464"
    )
    assert len(selection.sources) == 1
    assert selection.sources[0].binding.provider == "github-release"
    assert selection.sources[0].binding.config == {
        "repository": "FAROTECH/orbitfabric-fprime-adapter"
    }
    assert selection.sources[0].release_ref == "v0.1.1"


def test_exact_version_matching_does_not_normalize_provider_ref_or_version() -> None:
    catalog = _catalog()

    with pytest.raises(ReleaseResolutionError, match="Expected one exact Catalog release"):
        select_exact_release(catalog, _fprime_coordinate(), "v0.1.1")


def test_unknown_source_coordinate_fails_closed() -> None:
    catalog = _catalog()
    coordinate = AdapterSourceCoordinate(
        authority="github.com/FAROTECH",
        publisher="orbitfabric",
        name="missing",
    )

    with pytest.raises(ReleaseResolutionError, match="Expected one Catalog adapter"):
        select_exact_release(catalog, coordinate, "0.1.0")


def test_unknown_exact_release_fails_closed() -> None:
    with pytest.raises(ReleaseResolutionError, match="Expected one exact Catalog release"):
        select_exact_release(_catalog(), _fprime_coordinate(), "9.9.9")


def test_logical_key_selects_only_when_one_authority_matches() -> None:
    selection = select_exact_release_by_logical_key(
        _catalog(),
        publisher="orbitfabric",
        name="fprime",
        release_version="0.1.1",
    )

    assert selection.source_coordinate.authority == "github.com/FAROTECH"


def test_logical_key_fails_when_two_authorities_publish_same_key() -> None:
    payload = deepcopy(_catalog_payload())
    adapters = payload["adapters"]
    bindings = payload["source_bindings"]
    assert isinstance(adapters, list)
    assert isinstance(bindings, list)

    adapters.append(
        {
            "source_coordinate": {
                "authority": "example-registry.invalid/independent",
                "publisher": "orbitfabric",
                "name": "fprime",
            },
            "releases": [
                {
                    "version": "0.1.1",
                    "release_descriptor_digest": {
                        "algorithm": "sha256",
                        "value": "a" * 64,
                    },
                    "sources": [
                        {
                            "binding": "independent-fprime",
                            "release_ref": "release-17",
                        }
                    ],
                }
            ],
        }
    )
    bindings.append(
        {
            "id": "independent-fprime",
            "provider": "independent-provider",
            "config": {"locator": "opaque"},
        }
    )
    catalog = AdapterCatalog.model_validate(payload)

    with pytest.raises(ReleaseResolutionError, match="logical key orbitfabric/fprime"):
        select_exact_release_by_logical_key(
            catalog,
            publisher="orbitfabric",
            name="fprime",
            release_version="0.1.1",
        )


def test_multiple_source_bindings_are_mirrors_not_release_ambiguity() -> None:
    payload = deepcopy(_catalog_payload())
    adapters = payload["adapters"]
    bindings = payload["source_bindings"]
    assert isinstance(adapters, list)
    assert isinstance(bindings, list)

    fprime_release = adapters[2]["releases"][0]
    fprime_release["sources"].append(
        {"binding": "fprime-mirror", "release_ref": "mirror-v0.1.1"}
    )
    bindings.append(
        {
            "id": "fprime-mirror",
            "provider": "mirror-provider",
            "config": {"locator": "opaque-mirror"},
        }
    )

    selection = select_exact_release(
        AdapterCatalog.model_validate(payload),
        _fprime_coordinate(),
        "0.1.1",
    )

    assert selection.source_coordinate == _fprime_coordinate()
    assert selection.release_version == "0.1.1"
    assert [source.binding.id for source in selection.sources] == [
        "github-fprime",
        "fprime-mirror",
    ]


def test_unresolved_source_binding_is_invalid_catalog_data() -> None:
    payload = deepcopy(_catalog_payload())
    adapters = payload["adapters"]
    assert isinstance(adapters, list)
    adapters[2]["releases"][0]["sources"].append(
        {"binding": "missing-binding", "release_ref": "v0.1.1"}
    )

    with pytest.raises(ValidationError, match="source binding reference is unresolved"):
        AdapterCatalog.model_validate(payload)


def test_duplicate_binding_id_is_invalid_catalog_data() -> None:
    payload = deepcopy(_catalog_payload())
    bindings = payload["source_bindings"]
    assert isinstance(bindings, list)
    bindings.append(deepcopy(bindings[0]))

    with pytest.raises(ValidationError, match="source binding ids must be unique"):
        AdapterCatalog.model_validate(payload)


def test_duplicate_source_coordinate_is_invalid_catalog_data() -> None:
    payload = deepcopy(_catalog_payload())
    adapters = payload["adapters"]
    assert isinstance(adapters, list)
    adapters.append(deepcopy(adapters[0]))

    with pytest.raises(ValidationError, match="Source Coordinates must be unique"):
        AdapterCatalog.model_validate(payload)


def test_duplicate_release_version_is_invalid_catalog_data() -> None:
    payload = deepcopy(_catalog_payload())
    adapters = payload["adapters"]
    assert isinstance(adapters, list)
    releases = adapters[2]["releases"]
    releases.append(deepcopy(releases[0]))

    with pytest.raises(ValidationError, match="release versions must be unique"):
        AdapterCatalog.model_validate(payload)
