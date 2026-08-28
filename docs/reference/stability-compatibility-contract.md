# Stability and Compatibility Contract

Status: Active v1.x contract  
Scope: stable, candidate, disposable and internal compatibility classification  
Applies to: OrbitFabric Core from `v1.0.0 - Stable Mission Data Contract` onward

This page defines the stability and compatibility classification model for OrbitFabric Core.

---

## 1. Purpose

v1.0.0 established OrbitFabric's first stable narrow Mission Data Contract surface. Later minor releases may add stable-compatible capabilities only through explicit reviewed classification.

The contract distinguishes:

- stable contract surfaces;
- public preview/candidate surfaces;
- generated disposable artifacts;
- internal implementation details;
- compatibility-sensitive changes;
- intentionally out-of-scope behavior.

OrbitFabric remains a Mission Data Contract framework.

---

## 2. Source of truth

The Mission Model remains the source of truth.

Core-owned structured surfaces and generated artifacts derive from the loaded Mission Model. They must not become independent sources of mission semantics.

Downstream tools must consume documented Core-owned surfaces instead of reconstructing semantics from raw YAML, generated Markdown/C++/ground files, textual CLI output or UI state.

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

## 4. Stable Core classification through v1.2.0

Stable surfaces include:

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

---

## 5. Candidate surfaces after v1.2.0

These Core-owned surfaces remain candidate:

```text
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
simulation JSON structured expectation accounting additions
```

These extension-owned contracts also remain `0.1-candidate` and are not stable Core Mission Data Contract surfaces:

```text
Projection Profile
Integration Result
Integration Package / Adapter Execution
```

---

## 6. Compatibility-sensitive changes

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

Compatibility-sensitive does not mean forbidden. It means the change requires explicit review, release notes and migration guidance where needed.

---

## 7. Additive evolution

Additive changes may be compatible when they preserve existing meaning.

Examples include additive optional fields and explicitly admitted additive Relationship Manifest families.

Compatible consumers must tolerate additive fields or relationship types where the relevant contract says the set is extensible. Consumers must never guess semantics for unknown types.

The Mission Snapshot's complete `model` payload follows Mission Model compatibility rules. Its stable classification does not freeze every future additive Mission Model field.

---

## 8. Stable Integration Input consumer rule

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

## 9. Changes without public compatibility guarantees

Unless separately documented as stable, the following remain outside compatibility promises:

- internal Python function layout;
- private helper names;
- test helper structure;
- CI implementation details;
- formatting of human-oriented terminal output;
- disposable generated formatting;
- local development scripts.

---

## 10. Current non-goals

The stable v1.2 boundary does not introduce:

```text
Core plugin discovery/loading/execution
Core in-process Integration Adapter execution
relationship graph behavior
dependency graph behavior
runtime behavior
ground behavior
Studio-specific API
OpenOBSW/OpenSVF/YAMCS-specific Core semantics
schema migration tooling
```

---

## 11. Final statement

OrbitFabric v1.x means a stable Mission Data Contract framework with explicit compatibility governance.

v1.2.0 adds a stable Core-owned integration input boundary without turning Core into a flight software framework, ground segment, plugin runtime, target-specific integration implementation or visual modeling backend.
