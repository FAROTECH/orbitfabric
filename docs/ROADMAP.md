# OrbitFabric — Roadmap

Version: v0.6.0  
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

The current architectural objective is to model the mission data chain from payload behavior to data products, onboard storage intent, downlink assumptions, contact windows, commandability, recovery behavior, evidence and future ground-facing artifacts.

---

## 2. Roadmap Overview

```text
v0.1    Mission Contract MVP                                  completed
v0.2    Model Hardening                                       completed line
v0.2.1  Payload Contract Model                                completed
v0.2.2  Payload Contract Release Alignment                    completed
v0.2.3  Mission Data Chain Roadmap Alignment                  completed
v0.3.0  Data Product and Storage Contracts                    completed
v0.4.0  Contact Windows and Downlink Flow Contracts           completed
v0.5.0  Commandability and Autonomy Contracts                 completed
v0.6.0  End-to-End Mission Data Flow Evidence                 completed
v0.7    Generated Runtime Skeletons                           next
v0.8    Ground Integration Artifacts                          future
v0.9    Plugin and Extensibility Layer                        future
v1.0    Stable Mission Data Contract                          future
```

The immediate target is now `v0.7 — Generated Runtime Skeletons`.

Runtime skeleton generation remains downstream of the Mission Data Chain. v0.6 completed the first contract-level evidence layer required before that step.

---

## 3. Completed Baseline — v0.1 Mission Contract MVP

v0.1 proved that a user can:

1. define a mission once;
2. lint it semantically;
3. generate documentation;
4. execute an operational scenario;
5. receive readable logs and JSON reports.

---

## 4. Completed Slice — v0.2.1 Payload Contract Model

v0.2.1 introduced the first narrow vertical slice for Payload / IOD Payload Contracts.

It added:

```text
optional payloads.yaml domain
PayloadContract model
minimal payload lifecycle model
payload semantic lint rules
generated payload contract documentation
payload-aware scenario behavior
```

Payload contracts may describe expected mission-data behavior.

They must not describe payload firmware, payload drivers, hardware buses, onboard runtime services, physical instrument simulation or scientific processing pipelines.

---

## 5. Completed Alignment — v0.2.2 Payload Contract Release Alignment

v0.2.2 aligned README, public documentation, roadmap, changelog, release notes and public communication with the Payload Contract Model.

It did not introduce new model semantics.

---

## 6. Completed Alignment — v0.2.3 Mission Data Chain Roadmap Alignment

v0.2.3 formalized the post-payload direction:

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

It remained architecture-first and documentation-first.

---

## 7. Completed Slice — v0.3.0 Data Product and Storage Contracts

v0.3.0 introduced data products as first-class mission data artifacts.

It added:

```text
optional data_products.yaml domain
DataProductContract model
data product producer reference
data product type
estimated size
priority
storage intent
retention intent
overflow policy
downlink intent
data product semantic lint rules
generated data product documentation
synthetic demo mission data product
```

v0.3.0 did not implement real storage, file systems, compression, payload processing pipelines, contact windows or downlink runtime behavior.

---

## 8. Completed Slice — v0.4.0 Contact Windows and Downlink Flow Contracts

v0.4.0 modeled contact windows and downlink flow assumptions without becoming a ground segment, an orbital dynamics simulator, an RF simulator or a downlink runtime.

It added:

```text
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

It did not implement real contact scheduling, real downlink execution, RF behavior, CCSDS/PUS/CFDP, Yamcs/OpenC3 services or runtime skeleton generation.

---

## 9. Completed Slice — v0.5.0 Commandability and Autonomy Contracts

v0.5.0 made command use and autonomous behavior explicit in the Mission Data Contract.

It added:

```text
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

v0.5.0 did not implement real command authentication, authorization, encryption, live uplink, operator consoles, command queues, onboard schedulers, autonomy runtime or real FDIR.

---

## 10. Completed Slice — v0.6.0 End-to-End Mission Data Flow Evidence

### 10.1 Objective

v0.6.0 combines payload contracts, data products, storage intent, downlink assumptions, contact windows and command effects into deterministic scenario evidence.

The objective is to make this chain inspectable:

```text
payload acquisition command
        -> data product declared as expected effect
        -> storage intent inspectable
        -> downlink intent inspectable
        -> eligible downlink flow inspectable
        -> matching contact window inspectable
        -> scenario evidence generated
        -> JSON evidence exported
        -> Markdown evidence documented
```

### 10.2 Completed Capabilities

v0.6.0 introduced:

```text
command expected_effects.data_products
OF-CMD-008 / OF-CMD-009 lint rules
simulation data-flow evidence records
JSON data_flow_evidence report output
scenario expect.data_flow assertions
OF-SCN-014 through OF-SCN-017 scenario reference checks
payload_data_flow_evidence demo scenario
generated data_flow.md documentation
orbitfabric gen data-flow command
data_flow.md included in standard orbitfabric gen docs output
```

### 10.3 Boundary

v0.6.0 remains deterministic and contract-level.

It does not implement:

```text
real payload file generation
real onboard storage runtime
real downlink queue execution
real contact scheduling
RF behavior
ground integration artifacts
CCSDS/PUS/CFDP runtime behavior
runtime skeleton generation
```

The milestone proves that the Mission Data Chain is explicit and inspectable, not that flight or ground runtime software exists.

---

## 11. Next Milestone — v0.7 Generated Runtime Skeletons

### 11.1 Objective

Start deriving onboard-oriented artifacts from the Mission Data Contract after the mission data chain model is sufficiently clear.

This is not flight software.

It is generated skeleton code that demonstrates how the Mission Data Contract can support future onboard runtime integration.

### 11.2 Candidate Features

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

### 11.3 Required Boundary

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

## 12. Future Milestone — v0.8 Ground Integration Artifacts

Generate useful artifacts for ground integration without becoming a ground segment.

Candidate features:

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

OrbitFabric may export artifacts for ground tools.

OrbitFabric must not become a ground tool.

---

## 13. Future Milestone — v0.9 Plugin and Extensibility Layer

v0.9 should introduce controlled extension points after the core mission data chain has matured.

Candidate features:

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

Plugins must extend OrbitFabric without silently redefining core semantics.

---

## 14. Future Milestone — v1.0 Stable Mission Data Contract

v1.0 should be the first version where the Mission Data Contract is stable enough for external users to build around.

Possible requirements:

```text
stable Mission Model schema
stable Payload Contract Model schema
stable Data Product Contract schema
stable Contact/Downlink Contract schema
stable Commandability Contract schema
stable data-flow evidence semantics
stable CLI commands
stable lint rule code policy
stable generated documentation format
stable JSON report format
migration guide from earlier model versions
complete demo mission
multiple example missions
published documentation site
CI-tested release artifacts
clear contribution process
```

v1.0 should mean stable Mission Data Contract framework, not a complete space software ecosystem.

---

## 15. Backlog Parking Lot

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

---

## 16. Priority Rules

When deciding what to implement next, use these rules.

1. Protect the Core Identity.
2. Model Before Generator.
3. Chain Before Runtime.
4. Lint Before Runtime.
5. Docs from Model.
6. No Hidden Semantics.
7. No Private Examples.
8. Small Working Slice Beats Broad Incomplete Scope.
9. Payload Contracts Are Contracts.
10. Ground Assumptions Are Contracts.

---

## 17. Immediate Work Plan

The immediate work package is:

```text
v0.7 — Generated Runtime Skeletons
```

Required sequence:

```text
1. define the minimal runtime skeleton scope
2. keep generated code downstream of the Mission Model
3. generate IDs/enums/registries before behavior-heavy runtime code
4. provide a host-buildable example
5. avoid claiming flight readiness
6. preserve the Mission Data Contract as source of truth
```

Do not add ground exports before runtime skeleton boundaries are clear.

Do not turn generated skeletons into a flight software framework.

---

## 18. Final Roadmap Statement

OrbitFabric must first become excellent at one thing:

> defining, validating, simulating and documenting a Mission Data Contract for a small spacecraft.

The v0.6 roadmap step completed the first end-to-end contract-level Mission Data Flow Evidence slice.

Only after the mission data chain, commandability, autonomy and end-to-end evidence contracts are clear should OrbitFabric grow into runtime skeleton generation, ground integration artifacts and plugin extensibility.

The narrowness of the roadmap is intentional.
That narrowness is a strength, not a limitation.
