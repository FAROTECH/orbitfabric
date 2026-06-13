# JSON Report Compatibility

Status: Active v1.1 reference  
Scope: JSON report compatibility classification across stable v1.0.0 and candidate v1.1.0 surfaces  
Applies to: OrbitFabric JSON reports from `v1.0.0 - Stable Mission Data Contract` onward

This page classifies OrbitFabric JSON report compatibility expectations after v1.1.0.

It documents existing stable and candidate report families. It does not introduce new CLI behavior, new Mission Model semantics, plugin execution, runtime behavior, ground behavior or Studio-specific APIs.

---

## 1. Purpose

OrbitFabric JSON reports are machine-readable outputs used by CI, automated validation workflows, reproducible scenario evidence and downstream inspection tooling.

From v1.0.0 onward, selected JSON report families are part of the stable narrow Mission Data Contract surface.

v1.1.0 consolidates additional Core-owned candidate integration surfaces without promoting them to the original v1.0.0 stable compatibility class.

---

## 2. Source of truth

JSON reports are derived outputs.

They are not the source of truth.

The source of truth remains:

```text
Mission Model YAML
scenario YAML
```

JSON reports record OrbitFabric validation or scenario evidence derived from those sources.

Downstream tools may consume JSON reports for automation, but must not treat them as editable mission contract inputs.

---

## 3. Current report family classification

Current JSON report families are classified as follows:

| Report family | Classification | Notes |
|---|---|---|
| lint JSON report | Stable contract | Machine-readable validation result. |
| simulation JSON report | Stable contract with additive v1.1 expectation accounting | Machine-readable scenario evidence. |
| `model_summary.json` | Stable v1.0.0 Core-owned surface | Domain-level inspection surface. |
| `entity_index.json` | Stable v1.0.0 Core-owned surface | Entity-level inspection surface. |
| `relationship_manifest.json` | Stable v1.0.0 for admitted families | Relationship-level surface. |
| `dashboard_summary.json` | Candidate v1.1.0 Core-owned integration surface | Dashboard-ready aggregation of existing Core facts. |
| `scenario_run_index.json` | Candidate v1.1.0 Core-owned integration surface | Index of simulation JSON report runs. |
| `coverage_summary.json` | Candidate v1.1.0 Core-owned integration surface | Limited coverage derived from Core structured outputs. |
| `runtime_contract_manifest.json` | Public preview generated manifest | Runtime-facing contract manifest, not flight runtime. |
| `ground_contract_manifest.json` | Public preview generated manifest | Ground-facing contract manifest, not ground runtime. |

---

## 4. Report family rule

A report family is identified by its documented command, purpose and top-level identity fields.

Examples include:

```text
orbitfabric-lint
orbitfabric-sim
orbitfabric.model_summary
orbitfabric.entity_index
orbitfabric.relationship_manifest
orbitfabric.dashboard_summary
orbitfabric.scenario_run_index
orbitfabric.coverage_summary
```

Renaming a documented report family, changing its purpose or changing the answer it provides is compatibility-sensitive.

For stable v1.0.0 Core-owned inspection surfaces, the intended questions remain:

```text
model_summary.json          -> What contract domains are present?
entity_index.json           -> What contract entities are defined?
relationship_manifest.json  -> How are indexed mission contract entities related?
```

For candidate v1.1.0 integration surfaces, the intended questions are:

```text
dashboard_summary.json      -> What dashboard-ready Core facts are available?
scenario_run_index.json     -> Which Core simulation JSON reports are present?
coverage_summary.json       -> What limited coverage can Core derive from structured outputs?
```

---

## 5. Version field rule

OrbitFabric JSON reports may contain different version fields with different meanings.

Current documented examples include:

```text
version
model_version
orbitfabric_version
summary_version
index_version
manifest_version
dashboard_version
coverage_version
```

These fields must not be treated as interchangeable.

Changing the meaning of a documented version field is compatibility-sensitive.

---

## 6. Top-level field stability

Documented top-level JSON fields for stable report families are compatibility-sensitive after v1.0.0.

Documented top-level JSON fields for candidate v1.1.0 surfaces are candidate compatibility points and must not be changed silently.

Compatibility-sensitive does not mean forbidden.

It means the change must be explicit, reviewed and documented.

---

## 7. Result value stability

Result values are machine-facing fields.

Current documented result values include:

```text
passed
passed_with_warnings
failed
```

for lint reports, and:

```text
passed
failed
```

for simulation reports.

Adding, removing, renaming or changing the meaning of a result value is compatibility-sensitive.

---

## 8. Stable Core-owned surface field stability

The stable Core-owned structured surfaces in v1.0.0 are:

```text
model_summary.json
entity_index.json
relationship_manifest.json
```

Their documented fields, `kind` values, format version fields and boundary flags are compatibility-sensitive.

---

## 9. Candidate Core-owned integration surface posture

The candidate Core-owned integration surfaces consolidated in v1.1.0 are:

```text
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
simulation JSON structured expectation accounting
```

These are Core-owned read-only structured outputs.

They are not part of the original v1.0.0 stable surface.

They may evolve before promotion, but changes must remain explicit and documented because downstream tools are expected to consume them.

---

## 10. Additive evolution rule

Additive JSON evolution is preferred.

Adding an optional field is usually safer than renaming or removing an existing documented field.

The v1.1.0 simulation JSON structured expectation accounting is additive. The legacy top-level `failed_expectations` compatibility list remains available.

---

## 11. Downstream tool rule

Downstream tools should consume structured JSON fields and Core-owned structured surfaces.

When possible, downstream tools should consume:

```text
lint JSON report
simulation JSON report
model_summary.json
entity_index.json
relationship_manifest.json
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
```

They should not parse human-oriented terminal text, plain-text logs, Markdown prose or generated formatting as machine contracts.

---

## 12. Current non-goals

This JSON report compatibility classification does not introduce:

```text
new CLI behavior
new Mission Model semantics
schema migration tooling
JSON Schema publication
runtime behavior
ground behavior
plugin execution
Studio-specific API
OpenOBSW/OpenSVF-specific generation
```

---

## 13. Final statement

v1.1.0 is the current project release.

v1.0.0 remains the stable Mission Data Contract baseline.

v1.0.0 stabilizes selected machine-readable JSON report families and Core-owned structured surfaces.

v1.1.0 consolidates additional candidate Core-owned integration surfaces without making generated manifests, generated runtime bindings, generated ground dictionaries, terminal text, logs or Markdown prose stable machine contracts unless explicitly promoted by a later reviewed decision.
