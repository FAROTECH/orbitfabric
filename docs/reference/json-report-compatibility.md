# JSON Report Compatibility

Status: Active v1.0 contract  
Scope: JSON report compatibility classification  
Applies to: OrbitFabric JSON reports from `v1.0.0 - Stable Mission Data Contract` onward

This page classifies OrbitFabric JSON report compatibility expectations after v1.0.0.

It is a documentation contract. It does not introduce new JSON report fields, new report families, new report schemas, new CLI behavior, new Mission Model semantics, plugin execution, runtime behavior, ground behavior or Studio-specific APIs.

---

## 1. Purpose

OrbitFabric JSON reports are machine-readable outputs used by CI, automated validation workflows, reproducible scenario evidence and downstream inspection tooling.

From v1.0.0 onward, selected JSON report families are part of the stable narrow Mission Data Contract surface.

This document defines how JSON reports should evolve after v1.0.0.

It covers:

- report family classification;
- top-level field stability;
- version field meaning;
- result value stability;
- diagnostic field stability;
- Core-owned structured surface stability;
- additive evolution rules;
- downstream tooling expectations;
- non-goals.

The detailed field-level report structures remain documented in `JSON Reports v0.1` and the dedicated surface reference pages.

---

## 2. Source of truth

JSON reports are derived outputs.

They are not the source of truth.

The source of truth remains:

```text
Mission Model YAML
scenario YAML
```

JSON reports record OrbitFabric's interpretation, validation or scenario evidence derived from those sources.

Downstream tools may consume JSON reports for automation, but must not treat them as editable mission contract inputs.

---

## 3. Current report family classification

Current JSON report families are classified as follows:

| Report family | Classification | Notes |
|---|---|---|
| lint JSON report | Stable contract | Machine-readable validation result. |
| simulation JSON report | Stable contract | Machine-readable scenario evidence. |
| `model_summary.json` | Stable contract | Core-owned domain-level inspection surface. |
| `entity_index.json` | Stable contract | Core-owned entity-level inspection surface. |
| `relationship_manifest.json` | Stable contract for admitted families | Core-owned relationship-level surface. |
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
```

Renaming a documented report family, changing its purpose or changing the answer it provides is compatibility-sensitive.

For Core-owned inspection surfaces, the intended questions remain:

```text
model_summary.json          -> What contract domains are present?
entity_index.json           -> What contract entities are defined?
relationship_manifest.json  -> How are indexed mission contract entities related?
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
```

These fields must not be treated as interchangeable.

`version` identifies the OrbitFabric tool/package version where used.

`model_version` identifies the Mission Model version declared by a mission where used.

`orbitfabric_version` identifies the OrbitFabric tool/package version in Core-owned structured surfaces.

`summary_version`, `index_version` and `manifest_version` identify report format versions for their respective Core-owned surfaces.

Changing the meaning of a documented version field is compatibility-sensitive.

---

## 6. Top-level field stability

Documented top-level JSON fields for stable report families are compatibility-sensitive after v1.0.0.

The following changes are compatibility-sensitive:

- removing a documented top-level field;
- renaming a documented top-level field;
- changing the meaning of a documented top-level field;
- changing a documented field from required to optional without explanation;
- changing a documented field type;
- changing a documented object into an array or an array into an object;
- changing the report family identified by a `tool` or `kind` value.

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

Result values should remain lowercase machine-readable tokens unless a future reviewed design explicitly changes that rule.

---

## 8. Diagnostic field stability

Lint JSON reports expose diagnostic information.

Diagnostic structured fields are compatibility-sensitive after v1.0.0.

Examples include:

```text
severity
code
file
domain
object_id
message
suggestion
```

Downstream tools should rely on structured fields, especially `severity`, `code`, `file`, `domain` and `object_id`.

They must not rely on parsing human-readable message text or terminal formatting.

Diagnostic code evolution is classified separately in `Lint Rule Code Stability`.

---

## 9. Core-owned surface field stability

Core-owned structured surfaces are stable contract surfaces in v1.0.0.

These include:

```text
model_summary.json
entity_index.json
relationship_manifest.json
```

Their documented fields, `kind` values, format version fields and boundary flags are compatibility-sensitive.

Boundary flags are part of OrbitFabric's architectural safety model.

They should remain explicit where they prevent misinterpretation as runtime behavior, ground behavior, graph behavior, plugin behavior or Studio-specific behavior.

---

## 10. Additive evolution rule

Additive JSON evolution is preferred.

Adding an optional field is usually safer than renaming or removing an existing documented field.

However, additive fields can still be compatibility-sensitive if they change validation behavior, pass/fail interpretation, downstream expectations or the meaning of existing fields.

---

## 11. Downstream tool rule

Downstream tools should consume structured JSON fields and Core-owned structured surfaces.

They should not parse:

```text
human-oriented terminal text
plain-text logs
Markdown prose
generated C++ formatting
generated CSV formatting
```

When possible, downstream tools should consume:

```text
lint JSON report
simulation JSON report
model_summary.json
entity_index.json
relationship_manifest.json
```

---

## 12. Current non-goals

This JSON report compatibility classification does not introduce:

```text
new JSON report fields
new report families
new report schemas
new CLI behavior
new Mission Model semantics
schema migration tooling
JSON Schema publication
runtime behavior
ground behavior
plugin execution
Studio-specific API
```

---

## 13. Final statement

v1.0.0 stabilizes selected machine-readable JSON report families and Core-owned structured surfaces.

It does not make generated manifests, generated runtime bindings, generated ground dictionaries, terminal text, logs or Markdown prose stable machine contracts unless explicitly promoted by a later reviewed decision.
