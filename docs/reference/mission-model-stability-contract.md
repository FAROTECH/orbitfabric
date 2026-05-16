# Mission Model Stability Contract

Status: Development preview  
Scope: v0.10.0 Mission Model compatibility classification  
Applies to: OrbitFabric Mission Model before v1.0.0

This page classifies the OrbitFabric Mission Model surface on the path toward v1.0.0.

It is a documentation contract. It does not introduce new YAML fields, new Mission Model semantics, new validation rules, new generated surfaces, new CLI behavior, plugin execution, runtime behavior, ground behavior or Studio-specific APIs.

---

## 1. Purpose

The Mission Model is the canonical Mission Data Contract in OrbitFabric.

Before v1.0.0, the Mission Model is still a development-preview contract. However, documented files, top-level domain keys, field meanings, controlled values and identifier rules are compatibility-sensitive.

This document defines how the Mission Model should evolve before v1.0.0.

It covers:

- source-of-truth rules;
- required and optional model domains;
- file and top-level key stability;
- field meaning stability;
- identifier stability;
- controlled value stability;
- compatibility-sensitive changes;
- downstream tool expectations;
- non-goals.

The detailed field-level schema remains documented in the dedicated Mission Model and domain reference pages.

---

## 2. Source of truth

The Mission Model YAML is the source of truth for mission data contract semantics.

OrbitFabric Core loads, validates, lints, documents, simulates and exports derived surfaces from that Mission Model.

Generated artifacts and exported surfaces are derived outputs.

They must not become independent sources of mission semantics.

Downstream tools must not reconstruct Mission Data Contract semantics by independently interpreting raw YAML outside OrbitFabric Core.

They should consume Core-owned structured surfaces such as:

```text
model_summary.json
entity_index.json
relationship_manifest.json
```

---

## 3. Current classification

Current Mission Model surface classification before v1.0.0:

| Surface | Classification | Notes |
|---|---|---|
| Mission Model directory layout | Candidate contract | Current multi-file structure is compatibility-sensitive. |
| required core YAML files | Candidate contract | Core v0.1 files are required for the current Mission Model baseline. |
| optional extension YAML files | Public preview | Payload, data product, contact/downlink and commandability domains. |
| top-level domain keys | Candidate contract | Each YAML file has one expected top-level domain key. |
| documented field names | Candidate contract | Field names should change only deliberately. |
| documented field meanings | Candidate contract | Semantic meaning is compatibility-sensitive. |
| controlled values | Public preview, candidate where documented | Values such as severities, risks and priorities affect validation and generated outputs. |
| identifier format rules | Candidate contract | Dotted identifiers are central to cross-references. |
| raw YAML ordering | Not a semantic contract | Ordering should not carry hidden semantics unless explicitly documented. |
| comments and formatting | Not a semantic contract | Human formatting is not contract semantics. |
| internal Pydantic model layout | Internal implementation detail | Not a public compatibility surface unless explicitly documented. |

No Mission Model surface is classified as a stable v1.0 contract yet.

---

## 4. Current domain classes

The current Mission Model is composed of core domains and extension domains.

### 4.1 Core domains

Current core domains include:

```text
spacecraft
subsystems
modes
mode_transitions
telemetry
commands
events
faults
packets
policies
```

These domains define the core Mission Data Contract baseline.

### 4.2 Extension domains

Current extension domains include:

```text
payloads
data_products
contacts
commandability
```

These domains extend the Mission Data Chain without turning OrbitFabric into payload firmware, onboard storage runtime, contact scheduling software, command authorization runtime or autonomous flight software.

---

## 5. File and top-level key stability

The current multi-file Mission Model layout is compatibility-sensitive.

Changing a documented YAML file name, removing a documented file, renaming a top-level key or changing whether a domain is required or optional can affect users, examples, CI workflows and downstream tools.

Such changes are allowed before v1.0.0 only when explicit, reviewed and documented.

A new optional domain may be added before v1.0.0 if it is clearly documented and does not silently alter existing domain semantics.

---

## 6. Field meaning stability

A documented field has two compatibility-sensitive dimensions:

```text
field name
field meaning
```

Renaming a documented field is compatibility-sensitive.

Changing the meaning of a documented field is compatibility-sensitive even if the field name stays the same.

For example, a field currently describing a declared relationship or expected effect should not silently become an execution instruction, runtime action or ground automation rule.

OrbitFabric fields describe Mission Data Contract intent unless a future reviewed design explicitly says otherwise.

---

## 7. Identifier stability

OrbitFabric uses dotted identifiers as stable cross-reference anchors.

Identifier stability matters because identifiers are used by:

- cross-reference validation;
- lint diagnostics;
- generated documentation;
- scenario steps and expectations;
- generated runtime-facing bindings;
- generated ground-facing artifacts;
- Core-owned structured surfaces;
- downstream tools.

Changing identifier format rules, uniqueness rules or reference rules is compatibility-sensitive.

Identifiers should not gain hidden semantics from naming prefixes unless that meaning is explicitly modeled and documented.

---

## 8. Controlled value stability

Controlled values include, for example:

```text
severity values
criticality values
risk values
downlink priority values
persistence policy values
telemetry type values
packet type values
```

Adding, removing, renaming or changing the meaning of a controlled value is compatibility-sensitive.

Changing controlled values can affect validation, generated documentation, scenario evidence, generated artifacts and downstream tooling.

Controlled values should remain explicit and documented.

---

## 9. Compatibility-sensitive Mission Model changes

The following changes are compatibility-sensitive before v1.0.0:

- removing a documented YAML file;
- renaming a documented YAML file;
- changing a documented top-level key;
- changing whether a documented domain is required or optional;
- removing a documented field;
- renaming a documented field;
- changing the meaning of a documented field;
- changing a documented field type;
- changing documented identifier rules;
- changing documented uniqueness rules;
- changing documented reference rules;
- changing controlled value sets;
- changing controlled value meanings;
- changing scenario linkage expectations;
- changing how a modeled intent is interpreted by generated surfaces;
- changing whether a field is treated as declarative intent or execution behavior.

Compatibility-sensitive does not mean forbidden.

It means the change must be explicit, reviewed and documented.

---

## 10. Preferred evolution rules

Before v1.0.0, Mission Model evolution should follow these rules.

### 10.1 Prefer additive changes

Prefer adding optional fields or optional domains over renaming or removing existing documented fields.

### 10.2 Keep semantics explicit

Do not introduce hidden semantics through naming conventions, ordering, comments, file placement or downstream UI state.

### 10.3 Preserve declarative intent

Mission Model fields should describe mission data contract intent.

They should not silently become runtime execution instructions, ground automation behavior or plugin behavior.

### 10.4 Keep validation aligned

When a Mission Model rule changes, the reference documentation, lint behavior and JSON report expectations should remain aligned.

### 10.5 Keep downstream tools behind Core-owned surfaces

Downstream tools should consume Core-owned structured surfaces rather than becoming independent Mission Model interpreters.

---

## 11. What is not a Mission Model compatibility promise

The following are not Mission Model compatibility promises before v1.0.0:

- internal Python class names;
- internal loader function layout;
- internal Pydantic model organization;
- test helper layout;
- YAML formatting style;
- YAML key ordering unless explicitly documented;
- comments inside example YAML files;
- human-oriented generated Markdown wording;
- terminal text formatting;
- downstream UI layout.

These may still require review, but they do not define Mission Data Contract semantics.

---

## 12. Downstream tool rule

Downstream tools must not become a second source of Mission Model semantics.

They must not infer hidden Mission Data Contract meaning from:

```text
raw YAML parsing outside Core
generated Markdown documentation
generated runtime bindings
generated ground dictionaries
human-oriented CLI output
UI state
identifier prefixes not documented as semantic fields
YAML ordering
comments
```

The supported downstream inspection chain remains:

```text
model_summary.json
entity_index.json
relationship_manifest.json
```

---

## 13. Current non-goals

This Mission Model stability contract does not introduce:

```text
new YAML fields
new Mission Model semantics
new model domains
new controlled values
new lint rules
new JSON report fields
new CLI behavior
schema migration tooling
JSON Schema publication
relationship graph
dependency graph
plugin execution
plugin discovery
plugin loader
runtime behavior
ground behavior
Studio-specific API
stable v1.0 Mission Model guarantee
```

---

## 14. Relationship to existing references

This page complements, but does not replace:

```text
Mission Model v0.1
Payload Contract Model
Data Product Contract Model
Contact and Downlink Contract Model
Commandability and Autonomy Contract Model
Stability and Compatibility Contract
Generated Surfaces Stability
Lint Rule Code Stability
```

The dedicated reference pages remain the source for field-level schema documentation.

This page defines how those documented Mission Model surfaces should be treated as compatibility-sensitive before v1.0.0.

---

## 15. v1.0 direction

Before v1.0.0, OrbitFabric should decide which Mission Model domains, fields, controlled values and identifier rules become stable.

Likely v1.0 candidates include:

```text
core Mission Model directory layout
core domain top-level keys
core identifier rules
core reference rules
core telemetry, command, event, fault, mode and packet fields
payload contract fields
data product contract fields
contact and downlink contract fields
commandability and autonomy contract fields
scenario linkage expectations
```

v1.0.0 should stabilize the Mission Data Contract enough for users and downstream tools to build around it, without turning the Mission Model into flight software, ground software, a simulator runtime, a visual modeling database or a plugin execution interface.
