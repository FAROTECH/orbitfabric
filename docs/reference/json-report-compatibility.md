# JSON Report Compatibility

Status: Development preview  
Scope: v0.10.0 JSON report compatibility classification  
Applies to: OrbitFabric JSON reports before v1.0.0

This page classifies OrbitFabric JSON report compatibility expectations on the path toward v1.0.0.

It is a documentation contract. It does not introduce new JSON report fields, new report families, new report schemas, new CLI behavior, new Mission Model semantics, plugin execution, runtime behavior, ground behavior or Studio-specific APIs.

---

## 1. Purpose

OrbitFabric JSON reports are machine-readable outputs used by CI, automated validation workflows, reproducible scenario evidence and downstream inspection tooling.

Before v1.0.0, these reports are still development-preview surfaces. However, documented report families, top-level fields, result values, version fields and Core-owned surface identifiers are compatibility-sensitive.

This document defines how JSON reports should evolve before v1.0.0.

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
| lint JSON report | Public preview | Machine-readable validation result. |
| simulation JSON report | Public preview | Machine-readable scenario evidence. |
| `model_summary.json` | Candidate contract | Core-owned domain-level inspection surface. |
| `entity_index.json` | Candidate contract | Core-owned entity-level inspection surface. |
| `relationship_manifest.json` | Candidate contract | Core-owned relationship-level candidate surface. |
| `runtime_contract_manifest.json` | Public preview generated manifest | Runtime-facing contract manifest, not flight runtime. |
| `ground_contract_manifest.json` | Public preview generated manifest | Ground-facing contract manifest, not ground runtime. |

No JSON report family is classified as a stable v1.0 contract yet.

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

`model_version` identifies the Mission Model version declared by the mission where used.

`orbitfabric_version` identifies the OrbitFabric tool/package version in Core-owned structured surfaces.

`summary_version`, `index_version` and `manifest_version` identify report format versions for their respective Core-owned surfaces.

Changing the meaning of a documented version field is compatibility-sensitive.

---

## 6. Top-level field stability

Documented top-level JSON fields are compatibility-sensitive before v1.0.0.

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

Diagnostic structured fields are compatibility-sensitive before v1.0.0.

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

Core-owned structured surfaces are candidate contract surfaces.

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

## 10. Preferred evolution rules

Before v1.0.0, JSON reports should evolve with these rules.

### 10.1 Prefer additive changes

Prefer adding new fields over renaming or removing existing documented fields.

### 10.2 Preserve field meaning

Do not change the meaning of an existing documented field without an explicit compatibility note.

### 10.3 Preserve machine token stability

Machine-facing tokens such as `tool`, `kind`, `result`, severity values and report version fields should change only deliberately.

### 10.4 Keep human text separate

Human-readable messages, suggestions and terminal output may improve over time, but downstream tools should not parse them as strict machine contracts.

### 10.5 Keep reports derived

JSON reports should remain derived outputs, not editable mission inputs.

---

## 11. Downstream tool rule

Downstream tools may consume JSON reports for automation and inspection.

They should prefer documented structured fields and Core-owned surfaces.

They must not infer hidden semantics from:

```text
field ordering
JSON formatting
whitespace
human-readable message wording
terminal output
private implementation details
undocumented fields
```

For Mission Data Contract inspection, downstream tools should prefer:

```text
model_summary.json
entity_index.json
relationship_manifest.json
```

over parsing raw YAML or generated human-readable documentation.

---

## 12. Current non-goals

This JSON report compatibility classification does not introduce:

```text
new JSON report fields
new report families
new report schemas
new JSON Schema publication
schema migration tooling
new CLI behavior
new Mission Model semantics
new lint diagnostics
new scenario behavior
plugin execution
plugin discovery
plugin loader
relationship graph
dependency graph
runtime behavior
ground behavior
Studio-specific API
stable v1.0 JSON report guarantee
```

---

## 13. Relationship to existing references

This page complements, but does not replace:

```text
JSON Reports v0.1
Versioning Model
Generated Surfaces Stability
Lint Rule Code Stability
CLI Contract v1 Preview
Stability and Compatibility Contract
```

`JSON Reports v0.1` remains the source for the current field-level report documentation.

This page defines how those report surfaces should be treated as compatibility-sensitive before v1.0.0.

---

## 14. v1.0 direction

Before v1.0.0, OrbitFabric should decide which JSON report families and fields become stable.

Likely v1.0 candidates include:

```text
lint report family
simulation report family
model summary surface
entity index surface
relationship manifest surface
runtime contract manifest boundary
ground contract manifest boundary
```

v1.0.0 should stabilize machine-readable Mission Data Contract outputs enough for users and downstream tools to build around them, without turning JSON reports into editable mission sources, runtime state or ground operational databases.
