# Post-v1 Candidate Integration Surfaces

Status: Active reference for v1.1.0 candidate surfaces and later additive candidate development  
Scope: candidate Core-owned integration and inspection surfaces after `v1.0.0 - Stable Mission Data Contract`  
Applies to: OrbitFabric Core `v1.1.0 - Candidate Integration Surface Consolidation` and later, until any future promotion decision

This page is the public index for candidate Core-owned surfaces introduced after the v1.0.0 stable Mission Data Contract release.

It distinguishes the surfaces actually consolidated in v1.1.0 from additive development implemented later on `main`.

It exists to keep the boundary explicit:

```text
Core is the contract authority.
Downstream tools are read-only consumers.
Candidate surfaces are not automatically stable surfaces.
Published release contents and unreleased main development are distinct.
```

---

## 1. Current stable v1.0.0 Core-owned structured surfaces

The original v1.0.0 stable Core-owned structured surface chain remains:

```text
model_summary.json
entity_index.json
relationship_manifest.json
```

Those surfaces are derived from the validated Mission Model and protected by selected golden signatures.

The Mission Model remains the source of truth.

The original admitted v1 Relationship Manifest families remain compatibility commitments. Later additive relationship families do not rename, remove or change their meaning.

---

## 2. v1.1.0 candidate Core-owned integration surfaces

The candidate post-v1 surfaces consolidated in v1.1.0 are:

```text
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
simulation JSON structured expectation accounting
```

They are Core-owned because Core defines their fields, computes their values and declares their boundary flags.

They are candidate because they were introduced after v1.0.0 and have not yet been promoted to a stronger compatibility class.

---

## 3. Current unreleased candidate additions

Current `main` contains additional additive development after the v1.1.0 release:

```text
mission_snapshot.json
seven explicit FDIR relationship families in relationship_manifest.json
```

These additions are implemented and documented, but they are not retroactively part of v1.1.0.

### Mission Snapshot

`mission_snapshot.json` is a Core-owned read-only inspection surface that answers:

```text
What complete Mission Model did OrbitFabric Core actually load?
```

It serializes the complete loaded `MissionModel` in a versioned envelope and provides structured load diagnostics.

It does not:

```text
replace the Mission Model as source of truth
expose a YAML AST
expose source editing semantics
expose a partial semantic model after structural load failure
introduce a Studio-specific API
introduce plugin execution
introduce runtime behavior
introduce ground behavior
```

### Additive FDIR Relationship Manifest families

Current `main` also adds seven explicit FDIR-oriented relationship families:

```text
autonomous_action_triggered_by_fault
autonomous_action_uses_command_source
fault_observes_telemetry
fault_recovery_dispatches_command
fault_recovery_targets_mode
recovery_intent_includes_command
recovery_intent_targets_mode
```

Each family is derived deterministically from an explicit loaded Mission Model field.

The extension does not infer relationships, create synthetic nodes or turn the manifest into a relationship graph.

Compatible downstream consumers should consume relationship types they support and safely tolerate unknown additive types rather than treating the relationship-type set as permanently closed.

---

## 4. Surface inventory

| Surface | Release posture | Status | Purpose | Source of truth |
|---|---|---|---|---|
| `model_summary.json` | v1.0 stable | Stable | Domain/count summary | Mission Model |
| `entity_index.json` | v1.0 stable | Stable | Indexed entity inventory | Mission Model |
| `relationship_manifest.json` original families | v1.0 stable | Stable | Explicit relationship inventory | Mission Model |
| `dashboard_summary.json` | v1.1.0 | Candidate | Dashboard-ready aggregation of existing Core facts | Mission Model and Core structured surfaces |
| `scenario_run_index.json` | v1.1.0 | Candidate | Index simulation JSON report runs | Simulation JSON reports |
| `coverage_summary.json` | v1.1.0 | Candidate | Limited coverage metrics from Core structured outputs | Entity index, relationship manifest, scenario run index and referenced simulation JSON reports |
| Simulation JSON `expectations` object | v1.1.0 | Additive candidate extension | Structured passed/failed expectation accounting | Scenario execution evidence |
| `mission_snapshot.json` | Unreleased current `main` | Candidate | Complete loaded Mission Model inspection | Loaded Mission Model and structural load diagnostics |
| Relationship Manifest FDIR families | Unreleased current `main` | Additive compatibility extension | Additional explicit FDIR relationships | Explicit Mission Model fields |

---

## 5. Ownership boundary

The ownership boundary is:

```text
Core defines structured semantics.
Core computes and emits structured reports.
Studio and other downstream tools consume, navigate and render those reports.
Downstream tools do not invent private Mission Data Contract semantics.
```

Downstream tools may derive UI navigation state from these reports.

Downstream tools must not compute private substitutes for:

```text
coverage
contract health
contract completeness
relationship graph behavior
dependency graph behavior
runtime behavior
ground behavior
formal verification
```

If a value is not emitted by Core, downstream tools should display one of:

```text
Unavailable
Requires Core output
Not defined by Core
```

The Mission Snapshot exists specifically so downstream consumers can inspect the complete loaded model without reparsing OrbitFabric YAML or reconstructing domain semantics privately.

---

## 6. Generated artifact default paths

Mission-based CLI commands resolve omitted generated artifact paths under the mission workspace where that behavior is defined by the command.

For example:

```bash
orbitfabric export dashboard-summary examples/demo-3u/mission/
```

writes by default to:

```text
examples/demo-3u/generated/reports/dashboard_summary.json
```

and:

```bash
orbitfabric gen ground examples/demo-3u/mission/
```

writes by default to:

```text
examples/demo-3u/generated/ground/generic/
```

Explicit user-provided paths remain explicit.

For example:

```bash
orbitfabric gen docs examples/demo-3u/mission/ --output-dir custom/docs
```

continues to write to:

```text
custom/docs
```

relative to the current working directory unless the user provides an absolute path.

---

## 7. Compatibility posture

The post-v1 candidate surfaces do not change the original v1.0.0 stable Mission Data Contract.

They do not add, remove or rename Mission Model fields, model domains, controlled values, reference rules or scenario expectation syntax unless a future release explicitly says otherwise.

Structured expectation accounting is additive inside simulation JSON reports and preserves the legacy top-level `failed_expectations` array.

The Mission Snapshot is additive and candidate. Consumers must check its documented kind and surface-format version and must not assume that `orbitfabric_version` alone defines snapshot compatibility.

The additive FDIR relationship families preserve the original v1 relationship-family contract. Unknown additive relationship types must not be assigned guessed semantics.

Future promotion of any candidate field or surface requires a separate reviewed decision and, where appropriate, selected regression or golden-signature protection.

---

## 8. Explicit non-goals

The post-v1 candidate integration and inspection surfaces do not introduce:

```text
Projection Profiles implementation
OSRA/SAVOIR implementation
OpenOBSW/OpenSVF-specific generation
Studio-specific APIs
mission health scoring
contract health scoring unless separately implemented by Core
model completeness scoring
contract completeness scoring unless separately implemented by Core
flight readiness scoring
runtime telemetry behavior
ground execution behavior
relationship graph behavior
dependency graph behavior
plugin discovery
plugin loading
plugin execution
CCSDS/PUS/CFDP framing
transport behavior
flight software framework behavior
ground segment behavior
```

---

## 9. Release implication

Core v1.1.0 consolidates the dashboard summary, scenario run index, coverage summary and simulation structured expectation accounting surfaces.

Current `main` additionally implements the Mission Snapshot and additive FDIR relationship families.

A future minor-release decision must explicitly determine how those newer additions are classified. Their presence on `main` does not automatically promote them to a stable compatibility class.

The release discipline must continue to communicate:

```text
what is stable
what is candidate
what is released
what is unreleased
what is Core-owned
what is downstream-consumer-owned
what remains explicitly out of scope
```

---

## 10. Final statement

The post-v1 candidate integration and inspection surfaces are valid Core surfaces because they keep Mission Data Contract semantics inside Core.

They are deliberately narrow:

```text
emit structured evidence
expose the loaded contract without semantic duplication
preserve provenance
declare boundaries
allow reviewed additive relationship types
avoid downstream semantic invention
```
