# Generated Surfaces Stability

Status: Active v1.1 classification  
Scope: generated and exported surface compatibility classification  
Applies to: OrbitFabric generated and exported surfaces from `v1.0.0 - Stable Mission Data Contract` onward

This page classifies OrbitFabric generated and exported surfaces after v1.1.0.

It documents stable v1.0.0 surfaces and candidate v1.1.0 surfaces. It does not introduce new CLI behavior, new Mission Model semantics, plugin execution, runtime behavior, ground behavior or Studio-specific APIs.

---

## 1. Purpose

OrbitFabric generates and exports several surfaces derived from the validated Mission Model and from Core-generated structured evidence.

The Mission Model remains the source of truth.

This document separates:

- stable v1.0.0 Core-owned inspection surfaces;
- candidate v1.1.0 Core-owned integration surfaces;
- machine-readable validation and evidence reports;
- generated runtime-facing artifacts;
- generated ground-facing artifacts;
- generated Markdown documentation;
- disposable outputs.

---

## 2. Stable v1.0.0 Core-owned structured inspection surfaces

The stable v1.0.0 surfaces are:

```text
model_summary.json
entity_index.json
relationship_manifest.json
```

They exist to prevent downstream tools from reconstructing Mission Data Contract semantics from raw YAML, generated files, textual CLI output or UI state.

The stable Core-owned inspection chain is:

```text
model_summary.json          -> What contract domains are present?
entity_index.json           -> What contract entities are defined?
relationship_manifest.json  -> How are indexed mission contract entities related?
```

These surfaces are intentionally narrow.

`relationship_manifest.json` does not contain a graph engine, dependency graph, runtime routing table, ground routing table, plugin API or Studio-specific API.

---

## 3. Candidate v1.1.0 Core-owned integration surfaces

The candidate v1.1.0 surfaces are:

```text
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
simulation JSON structured expectation accounting
```

They are Core-owned, but they are not part of the original v1.0.0 stable surface.

They remain candidate until a later reviewed decision promotes selected fields or surfaces.

The candidate integration chain is:

```text
dashboard_summary.json      -> Dashboard-ready aggregation of existing Core facts
scenario_run_index.json     -> Index of Core simulation JSON report runs
coverage_summary.json       -> Limited coverage derived from Core structured outputs
simulation JSON expectations -> Additive structured expectation accounting
```

These surfaces are intentionally narrow.

They are not dashboard backend behavior, Studio API behavior, OpenOBSW/OpenSVF-specific generation, graph behavior, runtime behavior or ground behavior.

---

## 4. Machine-readable validation and evidence reports

These JSON report families are part of the narrow v1.0.0 stable surface:

```text
lint JSON report
simulation JSON report
```

The v1.1.0 structured expectation accounting inside simulation JSON is additive.

The legacy top-level `failed_expectations` compatibility list remains available.

---

## 5. Generated artifacts

Generated runtime-facing artifacts include:

```text
runtime_contract_manifest.json
generated C++17 runtime-facing bindings
generated C++17 host-build smoke files
```

They are not flight software and not a flight ABI guarantee.

Generated ground-facing artifacts include:

```text
ground_contract_manifest.json
generated JSON ground dictionaries
generated CSV ground dictionaries
generated human-reviewable ground Markdown artifacts
```

They are not a ground segment runtime and not a mission control system.

Generated Markdown documentation includes:

```text
generated mission documentation
generated data-flow documentation
```

Generated artifacts remain public preview and disposable unless explicitly promoted later.

---

## 6. Current classification

| Surface | Classification | Source of truth | Notes |
|---|---|---|---|
| `model_summary.json` | Stable v1.0.0 contract | Mission Model | Core-owned domain-level inspection surface. |
| `entity_index.json` | Stable v1.0.0 contract | Mission Model | Core-owned entity-level inspection surface. |
| `relationship_manifest.json` | Stable v1.0.0 for admitted families | Mission Model | Core-owned relationship-level surface. |
| lint JSON report | Stable v1.0.0 contract | Mission Model and lint rules | Machine-readable validation result. |
| simulation JSON report | Stable v1.0.0 contract with additive v1.1 accounting | Mission Model and scenario YAML | Machine-readable scenario evidence. |
| `dashboard_summary.json` | Candidate v1.1.0 surface | Mission Model and Core structured surfaces | Dashboard-ready aggregation of existing Core facts. |
| `scenario_run_index.json` | Candidate v1.1.0 surface | Simulation JSON reports | Index of simulation report runs. |
| `coverage_summary.json` | Candidate v1.1.0 surface | Core structured outputs | Limited coverage derived from Core outputs. |
| generated runtime artifacts | Public preview disposable artifact | Mission Model | Contract-facing artifacts, not flight software. |
| generated ground artifacts | Public preview disposable artifact | Mission Model | Integration artifacts, not ground runtime. |
| generated Markdown docs | Public preview disposable artifact | Mission Model | Human-reviewable docs, not machine contract. |

---

## 7. Compatibility-sensitive surface changes

The following changes are compatibility-sensitive after v1.0.0:

- renaming a documented generated or exported file;
- moving a documented default output path;
- removing a documented top-level JSON field;
- renaming a documented top-level JSON field;
- changing the meaning of a documented field;
- changing a documented `kind` value;
- changing a documented format version field;
- removing explicit boundary flags that downstream tools may inspect;
- changing the answer represented by a Core-owned inspection or candidate integration surface;
- changing generated artifact profile names such as `cpp17` or `generic`;
- changing whether a generated artifact is disposable.

Compatibility-sensitive does not mean forbidden.

It means the change must be explicit, reviewed and documented.

---

## 8. Downstream tool rule

Downstream tools must consume Core-owned structured surfaces when they need Mission Data Contract inspection.

They must not reconstruct Mission Data Contract semantics from:

```text
raw YAML files
generated Markdown documentation
generated runtime bindings
generated ground dictionaries
human-oriented CLI output
UI state
```

The Core loads, validates and owns Mission Data Contract semantics.

Generated and exported surfaces are derived from that Core-owned interpretation.

---

## 9. Current non-goals

This generated surfaces stability classification does not introduce:

```text
new CLI behavior
new Mission Model semantics
relationship graph
dependency graph
plugin execution
plugin discovery
plugin loader
runtime behavior
ground behavior
Studio-specific API
JSON Schema publication
schema migration tooling
```

---

## 10. Relationship to existing reference pages

Detailed structure remains documented in the dedicated references:

```text
Contract Introspection Surface
Entity Index Surface
Relationship Manifest Surface
Dashboard Summary Surface
Scenario Run Index Surface
Coverage Summary Surface
JSON Reports v0.1
Runtime Contract Bindings
Ground Integration Artifacts
```

This page classifies their stability and compatibility expectations after v1.1.0.

---

## 11. Final statement

v1.1.0 is the current project release.

v1.0.0 remains the stable Mission Data Contract baseline.

v1.0.0 stabilizes selected Mission Data Contract surfaces without turning generated artifacts into user-owned source files or runtime implementations.

v1.1.0 consolidates candidate Core-owned integration surfaces without promoting them to the original v1.0.0 stable compatibility class.
