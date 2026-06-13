# OrbitFabric - Architecture

Version: 1.1.0  
Status: Current public release with v1.0.0 Stable Mission Data Contract baseline preserved  
Scope: Mission Data Contract architecture, stable Core-owned surfaces, post-v1 candidate integration surfaces and extensibility boundary

---

## 1. Architectural Intent

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

Its architecture is centered on one primary artifact:

> the Mission Data Contract.

The Mission Data Contract is expressed as a structured Mission Model.

The Mission Model remains the source of truth.

OrbitFabric validates that model, executes deterministic host-side scenario evidence, generates documentation, generates runtime-facing and ground-facing contract artifacts and exports Core-owned structured surfaces for downstream inspection.

The current public release is:

```text
v1.1.0 - Candidate Integration Surface Consolidation
```

The stable Mission Data Contract baseline remains:

```text
v1.0.0 - Stable Mission Data Contract
```

v1.1.0 consolidates a deliberately narrow set of post-v1 Core-owned candidate integration surfaces. It does not replace the v1.0.0 stable Mission Data Contract baseline.

---

## 2. Architectural Role

OrbitFabric is the contract layer between:

```text
mission design
onboard software
simulation
testing
documentation
runtime-facing integration
ground integration
downstream inspection tools
future extension-owned outputs
```

OrbitFabric is not designed as:

```text
flight software framework
ground segment
mission control system
operator console
telemetry archive
spacecraft dynamics simulator
payload runtime framework
CCSDS/PUS/CFDP implementation
hardware abstraction layer
visual modeling tool
Studio-specific backend API
plugin discovery mechanism
plugin loading mechanism
plugin execution platform
security enforcement framework
schema migration tooling
JSON Schema publication layer
tool-specific integration layer
```

Its architectural role is:

> define, validate, simulate, document, introspect, index, relate, classify, govern compatibility and generate contract-facing artifacts from one Mission Data Contract.

---

## 3. Architectural Principles

### 3.1 Mission Model First

The Mission Model is the source of truth.

Runtime-facing bindings, ground-facing artifacts, Core-owned structured surfaces, simulation evidence, generated documentation, compatibility classifications, extensibility rules, v1.0 references and post-v1 candidate surface references must derive from or describe the Mission Model.

No important mission behavior should live only in Python code, generated files, documentation, simulator internals, extension-owned outputs, plugin outputs or downstream tools.

### 3.2 Contract Before Runtime

OrbitFabric does not implement a flight runtime or a ground runtime.

It implements a host-side toolchain that proves and hardens the Mission Data Contract.

Generated runtime-facing artifacts are contract bindings, not onboard behavior.

Generated ground-facing artifacts are contract exports, not ground behavior.

Core-owned structured surfaces are inspection and integration surfaces, not runtime services.

### 3.3 Core Surfaces Before Plugins

Downstream tools and future extensions must consume Core-owned structured surfaces.

They must not reconstruct Mission Data Contract semantics from raw YAML, generated files, terminal output, logs, UI state or private assumptions.

The stable v1.0.0 Core-owned structured surface chain is:

```text
model_summary.json          -> What contract domains are present?
entity_index.json           -> What contract entities are defined?
relationship_manifest.json  -> How are indexed contract entities related?
```

The post-v1 candidate Core-owned integration surface chain consolidated in v1.1.0 is:

```text
dashboard_summary.json      -> Dashboard-ready aggregation of existing Core facts
scenario_run_index.json     -> Index of Core simulation JSON report runs
coverage_summary.json       -> Limited coverage derived from Core structured outputs
simulation JSON expectations -> Additive structured expectation accounting
```

These surfaces are derived from validated Core facts.

They are not a second source of truth.

The v1.1.0 candidate surfaces do not promote dashboard, coverage, scenario indexing or expectation accounting to the original v1.0.0 stable compatibility class.

### 3.4 Generated Artifacts Are Disposable Unless Classified Otherwise

Generated files are reproducible outputs.

Users must not place handwritten implementation code inside generated output directories.

The following remain disposable unless explicitly classified otherwise:

```text
generated Markdown documentation
generated runtime-facing bindings
generated ground-facing dictionaries
plain-text logs
disposable generated formatting
```

The v1.0 golden signatures protect selected contract-significant fields of existing Core-owned structured surfaces.

They do not freeze full generated JSON files, absolute paths, human-oriented output, Markdown wording, generated runtime bindings, generated ground dictionaries or disposable artifact formatting.

### 3.5 Compatibility Must Be Explicit

After v1.0.0, any change to a selected stable surface must include explicit compatibility or migration notes.

A surface is not stable only because it exists, is documented, appears in examples or is generated by CI.

A surface becomes stable only when the v1.0 decision or a later reviewed decision says so.

---

## 4. High-Level System View

```text
OrbitFabric
├── Mission Data Contract
│   ├── spacecraft
│   ├── subsystems
│   ├── modes
│   ├── telemetry
│   ├── commands
│   ├── events
│   ├── faults
│   ├── packets
│   ├── payload contracts
│   ├── data product contracts
│   ├── contact/downlink contracts
│   ├── commandability/autonomy contracts
│   ├── scenario evidence contracts
│   └── Core-owned structured-surface inputs
│
├── Toolchain
│   ├── orbitfabric inspect mission
│   ├── orbitfabric validate scenario
│   ├── orbitfabric lint
│   ├── orbitfabric gen docs
│   ├── orbitfabric gen data-flow
│   ├── orbitfabric gen runtime
│   ├── orbitfabric gen ground
│   ├── orbitfabric export model-summary
│   ├── orbitfabric export entity-index
│   ├── orbitfabric export relationship-manifest
│   ├── orbitfabric export dashboard-summary
│   ├── orbitfabric export scenario-run-index
│   ├── orbitfabric export coverage-summary
│   └── orbitfabric sim
│
├── Model Layer
├── Lint Layer
├── Scenario Evidence Layer
├── RuntimeContract Layer
├── GroundContract Layer
├── Export Layer
├── Generation Layer
├── Compatibility Governance Layer
└── Extensibility Boundary Layer
```

---

## 5. Current Capability Boundary

OrbitFabric currently includes:

```text
Mission Model YAML loading
canonical multi-file mission directory
structural validation
semantic lint
scenario loading and reference validation
host-side deterministic scenario execution
contract-level data-flow evidence recording
additive structured expectation accounting in simulation JSON
generated Markdown documentation
generated runtime-facing C++17 contract bindings
generated runtime host-build smoke target
generated ground-facing JSON, CSV and Markdown artifacts
model_summary.json export
entity_index.json export
relationship_manifest.json export
dashboard_summary.json export
scenario_run_index.json export
coverage_summary.json export
v1.0 stable surface decision
v1.0 golden signatures for selected Core-owned structured surfaces
v1.0 demo evidence chain
v1.0 compatibility and migration posture
v1.1 candidate integration surface consolidation
```

OrbitFabric currently does not include:

```text
flight runtime behavior
ground runtime behavior
telemetry polling runtime
command dispatcher
scheduler
HAL
drivers
binary telemetry decoder
binary telecommand encoder
CCSDS/PUS/CFDP implementation
XTCE export
Yamcs integration
OpenC3 integration
F Prime mapping
cFS mapping
relationship graph engine
dependency graph engine
plugin discovery
plugin loading
plugin execution
Studio-specific API
security enforcement semantics
schema migration tooling
JSON Schema publication
```

---

## 6. v1.0 Stable Surface

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

## 7. v1.1 Candidate Integration Surfaces

The v1.1.0 candidate integration surfaces are Core-owned read-only structured outputs:

```text
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
simulation JSON structured expectation accounting
```

They are intended for downstream inspection and documentation workflows.

They do not make OrbitFabric Core a dashboard backend, ground segment, Studio API, OpenOBSW/OpenSVF-specific generator, plugin system or graph engine.

They remain candidate until a later reviewed stability decision explicitly promotes them.

---

## 8. Demo Evidence Chain

The selected v1.0 demonstration chain is:

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

The v1.1.0 candidate surfaces add downstream inspection evidence on top of that chain.

It does not demonstrate flight readiness, ground readiness, protocol compliance, tool-specific integration, security enforcement or operational completeness.

---

## 9. Final Architecture Boundary

OrbitFabric Core must remain a Mission Data Contract framework.

The correct architectural statement is:

```text
Define the contract once.
Validate it.
Exercise scenario evidence.
Generate review artifacts.
Export Core-owned structured surfaces.
Protect selected stable surface fields with golden signatures.
Keep the Mission Model as the source of truth.
```

The architecture must not drift into flight software, a ground segment, a simulator platform, a plugin execution framework, a graph engine or a Studio backend.
