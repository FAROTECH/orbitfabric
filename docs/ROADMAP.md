# OrbitFabric - Roadmap

Version: v0.8.1  
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
        -> runtime-facing contract bindings
        -> ground integration artifacts
        -> contract introspection surfaces
        -> entity index surfaces
        -> plugins and extensibility
```

Every milestone must reinforce the core identity:

> OrbitFabric is a Mission Data Contract framework.

The current architectural objective is to keep the Mission Data Chain explicit, inspectable and consumable by generated artifacts and downstream tools without turning OrbitFabric into flight software, a ground segment or a visual modeling tool.

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
v0.7.0  Generated Runtime Skeletons                           completed
v0.8.0  Ground Integration Artifacts                          completed
v0.8.1  Contract Introspection Surface                        completed
v0.8.2  Entity Index Surface                                  next
v0.9    Plugin and Extensibility Layer                        planned
v1.0    Stable Mission Data Contract                          future
```

The immediate target after v0.8.1 is now `v0.8.2 - Entity Index Surface`.

This is intentional. Contract introspection and entity indexing are Core-owned, read-only surfaces required before plugins and downstream tools can safely consume the Mission Data Contract.

Ground integration artifacts remain downstream of the Mission Data Contract. v0.8.0 completed the first ground-facing contract export layer. v0.8.1 completed the first Core-owned domain-level introspection surface. v0.8.2 should expose the first Core-owned entity index before v0.9 introduces controlled extension points.

---

## 3. Completed Baseline - v0.1 Mission Contract MVP

v0.1 proved that a user can:

1. define a mission once;
2. lint it semantically;
3. generate documentation;
4. execute an operational scenario;
5. receive readable logs and JSON reports.

---

## 4. Completed Slice - v0.2.1 Payload Contract Model

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

## 5. Completed Alignment - v0.2.2 Payload Contract Release Alignment

v0.2.2 aligned README, public documentation, roadmap, changelog, release notes and public communication with the Payload Contract Model.

It did not introduce new model semantics.

---

## 6. Completed Alignment - v0.2.3 Mission Data Chain Roadmap Alignment

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

## 7. Completed Slice - v0.3.0 Data Product and Storage Contracts

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

## 8. Completed Slice - v0.4.0 Contact Windows and Downlink Flow Contracts

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

## 9. Completed Slice - v0.5.0 Commandability and Autonomy Contracts

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

## 10. Completed Slice - v0.6.0 End-to-End Mission Data Flow Evidence

v0.6.0 combined payload contracts, data products, storage intent, downlink assumptions, contact windows and command effects into deterministic scenario evidence.

It made this chain inspectable:

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

v0.6.0 did not implement real payload file generation, onboard storage runtime, downlink queues, contact scheduling, RF behavior, ground integration artifacts, CCSDS/PUS/CFDP runtime behavior or runtime skeleton generation.

---

## 11. Completed Slice - v0.7.0 Generated Runtime Skeletons

v0.7.0 introduced the first generated runtime-facing contract binding layer derived from the Mission Data Contract.

The public milestone name was:

```text
Generated Runtime Skeletons
```

The precise architectural meaning is:

```text
runtime-facing contract bindings
```

This is not flight software.

It is a generated software boundary that implementation code can include, compile and implement against outside `generated/`.

v0.7.0 introduced:

```text
RuntimeContract intermediate model
deterministic naming rules
deterministic generated numeric identifiers
orbitfabric gen runtime command
cpp17 generation profile
runtime_contract_manifest.json
generated IDs and enums
generated static metadata registries
generated command argument structs
generated abstract adapter interfaces
host-buildable CMake smoke target
host-build smoke source including all generated headers
Runtime Contract Bindings reference documentation
v0.7.0 release notes
```

v0.7.0 intentionally did not implement flight-ready runtime, command dispatch runtime, command queues, telemetry polling runtime, event routing runtime, fault manager runtime, scheduler, HAL, drivers, RTOS abstraction, binary serialization, CCSDS/PUS/CFDP behavior, storage runtime, downlink runtime, user-code merge or protected regions.

---

## 12. Completed Slice - v0.8.0 Ground Integration Artifacts

v0.8.0 introduced the first generated ground-facing artifact package derived from the Mission Data Contract.

The public milestone name is:

```text
Ground Integration Artifacts
```

The precise architectural meaning is:

```text
ground-facing Mission Data Contract exports
```

This is not a ground segment.

It is a deterministic, inspectable, tool-neutral artifact package that ground software teams can review, adapt or consume downstream.

v0.8.0 introduced:

```text
GroundContract intermediate model
orbitfabric gen ground command
generic generation profile
ground_contract_manifest.json
JSON telemetry dictionary
JSON command dictionary
JSON event dictionary
JSON fault dictionary
JSON data product dictionary
JSON packet dictionary
CSV telemetry dictionary
CSV command dictionary
CSV event dictionary
CSV fault dictionary
CSV data product dictionary
CSV packet dictionary
generated ground artifact README.md
generated ground_dictionaries.md review document
Ground Integration Artifacts reference documentation
ADR-0012 Ground Integration Artifacts Boundary
v0.8.0 release notes
```

v0.8.0 intentionally does not implement:

```text
live ground segment
mission control system
operator console
telemetry archive
telemetry database
command uplink service
telecommand transport
telemetry downlink runtime
network/session/routing behavior
command authentication or authorization
security enforcement
Yamcs integration
OpenC3 integration
XTCE compliance
CCSDS/PUS/CFDP implementation
binary packet decoder
binary telecommand encoder
offset/bitfield layout model
calibration model
RF/link-budget behavior
pass scheduling
station automation
```

---

## 13. Completed Slice - v0.8.1 Contract Introspection Surface

v0.8.1 introduced the first Core-owned read-only contract introspection surface.

The purpose is to let downstream tools ask:

```text
What contract domains are present in this mission?
```

This is answered by the Core, not by downstream tools parsing YAML, generated files or human-oriented CLI output.

v0.8.1 introduced:

```text
orbitfabric.export package
model_summary_to_dict(model, mission_dir)
write_model_summary(model, mission_dir, output_file)
orbitfabric export model-summary command
model_summary.json report
summary_version 0.1
kind orbitfabric.model_summary
contract domain records
domain-level counts
source file metadata
required/present status
explicit boundary flags
Contract Introspection Surface reference documentation
v0.8.1 release notes
```

Command:

```bash
orbitfabric export model-summary examples/demo-3u/mission/ \
  --json generated/reports/model_summary.json
```

v0.8.1 intentionally does not introduce:

```text
entity index
entity list
relationship manifest
relationship graph
source line or column tracking
YAML node location tracking
plugin mechanism
plugin API
Studio-specific API
scenario evidence duplication
generated artifact explorer
new Mission Model semantics
```

---

## 14. Next Slice - v0.8.2 Entity Index Surface

v0.8.2 should introduce a Core-owned read-only entity index surface.

The purpose is to let downstream tools ask:

```text
What contract entities are defined in this mission?
```

This surface must be built from the loaded and validated Mission Model, not from raw YAML scanning.

Candidate command:

```bash
orbitfabric export entity-index examples/demo-3u/mission/ \
  --json generated/reports/entity_index.json
```

Candidate output:

```text
entity_index.json
```

The initial surface should include:

```text
schema version
OrbitFabric Core version
mission identity
entities
domain
entity id
entity type
display name when available
source file
provenance
domain summary
```

v0.8.2 intentionally must not introduce:

```text
relationship graph
dependency graph
plugin API
plugin discovery
UI concerns
Studio-specific API
source line or column data unless the Core supports it reliably
semantic expansion beyond the real Mission Model
```

---

## 15. Planned Milestone - v0.9 Plugin and Extensibility Layer

v0.9 should introduce controlled extension points only after the Core exposes the required introspection and entity surfaces.

Candidate features:

```text
extension boundary documentation
public versus internal surface classification
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

Plugins must not bypass Mission Model loading, validation, linting or Core-owned structured surfaces.

Relationship manifests may be introduced in v0.9 only if the Core can derive them deterministically and without fragile heuristics.

Candidate relationship surface:

```text
relationship_manifest.json
```

The relationship manifest must remain partial or experimental if the Core does not yet own enough explicit relationship semantics.

---

## 16. Future Milestone - v1.0 Stable Mission Data Contract

v1.0 should be the first version where the Mission Data Contract is stable enough for external users to build around.

Possible requirements:

```text
stable Mission Model schema
stable Payload Contract Model schema
stable Data Product Contract schema
stable Contact/Downlink Contract schema
stable Commandability Contract schema
stable data-flow evidence semantics
stable RuntimeContract semantics
stable GroundContract semantics
stable contract introspection surface
stable entity index surface
stable runtime-facing contract binding surface
stable ground-facing artifact package
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

## 17. Backlog Parking Lot

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
relationship manifest
second payload example
payload lifecycle expansion
additional runtime generation profiles
example user implementation outside generated/
```

---

## 18. Priority Rules

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
11. Generated Code Is Disposable.
12. User Code Lives Outside `generated/`.
13. Tool-specific Claims Require Tests.
14. Core Surfaces Before Plugins.
15. Downstream Tools Consume, Not Infer.

---

## 19. Immediate Work Plan

The immediate work package is:

```text
v0.8.2 - Entity Index Surface
```

Required sequence:

```text
1. define entity index shape
2. keep the surface Core-owned and read-only
3. derive entity records from the loaded Mission Model
4. expose machine-readable JSON through an explicit export command
5. avoid relationship output until v0.9 or later
6. avoid plugin machinery until entity index semantics are clear
7. preserve the Mission Data Contract as source of truth
```

Do not add plugin machinery before the entity index surface is clear.

Do not let downstream tools reconstruct contract semantics from raw YAML, generated files or human-oriented CLI output.

---

## 20. Final Roadmap Statement

OrbitFabric must first become excellent at one thing:

> defining, validating, simulating, documenting, introspecting and generating contract-facing artifacts from a Mission Data Contract for a small spacecraft.

The v0.6 roadmap step completed the first end-to-end contract-level Mission Data Flow Evidence slice.

The v0.7 roadmap step completed the first runtime-facing contract binding slice.

The v0.8.0 roadmap step completed the first ground-facing contract export slice.

The v0.8.1 roadmap step completed the first Core-owned contract introspection surface.

The v0.8.2 roadmap step should add a stable Core-owned entity index surface for downstream tools.

Only after the mission data chain, commandability, autonomy, end-to-end evidence, runtime-facing binding layer, ground-facing artifact layer, contract introspection and entity indexing are clear should OrbitFabric grow into plugin extensibility.

The narrowness of the roadmap is intentional.
That narrowness is a strength, not a limitation.
