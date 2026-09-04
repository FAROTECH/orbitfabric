# Stability and Compatibility Contract

Status: Active v1.x contract through v1.3.0  
Scope: stable, candidate, disposable and internal compatibility classification  
Applies to: OrbitFabric Core from `v1.0.0 - Stable Mission Data Contract` onward

This page defines the stability and compatibility classification model for OrbitFabric Core.

---

## 1. Purpose

v1.0.0 established OrbitFabric's first stable narrow Mission Data Contract surface. Later minor releases may add stable-compatible capabilities or candidate product capabilities only through explicit reviewed classification.

The contract distinguishes:

- stable contract surfaces;
- public preview/candidate surfaces;
- generated disposable artifacts;
- internal implementation details;
- compatibility-sensitive changes;
- intentionally out-of-scope behavior.

OrbitFabric remains a Mission Data Contract framework with provider-neutral adapter lifecycle capabilities at the product boundary.

---

## 2. Source of truth

The Mission Model remains the source of truth.

Core-owned structured surfaces and generated artifacts derive from the loaded Mission Model. They must not become independent sources of mission semantics.

Downstream tools must consume documented Core-owned surfaces instead of reconstructing semantics from raw YAML, generated Markdown/C++/ground files, textual CLI output or UI state.

Adapter lifecycle state is separate from Mission Model semantics. Adapter Release Descriptor, Project Lock and Adapter Catalog records describe exact external adapter lifecycle identity; they do not become alternate Mission Model sources.

---

## 3. Stability labels

### Stable contract

A stable contract surface is a v1.x compatibility commitment. Changes are compatibility-sensitive and must be explicit, reviewed and documented.

### Public preview / candidate

A documented candidate surface is intended for inspection or controlled downstream use but may evolve through explicit reviewed changes.

### Generated disposable artifact

A disposable generated artifact is reproducible output. It is not authoritative input and should not be hand-edited.

### Internal implementation detail

An internal detail is not a public compatibility surface and may change while documented public behavior remains valid.

---

## 4. Stable Core classification through v1.3.0

Stable Mission Data Contract and Core integration surfaces include:

| Surface | Classification | Notes |
|---|---|---|
| Mission Model documented semantics | Stable contract | Semantic source of truth. |
| Core structural validation | Stable contract | Loader/validation responsibilities for documented inputs. |
| Core semantic lint diagnostic policy | Stable contract | Codes, severities and meanings are compatibility-sensitive. |
| Scenario YAML evidence inputs | Stable contract | Host-side scenario evidence input semantics. |
| lint JSON report | Stable contract | Machine-readable Core lint result. |
| simulation JSON report | Stable contract | Machine-readable scenario evidence baseline. |
| `model_summary.json` | Stable contract | Core-owned domain-level structured surface. |
| `entity_index.json` | Stable contract | Core-owned entity-level structured surface. |
| `relationship_manifest.json` | Stable for admitted families | Original v1 and later explicitly admitted additive families. |
| `mission_snapshot.json` | Stable from v1.2.0 | Complete loaded Mission Model inspection envelope. |
| Core Integration Input Set | Stable from v1.2.0 | Coherent Core-to-external-integration input boundary. |
| documented stable CLI workflows | Stable contract | Human-oriented terminal wording remains non-machine output. |
| release compatibility policy | Stable governance surface | Post-v1 compatibility review discipline. |
| extensibility boundary contract | Stable governance surface | Core extension boundary without in-process ecosystem execution. |

The seven FDIR Relationship Manifest families admitted in v1.2.0 are additive stable-compatible families. Unknown additive relationship types must not receive guessed semantics.

The Mission Snapshot and Integration Input Set retain their `0.1-candidate` format identifiers. Stability classification and format-version identifiers are separate compatibility concepts.

v1.3.0 does not promote any additional Mission Data Contract surface to stable.

---

## 5. Candidate surfaces after v1.3.0

These Core-owned inspection surfaces remain candidate:

```text
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
simulation JSON structured expectation accounting additions
```

These integration contracts remain candidate:

```text
Projection Profile
Integration Result
Integration Package / Adapter Execution
operation-input v1 lane
```

These Adapter Management surfaces are also candidate:

```text
Adapter Manager lifecycle
Adapter Release Descriptor 0.1-candidate
Adapter Project Lock 0.1-candidate
explicit-source install-from-lock
source-neutral ResolvedAdapterRelease attachment
Adapter Catalog 0.1-candidate
Adapter Catalog CLI
```

Candidate status means usable and documented, but not silently promoted into the stable Mission Data Contract merely because Core v1.3.0 is a stable package release.

---

## 6. Adapter Management ownership boundary

Core owns provider-neutral lifecycle semantics:

```text
exact Source Coordinate identity
exact release version
Release Descriptor conformance
artifact identity and digest gates
project-scoped desired state through Project Lock
user-scoped Installed Adapter State
installation transaction and verification
provider-neutral Catalog model and exact selection
source-neutral ResolvedAdapterRelease handoff
```

Core does not own provider-specific acquisition:

```text
GitHub REST behavior
provider authentication
provider registration/dispatch
remote registry protocol
provider-specific release lookup
cache/mirror transport policy
```

A provider-specific Release Source may acquire and verify exact release material outside Core and hand a complete `ResolvedAdapterRelease` into the Core lifecycle.

Provider locators and mutable transport metadata must not silently become Project Lock identity.

---

## 7. Compatibility-sensitive changes

Compatibility-sensitive changes include:

- removing or renaming documented Mission Model fields;
- changing documented field meaning or controlled values;
- changing identifier/reference rules;
- changing stable CLI command names or required arguments;
- changing stable JSON/Core-owned surface required fields, result tokens, kind values or version semantics;
- changing lint rule codes or meanings;
- changing scenario expectation semantics;
- changing stable Integration Input Set role/state/coherence semantics;
- redefining an admitted Relationship Manifest family.

For candidate Adapter Management surfaces, preview compatibility-sensitive changes include:

- changing exact Source Coordinate semantics;
- changing Project Lock identity dimensions;
- changing Release Descriptor or Catalog identity/schema meaning;
- changing documented `MATCH`, `MISSING` or `MISMATCH` lifecycle meaning;
- changing fail-closed exact-selection semantics;
- introducing provider-specific assumptions into provider-neutral Core contracts.

Compatibility-sensitive does not mean forbidden. It means the change requires explicit review, release notes and migration guidance where needed.

---

## 8. Additive evolution

Additive changes may be compatible when they preserve existing meaning.

Examples include additive optional fields and explicitly admitted additive Relationship Manifest families.

Compatible consumers must tolerate additive fields or relationship types where the relevant contract says the set is extensible. Consumers must never guess semantics for unknown types.

The Mission Snapshot's complete `model` payload follows Mission Model compatibility rules. Its stable classification does not freeze every future additive Mission Model field.

Candidate Adapter Management contracts may also evolve additively, but changes must remain explicit because external tooling may already consume them.

---

## 9. Stable Integration Input consumer rule

A production integration consumer must negotiate:

```text
input-set kind/version
surface role
surface kind
surface format version
supported typed records where applicable
```

Package version alone is not a sufficient compatibility key.

A missing or incompatible required surface blocks semantic projection. No raw-YAML semantic fallback is allowed.

---

## 10. Adapter lifecycle consumer rule

Adapter lifecycle consumers must distinguish:

```text
logical adapter identity
exact release identity
artifact identity
provider/source acquisition metadata
installed local state
project desired state
```

A Catalog selector resolves one exact release before provider acquisition. A Release Source resolves exact bytes before Core installation. Project Lock remains exact desired identity and does not absorb mutable provider locators or local installation paths.

The absence of one unified provider-neutral install command in v1.3.0 is intentional. Core does not generalize a universal provider dispatch protocol from the first provider implementation.

---

## 11. Changes without public compatibility guarantees

Unless separately documented as stable, the following remain outside compatibility promises:

- internal Python function layout;
- private helper names;
- test helper structure;
- CI implementation details;
- formatting of human-oriented terminal output;
- disposable generated formatting;
- local development scripts;
- raw Installed Adapter Inventory persistence layout;
- local adapter instance identifiers;
- managed-environment filesystem layout;
- backend receipts;
- provider transport URLs and caches.

---

## 12. Current non-goals

The v1.3 boundary does not introduce:

```text
Core plugin discovery/loading
third-party adapter import/execution inside the Core Python process
provider-specific acquisition inside Core
universal provider plugin protocol
remote registry dependency for Core
version ranges / latest / channel resolution
relationship graph behavior
dependency graph behavior
flight runtime behavior
ground runtime behavior
Studio-specific semantic authority
OpenOBSW/OpenSVF/YAMCS/F Prime-specific Core semantics
schema migration tooling
```

Adapter Manager may execute an installed external adapter through the documented adapter execution contract and environment-local entrypoint. This does not make target-specific code or dependencies part of the Core process or semantic authority.

---

## 13. Final statement

OrbitFabric v1.x means a stable Mission Data Contract framework with explicit compatibility governance.

v1.3.0 preserves the stable Mission Data Contract and v1.2 Core Integration Input boundary while adding candidate, provider-neutral Adapter Management capabilities. Package stability does not silently promote those candidate lifecycle contracts, and provider-specific acquisition remains outside Core.
