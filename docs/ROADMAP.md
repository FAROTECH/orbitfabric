# OrbitFabric - Roadmap

Version: v0.8.2  
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
v0.8.2  Entity Index Surface                                  completed
v0.9    Plugin and Extensibility Layer                        next
v1.0    Stable Mission Data Contract                          future
```

The immediate target after v0.8.2 is now `v0.9 - Plugin and Extensibility Layer`.

This sequence is intentional. v0.8.1 exposed the first Core-owned domain-level introspection surface. v0.8.2 exposed the first Core-owned entity-level index surface. v0.9 can now introduce controlled extension points without forcing plugins or downstream tools to reconstruct Mission Data Contract semantics from raw YAML, generated files or human-oriented CLI output.

---

## 3. Completed Baseline - v0.1 Mission Contract MVP

v0.1 proved that a user can:

1. define a mission once;
2. lint it semantically;
3. generate documentation;
4. execute an operational scenario;
5. receive readable logs and JSON reports.

---

## 4. Completed Model and Mission Data Chain Slices

OrbitFabric has completed the following model and Mission Data Chain slices:

```text
v0.2.1  Payload Contract Model
v0.2.2  Payload Contract Release Alignment
v0.2.3  Mission Data Chain Roadmap Alignment
v0.3.0  Data Product and Storage Contracts
v0.4.0  Contact Windows and Downlink Flow Contracts
v0.5.0  Commandability and Autonomy Contracts
v0.6.0  End-to-End Mission Data Flow Evidence
```

Together, these slices formalized the chain:

```text
Payload behavior
        -> data products
        -> onboard storage and retention intent
        -> downlink queue intent
        -> contact window assumptions
        -> commandability constraints
        -> autonomy and recovery expectations
        -> end-to-end scenario evidence
```

They intentionally did not implement payload firmware, physical payload simulation, real onboard storage, real downlink execution, RF behavior, live command uplink, real FDIR or live spacecraft operations.

---

## 5. Completed Slice - v0.7.0 Generated Runtime Skeletons

v0.7.0 introduced the first generated runtime-facing contract binding layer derived from the Mission Data Contract.

The public milestone name was:

```text
Generated Runtime Skeletons
```

The precise architectural meaning is:

```text
runtime-facing contract bindings
```

v0.7.0 introduced:

```text
RuntimeContract intermediate model
orbitfabric gen runtime command
cpp17 generation profile
runtime_contract_manifest.json
generated IDs and enums
generated static metadata registries
generated command argument structs
generated abstract adapter interfaces
host-buildable CMake smoke target
Runtime Contract Bindings reference documentation
v0.7.0 release notes
```

v0.7.0 intentionally did not implement flight-ready runtime, command dispatch runtime, command queues, telemetry polling runtime, event routing runtime, fault manager runtime, scheduler, HAL, drivers, RTOS abstraction, binary serialization, CCSDS/PUS/CFDP behavior, storage runtime, downlink runtime, user-code merge or protected regions.

---

## 6. Completed Slice - v0.8.0 Ground Integration Artifacts

v0.8.0 introduced the first generated ground-facing artifact package derived from the Mission Data Contract.

The public milestone name is:

```text
Ground Integration Artifacts
```

The precise architectural meaning is:

```text
ground-facing Mission Data Contract exports
```

v0.8.0 introduced:

```text
GroundContract intermediate model
orbitfabric gen ground command
generic generation profile
ground_contract_manifest.json
JSON ground dictionaries
CSV ground dictionaries
generated ground artifact README.md
generated ground_dictionaries.md review document
Ground Integration Artifacts reference documentation
ADR-0012 Ground Integration Artifacts Boundary
v0.8.0 release notes
```

v0.8.0 intentionally did not implement a live ground segment, mission control system, telemetry archive, telemetry database, command uplink service, Yamcs integration, OpenC3 integration, XTCE compliance, CCSDS/PUS/CFDP implementation, binary packet decoder, binary telecommand encoder, RF behavior, pass scheduling or station automation.

---

## 7. Completed Slice - v0.8.1 Contract Introspection Surface

v0.8.1 introduced the first Core-owned read-only contract introspection surface.

It answers:

```text
What contract domains are present in this mission?
```

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

v0.8.1 intentionally did not introduce entity records, relationship manifests, relationship graphs, source locations, YAML AST export, plugin API, Studio-specific API, runtime behavior, ground behavior or new Mission Model semantics.

---

## 8. Completed Slice - v0.8.2 Entity Index Surface

v0.8.2 introduced the first Core-owned read-only entity index surface.

It answers:

```text
What contract entities are defined in this mission?
```

v0.8.2 introduced:

```text
entity_index_to_dict(model, mission_dir)
write_entity_index(model, mission_dir, output_file)
orbitfabric export entity-index command
entity_index.json report
index_version 0.1
kind orbitfabric.entity_index
entity-level records
per-domain entity counts
per-domain model counts
source file metadata
required/present domain status
indexed/not-indexed domain status
explicit boundary flags
Entity Index Surface reference documentation
v0.8.2 release notes
```

Command:

```bash
orbitfabric export entity-index examples/demo-3u/mission/ \
  --json generated/reports/entity_index.json
```

v0.8.2 intentionally does not introduce:

```text
new Mission Model semantics
relationship manifest
relationship graph
dependency graph
source line or column tracking
YAML AST export
plugin API
plugin discovery
Studio-specific API
runtime behavior
ground behavior
```

---

## 9. Next Milestone - v0.9 Plugin and Extensibility Layer

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

## 10. Future Milestone - v1.0 Stable Mission Data Contract

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

## 11. Backlog Parking Lot

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

## 12. Priority Rules

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

## 13. Immediate Work Plan

The immediate work package is:

```text
v0.9 - Plugin and Extensibility Layer
```

Required sequence:

```text
1. classify public versus internal Core surfaces
2. define plugin boundaries without allowing semantic override
3. define discovery and metadata rules
4. start with narrow, testable extension points
5. require plugins to consume loaded MissionModel or Core-owned structured surfaces
6. keep relationship manifests out unless they can be derived deterministically
7. preserve the Mission Data Contract as source of truth
```

Do not let plugins reconstruct contract semantics from raw YAML, generated files or human-oriented CLI output.

Do not let downstream tools become a second source of truth.

---

## 14. Final Roadmap Statement

OrbitFabric must first become excellent at one thing:

> defining, validating, simulating, documenting, introspecting and generating contract-facing artifacts from a Mission Data Contract for a small spacecraft.

The v0.6 roadmap step completed the first end-to-end contract-level Mission Data Flow Evidence slice.

The v0.7 roadmap step completed the first runtime-facing contract binding slice.

The v0.8.0 roadmap step completed the first ground-facing contract export slice.

The v0.8.1 roadmap step completed the first Core-owned contract introspection surface.

The v0.8.2 roadmap step completed the first Core-owned entity index surface for downstream tools.

Only after the mission data chain, commandability, autonomy, end-to-end evidence, runtime-facing binding layer, ground-facing artifact layer, contract introspection and entity indexing are clear should OrbitFabric grow into plugin extensibility.

The narrowness of the roadmap is intentional.
That narrowness is a strength, not a limitation.
