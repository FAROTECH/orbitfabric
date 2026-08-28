# Versioning Model

This page explains how OrbitFabric uses version numbers after `v1.0.0 - Stable Mission Data Contract`.

OrbitFabric distinguishes between:

- the OrbitFabric tool/package version;
- the Mission Model version declared by a mission;
- generated JSON report producer versions;
- Core-owned structured-surface format versions;
- the Core Integration Input Set version;
- extension-owned Projection Profile / Integration Result / Integration Package contract versions;
- runtime/ground generated manifest context;
- stability and compatibility classification.

These versions and classifications are related, but they are not interchangeable.

---

## OrbitFabric tool/package version

The OrbitFabric tool/package version identifies the Python package and CLI release.

It is defined in:

```text
pyproject.toml
src/orbitfabric/__init__.py
```

It is shown by:

```bash
orbitfabric --version
```

Current release:

```text
orbitfabric 1.2.0
```

This version answers:

```text
Which OrbitFabric tool release generated, validated or executed this artifact?
```

It is provenance/support information. It is not the sole compatibility key for structured surfaces.

---

## Mission Model version

The Mission Model version is declared inside the mission YAML, currently under `spacecraft.yaml`.

Demo example:

```yaml
spacecraft:
  id: demo-3u
  name: Demo 3U Spacecraft
  model_version: 0.1.0
```

This version answers:

```text
Which Mission Model contract version does this mission declare?
```

It is part of the mission data contract and is independent from the OrbitFabric package version.

---

## Generated JSON report producer version

Generated JSON reports may include the OrbitFabric package version that produced them.

Conceptual lint example:

```json
{
  "tool": "orbitfabric-lint",
  "version": "1.2.0",
  "mission": "demo-3u",
  "model_version": "0.1.0"
}
```

The top-level producer `version` and the mission's `model_version` answer different questions.

For compatibility-sensitive machine-readable surfaces, consumers must use the documented surface/report compatibility identifier rather than package version alone.

---

## Core-owned structured-surface format versions

Stable Core-owned surfaces may retain format-version identifiers that predate their stability promotion.

Current relevant identifiers are:

| Surface | Format version field | Current value | v1.2 classification |
|---|---|---|---|
| `model_summary.json` | `summary_version` | `0.1` | Stable |
| `entity_index.json` | `index_version` | `0.1` | Stable |
| `relationship_manifest.json` | `manifest_version` | `0.1-candidate` | Stable for admitted families |
| `mission_snapshot.json` | `snapshot_version` | `0.1-candidate` | Stable from v1.2.0 |
| Core Integration Input Set | `input_set_version` | `0.1-candidate` | Stable from v1.2.0 |

This is intentional:

```text
stability classification != format-version text
```

Changing a proven wire identifier merely to remove the word `candidate` would create avoidable consumer incompatibility without changing semantics.

A breaking change to a stable contract requires an explicit compatibility decision and a new identifier/version when appropriate.

---

## Core Integration Input Set version

The coherent input set uses:

```text
kind = orbitfabric.integration_input_set
input_set_version = 0.1-candidate
```

From v1.2.0, the documented input-set semantics are stable even though this identifier remains unchanged.

An external adapter must negotiate at least:

```text
input-set kind/version
surface role
surface kind
surface format version
supported typed records where applicable
```

`orbitfabric_version` alone is insufficient.

---

## Extension-owned integration contract versions

The generic Integration Framework also defines independently versioned extension contracts:

```text
Projection Profile
Integration Result
Integration Package / Adapter Execution
```

At the v1.2.0 Core release they remain:

```text
0.1-candidate
```

They are not stable Core Mission Data Contract surfaces.

The stable Core Integration Input Set can therefore be consumed by extension contracts whose own compatibility classification remains candidate.

This separation lets the Core input boundary stabilize without prematurely freezing ecosystem-specific projection or adapter-execution contracts.

---

## Runtime contract manifest context

Generated runtime-facing contract bindings include a runtime manifest under:

```text
generated/runtime/cpp17/runtime_contract_manifest.json
```

It records generation context and boundary flags such as:

```text
generation profile
contains_flight_runtime = false
generated_artifacts_are_disposable = true
```

It is a generated contract artifact, not flight runtime behavior and not automatically a stable schema merely because the OrbitFabric package is stable.

---

## Ground contract manifest context

Generated ground-facing artifacts include:

```text
generated/ground/generic/ground_contract_manifest.json
```

It records package/artifact generation context and boundary flags such as:

```text
generated_artifacts_are_disposable = true
contains_ground_runtime = false
contains_operator_console = false
contains_transport = false
contains_database = false
claims_yamcs_compatibility = false
claims_openc3_compatibility = false
claims_xtce_compliance = false
```

It is not a ground segment schema, mission database compatibility promise or tool-specific integration guarantee.

---

## Stability and compatibility context

`v1.0.0` established the first stable narrow Mission Data Contract.

`v1.2.0` additively extends that stable boundary with:

```text
mission_snapshot.json
Core Integration Input Set
seven admitted additive FDIR Relationship Manifest families
```

The v1.1.0 dashboard summary, scenario run index, coverage summary and structured expectation additions remain candidate unless separately promoted.

Stability classification is governed by explicit reviewed decisions, not by the mere existence of a file or version token.

---

## Extensibility boundary context

The Extensibility Boundary Contract remains a stable governance surface.

It records expectations such as:

```text
Core remains semantic owner
Mission Model remains source of truth
extensions consume Core-owned surfaces
extension-owned outputs remain distinguishable from Core-owned outputs
semantic override remains forbidden
Core in-process ecosystem execution remains out of scope
```

The stable v1.2 Integration Input Set reinforces that boundary: Core exports the coherent machine-readable input; external packages execute target-specific integration logic outside Core.

---

## Why the versions differ

A valid v1.2 configuration may therefore contain:

```text
OrbitFabric package version:             1.2.0
Mission Model version:                   0.1.0
Mission Snapshot format version:         0.1-candidate
Integration Input Set format version:    0.1-candidate
Projection Profile contract version:     0.1-candidate
Integration Result contract version:     0.1-candidate
```

There is no contradiction.

Each version identifies a different compatibility/provenance dimension.

The engineering rule is:

> negotiate the contract you consume; do not infer compatibility from one unrelated version number.
