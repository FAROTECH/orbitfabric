from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import rfc8785

from orbitfabric import __version__

CORE_INTERFACE_KIND = "orbitfabric.core_interface"
CORE_INTERFACE_VERSION = "0.1-candidate"
_CAPABILITY_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


@dataclass(frozen=True)
class CoreCapability:
    id: str
    contract_kind: str
    contract_version: str


CORE_CAPABILITIES: tuple[CoreCapability, ...] = (
    CoreCapability("coverage_summary", "orbitfabric.coverage_summary", "0.1-candidate"),
    CoreCapability("dashboard_summary", "orbitfabric.dashboard_summary", "0.1-candidate"),
    CoreCapability("entity_index", "orbitfabric.entity_index", "0.1"),
    CoreCapability(
        "integration_input_set", "orbitfabric.integration_input_set", "0.1-candidate"
    ),
    CoreCapability("mission_snapshot", "orbitfabric.mission_snapshot", "0.1-candidate"),
    CoreCapability("model_summary", "orbitfabric.model_summary", "0.1"),
    CoreCapability(
        "relationship_manifest", "orbitfabric.relationship_manifest", "0.1-candidate"
    ),
    CoreCapability(
        "scenario_declaration", "orbitfabric.scenario_declaration", "0.1-candidate"
    ),
    CoreCapability(
        "scenario_run_index", "orbitfabric.scenario_run_index", "0.1-candidate"
    ),
)


def core_interface_to_dict(
    capabilities: Iterable[CoreCapability] = CORE_CAPABILITIES,
) -> dict[str, Any]:
    """Return the deterministic Core Interface Manifest."""
    normalized = _normalize_capabilities(capabilities)
    declaration = {
        "kind": CORE_INTERFACE_KIND,
        "interface_version": CORE_INTERFACE_VERSION,
        "capabilities": normalized,
    }
    return {
        **declaration,
        "orbitfabric_version": __version__,
        "interface_sha256": hashlib.sha256(rfc8785.dumps(declaration)).hexdigest(),
    }


def write_core_interface(output_file: Path) -> Path:
    """Write one deterministic Core Interface Manifest JSON file."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(
        json.dumps(core_interface_to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output_file


def _normalize_capabilities(
    capabilities: Iterable[CoreCapability],
) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    seen_ids: set[str] = set()

    for capability in capabilities:
        if not isinstance(capability, CoreCapability):
            raise ValueError("Core capability declarations must be CoreCapability values")
        if not _CAPABILITY_ID_PATTERN.fullmatch(capability.id):
            raise ValueError(f"Invalid Core capability id: {capability.id!r}")
        if capability.id in seen_ids:
            raise ValueError(f"Duplicate Core capability id: {capability.id}")
        for field_name, value in (
            ("contract_kind", capability.contract_kind),
            ("contract_version", capability.contract_version),
        ):
            if not value or value != value.strip():
                raise ValueError(
                    f"Invalid {field_name} for Core capability {capability.id}: {value!r}"
                )
        seen_ids.add(capability.id)
        records.append(
            {
                "id": capability.id,
                "contract_kind": capability.contract_kind,
                "contract_version": capability.contract_version,
            }
        )

    return sorted(records, key=lambda record: record["id"])
