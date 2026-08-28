# JSON Report Compatibility

Status: Active v1.x reference through v1.2.0  
Scope: compatibility classification for machine-readable Core reports and structured surfaces  
Applies to: OrbitFabric JSON outputs from v1.0.0 onward

This page defines compatibility expectations for OrbitFabric machine-readable outputs.

It documents existing behavior. It does not introduce new CLI behavior, Mission Model semantics, plugin execution, runtime behavior, ground behavior or Studio-specific APIs.

## 1. Source of truth

JSON reports and structured surfaces are derived outputs.

The Mission Model remains the semantic source of truth. Scenario YAML remains the scenario-evidence input.

Downstream tools may consume JSON surfaces for automation and inspection, but they must not treat those surfaces as editable replacements for the Mission Model.

## 2. Current classification

| Report or surface | Classification | Notes |
|---|---|---|
| lint JSON report | Stable | Machine-readable validation result. |
| simulation JSON report | Stable | Machine-readable scenario evidence. |
| simulation JSON `expectations` | Candidate additive v1.1 extension | Structured expectation accounting. |
| `model_summary.json` | Stable | Domain-level Core inspection. |
| `entity_index.json` | Stable | Entity-level Core inspection. |
| `relationship_manifest.json` original v1 families | Stable | Original admitted relationship families. |
| Relationship Manifest v1.2 FDIR families | Additive stable-compatible | Explicit additional relationship families. |
| `mission_snapshot.json` | Stable from v1.2.0 | Complete loaded Mission Model inspection boundary. |
| Core Integration Input Set | Stable from v1.2.0 | Coherent external integration input boundary. |
| `dashboard_summary.json` | Candidate | v1.1 Core inspection surface. |
| `scenario_run_index.json` | Candidate | v1.1 simulation report index. |
| `coverage_summary.json` | Candidate | v1.1 limited coverage surface. |
| `runtime_contract_manifest.json` | Public preview | Generated runtime-facing contract manifest. |
| `ground_contract_manifest.json` | Public preview | Generated ground-facing contract manifest. |

## 3. Report identity

A machine-readable family is identified by its documented purpose and identity fields, not by file naming convention alone.

Representative identities include:

```text
orbitfabric-lint
orbitfabric-sim
orbitfabric.model_summary
orbitfabric.entity_index
orbitfabric.relationship_manifest
orbitfabric.mission_snapshot
orbitfabric.integration_input_set
orbitfabric.dashboard_summary
orbitfabric.scenario_run_index
orbitfabric.coverage_summary
```

Renaming a stable documented identity or changing the question a stable surface answers is compatibility-sensitive.

## 4. Version fields

Version fields are not interchangeable.

Representative fields include:

```text
version
model_version
orbitfabric_version
summary_version
index_version
manifest_version
snapshot_version
input_set_version
dashboard_version
coverage_version
```

`version` may identify the producing OrbitFabric package. `model_version` identifies the mission contract version declared by a mission. Surface-specific fields identify report formats.

A format identifier does not automatically encode release maturity.

The stable v1.2 Mission Snapshot and Core Integration Input Set intentionally retain:

```text
snapshot_version = 0.1-candidate
input_set_version = 0.1-candidate
```

Changing those tokens only to reflect maturity would create needless incompatibility in an already reference-proven producer and consumer chain.

## 5. Stable top-level fields

Documented top-level fields for stable report families are compatibility-sensitive.

Removing, renaming or redefining them requires explicit compatibility review.

Adding an optional field may be compatible when the relevant contract permits additive evolution and existing meaning is preserved.

## 6. Result value stability

Machine-facing result tokens are compatibility-sensitive.

Current lint values include:

```text
passed
passed_with_warnings
failed
```

Current simulation values include:

```text
passed
failed
```

Adding, removing, renaming or changing the meaning of result values requires explicit review.

## 7. Relationship Manifest evolution

The original v1 admitted relationship families remain stable compatibility commitments.

v1.2 admits seven additive stable-compatible FDIR families:

```text
autonomous_action_triggered_by_fault
autonomous_action_uses_command_source
fault_observes_telemetry
fault_recovery_dispatches_command
fault_recovery_targets_mode
recovery_intent_includes_command
recovery_intent_targets_mode
```

A later minor release may add another relationship type only through an explicit compatibility decision when the type is narrow, deterministic and derived from an explicit loaded Mission Model field.

Consumers of relationship collections must consume the types they understand and safely preserve or ignore unknown additive types according to their use case. They must never guess unknown semantics from names or endpoints.

A consumer that intentionally requires a closed relationship-type set must pin that expectation to the release contract it supports.

## 8. Mission Snapshot compatibility

Mission Snapshot is stable from v1.2 for its documented envelope, structural-load failure behavior, boundary flags and role as the faithful serialization of the complete loaded Mission Model.

The stable promise does not freeze the entire nested `model` payload byte-for-byte. That payload follows the Mission Model Stability Contract and may evolve additively where the Mission Model rules permit it.

Consumers must not use a failed or incompatible Snapshot as permission to reconstruct a partial Mission Model from raw YAML.

## 9. Core Integration Input Set compatibility

The Core Integration Input Set is stable from v1.2 as the supported Core-to-integration input boundary.

Compatibility-sensitive semantics include:

```text
required and companion role classification
surface availability records
load and lint state separation
surface identity and format version
per-surface SHA-256
RFC 8785/JCS input_set_sha256
manifest-last coherence
required-surface compatibility gating
Core diagnostic ownership
no raw-YAML semantic fallback
```

An incompatible required surface blocks semantic projection.

The input set does not make Projection Profile, Integration Result or Integration Package contracts stable Core surfaces.

## 10. Candidate v1.1 surfaces

The following remain candidate:

```text
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
simulation JSON structured expectation accounting
```

They are Core-owned read-only outputs, but they are not silently promoted by v1.2.

Their changes must be explicit because downstream tools may already consume them, even though their compatibility commitment is weaker than the stable v1 surface.

## 11. Additive evolution

Additive JSON evolution is preferred.

A compatible additive change normally preserves:

```text
existing documented fields
existing result tokens
existing identity meaning
existing relationship meaning
existing required-role semantics
existing failure-state distinctions
```

New optional fields or new explicitly admitted typed records may be compatible when the underlying contract permits them.

## 12. Downstream consumer rule

Downstream tools should consume structured Core surfaces such as:

```text
lint JSON report
simulation JSON report
model_summary.json
entity_index.json
relationship_manifest.json
mission_snapshot.json
integration_input_manifest.json
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
```

They must not reconstruct Core semantics from:

```text
terminal text
plain-text logs
Markdown prose
file names
timestamps
ID naming conventions
UI state
raw YAML when the integration contract requires Core-owned surfaces
```

## 13. Current non-goals

This compatibility classification does not introduce:

```text
new Mission Model semantics
schema migration tooling
JSON Schema publication for Core reports
runtime behavior
ground behavior
plugin execution
Studio-specific semantic authority
OpenOBSW/OpenSVF-specific Core generation
```

## 14. Final statement

v1.2.0 extends the stable Core machine-readable boundary with Mission Snapshot and the coherent Integration Input Set while preserving the v1.0 stable report families and the v1.1 candidate inspection surfaces.

Every compatibility decision remains explicit. No consumer should infer maturity from a format token alone or infer missing semantics from unstructured data.
