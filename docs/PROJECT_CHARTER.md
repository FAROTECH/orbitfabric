# OrbitFabric - Project Charter

Version: 1.2.0 Core Integration Input Consolidation  
Status: Stable Mission Data Contract with stable Core integration input boundary  
Scope: Mission Data Contract foundation, Core-owned stable/candidate surfaces, external integration boundary, extensibility and compatibility governance

---

## 1. Project Vision

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

Its purpose is to let small spacecraft teams define mission data once, in a structured Mission Model, and reuse that contract across validation, documentation, testing, scenario evidence, runtime-facing bindings, ground-facing artifacts, Core-owned structured surfaces and downstream integration/inspection workflows.

OrbitFabric is not intended to be another flight software framework, another CubeSat tutorial, another ground segment tool, a payload runtime framework, a plugin execution platform or a visual modeling backend.

It is the contract layer between mission design, onboard software, simulation, testing, documentation, runtime-facing integration, ground integration, external ecosystem integrations and downstream inspection tools.

The guiding principle is:

> Define once. Validate. Simulate. Test. Document. Integrate.

---

## 2. Current Status

OrbitFabric is currently released at:

```text
v1.2.0 - Core Integration Input Consolidation
```

The stable Mission Data Contract commitment originated with `v1.0.0 - Stable Mission Data Contract`.

v1.2.0 extends that stable boundary additively with:

```text
mission_snapshot.json
Core Integration Input Set
seven additive stable-compatible FDIR Relationship Manifest families
```

No Mission Model semantics are added, removed, renamed or redefined by this release.

The v1.1.0 dashboard summary, scenario run index, coverage summary and structured expectation additions remain candidate.

The generic Projection Profile, Integration Result and Integration Package / Adapter Execution contracts remain independently versioned `0.1-candidate` extension contracts and do not become Core Mission Data Contract surfaces.

---

## 3. Core Definition

OrbitFabric is a framework for defining and using a Mission Data Contract.

A Mission Data Contract describes, in a structured and machine-readable way:

- spacecraft identity and mission metadata;
- subsystems;
- telemetry;
- telecommands;
- events;
- faults;
- operational modes;
- packets;
- payload contracts;
- data products;
- storage and retention intent;
- downlink priorities and contact assumptions;
- commandability constraints;
- autonomy and recovery expectations;
- operational scenarios;
- validation and linting rules;
- runtime-facing generated contract bindings;
- ground-facing generated integration artifacts;
- Core-owned structured surfaces;
- stable Core integration input contracts;
- stability and compatibility classifications;
- extensibility boundary rules.

The Mission Model is the semantic source of truth for all derived Core artifacts.

---

## 4. Problem Statement

Small spacecraft projects often suffer from mission data fragmentation.

The same information is commonly duplicated and reinterpreted across onboard software structures, ground databases, test fixtures, manually written documentation, scripts, simulation setups, operational procedures, fault handling logic, payload integration notes, storage/downlink planning, contact assumptions, generated integration code and downstream tools.

This creates drift.

A command may be accepted by a simulator but rejected onboard. A telemetry field may exist in flight software but be missing in documentation. A fault may be described in a document but implemented differently in code. A payload may produce data products that have no storage policy, retention rule or downlink path. A downstream integration may reconstruct Mission Data Contract semantics differently from Core if the machine-readable boundary is not explicit.

OrbitFabric addresses this by making the Mission Data Contract explicit, validated, executable as host-side scenario evidence, documented, reusable, introspectable, indexable, relatable and compatibility-governed.

---

## 5. Target Users

The initial target users are:

- advanced makers working on serious spacecraft-like systems;
- university CubeSat and PicoSat teams;
- aerospace students building mission software prototypes;
- embedded engineers entering the small spacecraft domain;
- small space startups and technical teams needing disciplined mission-data organization;
- research labs needing repeatable mission simulations and test scenarios;
- space software architects who need a coherent contract between payload behavior, onboard data handling and ground-facing artifacts;
- ground software engineers who need reviewable mission data dictionaries before integration starts;
- downstream tool builders who need stable Core-owned surfaces instead of reconstructing semantics from raw YAML;
- ecosystem integration authors who need a stable Core input boundary and explicit separation from target-specific semantics.

OrbitFabric must be accessible to students and power makers while retaining the architectural discipline expected from a serious open-source engineering framework.

---

## 6. Positioning

OrbitFabric does not compete directly with mature space software frameworks and tools.

- NASA cFS is a reusable flight software framework.
- NASA F Prime is a component-based flight software and embedded systems framework.
- Yamcs and OpenC3 are command, telemetry and mission-control-oriented ground frameworks.
- Basilisk is a spacecraft simulation framework.
- TASTE is a model-based engineering toolchain for embedded real-time systems.

OrbitFabric is a Mission Data Contract framework.

It may feed other ecosystems through external Integration Packages, but it must not try to replace them or absorb their semantics into Core.

The long-term role is:

> OrbitFabric defines the mission data contract. Other systems may consume it through explicit, versioned boundaries.

---

## 7. Core Principles

### 7.1 Mission Model First

OrbitFabric starts from the Mission Model, not from onboard runtime, ground system, an integration package, plugin, generated file or visual tool.

The Mission Model remains the semantic source of truth.

### 7.2 Contract Before Code

The first valuable artifact is the contract.

Code generation, runtime-facing bindings, ground-facing artifacts, inspection surfaces, relationship surfaces, integration inputs and extension-owned outputs are secondary and must not redefine the model.

### 7.3 Core Surfaces Before External Semantics

Downstream tools and integrations consume Core-owned structured surfaces.

They must not reconstruct Mission Data Contract semantics from raw YAML, generated files, terminal output, logs, UI state or private assumptions.

Stable Core-owned surfaces relevant to downstream integration include:

```text
mission_snapshot.json
model_summary.json
entity_index.json
relationship_manifest.json for admitted families
lint JSON report
Core Integration Input Set
```

Candidate Core-owned inspection surfaces include:

```text
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
simulation JSON structured expectation accounting
```

The Mission Snapshot exposes the complete loaded contract through a versioned, Core-owned read-only envelope. The coherent Integration Input Set composes the required Core roles through one load/lint operation with explicit compatibility/provenance.

Target-specific Projection Profiles and Integration Results remain extension-owned contracts.

### 7.4 Generated Artifacts Are Disposable Unless Classified Otherwise

Generated runtime-facing bindings, generated ground-facing artifacts, generated Markdown documentation and plain-text logs are reproducible outputs.

They are not the source of truth.

Users must not place handwritten implementation code inside generated files.

### 7.5 Compatibility Must Be Explicit

After v1.0.0, any change to a selected stable surface must include explicit compatibility or migration notes.

A surface does not become stable merely because it exists. v1.2.0 is an explicit reviewed promotion of the Mission Snapshot and coherent Integration Input Set responsibilities.

Additive relationship types must remain explicitly documented compatibility additions and must not be silently treated as a permanently closed enumeration.

### 7.6 Scenario Evidence Is Host-Side Contract Evidence

Operational scenarios are first-class artifacts.

The simulator validates deterministic host-side contract behavior. It is not a real-time onboard runtime or a spacecraft dynamics simulator.

---

## 8. Stable Core Surface

The v1.x stable Core surface includes:

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
mission_snapshot.json
Core Integration Input Set
documented stable CLI workflows
release compatibility policy
extensibility boundary contract
```

The Mission Snapshot and Integration Input Set retain their already reference-proven `0.1-candidate` format identifiers. Stability classification and format-version text are separate compatibility concepts.

---

## 9. Candidate Core Inspection and Extension Contracts

The following Core-owned inspection surfaces remain candidate after v1.2.0:

```text
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
simulation JSON structured expectation accounting
```

The following extension contracts also remain independently versioned `0.1-candidate` contracts:

```text
Projection Profile
Integration Result
Integration Package / Adapter Execution
```

The latter define how target-specific integrations sit beside Core; they are not target semantics inside Core.

---

## 10. Stable External Integration Boundary

The stable v1.2 input direction is:

```text
Mission Model
    ↓
OrbitFabric Core
    ↓
coherent Core Integration Input Set
    ↓
external Integration Package / Adapter
    ↓
Projection Profile + target-native artifacts + Integration Result
```

Core does not dynamically discover, load or execute ecosystem-specific adapters in-process.

An external adapter must negotiate documented surface kind/version identities, verify exact digests and set coherence, and reject missing/incompatible required surfaces.

Raw-YAML semantic fallback is forbidden.

---

## 11. Non-Goals

OrbitFabric Core must not become:

- a flight software framework;
- a ground segment;
- a mission control system;
- an operator console;
- a telemetry archive;
- a command uplink service;
- a spacecraft dynamics simulator;
- a hardware abstraction layer;
- a CCSDS/PUS/CFDP implementation;
- an XTCE mission database;
- a Yamcs or OpenC3 implementation;
- an F Prime or cFS implementation layer;
- a relationship graph engine;
- a dependency graph engine;
- an in-process ecosystem adapter runtime;
- a plugin execution framework;
- a Studio-specific backend API;
- a security enforcement framework.

These may be valid adjacent or future projects only after separate architecture, implementation and tests.

---

## 12. Golden Signature Boundary

Selected golden signatures protect contract-significant fields of stable Core-owned structured surfaces.

The original v1 golden signatures protect Model Summary, Entity Index and original Relationship Manifest family commitments.

v1.2 adds a selected Mission Snapshot golden signature covering envelope, boundary flags and representative serialization invariants.

Dedicated FDIR tests protect the seven additive stable-compatible relationship families while leaving the original v1 Relationship Manifest golden unchanged.

Golden signatures do not freeze complete generated JSON files, absolute paths, compatible additive Mission Model fields, human-oriented terminal output, Markdown wording, generated runtime bindings, generated ground dictionaries or disposable artifact formatting.

---

## 13. Demo and Integration Evidence Chain

The stable demo evidence chain includes:

```text
payload.start_acquisition
        -> payload.acquisition_started
        -> payload.radiation_histogram data product evidence
        -> storage intent declared
        -> downlink intent declared
        -> science_next_available_contact downlink flow
        -> demo_contact_001 contact window
        -> scenario JSON evidence
        -> runtime-facing contract bindings
        -> ground-facing dictionaries
        -> model_summary.json
        -> entity_index.json
        -> relationship_manifest.json
        -> mission_snapshot.json
        -> selected stable-surface golden signatures
```

The integration evidence additionally demonstrates:

```text
real Mission Model
    -> Core coherent Integration Input Set
    -> external OpenOBSW/OpenSVF reference adapter
    -> candidate Projection Profile / Integration Result contracts
    -> independent OrbitFabric Studio consumption
```

This proves architectural contract continuity, not flight readiness, ground readiness, protocol compliance or operational completeness.

---

## 14. Final Charter Statement

OrbitFabric must remain excellent at one thing:

> defining, validating, simulating, documenting, introspecting, indexing, relating and exporting explicit contract-facing surfaces from a Mission Data Contract for a small spacecraft.

The narrowness of the charter is intentional.

That narrowness is a strength, not a limitation.
