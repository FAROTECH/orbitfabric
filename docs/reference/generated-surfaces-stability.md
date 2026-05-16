# Generated Surfaces Stability

Status: Development preview  
Scope: v0.10.0 generated surface compatibility classification  
Applies to: OrbitFabric generated and exported surfaces before v1.0.0

This page classifies OrbitFabric generated and exported surfaces on the path toward v1.0.0.

It is a documentation contract. It does not introduce new generated surfaces, new report fields, new CLI behavior, new Mission Model semantics, plugin execution, runtime behavior, ground behavior or Studio-specific APIs.

---

## 1. Purpose

OrbitFabric generates and exports several surfaces derived from the validated Mission Model.

This document defines how those surfaces should be treated before v1.0.0:

- which surfaces are Core-owned inspection surfaces;
- which surfaces are generated artifact packages;
- which surfaces are candidate contract surfaces;
- which surfaces are disposable generated outputs;
- which changes are compatibility-sensitive;
- which assumptions downstream tools must not make.

The Mission Model remains the source of truth.

---

## 2. Surface categories

OrbitFabric currently distinguishes these generated or exported surface categories.

### 2.1 Core-owned structured inspection surfaces

These are machine-readable, read-only surfaces exported by OrbitFabric Core for downstream inspection:

```text
model_summary.json
entity_index.json
relationship_manifest.json
```

They exist to prevent downstream tools from reconstructing Mission Data Contract semantics from raw YAML, generated files, textual CLI output or UI state.

### 2.2 Machine-readable validation and evidence reports

These are JSON reports produced by validation or scenario execution workflows:

```text
lint JSON report
simulation JSON report
```

They are intended for CI, automated checks and reproducible evidence.

### 2.3 Generated runtime-facing artifacts

These are generated contract-facing artifacts intended to help runtime integration work:

```text
runtime_contract_manifest.json
generated C++17 runtime-facing bindings
generated C++17 host-build smoke files
```

They are not flight software.

They are not a flight ABI guarantee.

### 2.4 Generated ground-facing artifacts

These are generated contract-facing artifacts intended to help ground integration work:

```text
ground_contract_manifest.json
generated JSON ground dictionaries
generated CSV ground dictionaries
generated human-reviewable ground Markdown artifacts
```

They are not a ground segment runtime.

They are not a mission control system.

### 2.5 Generated Markdown documentation

These are generated human-reviewable documentation artifacts:

```text
generated mission documentation
generated data-flow documentation
```

They are useful for review and communication.

They are not the source of truth.

---

## 3. Current classification

The current pre-v1.0 classification is:

| Surface | Classification | Source of truth | Notes |
|---|---|---|---|
| `model_summary.json` | Candidate contract | Mission Model | Core-owned domain-level inspection surface. |
| `entity_index.json` | Candidate contract | Mission Model | Core-owned entity-level inspection surface. |
| `relationship_manifest.json` | Candidate contract | Mission Model | Core-owned relationship-level candidate surface. |
| lint JSON report | Public preview | Mission Model and lint rules | Machine-readable validation result. |
| simulation JSON report | Public preview | Mission Model and scenario YAML | Machine-readable scenario evidence. |
| `runtime_contract_manifest.json` | Public preview generated artifact | Mission Model | Runtime-facing contract manifest, not flight runtime. |
| generated C++17 runtime bindings | Public preview disposable artifact | Mission Model | Regenerable contract-facing bindings, not flight software. |
| `ground_contract_manifest.json` | Public preview generated artifact | Mission Model | Ground-facing contract manifest, not ground runtime. |
| generated ground dictionaries | Public preview disposable artifact | Mission Model | Integration dictionaries, not live decoder or database behavior. |
| generated Markdown docs | Public preview disposable artifact | Mission Model | Human-reviewable docs, not machine contract. |

No generated or exported surface is currently classified as a stable v1.0 contract.

---

## 4. Core-owned inspection surface chain

The current Core-owned inspection chain is:

```text
model_summary.json          -> What contract domains are present?
entity_index.json           -> What contract entities are defined?
relationship_manifest.json  -> How are indexed mission contract entities related?
```

These surfaces are intentionally narrow.

`model_summary.json` does not contain entity records.

`entity_index.json` does not contain relationship records.

`relationship_manifest.json` does not contain a graph engine, dependency graph, runtime routing table, ground routing table, plugin API or Studio-specific API.

---

## 5. Compatibility-sensitive surface changes

The following changes are compatibility-sensitive before v1.0.0:

- renaming a documented generated or exported file;
- moving a documented default output path;
- removing a documented top-level JSON field;
- renaming a documented top-level JSON field;
- changing the meaning of a documented field;
- changing a documented `kind` value;
- changing a documented format version field such as `summary_version`, `index_version` or `manifest_version`;
- removing explicit boundary flags that downstream tools may inspect;
- changing the answer represented by a Core-owned inspection surface;
- changing generated artifact profile names such as `cpp17` or `generic`;
- changing generated manifest boundary claims;
- changing whether a generated artifact is disposable.

Compatibility-sensitive does not mean forbidden.

It means the change must be explicit, reviewed and documented.

---

## 6. Preferred evolution rules

Before v1.0.0, generated and exported surfaces should evolve with these rules.

### 6.1 Prefer additive changes

When possible, add fields instead of renaming or removing existing documented fields.

### 6.2 Keep boundary flags explicit

Boundary flags are part of OrbitFabric's architectural safety model.

They should remain explicit when a generated or exported surface might otherwise be misread as runtime behavior, ground behavior, plugin behavior or Studio-specific behavior.

### 6.3 Keep generated artifacts disposable

Generated artifacts should remain reproducible from the Mission Model.

User-owned implementation should live outside generated output directories unless a future reviewed design explicitly changes that rule.

### 6.4 Keep Core-owned surfaces read-only

Core-owned inspection surfaces are exported for inspection.

Downstream tools may consume them, but must not write back mission semantics through them.

### 6.5 Keep machine-readable surfaces separate from terminal text

Downstream tools should consume documented JSON outputs and generated manifests.

They should not parse human-oriented terminal output.

---

## 7. Downstream tool rule

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

## 8. Current non-goals

This generated surfaces stability classification does not introduce:

```text
new generated surfaces
new JSON report fields
new manifest fields
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
v1.0 compatibility guarantee
```

---

## 9. Relationship to existing reference pages

This page does not replace the existing surface reference pages.

Detailed structure remains documented in the dedicated references:

```text
Contract Introspection Surface
Entity Index Surface
Relationship Manifest Surface
JSON Reports v0.1
Runtime Contract Bindings
Ground Integration Artifacts
```

This page only classifies their stability and compatibility expectations before v1.0.0.

---

## 10. v1.0 direction

Before v1.0.0, OrbitFabric should decide which generated and exported surfaces become stable contract surfaces.

Likely v1.0 candidates include:

```text
model_summary.json
entity_index.json
relationship_manifest.json
lint JSON report family
simulation JSON report family
runtime contract manifest boundary
ground contract manifest boundary
```

v1.0.0 should stabilize the Mission Data Contract surfaces without turning generated artifacts into user-owned source files or runtime implementations.
