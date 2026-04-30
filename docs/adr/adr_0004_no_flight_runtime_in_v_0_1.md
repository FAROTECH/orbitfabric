# ADR-0004 — No Flight Runtime in v0.1

Status: Accepted  
Date: 2026-04-29  
Scope: OrbitFabric MVP v0.1  

---

## Context

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

A natural temptation is to implement an onboard runtime immediately, including components such as:

- telemetry registry;
- command router;
- event bus;
- mode manager;
- fault monitor;
- packet builder;
- storage interface;
- subsystem adapters;
- hardware abstraction interfaces;
- scheduler hooks;
- embedded C++ code generation.

These components are relevant to the long-term vision.

However, implementing a flight-like runtime in v0.1 would shift the center of the project away from the Mission Data Contract and toward flight software architecture.

That would create confusion with existing frameworks such as cFS and F Prime, and would weaken OrbitFabric's distinct identity.

The purpose of v0.1 is not to fly software.

The purpose of v0.1 is to prove that a mission can be described once, validated semantically, simulated operationally and documented automatically from a single Mission Model.

---

## Decision

OrbitFabric v0.1 shall not include a flight runtime.

v0.1 shall not attempt to provide flight-ready or flight-like onboard execution infrastructure.

The v0.1 implementation shall focus on:

- Mission Model definition;
- Mission Model loading;
- structural validation;
- semantic linting;
- documentation generation;
- scenario execution;
- deterministic simulation;
- readable logs;
- JSON reports;
- the synthetic `demo-3u` mission.

The simulation runtime used by `orbitfabric sim` is allowed, but it must be treated as a host-side validation and demonstration tool, not as onboard flight software.

---

## Explicit Non-Goals for v0.1

OrbitFabric v0.1 shall not include:

- flight-ready C++ runtime;
- onboard scheduler;
- RTOS integration;
- Linux onboard service integration;
- real-time constraints;
- hardware abstraction layer;
- real subsystem drivers;
- SPI/I2C/UART/CAN drivers;
- storage drivers;
- radio drivers;
- watchdog integration;
- boot sequencing for real hardware;
- deployment to embedded targets;
- memory-bounded runtime behavior;
- deterministic embedded allocation policy;
- flight software qualification flow;
- cFS integration;
- F Prime integration;
- generated flight application packages.

These are future concerns.

They must not enter v0.1.

---

## What Is Allowed in v0.1

v0.1 may include runtime-like concepts only inside the host-side simulator.

Allowed simulator components:

- `TelemetryRegistry`;
- `CommandRouter`;
- `EventBus`;
- `ModeManager`;
- `FaultMonitor`;
- `ScenarioRunner`;
- `SimulationClock`;
- `MockEPS`;
- `MockPayload`;
- `SimulationReport`.

These components exist to execute and validate scenarios.

They are not flight runtime components.

Their design must remain simple, deterministic and clearly tied to the Mission Model.

---

## Rationale

The strongest value proposition of OrbitFabric is not embedded execution.

The strongest value proposition is consistency across mission data, validation, simulation, testing, documentation and future integration artifacts.

A flight runtime in v0.1 would introduce several risks:

1. It would dilute the Mission Model focus.
2. It would invite comparison with mature flight software frameworks.
3. It would require premature choices about scheduling, memory, concurrency and hardware abstraction.
4. It would increase implementation scope dramatically.
5. It would slow down the development of linting and scenario testing.
6. It would make the MVP harder to explain and finish.

The correct order is:

1. Define the model.
2. Validate the model.
3. Simulate behavior from the model.
4. Generate documentation from the model.
5. Only later generate onboard/runtime artifacts from the model.

---

## Consequences

### Positive Consequences

The v0.1 scope remains achievable.

OrbitFabric keeps a distinct identity as a Mission Data Contract framework.

The project avoids premature competition with cFS, F Prime and other mature flight software ecosystems.

The team can focus on the highest-risk architectural problem: designing a useful Mission Model and lint system.

The first release can be useful without requiring embedded hardware.

The demo can run on a normal development machine.

### Negative Consequences

Some users may expect onboard code generation earlier.

Some embedded engineers may perceive v0.1 as only a tooling project.

Future runtime generation will require additional architectural decisions.

The simulator may need to be clearly documented to avoid being mistaken for a flight runtime.

### Neutral Consequences

OrbitFabric may still include a runtime concept in future versions.

OrbitFabric may still generate C++17 runtime skeletons in v0.3 or later.

OrbitFabric may still define interfaces compatible with onboard software frameworks in future versions.

This ADR only blocks flight runtime implementation in v0.1.

---

## Alternatives Considered

### Alternative 1 — Implement a Minimal C++ Runtime in v0.1

Build a small C++ runtime with telemetry, commands, events, modes and faults.

Rejected.

This would look attractive but would be strategically wrong. A minimal runtime would still require many premature design choices and would distract from Mission Model quality.

### Alternative 2 — Generate C++ Headers in v0.1

Generate enum IDs, telemetry IDs and command IDs from the model.

Rejected for v0.1.

This may be a good v0.3 milestone, but it is not needed to prove the first vertical slice.

### Alternative 3 — Build a Python Runtime and Treat It as the Reference Runtime

Use the Python simulator as the official runtime semantics.

Rejected.

The Python simulator is a validation and demonstration tool. It must not become the architectural source of truth.

The Mission Model is the source of truth.

### Alternative 4 — Integrate with an Existing Flight Framework Immediately

Generate cFS or F Prime artifacts in v0.1.

Rejected.

This would make OrbitFabric dependent on external ecosystems before its own model is stable.

### Alternative 5 — No Runtime-Like Components at All

Avoid even simulator runtime concepts such as command router and event bus.

Rejected.

The v0.1 demo needs scenario execution. A minimal host-side simulation runtime is necessary to demonstrate the value of the Mission Model.

---

## Boundary Between Simulator and Flight Runtime

The v0.1 simulator may implement operational behavior such as:

- command acceptance or rejection;
- allowed mode checks;
- telemetry injection;
- fault condition evaluation;
- event emission;
- mode transition;
- auto-dispatch of recovery commands;
- scenario expectation checks.

The simulator shall not claim to implement:

- real-time scheduling;
- real hardware I/O;
- embedded resource constraints;
- flight task architecture;
- interrupt behavior;
- bus communication;
- persistent onboard storage;
- watchdog recovery;
- radiation-tolerant behavior;
- flight qualification semantics.

This distinction must be explicit in the documentation.

---

## Implementation Guidance for v0.1

The v0.1 simulator shall be implemented under:

```text
src/orbitfabric/sim/
```

Suggested modules:

```text
src/orbitfabric/sim/
├── runner.py
├── clock.py
├── telemetry_registry.py
├── command_router.py
├── event_bus.py
├── mode_manager.py
├── fault_monitor.py
├── report.py
└── mocks/
    ├── eps.py
    ├── payload.py
    └── radio.py
```

These modules must be documented as simulation components.

They must consume validated Mission Model objects.

They must not contain mission definitions that should belong in YAML.

They must not become a hidden source of truth.

---

## Future Runtime Direction

A future runtime milestone may introduce:

- generated C++17 headers;
- generated command IDs;
- generated telemetry IDs;
- generated event IDs;
- generated mode IDs;
- adapter interface skeletons;
- command dispatch skeletons;
- telemetry registry skeletons;
- host-buildable CMake examples.

This should not happen before:

- Mission Model v0.1 is documented;
- lint rules are working;
- `demo-3u` is complete;
- scenario runner works;
- generated documentation works;
- tests validate the model and scenario behavior.

A reasonable future target for generated C++ skeletons is v0.3, not v0.1.

---

## Architectural Rule

No v0.1 feature shall require real onboard execution.

No v0.1 feature shall require embedded hardware.

No v0.1 feature shall require an RTOS, Linux target, board support package or hardware driver.

If a proposed feature requires any of these, it is out of scope for v0.1.

---

## Decision Summary

OrbitFabric v0.1 shall not implement a flight runtime.

It shall implement a host-side toolchain and simulator sufficient to validate, lint, simulate and document a Mission Model.

The flight/runtime path remains future work and must be derived from the Mission Model only after the model proves stable and useful.

