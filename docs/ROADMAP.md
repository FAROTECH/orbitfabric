# OrbitFabric - Roadmap

Version: v1.2.0 Core Integration Input Consolidation  
Status: v1.2.0 release baseline prepared from the reference-proven integration architecture  
Scope: stable Mission Data Contract, candidate downstream inspection surfaces, stable Core integration input boundary and post-v1 direction

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

The v1.0.0 release completed the first stable narrow Mission Data Contract baseline.

The v1.1.0 release consolidated post-v1 Core-owned candidate inspection surfaces without replacing that baseline.

The v1.2.0 release consolidates the Core-owned integration input boundary proven through the OpenOBSW/OpenSVF reference package and independent Studio consumption, without adding Mission Model semantics.

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
post-v1  Candidate Core-owned integration surfaces               completed
v1.1.0  Candidate surface consolidation release                  completed
post-v1.1 Mission Snapshot + additive FDIR relationships          completed / classified
Phase B  Generic Integration Framework contracts                 completed / reference-proven
v1.2.0  Core Integration Input Consolidation                     current release baseline
```

The current public release baseline is:

```text
v1.2.0 - Core Integration Input Consolidation
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
relationship_manifest.json for original admitted families
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
Studio-specific API
```

---

## 5. v1.1.0 Candidate Core-owned Integration Surfaces

OrbitFabric Core v1.1.0 consolidated a narrow set of candidate Core-owned inspection surfaces:

```text
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
simulation JSON structured expectation accounting
```

These surfaces support downstream inspection without moving Mission Data Contract semantics into downstream tools.

The ownership rule is:

```text
Core defines, computes and emits.
Studio and other downstream tools consume, navigate and render.
Downstream tools must not invent private coverage, health or completeness semantics.
```

These surfaces remain candidate after v1.2.0 unless a separate compatibility decision promotes them.

They do not change the v1.0.0 stable Mission Data Contract.

---

## 6. Integration Architecture Extraction — Completed

The OpenOBSW/OpenSVF PoC was used as a forcing function to extract a generic production integration architecture rather than to add OpenOBSW-specific behavior to Core.

The completed contract stack is:

```text
Core Integration Input Contract
        ↓
Projection Profile Contract
        ↓
Integration Package / Adapter Execution Contract
        ↓
Integration Result Contract
        ↓
generic downstream consumer
```

The reference package demonstrates real out-of-process adapter execution over the Core-owned input boundary. OrbitFabric Studio independently consumes the same generic package/result contracts.

The ownership split is explicit:

```text
Core                    Mission semantics + coherent integration inputs
Projection Profile      authored target-specific projection intent
Integration Adapter     target validation/projection/generation
Integration Result      explicit mappings/artifacts/diagnostics/provenance
Studio                  generic visualization/orchestration
```

Core still does not dynamically load or execute ecosystem-specific adapters.

---

## 7. v1.2.0 Core Integration Input Consolidation

v1.2.0 converts the proven Core input side of that architecture into a stable compatibility boundary.

### Stable Mission Snapshot

`mission_snapshot.json` is stable for its documented envelope, failure behavior and read-only complete-loaded-model role.

The existing `snapshot_version = 0.1-candidate` identifier is retained. Stability classification and format-version text are separate concepts.

The stable promise does not freeze the entire serialized `model` payload. That payload follows the Mission Model's own compatibility rules. A selected v1.2 golden signature protects contract-significant envelope and serialization invariants without blocking additive Mission Model evolution.

### Stable coherent Integration Input Set

The stable integration input workflow is:

```text
orbitfabric export integration-input-set <mission_dir>
```

It provides one coherent set containing required:

```text
mission_snapshot
entity_index
relationship_manifest
lint_report
```

and companion:

```text
model_summary
```

with explicit roles, states, format versions, SHA-256 digests, RFC 8785/JCS input-set fingerprinting and manifest-last completeness.

No raw-YAML semantic fallback is allowed for an incompatible required surface.

The existing `input_set_version = 0.1-candidate` identifier is retained to preserve compatibility with the reference-proven producer/consumer chain.

### Additive FDIR Relationship Manifest families

Seven explicit FDIR families are admitted as additive stable-compatible Relationship Manifest extensions. The original v1 golden signature remains fixed; dedicated FDIR tests protect the added families.

### Candidate extension contracts remain candidate

The following remain `0.1-candidate` extension contracts rather than stable Core Mission Data Contract surfaces:

```text
Projection Profile
Integration Result
Integration Package / Adapter Execution
```

This prevents the stable Core input decision from silently widening Core ownership into ecosystem-specific semantics or executable extension behavior.

---

## 8. Post-v1 Direction

Post-v1 work must preserve the same discipline:

```text
1. protect the Mission Model as source of truth
2. keep Core-owned semantics inside Core
3. keep generated artifacts reproducible and disposable unless explicitly promoted
4. require compatibility or migration notes for stable-surface changes
5. avoid tool-specific claims without implementation and tests
6. keep ecosystem adapter execution outside Core unless a separate architecture explicitly changes that rule
7. distinguish Core-owned stable surfaces from extension-owned candidate contracts
8. promote surfaces only after real producer/consumer evidence and explicit regression protection
```

Valid future work may include:

```text
additional golden signatures
additional mission examples
additional lint coverage
post-v1 compatibility refinements
additional coverage analysis beyond the v1.1.0 candidate coverage_summary.json surface
JSON Schema publication where owned by an explicit contract
schema migration tooling, if separately designed
tool-specific Integration Packages outside Core
additional Studio integration contribution families after concrete forcing functions
plugin discovery/loading/execution only after a separate architectural decision
```

---

## 9. Backlog Parking Lot

These ideas remain outside the stable v1.2 Core boundary unless separately designed, implemented, tested and classified:

```text
XTCE export in Core
CCSDS packet generator
PUS service mapping in Core
CFDP metadata
Yamcs integration in Core
OpenC3 integration in Core
Basilisk bridge
Space ROS bridge
F Prime topology generator
cFS table/app generator
web dashboard
visual mission model editor
SARIF lint export
VS Code extension
general Core JSON Schema registry
schema migration tool
simulation time acceleration
fault tree visualization
mode transition graph rendering
requirements traceability
advanced coverage metrics beyond coverage_summary.json
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
Core plugin discovery
Core plugin loading
Core plugin execution
```

---

## 10. Final Roadmap Statement

OrbitFabric v1.2.0 is the current release baseline.

OrbitFabric v1.0.0 remains the origin of the stable Mission Data Contract commitment; v1.2.0 extends that stable boundary additively with the Core-owned integration input surfaces proven after v1.1.0.

The stable statement is:

```text
Define the contract once.
Validate it.
Exercise scenario evidence.
Generate review artifacts.
Export Core-owned structured surfaces.
Export one coherent Core Integration Input Set for external consumers.
Protect selected stable surface fields with golden signatures.
Keep the Mission Model as the source of truth.
Keep target-specific semantics and execution outside Core.
```

The narrowness of the roadmap is intentional.

That narrowness is a strength, not a limitation.
