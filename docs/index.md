# OrbitFabric

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

It defines telemetry, commands, events, faults, operational modes, packets and scenarios in a single Mission Data Contract.

From that contract, OrbitFabric validates consistency, generates documentation and executes host-side operational scenarios.

## Core Idea

```text
Mission Model
  -> lint
  -> documentation
  -> scenario simulation
  -> future runtime and ground artifacts
```