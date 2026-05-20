# OrbitFabric

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

It defines telemetry, commands, events, faults, operational modes, packets, payload contracts, data products, contact/downlink assumptions, commandability/autonomy contracts, scenarios, runtime-facing contract bindings, ground-facing integration artifacts, Core-owned introspection surfaces, entity index surfaces, relationship manifest surfaces, compatibility classification references, extensibility boundary contracts and v1.0 candidate hardening references in a single Mission Data Contract workflow.

From that contract, OrbitFabric validates consistency, generates documentation, executes host-side operational scenarios and generates deterministic integration and inspection artifacts.

## Current status

OrbitFabric is currently at:

```text
v0.12.0 - v1.0 Release Candidate Hardening
```

The immediate target is:

```text
v1.0.0 - Stable Mission Data Contract
```

The repository now contains the v1.0 candidate documentation and regression-confidence material needed before the final v1.0.0 release alignment:

```text
v1.0 Stable Surface Decision
v1.0 Demo Evidence Chain
v1.0 Compatibility and Migration Notes
v1.0 golden signatures for selected Core-owned structured surfaces
```

These additions clarify the proposed v1.0 posture.

They do not change the package version, add Mission Model behavior, add YAML fields, add CLI behavior, add JSON report fields, add generated Core surfaces, add runtime behavior, add ground behavior, introduce schema migration tooling, publish JSON Schema, add security enforcement semantics, add plugin discovery, add plugin loading, add plugin execution or create a tool-specific integration layer.

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
  -> stability and compatibility classification
  -> extensibility boundary contract
  -> v1.0 stable surface decision
  -> v1.0 demo evidence chain
  -> v1.0 compatibility and migration posture
  -> v1.0 golden signatures for selected Core-owned structured surfaces
```

The current Core-owned structured surface chain is:

```text
model_summary.json          -> domain navigation
entity_index.json           -> entity navigation
relationship_manifest.json  -> relationship navigation
```

The current v1.0 candidate posture is:

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

Contract introspection, entity index and relationship manifest surfaces are not plugin APIs, graph engines or Studio-specific APIs.

Compatibility references, v1.0 candidate references and the Extensibility Boundary Contract are not schema migration tooling, plugin discovery, plugin loading, plugin execution, runtime behavior, ground behavior or tool-specific integrations.

The v1.0 golden signatures protect selected contract-significant fields of existing Core-owned structured surfaces.

They do not freeze full generated JSON files, absolute paths, human-oriented output, Markdown wording, generated runtime bindings, generated ground dictionaries or disposable artifact formatting.

The v1.0 demo evidence chain proves Mission Data Contract continuity from one validated Mission Model across scenario evidence, generated review artifacts and Core-owned structured surfaces.

It does not prove flight readiness, ground readiness, protocol compliance, tool-specific integration, security enforcement or operational completeness.
