# Post-v1 Integration Surface Classification

Status: Active compatibility inventory through v1.2.0  
Scope: Core-owned structured surfaces introduced after `v1.0.0 - Stable Mission Data Contract`

This page preserves the classification history of post-v1 Core-owned surfaces and records the v1.2 promotion decision.

Candidate surfaces are not automatically stable. Promotion requires an explicit reviewed compatibility decision and appropriate regression protection.

---

## 1. Original v1.0 stable Core-owned surfaces

```text
model_summary.json
entity_index.json
relationship_manifest.json for original admitted families
```

These remain stable. The Mission Model remains the source of truth.

---

## 2. v1.1.0 candidate surfaces

The following were consolidated as candidate Core-owned surfaces in v1.1.0 and remain candidate after v1.2.0:

```text
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
simulation JSON structured expectation accounting
```

They support downstream inspection but are not silently promoted by the v1.2 Core Integration Input decision.

---

## 3. v1.2.0 stable additions

### Mission Snapshot

`mission_snapshot.json` is stable from v1.2.0 for its documented envelope, load-failure behavior, boundary semantics and complete-loaded-model role.

Its format identifier remains `0.1-candidate` to preserve compatibility with the reference-proven producer/consumer chain.

The complete `model` payload follows Mission Model compatibility rules rather than a byte-for-byte Snapshot freeze.

### Core Integration Input Set

The coherent Core Integration Input Set is the stable Core input boundary for external ecosystem integrations from v1.2.0.

It combines one logical Core load/lint operation into explicit required/companion surface records with exact digests, compatibility identities, load/lint state and deterministic set fingerprinting.

Its `input_set_version` remains `0.1-candidate`; stability and format-version text are independent.

### Additive FDIR Relationship Manifest families

The following are admitted as additive stable-compatible relationship families:

```text
autonomous_action_triggered_by_fault
autonomous_action_uses_command_source
fault_observes_telemetry
fault_recovery_dispatches_command
fault_recovery_targets_mode
recovery_intent_includes_command
recovery_intent_targets_mode
```

Each is derived deterministically from an explicit loaded Mission Model field. They do not rename/remove/redefine original v1 families and do not introduce inferred graph semantics.

The original v1 Relationship Manifest golden remains fixed; dedicated regression tests protect these additive families.

---

## 4. Current classification inventory

| Surface | Classification after v1.2.0 | Purpose |
|---|---|---|
| `model_summary.json` | Stable | Domain/count summary |
| `entity_index.json` | Stable | Canonical entity inventory |
| `relationship_manifest.json` original families | Stable | Original admitted explicit relationships |
| Relationship Manifest FDIR families | Additive stable-compatible | Additional explicit FDIR relationships |
| `mission_snapshot.json` | Stable | Complete loaded Mission Model inspection |
| Core Integration Input Set | Stable | Coherent Core input boundary for external integrations |
| `dashboard_summary.json` | Candidate | Dashboard-ready Core aggregation |
| `scenario_run_index.json` | Candidate | Index of simulation JSON report runs |
| `coverage_summary.json` | Candidate | Limited coverage derived from Core outputs |
| simulation JSON structured `expectations` | Candidate additive extension | Structured expectation accounting |

---

## 5. Extension-owned integration contracts

The Integration Framework additionally defines these separately versioned extension contracts:

```text
Projection Profile
Integration Result
Integration Package / Adapter Execution
```

They remain `0.1-candidate` after v1.2.0.

They are not Core Mission Data Contract surfaces and do not move target-specific semantics into Core.

---

## 6. Compatibility posture

The v1.2 release does not change Mission Model semantics.

Compatible consumers must:

- check Core surface kind/version identifiers;
- tolerate unknown additive fields where the relevant contract permits them;
- tolerate unknown additive Relationship Manifest types without assigning guessed semantics;
- reject missing/incompatible required Integration Input Set surfaces;
- distinguish Core load/lint diagnostics from integration diagnostics;
- never use raw YAML, filenames, timestamps or UI state as semantic fallbacks.

---

## 7. Ownership boundary

```text
Core defines Mission Data Contract semantics.
Core emits stable and candidate structured surfaces.
Projection Profiles own authored target-specific projection intent.
External adapters own target-specific validation and generation.
Studio and other downstream tools consume and compose explicit records.
```

Core is not a dashboard backend, flight software framework, ground segment, runtime framework, graph engine, plugin execution platform or OpenOBSW/OpenSVF-specific generator.

---

## 8. Explicit non-goals

The post-v1 integration surfaces do not introduce:

```text
OpenOBSW/OpenSVF/YAMCS-specific Core semantics
CCSDS/PUS/CFDP implementation
runtime telemetry behavior
ground execution behavior
relationship graph behavior
dependency graph behavior
Core plugin discovery/loading/execution
Studio-specific APIs
```
