# Core Interface Manifest

Status: `0.1-candidate`

## Purpose and ownership

The Core Interface Manifest is the Core-owned, mission-independent machine-readable declaration of structured interfaces exposed by one OrbitFabric executable. Consumers obtain it without Mission Model input, repository access, command discovery, or parsing `--help`.

```bash
orbitfabric export core-interface --json core_interface.json
```

## Contract

```json
{
  "kind": "orbitfabric.core_interface",
  "interface_version": "0.1-candidate",
  "orbitfabric_version": "1.3.0",
  "interface_sha256": "<64 lowercase hexadecimal characters>",
  "capabilities": [
    {
      "id": "scenario_declaration",
      "contract_kind": "orbitfabric.scenario_declaration",
      "contract_version": "0.1-candidate"
    }
  ]
}
```

`capabilities` is sorted by capability `id`. Each id is unique and matches `^[a-z][a-z0-9_]*$`. Malformed internal declarations fail closed.

## Declared capabilities

| Capability id | Contract kind | Contract version |
|---|---|---|
| `coverage_summary` | `orbitfabric.coverage_summary` | `0.1-candidate` |
| `dashboard_summary` | `orbitfabric.dashboard_summary` | `0.1-candidate` |
| `entity_index` | `orbitfabric.entity_index` | `0.1` |
| `integration_input_set` | `orbitfabric.integration_input_set` | `0.1-candidate` |
| `mission_snapshot` | `orbitfabric.mission_snapshot` | `0.1-candidate` |
| `model_summary` | `orbitfabric.model_summary` | `0.1` |
| `relationship_manifest` | `orbitfabric.relationship_manifest` | `0.1-candidate` |
| `scenario_declaration` | `orbitfabric.scenario_declaration` | `0.1-candidate` |
| `scenario_run_index` | `orbitfabric.scenario_run_index` | `0.1-candidate` |

This candidate scope lists existing Core-owned JSON surfaces with independent contract kind/version identities. It is not an exhaustive CLI inventory.

## Canonical identity

`interface_sha256` is lowercase hexadecimal SHA-256 over RFC 8785/JCS canonical bytes for exactly `kind`, `interface_version`, and the normalized `capabilities` array. `orbitfabric_version` and `interface_sha256` are excluded from those canonical bytes.

The fingerprint is stable for an equivalent declaration regardless of implementation collection order. Adding, removing, or changing a declared capability changes it. It is compact provenance and identity, not an executable hash, Git commit, repository coordinate, owner, filesystem path, build host, timestamp, or environment identity.

## Consumer responsibility

Consumers must compare their required capability ids and contract kinds/versions. Fingerprint equality can identify an already-known complete declaration, but fingerprint inequality alone does not say which requirements are compatible.

## Non-goals

The manifest does not expose Studio concepts, inspect repository state, identify an Organization owner, load a Mission Model, redefine existing contracts, or promote candidate contracts. Adapter lifecycle commands and generated runtime/ground artifacts retain their separately documented boundaries and are not declared in this candidate manifest.
