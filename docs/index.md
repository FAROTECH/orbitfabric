# OrbitFabric

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

It defines telemetry, commands, events, faults, operational modes, packets, payload contracts, data products, contact/downlink assumptions, commandability/autonomy contracts and scenarios in a single Mission Data Contract.

From that contract, OrbitFabric validates consistency, generates documentation and executes host-side operational scenarios.

## Current development preview

OrbitFabric is currently at:

```text
v0.6.0 — End-to-End Mission Data Flow Evidence
```

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
  -> future runtime and ground artifacts
```

OrbitFabric is not a flight software framework, a ground segment or a spacecraft dynamics simulator.

It is the contract layer between mission design, onboard software, simulation, testing, documentation and future ground integration artifacts.
