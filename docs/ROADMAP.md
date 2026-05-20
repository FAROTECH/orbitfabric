# OrbitFabric - Roadmap

Version: v0.12.0 to v1.0 stability path  
Status: v1.0 candidate alignment  
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
- a payload runtime framework;
- a plugin execution platform.

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
        -> stable surface decision
        -> golden signatures for selected Core-owned surfaces
        -> demo evidence chain
        -> compatibility and migration posture
        -> stable Mission Data Contract
```

Every milestone must reinforce the core identity:

> OrbitFabric is a Mission Data Contract framework.

The current architectural objective is to keep the Mission Data Chain explicit, inspectable, compatibility-classified and safely extensible without turning OrbitFabric into flight software, a ground segment, a visual modeling tool or a plugin execution platform.

---

## 2. Roadmap Overview

```text
v0.1    Mission Contract MVP                                     completed
v0.2    Model Hardening                                          completed line
v0.2.1  Payload Contract Model                                   completed
v0.2.2  Payload Contract Release Alignment                       completed
v0.2.3  Mission Data Chain Roadmap Alignment                     completed
v0.3.0  Data Product and Storage Contracts                       completed
v0.4.0  Contact Windows and Downlink Flow Contracts              completed
v0.5.0  Commandability and Autonomy Contracts                    completed
v0.6.0  End-to-End Mission Data Flow Evidence                    completed
v0.7.0  Generated Runtime Skeletons                              completed
v0.8.0  Ground Integration Artifacts                             completed
v0.8.1  Contract Introspection Surface                           completed
v0.8.2  Entity Index Surface                                     completed
v0.9.0  Relationship Manifest Surface and Extensibility Boundary completed
v0.10.0 Stability and Compatibility Contract                     completed
v0.10.1 Documentation and Published Site Consistency             completed
v0.11.0 Extensibility Boundary Contract, no execution            completed
v0.12.0 v1.0 Release Candidate Hardening                         completed
v1.0.0  Stable Mission Data Contract                             next
```

The current completed released milestone is `v0.12.0 - v1.0 Release Candidate Hardening`.

The active unreleased alignment work is the v1.0 candidate stabilization path.

That path now includes:

```text
v1.0 Stable Surface Decision
v1.0 golden signatures for selected Core-owned structured surfaces
v1.0 Demo Evidence Chain
v1.0 Compatibility and Migration Notes aligned to the current candidate posture
```

The immediate target remains `v1.0.0 - Stable Mission Data Contract`.

This sequence is intentional. v0.8.1 exposed the first Core-owned domain-level introspection surface. v0.8.2 exposed the first Core-owned entity-level index surface. v0.9.0 introduced the first Core-owned relationship-level surface. v0.10.0 classified compatibility expectations around public and preview surfaces before v1.0. v0.10.1 verified documentation and published-site consistency. v0.11.0 defined the extensibility boundary without plugin execution. v0.12.0 hardened the release candidate path toward a stable Mission Data Contract. The v1.0 candidate alignment work now selects, protects, demonstrates and documents the narrow v1.0 posture before release.

The next step is not plugin execution. The next step is the stable Mission Data Contract release.

v1.0.0 should finalize the narrow stable surface selected from the existing Mission Data Contract core.

---

## 3. Completed Model and Mission Data Chain Slices

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

## 4. Completed Slice - v0.7.0 Generated Runtime Skeletons

v0.7.0 introduced generated runtime-facing contract bindings.

They expose identifiers, typed command argument structures, static metadata registries, abstract adapter interfaces and host-build smoke validation.

They intentionally do not implement flight-ready runtime, command dispatch runtime, command queues, telemetry polling runtime, event routing runtime, fault manager runtime, scheduler, HAL, drivers, RTOS abstraction, binary serialization, CCSDS/PUS/CFDP behavior, storage runtime, downlink runtime, user-code merge or protected regions.

---

## 5. Completed Slice - v0.8.0 Ground Integration Artifacts

v0.8.0 introduced generated ground-facing Mission Data Contract exports.

They expose deterministic JSON, CSV and Markdown artifacts for engineering review and downstream ground integration work.

They intentionally do not implement a live ground segment, mission control system, telemetry archive, telemetry database, command uplink service, Yamcs integration, OpenC3 integration, XTCE compliance, CCSDS/PUS/CFDP implementation, binary packet decoder, binary telecommand encoder, RF behavior, pass scheduling or station automation.

---

## 6. Completed Slice - v0.8.1 Contract Introspection Surface

v0.8.1 introduced `model_summary.json`, the first Core-owned read-only contract introspection surface.

It answers:

```text
What contract domains are present in this mission?
```

It intentionally did not introduce entity records, relationship manifests, relationship graphs, source locations, YAML AST export, plugin API, Studio-specific API, runtime behavior, ground behavior or new Mission Model semantics.

---

## 7. Completed Slice - v0.8.2 Entity Index Surface

v0.8.2 introduced `entity_index.json`, the first Core-owned read-only entity index surface.

It answers:

```text
What contract entities are defined in this mission?
```

It intentionally did not introduce new Mission Model semantics, relationship manifest export, relationship graph, dependency graph, source line or column tracking, YAML AST export, plugin API, plugin discovery, Studio-specific API, runtime behavior or ground behavior.

---

## 8. Completed Slice - v0.9.0 Relationship Manifest Surface and Extensibility Boundary

v0.9.0 introduced `relationship_manifest.json`, the first Core-owned read-only relationship manifest surface.

It answers:

```text
How are indexed mission contract entities related?
```

The current candidate surface admits nineteen deliberately narrow relationship families.

For `examples/demo-3u/mission`, the current manifest emits 46 relationship records across 17 emitted relationship families.

v0.9.0 intentionally did not introduce relationship inference, relationship graph, dependency graph, source line or column tracking, YAML AST export, plugin execution, plugin discovery, plugin loader, custom lint plugin support, custom generator plugin support, Studio-specific API, runtime behavior or ground behavior.

---

## 9. Completed Slice - v0.10.0 Stability and Compatibility Contract

v0.10.0 introduced the first stability and compatibility classification baseline before v1.0.

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

v0.10.0 intentionally did not introduce new Mission Model semantics, new YAML fields, new CLI behavior, new JSON report fields, new generated surfaces, new lint diagnostics, new scenario behavior, schema migration tooling, JSON Schema publication, plugin execution, plugin discovery, plugin loader, relationship graph, dependency graph, runtime behavior, ground behavior, Studio-specific API or a stable v1.0 compatibility guarantee.

---

## 10. Completed Slice - v0.10.1 Documentation and Published Site Consistency

v0.10.1 verified and preserved consistency between repository documentation and the published documentation site.

It clarified README wording around Relationship Manifest family counts and preserved the v0.10.0 compatibility baseline as the current compatibility foundation before v1.0.0.

v0.10.1 intentionally did not introduce new Mission Model semantics, new YAML fields, new CLI behavior beyond version reporting, new JSON report fields, new generated surfaces, new lint diagnostics, new scenario behavior, schema migration tooling, JSON Schema publication, plugin execution, plugin discovery, plugin loader, relationship graph, dependency graph, runtime behavior, ground behavior, Studio-specific API or a stable v1.0 compatibility guarantee.

---

## 11. Completed Slice - v0.11.0 Extensibility Boundary Contract, no execution

v0.11.0 defines the extensibility boundary without executing plugins.

It introduces:

```text
ADR-0015 - Extensibility Boundary Contract, No Execution
Extensibility Boundary Contract reference documentation
non-normative guidance for future descriptive extension metadata
explicit Core ownership rules
explicit extension ownership rules
provenance expectations for future extension-owned artifacts
semantic override ban
explicit downstream consumer rules
compatibility-sensitive extensibility boundary expectations before v1.0.0
```

The stable rule is:

```text
Mission Model remains the source of truth.
Core owns Mission Data Contract semantics.
Extensions consume Core-owned structured surfaces.
Extension-owned outputs remain distinguishable from Core-owned outputs.
Extensions must not override Core semantics.
Execution is out of scope.
```

v0.11.0 intentionally does not introduce new Mission Model semantics, new YAML fields, new CLI behavior beyond version reporting, new JSON report fields, new generated Core surfaces, new lint diagnostics, new scenario behavior, metadata schema, metadata parser, metadata loader, metadata validator, plugin discovery, plugin loading, plugin execution, custom lint plugin execution, custom generator plugin execution, relationship graph, dependency graph, runtime behavior, ground behavior, Studio-specific API, schema migration tooling, JSON Schema publication or a stable v1.0 compatibility guarantee.

---

## 12. Completed Slice - v0.12.0 v1.0 Release Candidate Hardening

v0.12.0 hardens the release candidate path toward v1.0.0.

It introduced these hardening references:

```text
v1.0 Candidate Surface Inventory
Golden Output and Regression Confidence Policy
v1.0 Compatibility and Migration Notes
```

Their role was to make the v1.0 path explicit before final stable release work.

They did not themselves decide the final v1.0 stable surface.

They did not add golden baselines, migration tooling, JSON Schema publication, generated Core surfaces or new Mission Model semantics.

v0.12.0 answered or explicitly deferred central stabilization questions before the project moved to v1.0.0 candidate alignment.

Security assumptions and command criticality contracts remain valid future explorations, but they are deferred beyond v1.0.0 unless separately scoped in a post-v1.0 milestone.

v0.12.0 intentionally does not broaden OrbitFabric into flight software, ground software, simulation runtime, visual modeling, plugin discovery, plugin loading or plugin execution.

---

## 13. Active v1.0 Candidate Alignment

The active v1.0 candidate alignment work prepares the final stable Mission Data Contract release.

It has already added:

```text
v1.0 Stable Surface Decision
v1.0 golden signatures for selected Core-owned structured surfaces
v1.0 Demo Evidence Chain
v1.0 Compatibility and Migration Notes aligned to the current candidate posture
```

This work does not change the package version and does not introduce new Mission Model semantics, YAML fields, CLI behavior, JSON report fields, generated artifact families, runtime behavior, ground behavior, plugin execution, schema migration tooling or JSON Schema publication.

It selects, protects, demonstrates and documents the narrow stable surface before the final v1.0.0 release alignment.

---

## 14. Next Milestone - v1.0.0 Stable Mission Data Contract

v1.0.0 should be the first version where the Mission Data Contract is stable enough for external users and downstream consumers to build around.

Selected stable surface candidates:

```text
Mission Model documented contract semantics
Core structural validation
Core semantic lint diagnostic policy
scenario YAML evidence inputs
lint JSON report
simulation JSON report
model_summary.json
entity_index.json
relationship_manifest.json for admitted families
CLI command interface for documented workflows
release compatibility policy
extensibility boundary contract
```

Surfaces that must remain preview or disposable unless explicitly promoted later:

```text
CLI textual output
generated Markdown mission documentation
plain-text simulation logs
generated C++17 runtime-facing bindings
generated ground-facing dictionaries
runtime_contract_manifest.json
ground_contract_manifest.json
```

The final v1.0.0 stable surface must remain narrow.

A surface listed as a candidate, preview or generated artifact before v1.0.0 does not become stable automatically.

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
plugin discovery
plugin loading
plugin execution
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
17. Boundary Before Execution.
18. Hardening Before Stability.
19. Stable Surface Decision Before v1.0 Release.
20. Golden Signatures Before Compatibility Claims.

---

## 17. Immediate Work Plan

The immediate work package is:

```text
v1.0.0 - Stable Mission Data Contract
```

Required next-step discipline:

```text
1. keep the final v1.0 stable surface narrow
2. keep generated runtime-facing and ground-facing artifacts preview/disposable unless explicitly promoted
3. keep plugin execution out of scope
4. keep security enforcement out of scope
5. keep JSON Schema publication and migration tooling out of scope
6. align documentation claims without broadening scope
7. prepare final v1.0.0 release alignment only after documentation and CI are clean
```

Do not start plugin execution, plugin discovery or plugin loader work in v1.0.0.

Do not introduce a Mission Model security domain, security YAML fields or security enforcement semantics in v1.0.0.

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

The v0.11.0 roadmap step completed the extensibility boundary contract without plugin execution.

The v0.12.0 roadmap step completed the release candidate hardening path to v1.0.0 without broadening the Core.

The v1.0 candidate alignment path selected, protected, demonstrated and documented the narrow stable Mission Data Contract posture before the final v1.0.0 release.

The narrowness of the roadmap is intentional.
That narrowness is a strength, not a limitation.
