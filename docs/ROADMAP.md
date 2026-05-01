# OrbitFabric — Roadmap

Version: v0.2.2 alignment  
Status: Development preview  
Scope: v0.2.x to v1.0 planning

---

## 1. Roadmap Principle

OrbitFabric must grow through coherent vertical slices, not through feature accumulation.

The project must not try to become, at the same time:

- a flight software framework;
- a ground segment;
- a spacecraft dynamics simulator;
- a packet standard implementation;
- a formal verification tool;
- a hardware abstraction layer;
- a CubeSat tutorial;
- a payload runtime framework.

The correct growth path is:

```text
Mission Model
        → lint
        → scenario simulation
        → generated documentation
        → model hardening
        → runtime skeletons
        → ground integration artifacts
        → plugins and extensibility
```

Every milestone must reinforce the core identity:

> OrbitFabric is a Mission Data Contract framework.

---

## 2. Version Strategy

OrbitFabric versions before v1.0 are allowed to evolve the model quickly.

The priority before v1.0 is:

1. clarity;
2. usefulness;
3. consistency;
4. testability;
5. extensibility;
6. compatibility.

Backward compatibility matters, but it must not prevent correction of weak early model choices.

The model should become progressively more stable before generated runtime artifacts are introduced.

---

## 3. Roadmap Overview

```text
v0.1    Mission Contract MVP                         completed
v0.2    Model Hardening                              active line
v0.2.1  Payload Contract Model                       completed
v0.2.2  Payload Contract Release Alignment           active
v0.3    Generated Runtime Skeletons                  future
v0.4    Ground Integration Artifacts                 future
v0.5    Plugin and Extensibility Layer               future
v1.0    Stable Mission Data Contract                 future
```

The immediate target is `v0.2.2`.

The next implementation priority is not runtime generation.  
The next priority is to align documentation, release notes, roadmap and public communication after the Payload Contract Model vertical slice.

---

## 4. Completed Baseline — v0.1 Mission Contract MVP

### 4.1 Objective

Demonstrate the complete OrbitFabric philosophy with one small, coherent, synthetic mission.

v0.1 proves that a user can:

1. define a mission once;
2. lint it semantically;
3. generate documentation;
4. execute an operational scenario;
5. receive readable logs and JSON reports.

The v0.1 goal was coherence, not breadth.

### 4.2 Capabilities

The v0.1 baseline includes:

```text
Mission Model YAML
Model loader
Typed validation
Structural validation
Semantic linting
Engineering lint rules
JSON lint report generation
Generated Markdown docs
Scenario model loading
Scenario reference validation
Host-side deterministic scenario execution
Simulation JSON report generation
Simulation plain-text log generation
Synthetic demo mission demo-3u
```

### 4.3 Non-Goals

v0.1 intentionally did not include:

```text
C++ runtime generation
flight runtime
hardware drivers
RTOS integration
Linux onboard service
CCSDS implementation
PUS implementation
CFDP implementation
Yamcs export
OpenC3 export
XTCE export
Basilisk bridge
cFS bridge
F Prime bridge
web UI
database
message broker
real spacecraft data
```

These are not missing features.  
They are intentionally outside the first vertical slice.

---

## 5. Completed Slice — v0.2.1 Payload Contract Model

### 5.1 Objective

Introduce a first narrow vertical slice for Payload / IOD Payload Contracts.

The goal is to let OrbitFabric describe mission-specific or IOD payload behavior as part of the Mission Data Contract without turning OrbitFabric into a payload firmware, driver or runtime framework.

### 5.2 Completed Capabilities

v0.2.1 introduced:

```text
Payload Contract Model ADR
optional payloads.yaml domain
PayloadContract model
minimal payload lifecycle model
payload profile model
payload semantic lint rules
payload reference checks
generated payload contract documentation
payload-aware scenario behavior
invalid payload contract fixtures
negative tests for mutated fixtures
```

The current payload lifecycle model is intentionally minimal:

```text
OFF
READY
ACQUIRING
FAULT
```

The first demo payload vertical slice demonstrates:

```text
READY → ACQUIRING → READY
```

### 5.3 Payload Contract Boundary

A payload contract may describe:

```text
payload identity
payload profile
linked subsystem
telemetry references
command references
event references
fault references
lifecycle states
command preconditions
expected effects
scenario-level behavior
generated documentation
```

A payload contract must not describe:

```text
payload firmware
payload drivers
hardware buses
onboard runtime services
payload data processing pipelines
physical instrument simulation
thermal, optical or scientific simulation
ground segment implementation
```

The Payload Contract Model strengthens OrbitFabric as a Mission Data Contract Layer.

It does not expand OrbitFabric into a payload runtime.

---

## 6. Active Milestone — v0.2.2 Payload Contract Release Alignment

### 6.1 Objective

Capitalise on the completed Payload Contract Model vertical slice.

v0.2.2 is a release-alignment milestone.  
It must make the repository, public documentation, roadmap, changelog, release notes and public communication consistent with the current state of the project.

### 6.2 Required Work

v0.2.2 should include:

```text
README alignment
public documentation alignment
ROADMAP alignment
CHANGELOG update
release/version decision
release notes preparation
Payload Contract Model communication draft
```

### 6.3 Required Boundary

v0.2.2 must not introduce new core model features.

The milestone must not include:

```text
new payload lifecycle states
new payload scenario semantics
second payload example
runtime skeleton generation
C++ generator work
ground integration export
plugin API
payload runtime behavior
physical payload simulation
```

The purpose of v0.2.2 is alignment, not expansion.

---

## 7. Possible Follow-Up — v0.2.x Additional Model Hardening

After v0.2.2, a small additional v0.2.x milestone may be considered if the model still needs hardening before v0.3.

Possible candidates:

```text
second clean-room payload example
improved payload rule documentation
more invalid payload fixtures
clearer payload command precondition checks
improved diagnostics
expanded scenario validation
schema/versioning cleanup
```

A second payload example may be valuable, but only if it proves generality without expanding the core too aggressively.

Candidate examples:

```text
imaging payload
radiation monitor
AIS or IoT receiver
generic science payload
technology demonstration payload
```

Any second example must remain synthetic and clean-room.

---

## 8. Future Milestone — v0.3 Generated Runtime Skeletons

### 8.1 Objective

Start deriving onboard-oriented artifacts from the Mission Data Contract.

This is not flight software.  
This is generated skeleton code that demonstrates how the Mission Data Contract can support future onboard runtime integration.

### 8.2 Candidate Features

```text
C++17 generated headers
generated telemetry IDs
generated command IDs
generated event IDs
generated mode IDs
generated packet IDs
generated command argument structs
generated adapter interfaces
generated command dispatch skeleton
generated telemetry registry skeleton
host-buildable CMake example
```

### 8.3 Required Boundary

v0.3 generated code must be described as:

```text
runtime skeleton
host-buildable example
integration starting point
```

It must not be described as:

```text
flight-ready runtime
qualified software
complete OBC framework
replacement for cFS or F Prime
```

### 8.4 v0.3 Non-Goals

Still out of scope:

```text
real hardware support
RTOS-specific runtime
Linux service integration
flight qualification
complete scheduler
complete storage subsystem
complete radio stack
payload firmware
payload driver generation
```

v0.3 must only start after the Mission Data Contract model is sufficiently stable.

---

## 9. Future Milestone — v0.4 Ground Integration Artifacts

### 9.1 Objective

Generate useful artifacts for ground integration without becoming a ground segment.

OrbitFabric should help external tools consume the Mission Data Contract.

### 9.2 Candidate Features

```text
JSON mission database export
packet dictionary export
simple decoder skeletons
telemetry dictionary export
command dictionary export
Yamcs-like export prototype
OpenC3-like export prototype
XTCE exploration/prototype
```

### 9.3 Required Boundary

OrbitFabric may export artifacts for ground tools.  
OrbitFabric must not become a ground tool.

No v0.4 feature should implement:

```text
complete mission control UI
operator console
database-backed telemetry archive
real command uplink service
user management
security system
live spacecraft operations stack
```

---

## 10. Future Milestone — v0.5 Plugin and Extensibility Layer

### 10.1 Objective

Turn OrbitFabric from a useful tool into an extensible framework.

v0.5 should introduce controlled extension points.

### 10.2 Candidate Features

```text
custom lint rule plugins
custom generator plugins
mission model extension mechanism
adapter SDK
plugin discovery
plugin metadata
example plugin
contribution guide
rule documentation generator
semantic versioning policy
```

### 10.3 Required Boundary

Plugins must extend OrbitFabric without breaking the core contract.

A plugin may consume or extend the Mission Model.  
A plugin must not silently redefine core semantics.

---

## 11. Future Milestone — v1.0 Stable Mission Data Contract

### 11.1 Objective

v1.0 should be the first version where the Mission Data Contract is stable enough for external users to build around.

### 11.2 Possible v1.0 Requirements

```text
stable Mission Model schema
stable Payload Contract Model schema
stable CLI commands
stable lint rule code policy
stable generated documentation format
stable JSON report format
stable plugin API if introduced
migration guide from earlier model versions
complete demo mission
multiple example missions
published documentation site
CI-tested release artifacts
clear contribution process
```

### 11.3 v1.0 Should Not Require

```text
flight qualification
complete CCSDS/PUS stack
complete Yamcs/OpenC3 compatibility
complete cFS/F Prime bridge
real spacecraft deployment
payload firmware support
payload hardware support
```

v1.0 should mean stable Mission Data Contract framework, not complete space software ecosystem.

---

## 12. Backlog Parking Lot

These ideas are valid but must not distract from the active milestone.

```text
XTCE export
CCSDS packet generator
PUS service mapping
CFDP metadata
Yamcs integration
OpenC3 integration
Basilisk bridge
Space ROS bridge
F Prime topology generator
cFS table/app generator
web dashboard
visual mission model editor
SARIF lint export
VS Code extension
JSON Schema publication
schema migration tool
simulation time acceleration
fault tree visualization
mode transition graph rendering
requirements traceability
coverage metrics for scenarios
packet budget analyzer
downlink window planner
power budget toy model
ADCS abstract mode examples
thermal abstract mode examples
security policy model
command authorization model
second payload example
payload lifecycle expansion
```

Parking lot items are not rejected.  
They are explicitly deferred.

---

## 13. Priority Rules

When deciding what to implement next, use these rules.

### Rule 1 — Protect the Core Identity

If a feature weakens the Mission Data Contract identity, defer it.

### Rule 2 — Model Before Generator

If the model cannot express a concept cleanly, do not generate code for it.

### Rule 3 — Lint Before Runtime

If a behavior can be inconsistent, create a lint rule before creating downstream generators.

### Rule 4 — Docs from Model

If information exists in the model, generated docs should expose it.

### Rule 5 — No Hidden Semantics

If behavior matters, it must not live only in Python code.

### Rule 6 — No Private Examples

If an example resembles a private mission, remove or generalize it.

### Rule 7 — Small Working Slice Beats Broad Incomplete Scope

A working vertical slice is more valuable than multiple half-implemented integrations.

### Rule 8 — Payload Contracts Are Contracts

Payload contracts describe expected mission-data behavior.

They must not become payload firmware, payload drivers, hardware simulation or scientific processing pipelines.

---

## 14. Immediate Work Plan

The immediate work package is:

```text
v0.2.2 — Payload Contract Release Alignment
```

Required sequence:

```text
1. README alignment
2. public documentation alignment
3. ROADMAP alignment
4. CHANGELOG update
5. release/version alignment
6. public communication draft
```

Do not start v0.3 until v0.2.2 is complete.

Do not add runtime skeletons before the model and documentation are coherent.

Do not add a second payload example until the current Payload Contract Model has been clearly documented and communicated.

---

## 15. Final Roadmap Statement

OrbitFabric must first become excellent at one thing:

> defining, validating, simulating and documenting a Mission Data Contract for a small spacecraft.

The Payload Contract Model strengthens this mission by making mission-specific and IOD payload behavior explicit, lintable, documentable and scenario-aware.

Only after the model is clear and stable should OrbitFabric grow into runtime skeleton generation, ground integration artifacts and plugin extensibility.

The narrowness of the roadmap is intentional.  
That narrowness is a strength, not a limitation.
