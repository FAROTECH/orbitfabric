# OrbitFabric

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

It defines telemetry, commands, events, faults, operational modes, packets, payload contracts, data products, contact/downlink assumptions, commandability/autonomy contracts and scenarios in a single Mission Data Contract.

From that contract, OrbitFabric validates consistency, generates documentation and executes host-side operational scenarios.

## Current development preview

OrbitFabric is currently at:

```text
v0.5 — Commandability and Autonomy Contracts
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
- generated payload documentation;
- generated data product documentation;
- generated contact/downlink documentation;
- generated commandability/autonomy documentation;
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
  -> future end-to-end mission data flow evidence
  -> future runtime and ground artifacts
```

OrbitFabric is not a flight software framework, a ground segment or a spacecraft dynamics simulator.

It is the contract layer between mission design, onboard software, simulation, testing, documentation and future ground integration artifacts.
