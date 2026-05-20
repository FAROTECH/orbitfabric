# Stability and Compatibility Contract

Status: Active v1.0 contract  
Scope: v1.0 stability and compatibility classification baseline  
Applies to: OrbitFabric Core from `v1.0.0 - Stable Mission Data Contract` onward

This page defines the stability and compatibility classification model for OrbitFabric Core after v1.0.0.

It is a documentation contract. It does not introduce new Mission Model semantics, new generated surfaces, new CLI behavior, new report fields, runtime behavior, ground behavior, plugin execution or Studio-specific APIs.

---

## 1. Purpose

v1.0.0 establishes OrbitFabric's first stable narrow Mission Data Contract surface.

The purpose of this document is to classify:

- which surfaces are part of the stable Mission Data Contract;
- which surfaces are public but still preview;
- which surfaces are generated and disposable;
- which surfaces are internal implementation details;
- which changes should be treated as compatibility-sensitive;
- which areas are intentionally outside the compatibility promise.

OrbitFabric remains a Mission Data Contract framework.

---

## 2. Source of truth

The Mission Model remains the source of truth.

Core-owned structured surfaces, generated documentation, runtime-facing bindings, ground-facing artifacts and reports are derived from the validated Mission Model.

They must not become independent sources of mission semantics.

Downstream tools must consume Core-owned structured surfaces instead of reconstructing contract semantics from:

- raw YAML parsing outside OrbitFabric Core;
- generated Markdown documentation;
- generated C++ headers;
- generated ground dictionaries;
- textual CLI output;
- UI state.

---

## 3. Stability labels

OrbitFabric uses these stability labels from v1.0.0 onward.

### 3.1 Stable contract

A stable contract surface is a v1.0 or later compatibility commitment.

Changes to stable surfaces are compatibility-sensitive and must be explicit, reviewed and documented.

### 3.2 Public preview

A public preview surface is intentionally documented and intended for users or downstream tools to inspect.

Public preview surfaces may evolve, but changes should be deliberate, documented and reviewed.

### 3.3 Generated disposable artifact

A disposable generated artifact is intended to be regenerated from the Mission Model.

Users should not hand-edit it or treat it as authoritative source input.

### 3.4 Internal implementation detail

An internal implementation detail is not a public compatibility surface.

It may change without migration support as long as public behavior and documented stable surfaces remain valid.

---

## 4. Current surface classification

The current v1.0 classification is:

| Surface | Classification | Notes |
|---|---|---|
| Mission Model documented semantics | Stable contract | Source of truth for documented domains, fields, identifiers and reference rules. |
| Core structural validation | Stable contract | Loader and validation responsibilities for documented inputs. |
| Core semantic lint diagnostic policy | Stable contract | Diagnostic codes, severities and meanings are compatibility-sensitive. |
| Scenario YAML evidence inputs | Stable contract | Host-side scenario evidence input semantics. |
| lint JSON report | Stable contract | Machine-readable validation result. |
| simulation JSON report | Stable contract | Machine-readable scenario evidence. |
| `model_summary.json` | Stable contract | Core-owned domain-level structured surface. |
| `entity_index.json` | Stable contract | Core-owned entity-level structured surface. |
| `relationship_manifest.json` | Stable contract for admitted families | Core-owned relationship-level structured surface. |
| documented CLI workflow commands and options | Stable contract | Human-oriented terminal wording remains preview. |
| release compatibility policy | Stable governance surface | Post-v1 compatibility review discipline. |
| extensibility boundary contract | Stable governance surface | Boundary without plugin execution. |
| CLI textual output | Public preview, human-oriented | Useful for humans. Not a machine contract. |
| generated Markdown documentation | Public preview, generated artifact | Human-reviewable output. Not source of truth. |
| generated runtime-facing bindings | Public preview, disposable generated artifact | Contract-facing bindings. Not flight software ABI. |
| generated ground-facing artifacts | Public preview, disposable generated artifact | Integration artifacts. Not a ground segment runtime. |
| Python module internals | Internal implementation detail | Not a public API unless explicitly documented. |
| tests | Internal validation asset | May change with implementation and behavior coverage. |
| demo mission | Public example | Synthetic clean-room example, not a real mission profile. |

---

## 5. Compatibility-sensitive changes

These changes are compatibility-sensitive after v1.0.0:

- removing or renaming documented Mission Model fields;
- changing the meaning of documented Mission Model fields;
- changing documented controlled values;
- changing documented identifier rules;
- changing CLI command names or required arguments;
- changing JSON report top-level fields;
- changing Core-owned structured surface record shapes;
- changing lint rule codes;
- changing scenario expectation semantics;
- changing generated artifact paths that are documented as public preview;
- changing boundary flags that downstream tools may inspect.

Compatibility-sensitive does not mean forbidden.

It means the change must be explicit, reviewed and documented.

---

## 6. Changes that do not require compatibility guarantees

These areas are not compatibility promises unless explicitly documented as stable:

- internal Python function layout;
- private helper names;
- test helper structure;
- implementation order;
- formatting of human-oriented CLI text;
- generated file formatting when the machine-readable contract is unchanged;
- non-documented internal data structures;
- local development scripts;
- CI implementation details;
- synthetic example wording.

These may still require review, but they do not define public Mission Data Contract compatibility.

---

## 7. Current non-goals

This stability and compatibility contract does not introduce:

```text
new Mission Model semantics
new YAML fields
new lint diagnostics
new CLI commands
new JSON report fields
new generated surfaces
plugin execution
plugin discovery
plugin loader
relationship graph
dependency graph
runtime behavior
ground behavior
Studio-specific API
schema migration tooling
JSON Schema publication
```

---

## 8. Downstream tool rule

Downstream tools must treat Core-owned structured surfaces as the supported inspection boundary.

The intended downstream inspection chain remains:

```text
model_summary.json          -> What contract domains are present?
entity_index.json           -> What contract entities are defined?
relationship_manifest.json  -> How are indexed mission contract entities related?
```

Downstream tools must not become a second source of truth.

They must not reconstruct Mission Data Contract semantics from raw YAML, generated files, textual CLI output or UI state.

---

## 9. Relationship to versioning

This document complements the Versioning Model.

Versioning explains which version fields exist and what they mean.

This document explains which surfaces are stable, preview, disposable, internal or out of scope after v1.0.0.

The OrbitFabric package version and the Mission Model version remain distinct concepts.

---

## 10. Final statement

v1.0.0 means a stable Mission Data Contract framework.

It does not mean a complete flight software framework, ground segment, simulator, mission control system, visual modeling tool or plugin execution platform.
