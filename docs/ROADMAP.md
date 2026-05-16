# OrbitFabric - Roadmap

Version: v0.10.1 to v1.0 stability path  
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
        -> relationship manifest surfaces
        -> stability and compatibility contract
        -> documentation and published site consistency
        -> extensibility boundary contract
        -> release candidate hardening
        -> stable Mission Data Contract
```

Every milestone must reinforce the core identity:

> OrbitFabric is a Mission Data Contract framework.

The current architectural objective is to keep the Mission Data Chain explicit, inspectable and consumable by generated artifacts and downstream tools without turning OrbitFabric into flight software, a ground segment, a visual modeling tool or a plugin execution platform.

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
v0.9.0  Relationship Manifest Surface and Extensibility Boundary completed
v0.10.0 Stability and Compatibility Contract                  completed
v0.10.1 Documentation and Published Site Consistency          completed
v0.11.0 Extensibility Boundary Contract, no execution         next
v0.12.0 v1.0 Release Candidate Hardening                      future
v1.0.0  Stable Mission Data Contract                          future
```

The current completed milestone is `v0.10.1 - Documentation and Published Site Consistency`.

The immediate target after v0.10.1 is `v0.11.0 - Extensibility Boundary Contract, no execution`.

This sequence is intentional. v0.8.1 exposed the first Core-owned domain-level introspection surface. v0.8.2 exposed the first Core-owned entity-level index surface. v0.9.0 introduced the first Core-owned relationship-level surface. v0.10.0 classified the compatibility expectations around those public and preview surfaces before v1.0. v0.10.1 verified and preserved documentation and published-site consistency before the extensibility boundary work.

The next step is not plugin execution. The next step is to define the extensibility boundary without plugin execution.

v0.11.0 must not introduce plugin execution, plugin discovery, plugin loaders, relationship graphs, dependency graphs, runtime behavior, ground behavior, Studio-specific APIs or new Mission Model semantics unless explicitly scoped and reviewed.

Future extensibility must build on Core-owned structured surfaces without forcing plugins or downstream tools to reconstruct Mission Data Contract semantics from raw YAML, generated files, textual CLI output or UI state.

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

v0.8.2 intentionally did not introduce new Mission Model semantics, relationship manifest implementation, relationship graph, dependency graph, source line or column tracking, YAML AST export, plugin API, plugin discovery, Studio-specific API, runtime behavior or ground behavior.

---

## 9. Completed Slice - v0.9.0 Relationship Manifest Surface and Extensibility Boundary

v0.9.0 introduces the first Core-owned read-only relationship manifest surface.

It answers:

```text
How are indexed mission contract entities related?
```

The relationship manifest builds directly on `entity_index.json`.

The intended downstream chain is now:

```text
model_summary.json          -> domain navigation
entity_index.json           -> entity navigation
relationship_manifest.json  -> relationship navigation
```

v0.9.0 includes:

```text
relationship_manifest_to_dict(model, mission_dir)
write_relationship_manifest(model, mission_dir, output_file)
orbitfabric export relationship-manifest command
relationship_manifest.json report
manifest_version 0.1-candidate
kind orbitfabric.relationship_manifest
relationship records
relationship type records
relationship type counts
explicit derivation policy
explicit boundary flags
Relationship Manifest Surface reference documentation
ADR-0014 v0.9 plugin and relationship surface boundaries
v0.9.0 release notes
```

Command:

```bash
orbitfabric export relationship-manifest examples/demo-3u/mission/ \
  --json generated/reports/relationship_manifest.json
```

The current candidate surface admits nineteen deliberately narrow relationship families:

```text
autonomous_action_dispatches_command
command_emits_event
command_targets_subsystem
commandability_rule_constrains_command
data_product_produced_by_payload
data_product_produced_by_subsystem
downlink_flow_includes_data_product
event_sourced_from_subsystem
fault_emits_event
fault_sourced_from_subsystem
packet_includes_telemetry
payload_accepts_command
payload_belongs_to_subsystem
payload_generates_event
payload_may_raise_fault
payload_produces_telemetry
recovery_intent_reacts_to_event
recovery_intent_reacts_to_fault
telemetry_sourced_from_subsystem
```

For `examples/demo-3u/mission`, the current manifest emits 46 relationship records across 17 relationship families.

v0.9.0 intentionally does not introduce:

```text
relationship inference
relationship graph
dependency graph
source line or column tracking
YAML AST export
plugin execution
plugin discovery
plugin loader
custom lint plugin support
custom generator plugin support
Studio-specific API
runtime behavior
ground behavior
```

The relationship manifest is a candidate Core-owned surface. It is deterministic, read-only and derived from explicit loaded Mission Model fields. It is not a graph engine, visualization format, plugin API, Studio API, runtime routing table, ground routing table, scheduler input or command dispatcher input.

---

## 10. Completed Slice - v0.10.0 Stability and Compatibility Contract

v0.10.0 introduced the first stability and compatibility classification baseline before v1.0.

It defines how OrbitFabric treats public, preview, candidate, generated and internal surfaces.

The classification scope includes:

```text
Mission Model stability expectations
Core-owned generated surfaces
CLI command stability
JSON report compatibility expectations
lint rule code evolution
scenario evidence stability
release compatibility policy
```

v0.10.0 introduced these reference documents:

```text
Stability and Compatibility Contract
Mission Model Stability Contract
CLI Contract v1 Preview
Generated Surfaces Stability
Lint Rule Code Stability
JSON Report Compatibility
Scenario Evidence Stability
Release Compatibility Policy
v0.10.0 release notes
```

v0.10.0 intentionally does not introduce:

```text
new Mission Model semantics
new YAML fields
new model domains
new CLI behavior
new JSON report fields
new generated surfaces
new lint diagnostics
new scenario behavior
schema migration tooling
JSON Schema publication
plugin execution
plugin discovery
plugin loader
relationship graph
dependency graph
runtime behavior
ground behavior
Studio-specific API
stable v1.0 compatibility guarantee
```

---

## 11. Completed Slice - v0.10.1 Documentation and Published Site Consistency

v0.10.1 verified and preserved consistency between repository documentation and the published documentation site.

It ensured that the public documentation remains aligned with the released baseline and the roadmap toward v1.0.

It also clarified README wording around Relationship Manifest family counts:

```text
19 admitted relationship families at the candidate surface level
46 emitted relationship records for examples/demo-3u/mission
17 emitted relationship families for examples/demo-3u/mission
```

v0.10.1 intentionally does not introduce:

```text
new Mission Model semantics
new YAML fields
new model domains
new CLI behavior beyond version reporting
new JSON report fields
new generated surfaces
new lint diagnostics
new scenario behavior
schema migration tooling
JSON Schema publication
plugin execution
plugin discovery
plugin loader
relationship graph
dependency graph
runtime behavior
ground behavior
Studio-specific API
stable v1.0 compatibility guarantee
```

---

## 12. Next Milestone - v0.11.0 Extensibility Boundary Contract, no execution

v0.11.0 should define the extensibility boundary without executing plugins.

It may document what future extension metadata would be allowed to describe, but it must not introduce plugin discovery, plugin loading, plugin execution or arbitrary third-party code execution.

Plugins must never become a second source of Mission Data Contract semantics.

---

## 13. Future Milestone - v0.12.0 v1.0 Release Candidate Hardening

v0.12.0 should harden the release candidate path toward v1.0.0.

The focus should be consistency, documentation, validation coverage, release hygiene and removal of ambiguity before declaring a stable Mission Data Contract.

It should not broaden OrbitFabric into flight software, ground software, simulation runtime, visual modeling or plugin execution.

---

## 14. Future Milestone - v1.0.0 Stable Mission Data Contract

v1.0.0 should be the first version where the Mission Data Contract is stable enough for external users to build around.

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
stable relationship manifest surface
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

v1.0.0 should mean stable Mission Data Contract framework, not a complete space software ecosystem.

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
additional runtime generation profiles
example user implementation outside generated/
plugin metadata manifest
plugin capability manifest
custom lint plugin support
custom generator plugin support
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
11. Generated Code Is Disposable.
12. User Code Lives Outside `generated/`.
13. Tool-specific Claims Require Tests.
14. Core Surfaces Before Plugins.
15. Downstream Tools Consume, Not Infer.
16. Relationship Semantics Before Relationship Visualization.

---

## 17. Immediate Work Plan

The immediate work package after v0.10.1 is:

```text
v0.11.0 - Extensibility Boundary Contract, no execution
```

Required next-step discipline:

```text
1. define the extensibility boundary without executing plugins
2. preserve Core-owned structured surfaces as the only downstream semantic source
3. avoid runtime, ground, Studio-specific or plugin execution behavior
4. keep the Mission Model as the source of truth
5. keep downstream tools consuming Core-owned structured surfaces
```

Do not start plugin execution, plugin discovery or plugin loader work in v0.11.0.

Do not let plugins reconstruct contract semantics from raw YAML, generated files or human-oriented CLI output.

Do not let downstream tools become a second source of truth.

---

## 18. Final Roadmap Statement

OrbitFabric must first become excellent at one thing:

> defining, validating, simulating, documenting, introspecting, indexing, relating and generating contract-facing artifacts from a Mission Data Contract for a small spacecraft.

The v0.6 roadmap step completed the first end-to-end contract-level Mission Data Flow Evidence slice.

The v0.7 roadmap step completed the first runtime-facing contract binding slice.

The v0.8.0 roadmap step completed the first ground-facing contract export slice.

The v0.8.1 roadmap step completed the first Core-owned contract introspection surface.

The v0.8.2 roadmap step completed the first Core-owned entity index surface for downstream tools.

The v0.9.0 roadmap step completed the first Core-owned relationship manifest surface and preserved the plugin/extensibility boundary before plugin execution.

The v0.10.0 roadmap step completed the first stability and compatibility classification baseline before v1.0.

The v0.10.1 roadmap step completed the documentation and published-site consistency pass.

The v0.11.0 roadmap step should define the extensibility boundary without plugin execution.

Only after the mission data chain, commandability, autonomy, end-to-end evidence, runtime-facing binding layer, ground-facing artifact layer, contract introspection, entity indexing, relationship semantics and compatibility boundaries are clear should OrbitFabric consider plugin execution.

The narrowness of the roadmap is intentional.
That narrowness is a strength, not a limitation.
