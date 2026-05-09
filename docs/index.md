# OrbitFabric

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

It defines telemetry, commands, events, faults, operational modes, packets, payload contracts, data products, contact/downlink assumptions, commandability/autonomy contracts, scenarios and runtime-facing contract bindings in a single Mission Data Contract.

From that contract, OrbitFabric validates consistency, generates documentation, executes host-side operational scenarios and generates deterministic host-buildable software-facing artifacts.

## Current development preview

OrbitFabric is currently at:

```text
v0.7.0 — Generated Runtime Skeletons
```

In v0.7.0, Generated Runtime Skeletons means **runtime-facing contract bindings**.

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
- generated C++17 identifiers, enums and registries;
- generated C++17 command argument structs;
- generated C++17 abstract adapter interfaces;
- generated C++17 host-build smoke files;
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
  -> future ground integration artifacts
```

OrbitFabric is not a flight software framework, a ground segment or a spacecraft dynamics simulator.

It is the contract layer between mission design, onboard software, simulation, testing, documentation and future ground integration artifacts.

Generated runtime-facing contract bindings are not flight software.
