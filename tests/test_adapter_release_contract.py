from __future__ import annotations

from copy import deepcopy

import pytest

from orbitfabric.conformance.adapter_release import (
    AdapterReleaseContractError,
    validate_release_descriptor,
)

SHA_A = "a" * 64
SHA_B = "b" * 64


def _valid_descriptor() -> dict:
    return {
        "kind": "orbitfabric.adapter_release",
        "descriptor_version": "0.1-candidate",
        "source_coordinate": {
            "authority": "registry.example",
            "publisher": "example",
            "name": "adapter",
        },
        "release_version": "1.2.3",
        "source_provenance": {"commit": "abc123"},
        "artifacts": [
            {
                "id": "python-wheel",
                "artifact_type": "python-wheel",
                "filename": "example_adapter-1.2.3-py3-none-any.whl",
                "sha256": SHA_A,
                "size": 1234,
                "selectors": {"python": ">=3.11"},
            }
        ],
        "integration_package": {"sha256": SHA_B},
    }


def test_release_descriptor_candidate_accepts_valid_payload() -> None:
    validate_release_descriptor(_valid_descriptor())


def test_release_descriptor_candidate_rejects_unknown_fields() -> None:
    payload = _valid_descriptor()
    payload["trusted"] = True

    with pytest.raises(AdapterReleaseContractError, match="not conformant"):
        validate_release_descriptor(payload)


def test_release_descriptor_candidate_rejects_bad_sha256() -> None:
    payload = _valid_descriptor()
    payload["artifacts"][0]["sha256"] = "not-a-digest"

    with pytest.raises(AdapterReleaseContractError, match="not conformant"):
        validate_release_descriptor(payload)


def test_release_descriptor_candidate_rejects_duplicate_artifact_ids() -> None:
    payload = _valid_descriptor()
    second = deepcopy(payload["artifacts"][0])
    second["sha256"] = "c" * 64
    payload["artifacts"].append(second)

    with pytest.raises(AdapterReleaseContractError, match="artifact ids must be unique"):
        validate_release_descriptor(payload)
