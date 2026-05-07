# OrbitFabric — Roadmap

Version: v0.5.0
Status: Development preview
Scope: v0.3 to v1.0 planning

---

## 1. Roadmap Principle

OrbitFabric grows through coherent vertical slices, not through feature accumulation.

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
        -> lint
        -> scenario simulation
        -> generated documentation
        -> payload contracts
        -> data product and storage contracts
        -> contact and downlink contracts
        -> commandability and autonomy contracts
        -> end-to-end mission data flow evidence
        -> runtime skeletons
        -> ground integration artifacts
        -> plugins and extensibility
```

Every milestone must reinforce the core identity:

> OrbitFabric is a Mission Data Contract framework.

The current architectural objective is to model the mission data chain from payload behavior to data products, onboard storage intent, downlink assumptions, contact windows, commandability, recovery behavior and ground-facing artifacts.

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
v0.1    Mission Contract MVP                                  completed
v0.2    Model Hardening                                       completed line
v0.2.1  Payload Contract Model                                completed
v0.2.2  Payload Contract Release Alignment                    completed
v0.2.3  Mission Data Chain Roadmap Alignment                  completed
v0.3.0  Data Product and Storage Contracts                    completed
v0.4    Contact Windows and Downlink Flow Contracts           completed
v0.5    Commandability and Autonomy Contracts                 completed
v0.6    End-to-End Mission Data Flow Evidence                 next
v0.7    Generated Runtime Skeletons                           future
v0.8    Ground Integration Artifacts                          future
v0.9    Plugin and Extensibility Layer                        future
v1.0    Stable Mission Data Contract                          future
```

The immediate target is `v0.6 — End-to-End Mission Data Flow Evidence`.

Runtime skeleton generation remains deferred until the Mission Data Chain is coherent enough to generate useful artifacts from it.

---

## 4. Completed Baseline — v0.1 Mission Contract MVP

### 4.1 Objective

Demonstrate the complete OrbitFabric philosophy with one small, coherent, synthetic mission.

v0.1 proved that a user can:

1. define a mission once;
2. lint it semantically;
3. generate documentation;
4. execute an operational scenario;
5. receive readable logs and JSON reports.

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

The first demo payload vertical slice demonstrates:

```text
READY -> ACQUIRING -> READY
```

### 5.3 Boundary

Payload contracts may describe expected mission-data behavior.

They must not describe:

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

---

## 6. Completed Alignment — v0.2.2 Payload Contract Release Alignment

### 6.1 Objective

Capitalise on the completed Payload Contract Model vertical slice.

v0.2.2 made the repository, public documentation, roadmap, changelog, release notes and public communication consistent with the Payload Contract Model.

### 6.2 Completed Work

v0.2.2 aligned:

```text
README
public documentation
ROADMAP
CHANGELOG
release/version story
Payload Contract Model communication
```

### 6.3 Boundary

v0.2.2 was alignment work, not model expansion.

It did not introduce:

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

---

## 7. Completed Alignment — v0.2.3 Mission Data Chain Roadmap Alignment

### 7.1 Objective

Formalize the next architectural direction after the Payload Contract Model.

OrbitFabric should not jump directly from payload contracts to generated runtime skeletons.

The model must first express the mission data chain:

```text
Payload behavior
        -> data products
        -> onboard storage and retention
        -> downlink queue intent
        -> contact window assumptions
        -> commandability constraints
        -> autonomy and recovery expectations
        -> end-to-end scenario evidence
        -> future runtime and ground artifacts
```

### 7.2 Completed Work

v0.2.3 introduced:

```text
ROADMAP update
Project Charter alignment
ADR-0007 Mission Data Chain Before Runtime Generation
public documentation navigation update
issue backlog alignment
```

### 7.3 Boundary

v0.2.3 remained documentation-first and architecture-first.

It did not introduce:

```text
data_products.yaml
contacts.yaml
storage simulator behavior
downlink simulator behavior
new scenario semantics
runtime skeleton generation
ground export
plugin API
```

---

## 8. Completed Slice — v0.3.0 Data Product and Storage Contracts

### 8.1 Objective

Introduce data products as first-class mission data artifacts.

A telemetry item describes state or measurement.
A packet describes transport grouping.
A data product describes an object produced by the mission or payload.

Examples:

```text
image frame
radiation histogram
science sample batch
AIS capture window
IoT receiver burst
diagnostic dump
compressed payload product
```

### 8.2 Completed Capabilities

v0.3.0 introduced:

```text
Data Product and Storage Contract ADR
optional data_products.yaml domain
DataProductContract model
data product producer reference
optional payload reference
data product type
estimated size
priority
storage class
retention intent
overflow policy
downlink intent
data product semantic lint rules
generated data product documentation
invalid data product fixtures
synthetic demo mission data product
```

### 8.3 Implemented Lint Direction

The first data product lint slice covers:

```text
producer reference must be known
optional payload reference must be known
storage intent should define retention
storage intent should define overflow_policy
high-priority data product should define downlink intent
```

Structural validation covers:

```text
unique data product IDs
positive estimated size
known priority values
known storage class values
known overflow policy values
known downlink policy values
```

### 8.4 Boundary

v0.3.0 does not implement real storage, file systems, compression, payload processing pipelines, contact windows or downlink runtime behavior.

It describes contract intent only.

---

## 9. Completed Slice — v0.4.0 Contact Windows and Downlink Flow Contracts

### 9.1 Objective

Model contact windows and downlink flow assumptions without becoming a ground segment, an orbital dynamics simulator, an RF simulator or a downlink runtime.

OrbitFabric now lets a mission designer ask:

> Given the declared data products, priorities, storage policies, downlink intent and contact assumptions, is the mission data flow coherent?

### 9.2 Completed Capabilities

v0.4.0 introduced:

```text
ADR-0009 Contact Windows and Downlink Flow Contracts
Contact and Downlink Contract reference documentation
optional contacts.yaml domain
contact profile model
link profile model
contact window model
declared contact capacity assumption
downlink flow contract model
data product downlink eligibility
contact/downlink reference validation
minimal contact/downlink semantic lint rules
generated contact/downlink documentation
one synthetic demo contact/downlink slice
```

The implemented file is:

```text
mission/contacts.yaml
```

The file may contain contact profiles, link profiles, contact windows and downlink flow contracts.

### 9.3 Implemented Lint Direction

v0.4.0 introduced:

```text
OF-CON-001 contact window references unknown contact profile
OF-CON-002 contact window references unknown link profile
OF-DL-001  downlink flow references unknown contact profile
OF-DL-002  downlink flow references unknown link profile
OF-DL-003  downlink flow references unknown data product
OF-DL-004  high-priority data product has downlink intent but no eligible downlink flow
OF-DL-005  estimated data product volume may exceed declared contact capacity
```

Linting exposes ambiguity.

It does not schedule real downlink operations.

### 9.4 Generated Documentation

When contact/downlink contracts are present, OrbitFabric now generates:

```text
generated/docs/contacts.md
```

### 9.5 Demo Evidence

The synthetic `demo-3u` mission now demonstrates:

```text
Data Product Contract
        -> Storage Intent
        -> Downlink Intent
        -> Contact Window Assumption
        -> Downlink Flow Contract
```

### 9.6 Boundary

v0.4.0 does not implement:

```text
orbit propagation
TLE parsing
ground track computation
antenna pointing
RF link budgets
live ground links
real contact scheduling
real downlink execution
onboard downlink queues
file transfer protocols
CCSDS/PUS/CFDP implementation
Yamcs/OpenC3 services
real spacecraft operations
runtime skeleton generation
ground export generation
```

Contact windows and downlink flows are contract assumptions, not physical simulation or runtime behavior.

---
## 10. Completed Slice — v0.5.0 Commandability and Autonomy Contracts

### 10.1 Objective

Make command use and autonomous behavior explicit in the Mission Data Contract.

Commands should not only exist.

The model should express when they can be used, who or what may dispatch them, what they require and what evidence they should produce.

### 10.2 Completed Capabilities

```text
ADR-0010 Commandability and Autonomy Contracts
optional commandability.yaml domain
CommandSource model
CommandabilityRule model
AutonomousActionContract model
RecoveryIntent model
commandability/autonomy semantic lint rules
OF-CAB-* lint rule family
OF-AUT-* lint rule family
OF-REC-* lint rule family
generated commandability/autonomy documentation
generated commandability.md output
one synthetic demo commandability/autonomy slice
```

### 10.3 Boundary

v0.5 does not implement real command authentication, authorization, encryption, live uplink, operator consoles, command queues, onboard schedulers, autonomy runtime or real FDIR.

It defines commandability and autonomy contracts only.

---

## 11. Future Milestone — v0.6 End-to-End Mission Data Flow Evidence

### 11.1 Objective

Combine payload contracts, data products, storage intent, downlink assumptions, contact windows, commandability and recovery expectations into end-to-end scenario evidence.

The user should be able to inspect a data chain such as:

```text
payload acquisition
        -> data product generated
        -> stored onboard
        -> queued for downlink
        -> contact window available
        -> product downlinked, partially downlinked, retained or dropped
        -> ground-facing artifact prepared
        -> scenario evidence generated
```

### 11.2 Candidate Features

```text
mission data flow graph
scenario assertions on data product state
scenario assertions on storage state
scenario assertions on downlink state
generated mission data flow documentation
JSON data-flow evidence report
scenario coverage for data products
end-to-end demo scenario
```

### 11.3 Boundary

v0.6 must remain deterministic and contract-level.

It must not become real onboard storage software, a ground segment, a live simulator or an operations console.

---

## 12. Future Milestone — v0.7 Generated Runtime Skeletons

### 12.1 Objective

Start deriving onboard-oriented artifacts from the Mission Data Contract after the mission data chain model is sufficiently clear.

This is not flight software.
This is generated skeleton code that demonstrates how the Mission Data Contract can support future onboard runtime integration.

### 12.2 Candidate Features

```text
C++17 generated headers
generated telemetry IDs
generated command IDs
generated event IDs
generated mode IDs
generated packet IDs
generated payload IDs
generated data product IDs
generated storage policy enums
generated downlink policy enums
generated command argument structs
generated adapter interfaces
generated command dispatch skeleton
generated telemetry registry skeleton
generated data product registry skeleton
host-buildable CMake example
```

### 12.3 Required Boundary

v0.7 generated code must be described as:

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

---

## 13. Future Milestone — v0.8 Ground Integration Artifacts

### 13.1 Objective

Generate useful artifacts for ground integration without becoming a ground segment.

OrbitFabric should help external tools consume the Mission Data Contract.

### 13.2 Candidate Features

```text
JSON mission database export
packet dictionary export
simple decoder skeletons
telemetry dictionary export
command dictionary export
data product dictionary export
downlink policy export
Yamcs-like export prototype
OpenC3-like export prototype
XTCE exploration/prototype
```

### 13.3 Required Boundary

OrbitFabric may export artifacts for ground tools.
OrbitFabric must not become a ground tool.

No v0.8 feature should implement:

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

## 14. Future Milestone — v0.9 Plugin and Extensibility Layer

### 14.1 Objective

Turn OrbitFabric from a useful tool into an extensible framework.

v0.9 should introduce controlled extension points after the core mission data chain has matured.

### 14.2 Candidate Features

```text
custom lint rule plugins
custom generator plugins
custom data product validators
custom ground exporters
custom scenario step plugins
mission model extension mechanism
adapter SDK
plugin discovery
plugin metadata
example plugin
contribution guide
rule documentation generator
semantic versioning policy
```

### 14.3 Required Boundary

Plugins must extend OrbitFabric without breaking the core contract.

A plugin may consume or extend the Mission Model.
A plugin must not silently redefine core semantics.

---

## 15. Future Milestone — v1.0 Stable Mission Data Contract

### 15.1 Objective

v1.0 should be the first version where the Mission Data Contract is stable enough for external users to build around.

### 15.2 Possible v1.0 Requirements

```text
stable Mission Model schema
stable Payload Contract Model schema
stable Data Product Contract schema
stable Contact/Downlink Contract schema
stable Commandability Contract schema
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

### 15.3 v1.0 Should Not Require

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

## 16. Backlog Parking Lot

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

## 17. Priority Rules

When deciding what to implement next, use these rules.

### Rule 1 — Protect the Core Identity

If a feature weakens the Mission Data Contract identity, defer it.

### Rule 2 — Model Before Generator

If the model cannot express a concept cleanly, do not generate code for it.

### Rule 3 — Chain Before Runtime

If the mission data chain is not explicit, do not generate runtime skeletons from it.

### Rule 4 — Lint Before Runtime

If a behavior can be inconsistent, create a lint rule before creating downstream generators.

### Rule 5 — Docs from Model

If information exists in the model, generated docs should expose it.

### Rule 6 — No Hidden Semantics

If behavior matters, it must not live only in Python code.

### Rule 7 — No Private Examples

If an example resembles a private mission, remove or generalize it.

### Rule 8 — Small Working Slice Beats Broad Incomplete Scope

A working vertical slice is more valuable than multiple half-implemented integrations.

### Rule 9 — Payload Contracts Are Contracts

Payload contracts describe expected mission-data behavior.

They must not become payload firmware, payload drivers, hardware simulation or scientific processing pipelines.

### Rule 10 — Ground Assumptions Are Contracts

Contact windows, downlink budgets and ground-facing artifacts are model assumptions and derived outputs.

They must not become a live ground segment inside OrbitFabric.

---

## 18. Immediate Work Plan

The immediate work package is:

```text
v0.6 — End-to-End Mission Data Flow Evidence
```

Required sequence:

```text
1. define end-to-end mission data flow evidence scope
2. connect payload/data product/storage/downlink/contact assumptions into scenario evidence
3. keep storage and downlink behavior deterministic and contract-level
4. add scenario assertions for data product state where appropriate
5. generate mission data flow documentation or reports
6. update the synthetic demo mission with one clean end-to-end evidence slice
```

Do not add runtime skeletons before the mission data chain model is coherent.

Do not add ground exports before contact, downlink and data product contracts exist.

---
## 19. Final Roadmap Statement

OrbitFabric must first become excellent at one thing:

> defining, validating, simulating and documenting a Mission Data Contract for a small spacecraft.

The Payload Contract Model strengthens this mission by making mission-specific and IOD payload behavior explicit, lintable, documentable and scenario-aware.

The Data Product and Storage Contract Model strengthens the mission data chain by making payload and subsystem data products, storage intent and downlink intent explicit.

The v0.4 roadmap step completed the first Contact Windows and Downlink Flow Contract slice.

The v0.5 roadmap step completed the first Commandability and Autonomy Contract slice.

The next roadmap step is to produce end-to-end mission data flow evidence before runtime or ground artifacts are generated.

Only after the mission data chain, commandability, autonomy and end-to-end evidence contracts are clear should OrbitFabric grow into runtime skeleton generation, ground integration artifacts and plugin extensibility.

The narrowness of the roadmap is intentional.
That narrowness is a strength, not a limitation.
