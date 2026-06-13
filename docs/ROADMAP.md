# OrbitFabric - Roadmap

Version: v1.1.0  
Status: Candidate Integration Surface Consolidation released  
Scope: completed path to v1.0.0, post-v1 candidate Core-owned integration surfaces and v1.1.0 consolidation direction

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

Every milestone must reinforce the core identity:

> OrbitFabric is a Mission Data Contract framework.

The v1.0.0 release completes the first stable narrow Mission Data Contract baseline.

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
v1.0.0  Stable Mission Data Contract                             completed
post-v1  Candidate Core-owned integration surfaces                completed
v1.1.0   Candidate surface consolidation release                  completed
```

The current completed milestone is:

```text
v1.1.0 - Candidate Integration Surface Consolidation
```

---

## 3. Completed Path to v1.0.0

The path to v1.0.0 established the following chain:

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

The v1.0.0 stable surface is intentionally narrow.

It stabilizes the Mission Data Contract core, not a full space software ecosystem.

---

## 4. v1.0.0 Stable Surface

The v1.0.0 stable surface includes:

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

The following remain preview, disposable or out of scope unless explicitly promoted later:

```text
CLI textual output
generated Markdown mission documentation
plain-text simulation logs
generated C++17 runtime-facing bindings
generated ground-facing dictionaries
runtime_contract_manifest.json
ground_contract_manifest.json
plugin execution
relationship graph behavior
schema migration tooling
JSON Schema publication
security enforcement semantics
Studio-specific API
```

---

## 5. Post-v1 Candidate Core-owned Integration Surfaces

After v1.0.0, OrbitFabric Core introduced a narrow set of candidate Core-owned integration surfaces:

```text
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
simulation JSON structured expectation accounting
```

These surfaces are intended to support downstream inspection without moving Mission Data Contract semantics into downstream tools.

The ownership rule is:

```text
Core defines, computes and emits.
Studio and other downstream tools consume, navigate and render.
Downstream tools must not invent private coverage, health or completeness semantics.
```

These surfaces remain candidate until a later compatibility decision promotes selected fields or surfaces.

They do not change the v1.0.0 stable Mission Data Contract.

They do not introduce:

```text
new Mission Model semantics
new YAML fields
runtime behavior
ground behavior
mission health scoring
model completeness scoring
formal verification
relationship graph behavior
dependency graph behavior
plugin execution
Studio-specific APIs
OpenOBSW/OpenSVF-specific generation
Projection Profiles implementation
OSRA/SAVOIR implementation
```

---

## 6. v1.1.0 Consolidation Direction

OrbitFabric Core v1.1.0 should be a consolidation release, not a conceptual expansion release.

The v1.1.0 preparation scope is:

```text
document candidate Core-owned integration surfaces
clarify stable vs candidate boundaries
keep generated artifact defaults mission-workspace relative
preserve explicit user-provided output paths
release notes and checklist added in the v1.1.0 release metadata PR
avoid Projection Profiles implementation until a separate RFC/design decision
```

---

## 7. Post-v1.0 Direction

Post-v1.0 work must preserve the same discipline:

```text
1. protect the Mission Model as source of truth
2. keep Core-owned semantics inside Core
3. keep generated artifacts reproducible and disposable unless explicitly promoted
4. require compatibility or migration notes for stable-surface changes
5. avoid tool-specific claims without implementation and tests
6. avoid plugin execution until a separate design accepts that scope
7. avoid security enforcement semantics until a separate design accepts that scope
```

Valid future work may include:

```text
additional golden signatures
additional mission examples
additional lint coverage
post-v1 compatibility refinements
JSON Schema publication, if separately designed
schema migration tooling, if separately designed
tool-specific exports, if implemented and tested
extension metadata, if kept descriptive and non-executing
plugin discovery/loading/execution, only after a separate architectural decision
```

---

## 8. Backlog Parking Lot

These ideas are valid but are not part of the v1.0.0 stable release boundary:

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

## 9. Final Roadmap Statement

OrbitFabric v1.0.0 stabilizes OrbitFabric Core as a Mission Data Contract framework.

The stable statement is:

```text
Define the contract once.
Validate it.
Exercise scenario evidence.
Generate review artifacts.
Export Core-owned structured surfaces.
Protect selected stable surface fields with golden signatures.
Keep the Mission Model as the source of truth.
```

The narrowness of the roadmap is intentional.

That narrowness is a strength, not a limitation.
