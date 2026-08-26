# OrbitFabric

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

It defines telemetry, commands, events, faults, operational modes, packets, payload contracts, data products, contact/downlink assumptions, commandability/autonomy contracts, scenarios, runtime-facing contract bindings, ground-facing integration artifacts, Core-owned introspection surfaces, entity index surfaces, relationship manifest surfaces, compatibility references, extensibility boundary contracts and v1.0 stable Mission Data Contract governance in a single workflow.

From that contract, OrbitFabric validates consistency, generates documentation, executes host-side operational scenarios and generates deterministic integration and inspection artifacts.

## Current status

OrbitFabric is currently released at:

```text
v1.1.0 - Candidate Integration Surface Consolidation
```

v1.1.0 consolidates the post-v1 candidate Core-owned integration surfaces while preserving the deliberately narrow v1.0.0 Stable Mission Data Contract.

The stable surface is intentionally limited.

Current `main` contains additional unreleased additive development after v1.1.0:

```text
mission_snapshot.json        -> complete loaded Mission Model inspection surface
relationship_manifest.json   -> seven additive explicit FDIR relationship families
```

These additions are development-state capabilities. They are not retroactively part of v1.1.0 and do not change the v1.0.0 stable Mission Data Contract baseline.

OrbitFabric is not a flight software framework, not a ground segment, not a mission control system, not a spacecraft dynamics simulator, not a plugin execution platform and not a tool-specific integration layer.

## Core idea

```text
Mission Model
  -> lint
  -> documentation
  -> scenario simulation
  -> payload contracts
  -> data product and storage contracts
  -> contact/downlink contracts
  -> commandability/autonomy contracts
  -> end-to-end mission data flow evidence
  -> RuntimeContract
  -> generated runtime-facing contract bindings
  -> GroundContract
  -> generated ground-facing integration artifacts
  -> Core-owned contract introspection surfaces
  -> Core-owned entity index surfaces
  -> Core-owned relationship manifest surfaces
  -> candidate full Mission Model snapshot surface
  -> stability and compatibility classification
  -> extensibility boundary contract
  -> v1.0 stable surface decision
  -> v1.0 demo evidence chain
  -> v1.0 compatibility and migration posture
  -> v1.0 golden signatures for selected Core-owned structured surfaces
```

The stable Core-owned structured surface chain is:

```text
model_summary.json          -> domain navigation
entity_index.json           -> entity navigation
relationship_manifest.json  -> relationship navigation
```

The post-v1 candidate Core-owned integration surfaces consolidated in v1.1.0 are:

```text
dashboard_summary.json       -> dashboard-ready aggregation of existing Core facts
scenario_run_index.json      -> simulation JSON run index
coverage_summary.json        -> limited coverage from Core structured outputs
simulation JSON expectations -> additive structured expectation accounting
```

Current unreleased development adds:

```text
mission_snapshot.json        -> full loaded contract inspection
FDIR relationship families   -> additive explicit relationship types in relationship_manifest.json
```

`mission_snapshot.json` is Core-owned and read-only. It exposes what Core actually loaded without asking downstream consumers to reparse OrbitFabric YAML and without becoming a second source of truth or a Studio-specific API.

The additive FDIR relationship families are derived deterministically from explicit Mission Model fields. They preserve the original v1 relationship-family compatibility commitments.

The boundary is:

```text
Core owns Mission Data Contract semantics.
Core emits structured surfaces.
Downstream tools consume and render them.
Downstream tools do not invent coverage, health or completeness semantics.
```

Generated artifact defaults for mission-based commands are mission-workspace relative.

For `examples/demo-3u/mission/`, omitted generated outputs are written under:

```text
examples/demo-3u/generated/
```

Explicit output paths remain explicit and are not rewritten.

The stable v1.0 posture is:

```text
Mission Model remains the source of truth.
Core owns Mission Data Contract semantics.
Core-owned structured surfaces are derived from the validated Mission Model.
Downstream tools consume Core-owned structured surfaces.
Generated runtime-facing and ground-facing artifacts remain reproducible and disposable unless explicitly classified otherwise.
Plugin execution remains out of scope.
```

OrbitFabric is not a flight software framework, a ground segment or a spacecraft dynamics simulator.

It is the contract layer between mission design, onboard software, simulation, testing, documentation, runtime-facing bindings, ground-facing integration artifacts, downstream inspection tools and future extension-owned outputs.

Generated runtime-facing contract bindings are not flight software.

Generated ground integration artifacts are not ground software.

Contract introspection, entity index, relationship manifest and Mission Snapshot surfaces are not plugin APIs, graph engines or Studio-specific APIs.

Compatibility references and the Extensibility Boundary Contract are not schema migration tooling, plugin discovery, plugin loading, plugin execution, runtime behavior, ground behavior or tool-specific integrations.

The v1.0 golden signatures protect selected contract-significant fields of existing Core-owned structured surfaces.

They do not freeze full generated JSON files, absolute paths, human-oriented output, Markdown wording, generated runtime bindings, generated ground dictionaries or disposable artifact formatting.

The v1.0 demo evidence chain proves Mission Data Contract continuity from one validated Mission Model across scenario evidence, generated review artifacts and Core-owned structured surfaces.

It does not prove flight readiness, ground readiness, protocol compliance, tool-specific integration, security enforcement or operational completeness.