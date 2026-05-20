# OrbitFabric - Project Charter

Version: 1.0.0  
Status: Stable Mission Data Contract released  
Scope: Mission Data Contract foundation, Core-owned structured surfaces, extensibility boundary and v1.0 stable surface

---

## 1. Project Vision

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

Its purpose is to let small spacecraft teams define mission data once, in a structured Mission Model, and then reuse that contract across validation, documentation, testing, scenario evidence, runtime-facing bindings, ground-facing artifacts, Core-owned structured surfaces and downstream inspection workflows.

OrbitFabric is not intended to be another flight software framework, another CubeSat tutorial, another ground segment tool, a payload runtime framework, a plugin execution platform, a plugin loader, a plugin discovery mechanism or a visual modeling backend.

It is the contract layer between mission design, onboard software, simulation, testing, documentation, runtime-facing integration, ground integration, downstream inspection tools and future extension-owned outputs.

The guiding principle is:

> Define once. Validate. Simulate. Test. Document. Integrate.

---

## 2. Current Status

OrbitFabric is currently released at:

```text
v1.0.0 - Stable Mission Data Contract
```

v1.0.0 stabilizes a deliberately narrow Core surface around the Mission Model, validation, linting, scenario evidence, machine-readable JSON reports, Core-owned structured surfaces, release compatibility governance and the extensibility boundary.

The stable surface is intentionally limited.

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
- stability and compatibility classifications;
- extensibility boundary rules;
- v1.0 stable Mission Data Contract governance references.

The Mission Data Contract is the single source of truth for all derived artifacts.

---

## 4. Problem Statement

Small spacecraft projects often suffer from mission data fragmentation.

The same information is commonly duplicated and reinterpreted across multiple places:

- onboard software structures;
- ground segment mission databases;
- test fixtures;
- manually written documentation;
- scripts;
- simulation setups;
- operational procedures;
- fault handling logic;
- payload-specific integration notes;
- storage and downlink planning notes;
- contact and pass assumptions;
- generated integration code;
- downstream inspection tools;
- extension-owned outputs.

This creates drift.

A command may be accepted by a simulator but rejected onboard. A telemetry field may exist in flight software but be missing in documentation. A fault may be described in a document but implemented differently in code. A payload may produce data products that have no storage policy, retention rule or downlink path. A downstream tool may infer contract semantics differently from the Core. A future extension may accidentally become a second semantic source if the ownership boundary is not explicit.

OrbitFabric addresses this by making the Mission Data Contract explicit, validated, executable as host-side scenario evidence, documented, reusable, introspectable, indexable, relatable, compatibility-classified, extensibility-bounded and protected through selected golden signatures.

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
- future extension authors who need a clear boundary between Core-owned semantics and extension-owned outputs.

The target is not purely educational.

OrbitFabric must be accessible to students and power makers, but designed with the architectural discipline expected from a serious open-source engineering framework.

---

## 6. Positioning

OrbitFabric does not compete directly with mature space software frameworks and tools.

Its position is deliberately different.

- NASA cFS is a reusable flight software framework.
- NASA F Prime is a component-based flight software and embedded systems framework.
- Yamcs and OpenC3 are primarily command, telemetry and mission-control-oriented ground frameworks.
- Basilisk is a spacecraft simulation framework.
- TASTE is a model-based engineering toolchain for embedded real-time systems.

OrbitFabric is a Mission Data Contract framework.

It should be able to export or integrate with other ecosystems in the future, but it must not try to replace them.

The correct long-term role is:

> OrbitFabric defines the mission data contract. Other systems may consume it.

---

## 7. Core Principles

### 7.1 Mission Model First

OrbitFabric starts from the Mission Model, not from the onboard runtime, the ground system, a plugin, an extension-owned output or a visual tool.

The Mission Model remains the source of truth.

### 7.2 Contract Before Code

The first valuable artifact is the contract.

Code generation, runtime-facing bindings, ground-facing artifacts, inspection surfaces, relationship surfaces, compatibility references, extension-owned outputs and integration bridges are secondary.

They must not redefine the model.

### 7.3 Core Surfaces Before Plugins

Downstream tools and future extensions must consume Core-owned structured surfaces.

They must not reconstruct Mission Data Contract semantics from raw YAML, generated files, terminal output, logs, UI state or private assumptions.

The current stable Core-owned structured surfaces are:

```text
model_summary.json
entity_index.json
relationship_manifest.json
```

### 7.4 Generated Artifacts Are Disposable Unless Classified Otherwise

Generated runtime-facing bindings, generated ground-facing artifacts, generated Markdown documentation and plain-text logs are reproducible outputs.

They are not the source of truth.

Users must not place handwritten implementation code inside generated files.

### 7.5 Compatibility Must Be Explicit

After v1.0.0, any change to a selected stable surface must include explicit compatibility or migration notes.

A surface does not become stable only because it exists.

### 7.6 Scenario Evidence Is Host-Side Contract Evidence

Operational scenarios must be first-class artifacts.

The simulator validates deterministic host-side contract behavior.

It is not a real-time onboard runtime or a spacecraft dynamics simulator.

---

## 8. v1.0 Stable Surface

The v1.0 stable surface is intentionally narrow.

It includes:

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

The following remain preview, disposable, internal or out of scope unless explicitly promoted later:

```text
CLI textual output
generated Markdown mission documentation
plain-text simulation logs
generated C++17 runtime-facing bindings
generated ground-facing dictionaries
runtime_contract_manifest.json
ground_contract_manifest.json
plugin discovery
plugin loading
plugin execution
relationship graph behavior
schema migration tooling
JSON Schema publication
security enforcement semantics
Studio-specific API
```

---

## 9. Non-Goals

OrbitFabric must not become:

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
- a Yamcs integration;
- an OpenC3 integration;
- an F Prime or cFS mapping layer;
- a relationship graph engine;
- a dependency graph engine;
- a plugin execution framework;
- a Studio-specific backend API;
- a schema migration tool;
- a JSON Schema publication layer;
- a security enforcement framework.

These may be valid future directions only after separate design, implementation and tests.

They are not part of the current Core charter.

---

## 10. Golden Signature Boundary

The v1.0 golden signatures protect selected contract-significant fields of existing Core-owned structured surfaces.

They protect:

```text
surface kind
surface version
mission identity
boundary flags
domain counts
entity identifiers
relationship family counts
selected relationship records
```

They do not freeze:

```text
full generated JSON files
absolute paths
human-oriented terminal output
Markdown wording
generated runtime bindings
generated ground dictionaries
disposable artifact formatting
```

---

## 11. Demo Evidence Chain

The selected v1.0 demo evidence chain is:

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
        -> golden signatures protecting selected Core-owned surface fields
```

This demonstrates Mission Data Contract continuity.

It does not demonstrate flight readiness, ground readiness, protocol compliance, tool-specific integration, security enforcement or operational completeness.

---

## 12. Final Charter Statement

OrbitFabric must remain excellent at one thing:

> defining, validating, simulating, documenting, introspecting, indexing, relating and generating contract-facing artifacts from a Mission Data Contract for a small spacecraft.

The narrowness of the charter is intentional.

That narrowness is a strength, not a limitation.
