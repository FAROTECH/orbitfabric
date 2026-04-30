# ADR-0001 — Mission Model First

Status: Accepted  
Date: 2026-04-29  
Scope: OrbitFabric MVP v0.1  

---

## Context

OrbitFabric aims to become a model-first Mission Data Fabric for small spacecraft.

The project could be incorrectly started from several tempting directions:

- an onboard runtime;
- a flight software skeleton;
- a simulator;
- a packet encoder;
- a ground bridge;
- a C++ code generator;
- a demo application;
- a CubeSat-like firmware architecture.

These directions are technically attractive, but they are not the core of OrbitFabric.

The core problem OrbitFabric addresses is mission-data fragmentation: telemetry, commands, events, faults, modes, packets, documentation, tests and ground integration artifacts are often duplicated across disconnected tools and files.

If OrbitFabric starts from runtime code, it risks becoming another software framework.

If OrbitFabric starts from simulation, it risks becoming another spacecraft simulator.

If OrbitFabric starts from packet formats, it risks becoming another telemetry encoding tool.

If OrbitFabric starts from ground integration, it risks becoming another mission-control adapter.

OrbitFabric must instead start from the Mission Model.

---

## Decision

OrbitFabric shall be designed Mission Model first.

The Mission Model is the primary artifact of the project and the single source of truth for:

- spacecraft metadata;
- subsystems;
- telemetry definitions;
- command definitions;
- event definitions;
- fault definitions;
- operational modes;
- mode transitions;
- packet definitions;
- persistence policies;
- downlink policies;
- operational scenarios;
- linting and validation rules.

All other artifacts must be derived from, validated against or explicitly connected to the Mission Model.

This includes:

- semantic linting;
- generated documentation;
- scenario execution;
- simulation reports;
- packet descriptions;
- future onboard runtime stubs;
- future ground integration exports;
- future C++ generated code;
- future Yamcs/OpenC3/XTCE-related artifacts.

For OrbitFabric v0.1, development shall prioritize the Mission Model specification, model loader, validation rules, semantic linting and scenario execution over runtime code generation.

---

## Consequences

### Positive Consequences

The project will have a clear architectural center.

OrbitFabric will not be confused with an onboard flight software framework, a simulator or a ground system.

The MVP can demonstrate value without requiring real hardware, real spacecraft protocols or a complete embedded runtime.

The same mission definition can drive:

- documentation;
- simulation;
- testing;
- linting;
- future code generation;
- future ground exports.

This makes the project easier to explain, test and extend.

### Negative Consequences

Initial progress may look slower because the first effort goes into modeling, validation and specification rather than visible runtime behavior.

Some users may expect immediate onboard code generation or hardware examples, but those are intentionally deferred.

The Mission Model must be designed carefully. A weak model would weaken the entire framework.

### Neutral Consequences

OrbitFabric may still generate runtime code in the future, but generated code is a downstream artifact, not the source of truth.

OrbitFabric may still integrate with ground systems in the future, but ground integration is a consumer of the model, not the architectural center.

OrbitFabric may still include simulation, but simulation validates behavior described by the model rather than defining the model itself.

---

## Alternatives Considered

### Alternative 1 — Runtime First

Start by implementing an onboard runtime with telemetry registry, command router, event bus, mode manager and fault monitor.

Rejected.

This would make OrbitFabric look like a small flight software framework. It would also force runtime design decisions before the Mission Model is stable.

### Alternative 2 — Simulator First

Start by implementing the scenario runner and mock subsystems.

Rejected.

Simulation is important, but it is not the source of truth. The simulator must execute behavior derived from the Mission Model.

### Alternative 3 — Packet Format First

Start by defining binary packets, JSON packets or CCSDS-like structures.

Rejected.

Packet formats are downstream representations. Starting from packets would overemphasize encoding and underemphasize mission consistency.

### Alternative 4 — Ground Export First

Start by generating Yamcs/OpenC3/XTCE-like artifacts.

Rejected.

Ground integration is valuable but premature. OrbitFabric must first prove that its own Mission Model is coherent.

### Alternative 5 — Documentation Generator First

Start by generating Markdown documentation from YAML.

Rejected as the primary direction.

Documentation generation is a useful early feature, but without semantic validation it would only be a formatter around YAML files.

---

## Implementation Guidance for v0.1

OrbitFabric v0.1 shall implement the following in this order:

1. Mission Model v0.1 specification.
2. Demo mission model for `demo-3u`.
3. Model loader.
4. Structural validation.
5. Semantic linting.
6. Scenario model.
7. Scenario runner.
8. Documentation generator.
9. JSON reports and readable logs.

OrbitFabric v0.1 shall not implement:

- flight-ready runtime;
- hardware drivers;
- RTOS integration;
- CCSDS/PUS/CFDP implementation;
- cFS/F Prime integration;
- Yamcs/OpenC3 integration;
- Basilisk integration;
- C++ runtime generation.

These may be considered only after the Mission Model and linting system prove useful.

---

## Architectural Rule

No major OrbitFabric feature shall be accepted unless it answers at least one of these questions:

1. Does it improve the Mission Model?
2. Does it validate the Mission Model?
3. Does it derive useful artifacts from the Mission Model?
4. Does it execute or test behavior explicitly described by the Mission Model?
5. Does it help external systems consume the Mission Model?

If the answer is no, the feature does not belong in the core.

---

## Decision Summary

OrbitFabric starts from the Mission Model.

The Mission Model is the contract.

The runtime, simulator, documentation and integrations are consumers of that contract.

This decision is mandatory for the MVP and remains a core architectural principle for future versions.

