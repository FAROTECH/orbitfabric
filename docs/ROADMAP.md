# OrbitFabric - Roadmap

Version: v1.3.0 Adapter Management Foundation  
Status: v1.3.0 release baseline under final readiness review  
Scope: stable Mission Data Contract, stable Core integration input boundary, candidate Integration Framework contracts and candidate Adapter Management foundation

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
- an in-process plugin execution platform;
- a provider-specific package manager.

Every milestone must reinforce the core identity:

> OrbitFabric is a Mission Data Contract framework with explicit external integration and adapter lifecycle boundaries.

The v1.0.0 release completed the first stable narrow Mission Data Contract baseline.

The v1.1.0 release consolidated post-v1 Core-owned candidate inspection surfaces without replacing that baseline.

The v1.2.0 release consolidated the Core-owned integration input boundary proven through external reference adapters and independent Studio consumption, without adding Mission Model semantics.

The v1.3.0 release adds the first provider-neutral Adapter Management foundation while preserving those stable semantics and keeping provider-specific acquisition outside Core.

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
v1.2.0  Core Integration Input Consolidation                     completed
post-v1.2 Adapter Manager / Lock / Release Source / Catalog       completed / candidate productized
v1.3.0  Adapter Management Foundation                            release readiness
```

The release candidate baseline is:

```text
v1.3.0 - Adapter Management Foundation
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
in-process plugin execution
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

These surfaces remain candidate after v1.3.0 unless a separate compatibility decision promotes them.

They do not change the v1.0.0 stable Mission Data Contract.

---

## 6. Generic Integration Architecture Extraction - Completed

The OpenOBSW/OpenSVF PoC was used as an early forcing function to extract a generic production integration architecture rather than to add OpenOBSW-specific behavior to Core.

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

The reference package demonstrated real out-of-process adapter execution over the Core-owned input boundary. OrbitFabric Studio independently consumed the same generic package/result contracts.

The ownership split is explicit:

```text
Core                    Mission semantics + coherent integration inputs
Projection Profile      authored target-specific projection intent
Integration Adapter     target validation/projection/generation
Integration Result      explicit mappings/artifacts/diagnostics/provenance
Studio                  generic visualization/orchestration
```

Core does not import ecosystem-specific adapter implementation code in-process.

---

## 7. v1.2.0 Core Integration Input Consolidation

v1.2.0 converted the proven Core input side of that architecture into a stable compatibility boundary.

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

The Projection Profile, Integration Result and Integration Package / Adapter Execution contracts remain independently versioned candidate extension contracts rather than stable Core Mission Data Contract surfaces.

This prevents the stable Core input decision from silently widening Core ownership into ecosystem-specific semantics.

---

## 8. Post-v1.2 Operation-Input Contract Lane

The first versioned operation-input lane extends the external Integration Package contract without changing Core scenario semantics.

The candidate lane is:

```text
Integration Package Manifest 0.2-candidate
orbitfabric.adapter_cli.v1
Integration Result 0.2-candidate
```

It preserves the coherent Core Integration Input Set and Projection Profile as common context and allows zero or one required file-backed operation input.

The first contract-defined role is:

```text
scenario
```

Core owns the generic role/transport contract and conformance schemas. Target-specific scenario realization remains adapter-owned.

---

## 9. v1.3.0 Adapter Management Foundation

v1.3.0 adds the first candidate Core-owned lifecycle for exact external adapter releases.

### Adapter Manager M0

Core owns exact installation, inventory, inspection, verification, execution and removal semantics.

The first backend is:

```text
python-wheel-managed-env
```

Adapter code remains installed in a dedicated managed environment rather than imported into the Core process.

### Adapter Project Lock M1

Project Lock records exact desired adapter identity:

```text
Source Coordinate
exact release version
Release Descriptor SHA-256
artifact id
artifact SHA-256
installation backend id
```

Installed Adapter State remains separate user-scoped actual state.

### Explicit-source install-from-lock

An exact lock entry can be satisfied from already-available descriptor/artifact bytes through the same Core installation transaction.

`MATCH -> NOOP` is idempotent. Mismatching installed releases are not silently destroyed.

### Source-neutral Release Source attachment

Provider-specific acquisition is separated from Core lifecycle by:

```text
provider-specific Release Source
    -> verified local release bytes
    -> ResolvedAdapterRelease
    -> Core Project Lock lifecycle
```

GitHub/provider behavior remains outside Core.

### Provider-neutral Adapter Catalog

Core owns a minimal exact Catalog model and exact selector anchored by:

```text
Source Coordinate
+ exact release version
+ expected Release Descriptor SHA-256
```

The local Core CLI provides:

```text
orbitfabric adapter catalog validate
orbitfabric adapter catalog list
orbitfabric adapter catalog select
```

The Catalog does not introduce version ranges, `latest`, automatic updates or provider dispatch.

### Supported provider-explicit path

The accepted public consumer path is:

```text
Core Catalog CLI
    -> provider-specific Release Source
    -> ResolvedAdapterRelease
    -> Core Project Lock lifecycle
    -> Installed Adapter State
```

The first provider product is the separate GitHub Release Source. It depends on Core `>=1.3,<2` and remains outside Core.

The absence of a single provider-neutral install-from-Catalog command is deliberate. A universal provider registration/dispatch protocol is deferred until more than one materially different provider can justify the abstraction.

### Maturity

The v1.3 Adapter Management surfaces remain candidate unless separately promoted:

```text
Adapter Manager lifecycle
Adapter Release Descriptor 0.1-candidate
Adapter Project Lock 0.1-candidate
explicit-source install-from-lock
source-neutral resolved-release attachment
Adapter Catalog 0.1-candidate
Adapter Catalog CLI
```

A `1.3.0` package release does not make these surfaces part of the stable Mission Data Contract.

---

## 10. Post-v1.3 Direction

Post-v1 work must preserve the same discipline:

```text
1. protect the Mission Model as source of truth
2. keep Core-owned semantics inside Core
3. keep generated artifacts reproducible and disposable unless explicitly promoted
4. require compatibility or migration notes for stable-surface changes
5. avoid tool-specific claims without implementation and tests
6. keep provider-specific acquisition outside Core
7. keep ecosystem adapter implementation outside the Core process
8. distinguish Core-owned stable surfaces from candidate integration/lifecycle surfaces
9. promote surfaces only after real producer/consumer evidence and explicit regression protection
10. generalize provider dispatch only after materially different provider evidence exists
```

Valid future work may include:

```text
additional golden signatures
additional mission examples
additional lint coverage
post-v1 compatibility refinements
additional coverage analysis beyond the v1.1.0 candidate coverage_summary.json surface
schema migration tooling, if separately designed
tool-specific Integration Packages outside Core
additional provider-specific Release Sources
provider-neutral dispatch only after a second materially different provider
additional Studio integration contribution families after concrete forcing functions
```

---

## 11. Backlog Parking Lot

These ideas remain outside the stable Core boundary unless separately designed, implemented, tested and classified:

```text
XTCE export in Core
CCSDS packet generator
PUS service mapping in Core
CFDP metadata
Yamcs-specific semantics in Core
OpenC3-specific semantics in Core
Basilisk bridge
Space ROS bridge
F Prime-specific topology generation in Core
cFS-specific table/app generation in Core
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
Core in-process plugin discovery/loading/execution
provider-specific remote acquisition inside Core
latest/stable/range version solving
automatic adapter upgrades
```

---

## 12. Final Roadmap Statement

OrbitFabric v1.3.0 is the current release candidate baseline.

OrbitFabric v1.0.0 remains the origin of the stable Mission Data Contract commitment. v1.2.0 extended that stable boundary with the Core-owned integration input surfaces. v1.3.0 adds a candidate external adapter lifecycle without changing those stable semantics.

The architectural statement is:

```text
Define the contract once.
Validate it.
Exercise scenario evidence.
Generate review artifacts.
Export Core-owned structured surfaces.
Export one coherent Core Integration Input Set for external consumers.
Manage exact adapter desired/actual state through provider-neutral Core contracts.
Keep provider-specific acquisition and target-specific semantics outside Core.
Protect selected stable surface fields with golden signatures.
Keep the Mission Model as the source of truth.
```

The narrowness of the roadmap is intentional.

That narrowness is a strength, not a limitation.
