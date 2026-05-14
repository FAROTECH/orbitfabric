# OrbitFabric

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

It defines telemetry, commands, events, faults, operational modes, packets, payload contracts, data products, contact/downlink assumptions, commandability/autonomy contracts, scenarios, runtime-facing contract bindings, ground-facing integration artifacts, Core-owned introspection surfaces and entity index surfaces in a single Mission Data Contract.

From that contract, OrbitFabric validates consistency, generates documentation, executes host-side operational scenarios and generates deterministic integration and inspection artifacts.

## Current development preview

OrbitFabric is currently at:

```text
v0.8.2 - Entity Index Surface
```

In v0.8.2, Entity Index Surface means the first **Core-owned read-only entity index surface** derived from the loaded Mission Model.

It builds on v0.8.1, which introduced the domain-level `model_summary.json` surface.

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
```

OrbitFabric is not a flight software framework, a ground segment or a spacecraft dynamics simulator.

It is the contract layer between mission design, onboard software, simulation, testing, documentation, runtime-facing bindings, ground-facing integration artifacts and downstream inspection tools.

Generated runtime-facing contract bindings are not flight software.

Generated ground integration artifacts are not ground software.

Contract introspection and entity index surfaces are not plugin APIs, relationship graphs or Studio-specific APIs.
