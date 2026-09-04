# Versioning Model

This page explains how OrbitFabric uses version numbers after `v1.0.0 - Stable Mission Data Contract`.

OrbitFabric distinguishes between:

- the OrbitFabric tool/package version;
- the Mission Model version declared by a mission;
- generated JSON report producer versions;
- Core-owned structured-surface format versions;
- the Core Integration Input Set version;
- extension-owned Projection Profile / Integration Result / Integration Package contract versions;
- Adapter Management contract format versions;
- an adapter's own exact release version;
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
orbitfabric 1.3.0
```

This version answers:

```text
Which OrbitFabric Core release generated, validated or executed this artifact/workflow?
```

It is provenance/support information. It is not the sole compatibility key for structured surfaces, Integration Package contracts or adapter releases.

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
  "version": "1.3.0",
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

| Surface | Format version field | Current value | Current classification |
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

The generic Integration Framework defines independently versioned extension contracts.

The original frozen candidate lane remains conceptually:

```text
Projection Profile 0.1-candidate
Integration Package / Adapter Execution v0 lane
Integration Result 0.1-candidate
```

v1.3.0 also includes the candidate operation-input execution lane:

```text
Integration Package Manifest 0.2-candidate
orbitfabric.adapter_cli.v1
Integration Result 0.2-candidate
```

The Projection Profile remains independently versioned and target-specific intent remains extension-owned.

These contracts are not stable Core Mission Data Contract surfaces.

The stable Core Integration Input Set can therefore be consumed by extension contracts whose own compatibility classification remains candidate.

This separation lets the Core input boundary remain stable while integration invocation/result contracts evolve under their own explicit versions.

---

## Adapter Management contract format versions

v1.3.0 introduces candidate Adapter Management contracts with their own format identities.

Current formats include:

```text
Adapter Release Descriptor  0.1-candidate
Adapter Project Lock         0.1-candidate
Adapter Catalog              0.1-candidate
```

These format versions answer questions such as:

```text
Which Release Descriptor schema does this document follow?
Which Project Lock structure/semantics does this project use?
Which Catalog format does this data product use?
```

They do not answer which OrbitFabric package release is installed and they do not answer which adapter release is selected.

Core package version `1.3.0` does not promote these candidate format versions to stable.

---

## Adapter exact release version

An external adapter has its own release version, for example:

```text
orbitfabric/fprime @ 0.1.1
```

That value is part of exact adapter release identity.

It is distinct from:

```text
OrbitFabric Core version
Adapter Release Descriptor format version
Adapter Project Lock format version
Adapter Catalog format version
provider release reference/tag
```

A Project Lock records the exact adapter release version together with descriptor/artifact digests.

A provider release reference such as a Git tag may help locate that release, but it is provider-owned acquisition metadata rather than a substitute for the Core Source Coordinate + exact release identity.

---

## Adapter Catalog exact release anchor

The provider-neutral Catalog uses an exact release anchor:

```text
Source Coordinate
+ exact adapter release version
+ expected Release Descriptor SHA-256
```

The Catalog's own `catalog_version` describes the Catalog format, not the adapter release.

Provider-owned fields such as a GitHub release tag/reference remain source-binding metadata and do not become Project Lock identity merely because they are present in a Catalog.

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

`v1.2.0` additively extended that stable boundary with:

```text
mission_snapshot.json
Core Integration Input Set
seven admitted additive FDIR Relationship Manifest families
```

`v1.3.0` preserves that stable boundary and adds separately classified candidate operation-input and Adapter Management capabilities.

The v1.1.0 dashboard summary, scenario run index, coverage summary and structured expectation additions remain candidate unless separately promoted.

Stability classification is governed by explicit reviewed decisions, not by the mere existence of a file, package release or version token.

---

## Extensibility and provider boundary context

The Extensibility Boundary Contract remains a stable governance surface.

It records expectations such as:

```text
Core remains semantic owner
Mission Model remains source of truth
extensions consume Core-owned surfaces
extension-owned outputs remain distinguishable from Core-owned outputs
semantic override remains forbidden
Core in-process ecosystem implementation loading remains out of scope
```

The stable v1.2 Integration Input Set reinforces that boundary: Core exports the coherent machine-readable input; external packages own target-specific integration logic.

The v1.3 Adapter Management boundary adds a parallel ownership rule:

```text
Core owns exact adapter identity, desired/actual state and lifecycle semantics
provider-specific Release Sources own provider acquisition
ResolvedAdapterRelease is the handoff
```

Provider implementation versioning is therefore separate from Core versioning and separate from adapter release versioning.

---

## Why the versions differ

A valid v1.3 configuration may therefore contain:

```text
OrbitFabric Core package version:            1.3.0
Mission Model version:                       0.1.0
Mission Snapshot format version:             0.1-candidate
Integration Input Set format version:        0.1-candidate
Projection Profile contract version:         0.1-candidate
Integration Package Manifest version:        0.2-candidate
Integration Result version:                  0.2-candidate
Adapter Release Descriptor format version:   0.1-candidate
Adapter Project Lock format version:          0.1-candidate
Adapter Catalog format version:               0.1-candidate
Selected F Prime adapter release version:    0.1.1
```

There is no contradiction.

Each version identifies a different compatibility, identity or provenance dimension.

The engineering rule is:

> negotiate the contract you consume; pin the exact release you install; do not infer compatibility or identity from one unrelated version number.
