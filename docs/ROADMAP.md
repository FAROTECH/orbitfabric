# OrbitFabric - Roadmap

Version: v0.9.0  
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
        -> plugins and controlled extensibility
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
v1.0    Stable Mission Data Contract                          future
```

The current completed milestone is `v0.9.0 - Relationship Manifest Surface and Extensibility Boundary`.

This is the first v0.9 slice. It keeps the original `Plugin and Extensibility Layer` roadmap direction, but starts with the Core-owned relationship surface required before downstream tools or future plugins can safely reason about relationships.

This sequence is intentional. v0.8.1 exposed the first Core-owned domain-level introspection surface. v0.8.2 exposed the first Core-owned entity-level index surface. v0.9.0 introduces the first Core-owned relationship-level surface. Future plugin extensibility can build on these surfaces without forcing plugins or downstream tools to reconstruct Mission Data Contract semantics from raw YAML, generated files or human-oriented CLI output.

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

## 10. Deferred Plugin and Extensibility Work

The wider roadmap direction remains controlled plugin and extensibility support.

Candidate future features include:

```text
extension boundary documentation
public versus internal surface classification
plugin metadata manifest
plugin capability manifest
plugin-generated report manifest
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

These are not part of the current relationship manifest slice.

Plugins must extend OrbitFabric without silently redefining Core semantics.

Plugins must not bypass Mission Model loading, validation, linting or Core-owned structured surfaces.

Plugin execution requires explicit trust and security design before arbitrary or untrusted plugin code is supported.

---

## 11. Future Milestone - v1.0 Stable Mission Data Contract

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

v1.0 should mean stable Mission Data Contract framework, not a complete space software ecosystem.

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
additional runtime generation profiles
example user implementation outside generated/
plugin metadata manifest
plugin capability manifest
custom lint plugin support
custom generator plugin support
```

---

## 13. Priority Rules

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

## 14. Immediate Work Plan

The immediate work package after v0.9.0 is:

```text
post-v0.9.0 plugin and extensibility boundary planning
```

Required next-step discipline:

```text
1. keep relationship_manifest.json candidate and explicitly bounded
2. avoid plugin execution until trust and metadata boundaries are defined
3. avoid plugin loader, discovery and execution without reviewed design
4. keep downstream tools consuming Core-owned structured surfaces
5. prevent downstream tools from becoming a second source of truth
```

Do not let plugins reconstruct contract semantics from raw YAML, generated files or human-oriented CLI output.

Do not let downstream tools become a second source of truth.

---

## 15. Final Roadmap Statement

OrbitFabric must first become excellent at one thing:

> defining, validating, simulating, documenting, introspecting, indexing, relating and generating contract-facing artifacts from a Mission Data Contract for a small spacecraft.

The v0.6 roadmap step completed the first end-to-end contract-level Mission Data Flow Evidence slice.

The v0.7 roadmap step completed the first runtime-facing contract binding slice.

The v0.8.0 roadmap step completed the first ground-facing contract export slice.

The v0.8.1 roadmap step completed the first Core-owned contract introspection surface.

The v0.8.2 roadmap step completed the first Core-owned entity index surface for downstream tools.

The v0.9.0 roadmap step completed the first Core-owned relationship manifest surface and preserved the plugin/extensibility boundary before plugin execution.

Only after the mission data chain, commandability, autonomy, end-to-end evidence, runtime-facing binding layer, ground-facing artifact layer, contract introspection, entity indexing and relationship semantics are clear should OrbitFabric grow into plugin execution.

The narrowness of the roadmap is intentional.
That narrowness is a strength, not a limitation.
