# OrbitFabric

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

It defines telemetry, commands, events, faults, operational modes, packets, payload contracts, data products, contact/downlink assumptions, commandability/autonomy contracts, scenarios, runtime-facing contract bindings, ground-facing integration artifacts, Core-owned introspection surfaces, entity index surfaces, relationship manifest surfaces, compatibility classification references and extensibility boundary contracts in a single Mission Data Contract workflow.

From that contract, OrbitFabric validates consistency, generates documentation, executes host-side operational scenarios and generates deterministic integration and inspection artifacts.

## Current development preview

OrbitFabric is currently at:

```text
v0.11.0 - Extensibility Boundary Contract, no execution
```

v0.11.0 defines the extensibility boundary without introducing plugin execution.

It introduces no Mission Model semantics, CLI behavior beyond version reporting, generated Core surfaces, JSON report fields, lint diagnostics, scenario behavior, runtime behavior, ground behavior, plugin discovery, plugin loading, plugin execution, metadata schema, metadata parser, metadata loader, metadata validator or Studio-specific APIs.

It builds on:

```text
v0.8.1  -> model_summary.json
v0.8.2  -> entity_index.json
v0.9.0  -> relationship_manifest.json
v0.10.0 -> stability and compatibility classification
v0.10.1 -> documentation and published-site consistency
v0.11.0 -> extensibility boundary contract, no execution
```

The active hardening path after v0.11.0 is:

```text
v0.12.0 - v1.0 Release Candidate Hardening
```

Current v0.12.0 hardening references are documentation and review surfaces only:

```text
v1.0 Candidate Surface Inventory
Golden Output and Regression Confidence Policy
v1.0 Compatibility and Migration Notes
```

They do not make v0.12.0 released.

They do not make any surface stable v1.0.

They do not introduce new Mission Model semantics, generated Core surfaces, JSON report fields, CLI behavior, schema migration tooling, JSON Schema publication, plugin discovery, plugin loading, plugin execution, runtime behavior, ground behavior or Studio-specific APIs.

The current public preview includes:

- Mission Model YAML loading;
- structural validation;
- semantic linting;
- generated Markdown documentation;
- deterministic scenario execution;
- optional Payload / IOD Payload Contracts;
- optional Data Product and Storage Contracts;
- optional Contact Windows and Downlink Flow Contracts;
- optional Commandability and Autonomy Contracts;
- command-declared data product effects;
- generated payload documentation;
- generated data product documentation;
- generated contact/downlink documentation;
- generated commandability/autonomy documentation;
- generated data-flow evidence documentation;
- JSON lint reports;
- JSON simulation reports with contract-level data-flow evidence;
- data-flow scenario assertions;
- RuntimeContract generation;
- generated C++17 runtime-facing contract bindings;
- generated C++17 host-build smoke files;
- GroundContract generation;
- generated ground contract manifest;
- generated JSON ground dictionaries;
- generated CSV ground dictionaries;
- generated human-reviewable ground Markdown artifacts;
- `orbitfabric export model-summary`;
- generated `model_summary.json` contract introspection report;
- `orbitfabric export entity-index`;
- generated `entity_index.json` entity index report;
- `orbitfabric export relationship-manifest`;
- generated `relationship_manifest.json` candidate relationship report;
- stability and compatibility classification references;
- Extensibility Boundary Contract reference documentation;
- ADR-0015 for the extensibility boundary;
- release compatibility policy;
- v1.0 candidate surface inventory;
- golden output and regression confidence policy;
- v1.0 compatibility and migration notes;
- a clean-room synthetic `demo-3u` mission.

## Core Idea

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
  -> v1.0 release candidate hardening references
```

The current Core-owned structured surface chain is:

```text
model_summary.json          -> domain navigation
entity_index.json           -> entity navigation
relationship_manifest.json  -> relationship navigation
```

The extensibility boundary rule is:

```text
Mission Model remains the source of truth.
Core owns Mission Data Contract semantics.
Extensions consume Core-owned structured surfaces.
Extension-owned outputs remain distinguishable from Core-owned outputs.
Extensions must not override Core semantics.
Execution is out of scope.
```

The v0.12.0 hardening rule is:

```text
Review candidate v1.0 surfaces.
Define confidence policy before adding golden baselines.
Document compatibility and migration decisions before stabilization.
Remove ambiguity before declaring a stable Mission Data Contract.
Do not broaden OrbitFabric.
```

OrbitFabric is not a flight software framework, a ground segment or a spacecraft dynamics simulator.

It is the contract layer between mission design, onboard software, simulation, testing, documentation, runtime-facing bindings, ground-facing integration artifacts, downstream inspection tools and future extension-owned outputs.

Generated runtime-facing contract bindings are not flight software.

Generated ground integration artifacts are not ground software.

Contract introspection, entity index and relationship manifest surfaces are not plugin APIs, graph engines or Studio-specific APIs.

Compatibility classification references, v0.12.0 hardening references and the Extensibility Boundary Contract are not schema migration tooling, plugin discovery, plugin loading, plugin execution, runtime behavior, ground behavior or a v1.0 stability guarantee.
