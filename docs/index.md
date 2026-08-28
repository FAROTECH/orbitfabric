# OrbitFabric

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

It defines telemetry, commands, events, faults, operational modes, packets, payload contracts, data products, contact/downlink assumptions, commandability/autonomy contracts, scenarios, runtime-facing contract bindings, ground-facing integration artifacts and Core-owned structured surfaces in one Mission Data Contract workflow.

From that contract, OrbitFabric validates consistency, executes deterministic host-side scenario evidence, generates documentation and contract-facing artifacts, and exports machine-readable Core-owned surfaces for downstream consumers.

## Current status

OrbitFabric is currently released at:

```text
v1.2.0 - Core Integration Input Consolidation
```

v1.2.0 extends the stable Core boundary additively without changing Mission Model semantics.

Stable Core-owned integration/inspection surfaces now include:

```text
model_summary.json
entity_index.json
relationship_manifest.json for admitted families
mission_snapshot.json
```

The coherent external-integration input workflow is:

```text
orbitfabric export integration-input-set <mission_dir>
        ↓
integration_input_manifest.json
        + mission_snapshot.json
        + entity_index.json
        + relationship_manifest.json
        + lint_report.json
        + model_summary.json
```

The set is generated from one logical Core load/lint operation and records explicit surface roles, compatibility identities, SHA-256 digests and a deterministic input-set fingerprint. A required surface that is unavailable or incompatible blocks semantic projection; an adapter must not reconstruct OrbitFabric semantics by reparsing raw Mission Model YAML.

`mission_snapshot.json` answers:

```text
What complete Mission Model did Core actually load?
```

It is read-only, contains structured load diagnostics and exposes no partial semantic model after structural load failure.

The seven post-v1.1 FDIR relationship families are admitted as additive stable-compatible Relationship Manifest families. They are derived from explicit Mission Model fields and do not redefine original v1 relationship semantics.

The following v1.1.0 inspection surfaces remain candidate unless separately promoted:

```text
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
simulation JSON structured expectation accounting
```

The generic Integration Framework is reference-proven, but these extension-owned contracts remain `0.1-candidate`:

```text
Projection Profile
Integration Result
Integration Package / Adapter Execution
```

The stable Core input boundary does not make target-specific projection semantics Core-owned.

## Core idea

```text
Mission Model
  -> structural validation
  -> semantic lint
  -> documentation and scenario evidence
  -> runtime/ground-facing generated contract artifacts
  -> Core-owned structured surfaces
  -> coherent Core Integration Input Set
  -> external Integration Packages consume explicit versioned surfaces
```

The boundary is:

```text
Mission Model remains the source of truth.
Core owns Mission Data Contract semantics.
Core emits structured surfaces and the coherent integration input set.
Projection Profiles own authored target-specific choices.
External adapters own target projection, target diagnostics and target artifacts.
Downstream tools consume explicit records instead of inventing private semantics.
```

Generated artifact defaults for mission-based commands are mission-workspace relative. Explicit user-provided output paths remain explicit.

The selected golden signatures protect contract-significant fields rather than freezing complete generated JSON files. The v1.2 Mission Snapshot golden protects envelope, boundary and representative serialization invariants while allowing compatible additive Mission Model evolution.

OrbitFabric is not a flight software framework, a ground segment, a mission control system, a graph engine, a plugin execution platform or a Studio-specific backend.

Core does not dynamically load or execute ecosystem-specific adapters.
