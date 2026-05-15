# OrbitFabric - Project Charter

Version: 0.9.0 development baseline
Status: Draft
Scope: Mission Data Contract foundation, Mission Data Chain and generated contract-facing artifacts

---

## 1. Project Vision

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

Its purpose is to let small spacecraft teams define telemetry, commands, events, faults, operational modes, packets, payload contracts, data products, storage intent, downlink assumptions, commandability/autonomy assumptions, operational scenarios, runtime-facing contract bindings, ground-facing integration artifacts, Core-owned introspection surfaces, entity index surfaces and relationship manifest surfaces once, in a single mission contract, and then use that contract to validate consistency, generate documentation, run simulations, support tests and prepare integration and inspection artifacts for onboard, ground and downstream tooling.

OrbitFabric is not intended to be another flight software framework, another CubeSat tutorial, another ground segment tool, a payload runtime framework, a plugin execution platform or a visual modeling backend.

It is the contract layer between mission design, onboard software, simulation, testing, documentation, runtime-facing integration, ground integration and downstream inspection tools.

The guiding principle is:

> Define once. Validate. Simulate. Test. Document. Integrate.

---

## 2. Core Definition

OrbitFabric is a framework for defining and using a Mission Data Contract.

A Mission Data Contract describes, in a structured and machine-readable way:

- spacecraft identity and mission metadata;
- subsystems;
- telemetry;
- telecommands;
- events;
- faults;
- operational modes;
- mode transitions;
- packets;
- payload contracts;
- data products;
- persistence, storage and retention policies;
- downlink priorities and contact assumptions;
- commandability constraints;
- autonomy and recovery expectations;
- operational scenarios;
- validation and linting rules;
- runtime-facing generated contract bindings;
- ground-facing generated integration artifacts;
- Core-owned contract introspection surfaces;
- Core-owned entity index surfaces;
- Core-owned relationship manifest surfaces.

The Mission Data Contract is the single source of truth for all derived artifacts.

---

## 3. Problem Statement

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
- downstream inspection tools.

This creates drift.

A command may be accepted by a simulator but rejected onboard. A telemetry field may exist in flight software but be missing in documentation. A fault may be described in a document but implemented differently in code. A packet may exceed its expected size without being detected early. A mode may forbid an operation in principle, while the command router still accepts it in practice. A payload may produce data products that have no storage policy, retention rule or downlink path. A ground dictionary may describe data that the onboard design does not actually preserve or prioritize. A generated software boundary may diverge from the mission model it was supposed to represent. A downstream tool may infer contract semantics differently from the Core.

OrbitFabric addresses this by making the mission data model explicit, validated, executable, documented, reusable, introspectable, indexable and relatable through Core-owned structured surfaces.

---

## 4. Target Users

The initial target users are:

- advanced makers working on serious spacecraft-like systems;
- university CubeSat and PicoSat teams;
- aerospace students building mission software prototypes;
- embedded engineers entering the small spacecraft domain;
- small space startups and technical teams needing disciplined mission-data organization;
- research labs needing repeatable mission simulations and test scenarios;
- space software architects who need a coherent contract between payload behavior, onboard data handling and ground-facing artifacts;
- ground software engineers who need reviewable mission data dictionaries before integration starts;
- downstream tool builders who need stable Core-owned surfaces instead of reconstructing semantics from raw YAML.

The target is not purely educational.

OrbitFabric must be accessible to students and power makers, but designed with the architectural discipline expected from a serious open-source engineering framework.

---

## 5. Positioning

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

## 6. Core Principles

### 6.1 Mission Model First

OrbitFabric starts from the Mission Model, not from the onboard runtime, the ground system, a plugin or a visual tool.

The runtime-facing bindings, ground-facing artifacts, contract introspection reports, entity index reports, relationship manifest reports, simulator and documentation must be derived from the model, not the other way around.

### 6.2 Contract Before Code

The first valuable artifact is the contract.

Code generation, runtime execution, ground integration, inspection surfaces, relationship surfaces, entity surfaces and integration bridges are secondary and must not redefine the model.

### 6.3 Mission Data Chain Before Generated Artifacts

OrbitFabric must make the mission data chain explicit before generating software-facing, ground-facing, introspection, entity-index, relationship or plugin-facing artifacts.

The current chain is:

```text
payload behavior
        -> data products
        -> onboard storage and retention intent
        -> downlink queue intent
        -> contact window assumptions
        -> commandability constraints
        -> autonomy and recovery expectations
        -> end-to-end scenario evidence
        -> runtime-facing contract bindings
        -> ground-facing integration artifacts
        -> contract introspection surface
        -> entity index surface
        -> relationship manifest surface
```

Only after these concepts are sufficiently clear should OrbitFabric derive plugin, tool-specific or external integration layers from them.

### 6.4 Generated Artifacts Are Disposable

Generated runtime-facing contract bindings, ground-facing integration artifacts, contract introspection reports, entity index reports and relationship manifest reports are reproducible outputs.

They are not the source of truth.

Users must not place handwritten implementation code inside generated files.

User implementation code and downstream integration code must live outside `generated/` and integrate through generated identifiers, descriptors, typed structures, abstract interfaces, manifests, dictionaries or Core-owned reports.

### 6.5 Linting as Engineering Judgment

OrbitFabric linting must not be limited to YAML syntax validation.

It must perform mission consistency analysis.

The lint system is a core feature, not a utility.

### 6.6 Scenario-First Testing

Operational scenarios must be first-class artifacts.

A mission scenario should be expressible as structured data and executable by the simulator.

The simulator must be able to answer a practical engineering question:

> Given this mission model and this scenario, does the system behave as expected?

Scenarios provide evidence for mode transitions, command behavior, payload data production, storage intent, downlink assumptions, contact windows and recovery expectations.

### 6.7 Ground by Construction

OrbitFabric must not become a full ground segment.

However, it must generate artifacts useful for ground integration:

- generated review documentation;
- JSON ground dictionaries;
- CSV review dictionaries;
- packet membership dictionaries;
- data product dictionaries;
- downlink policy descriptions;
- future Yamcs/OpenC3/XTCE exports when explicitly implemented and tested.

### 6.8 Core Surfaces Before Plugins

Downstream tools must consume Core-owned structured surfaces.

They must not reconstruct Mission Model semantics from raw YAML, generated artifacts or human-oriented CLI output.

v0.8.1 introduces `model_summary.json` as the first such surface.

v0.8.2 introduces `entity_index.json` as the second such surface.

v0.9.0 introduces `relationship_manifest.json` as the third such surface.

Future plugin extensibility must build on these surfaces without silently redefining Core semantics.

### 6.9 Clean-Room Development

OrbitFabric must be developed from scratch using public knowledge, synthetic examples and generic engineering concepts.

It must not contain proprietary mission details, real non-public architectures, private protocols, real bus maps, real pinouts, real logs, real payload data or any information under NDA.

### 6.10 Small Core, Extensible Edges

The core must stay small.

Extensibility should come through plugins, generators, custom lint rules and adapters, not through a bloated core.

Plugin execution requires explicit trust, metadata and boundary design before arbitrary or untrusted plugin code is supported.

### 6.11 Practical Before Perfect

OrbitFabric must favor useful, testable, well-documented behavior over broad but shallow standard compliance.

CCSDS, PUS, CFDP, XTCE, Yamcs, OpenC3, cFS, F Prime and Basilisk integrations are future extensions, not early-version requirements.

---

## 7. Current Development Baseline

The current v0.9.0 development baseline includes:

- Mission Model YAML files;
- model loading;
- structural validation;
- semantic linting;
- generated Markdown documentation;
- deterministic host-side scenario simulation;
- scenario runner;
- payload contract model;
- data product contract model;
- contact/downlink contract model;
- commandability/autonomy contract model;
- end-to-end mission data flow evidence;
- RuntimeContract intermediate model;
- generated C++17 runtime-facing contract bindings;
- C++17 host-build smoke validation;
- GroundContract intermediate model;
- generated generic ground-facing dictionaries;
- generated JSON ground dictionaries;
- generated CSV ground dictionaries;
- generated ground Markdown review artifacts;
- Core-owned model summary export;
- Core-owned entity index export;
- Core-owned relationship manifest export;
- readable logs;
- JSON reports;
- one complete demo mission named `demo-3u`.

The current baseline supports these commands:

```bash
orbitfabric lint examples/demo-3u/mission/
orbitfabric export model-summary examples/demo-3u/mission/ --json generated/reports/model_summary.json
orbitfabric export entity-index examples/demo-3u/mission/ --json generated/reports/entity_index.json
orbitfabric export relationship-manifest examples/demo-3u/mission/ --json generated/reports/relationship_manifest.json
orbitfabric gen docs examples/demo-3u/mission/
orbitfabric gen data-flow examples/demo-3u/mission/
orbitfabric gen runtime examples/demo-3u/mission/
orbitfabric gen ground examples/demo-3u/mission/
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml
orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml
```

---

## 8. Ground Integration Artifact Direction

The Ground Integration Artifacts slice makes mission data visible to ground-side engineering workflows without turning OrbitFabric into ground software.

A ground artifact may describe telemetry identity and metadata, command identity, arguments and allowed modes, event identity and severity, fault identity and recovery intent metadata, data product identity, storage intent and downlink intent, packet membership, manifest boundary flags and human-reviewable dictionary documentation.

A ground artifact must not describe or implement live telemetry transport, binary packet decoding, command uplink, authentication or authorization, telemetry archive storage, operator displays, ground station scheduling, Yamcs/OpenC3/XTCE compatibility unless explicitly implemented and tested.

Ground artifacts are part of the Mission Data Contract output chain.

They are the foundation for later tool-specific exporters and plugin extensibility.

---

## 9. Contract Introspection, Entity Index and Relationship Manifest Direction

Core-owned structured surfaces make the loaded Mission Model visible to downstream tools without letting those tools infer Core semantics privately.

The v0.8.1 model summary report describes:

- mission identity;
- source mission directory;
- contract domains;
- domain counts;
- required or optional domain status;
- source file metadata;
- explicit boundary flags.

The v0.8.2 entity index report describes:

- mission identity;
- source mission directory;
- contract entities;
- entity IDs;
- entity domains;
- entity types;
- display names;
- source file metadata;
- explicit boundary flags.

The v0.9.0 relationship manifest report describes:

- mission identity;
- source mission directory;
- relationship records;
- relationship IDs;
- relationship types;
- source and target indexed entities;
- relationship type counts;
- derivation policy;
- explicit boundary flags.

These reports must not describe or implement:

- relationship graph execution;
- dependency graph execution;
- source line or column tracking;
- YAML AST export;
- plugin API;
- plugin execution;
- Studio-specific API;
- runtime behavior;
- ground behavior.

---

## 10. Mission Data Chain Direction

After the Payload Contract Model, OrbitFabric evolved toward explicit Mission Data Chain modeling.

The current chain is:

```text
Payload or subsystem activity
        -> generated telemetry and data products
        -> onboard storage and retention intent
        -> downlink queue and priority intent
        -> contact window assumptions
        -> commandability and autonomy constraints
        -> end-to-end scenario evidence
        -> runtime-facing contract bindings
        -> ground-facing integration artifacts
        -> contract introspection surface
        -> entity index surface
        -> relationship manifest surface
        -> future plugins
```

This direction is essential for small spacecraft and CubeSat missions because the value of mission data depends on the full path from onboard generation to ground consumption and downstream inspection.

OrbitFabric must model the contract of that path.

It must not implement the physical, flight or operational stack behind that path.

---

## 11. Early Non-Goals

Early OrbitFabric versions must not include:

- real spacecraft hardware support;
- real SPI/I2C/UART drivers;
- a complete onboard runtime;
- a flight-ready C++ runtime;
- RTOS integration;
- Linux onboard integration;
- CCSDS packet implementation;
- PUS implementation;
- CFDP implementation;
- CSP integration;
- SpaceWire integration;
- CANopen integration;
- cFS integration;
- F Prime integration;
- Yamcs integration as a live service;
- OpenC3 integration as a live service;
- XTCE compliance;
- telemetry archive implementation;
- operator console implementation;
- command uplink implementation;
- Basilisk integration as a dynamics simulator;
- formal verification;
- advanced security;
- real mission operations procedures;
- proprietary mission examples;
- payload firmware support;
- payload driver support;
- physical payload simulation;
- live ground operations;
- plugin APIs before Core-owned surfaces and plugin boundaries are stable;
- relationship graphs before entity indexing and relationship semantics are stable.

These items may become future integration targets, generated artifacts or external consumers only after the Mission Model, lint engine, scenario runner, mission data chain contracts and generated contract-facing artifacts prove valuable.

---

## 12. Demo Mission

The initial demo mission is `demo-3u`.

It is a synthetic 3U CubeSat-like mission used only to demonstrate OrbitFabric concepts.

It contains the full current Mission Data Chain from telemetry, commands, events, faults and modes through payload contracts, data products, contact/downlink assumptions, commandability/autonomy assumptions, data-flow evidence, runtime-facing contract bindings, ground-facing integration artifacts, contract introspection surface, entity index surface and relationship manifest surface.

The demo assumptions remain generic and do not encode private mission details, real ground station data, real orbit data or real RF behavior.

---

## 13. Initial Technical Direction

The recommended technical baseline is:

- Python 3.11 or newer;
- YAML for the Mission Model;
- Pydantic v2 for typed model validation;
- Typer for the command-line interface;
- PyYAML for YAML loading;
- pytest for tests;
- ruff for formatting and linting;
- MkDocs Material for documentation;
- C++17 for the first generated runtime-facing binding profile;
- CMake for host-build smoke validation;
- JSON, CSV and Markdown for the first generated ground-facing artifact package;
- JSON for Core-owned introspection, entity index and relationship manifest reports;
- GitHub Actions for CI;
- Apache-2.0 license.

The generated C++17 surface is intentionally contract-facing and host-buildable.

It is not a flight runtime.

The generated ground-facing package is intentionally tool-neutral and reviewable.

The generated model summary report is intentionally Core-owned and read-only.

The generated entity index report is intentionally Core-owned and read-only.

The generated relationship manifest report is intentionally Core-owned, read-only and candidate.

None is a relationship graph engine, plugin API, plugin execution mechanism or Studio-specific API.

---

## 14. Repository Philosophy

OrbitFabric should use a monorepo at the beginning.

The repository should contain:

- framework source code;
- documentation;
- examples;
- tests;
- generated artifact examples only when explicitly required;
- architectural decision records.

Initial repository structure:

```text
orbitfabric/
├── README.md
├── LICENSE
├── pyproject.toml
├── mkdocs.yml
├── docs/
├── examples/
├── src/
├── tests/
└── generated/
```

Splitting into multiple repositories too early would add complexity without architectural benefit.

---

## 15. Success Criteria for the Early Public Preview

OrbitFabric is successful in the early public preview if a user can:

1. inspect the `demo-3u` Mission Model;
2. run mission linting;
3. receive meaningful semantic errors and warnings;
4. run the battery degradation scenario;
5. see events, faults, mode transitions and auto-dispatched commands in the log;
6. generate Markdown documentation from the same Mission Model;
7. generate runtime-facing C++17 contract bindings from the same Mission Model;
8. validate those generated bindings through a host-side C++17 smoke build;
9. generate ground-facing JSON, CSV and Markdown artifacts from the same Mission Model;
10. export a Core-owned model summary report from the same Mission Model;
11. export a Core-owned entity index report from the same Mission Model;
12. export a Core-owned relationship manifest report from the same Mission Model;
13. understand the project positioning from the README in less than one minute;
14. extend the demo mission with one telemetry item, one command or one event without modifying the simulator internals;
15. understand how payload contracts fit into the Mission Data Contract;
16. understand how data products, storage intent, downlink intent, contact assumptions, commandability constraints, recovery expectations, runtime-facing bindings, ground-facing artifacts and Core-owned surfaces fit into the roadmap before plugin execution.

A minimal but strong preview is better than a broad, fragile and unfinished feature set.

---

## 16. Clean-Room Policy Summary

OrbitFabric must not use or encode non-public mission information.

Forbidden content includes:

- real non-public mission names;
- real proprietary subsystem architectures;
- real payload interfaces;
- real bus maps;
- real pinouts;
- real packet formats from private programs;
- real logs;
- real failure cases;
- real operational procedures;
- real data rates from private systems;
- proprietary code;
- proprietary documentation.

Allowed content includes:

- synthetic mission examples;
- public standards and public documentation;
- generic CubeSat concepts;
- abstract subsystem models;
- invented telemetry;
- invented commands;
- invented scenarios;
- invented data products;
- invented contact windows;
- clean-room code written from scratch.

If a design choice risks being too close to a private mission, it must be generalized or removed.

---

## 17. Governance Principles

Technical decisions should optimize for clarity, minimalism and architectural coherence.

The project should prefer:

- explicit models over implicit behavior;
- small examples over large fake missions;
- readable YAML over clever DSLs;
- deterministic simulation over realism;
- semantic lint rules over superficial validation;
- generated documentation over manually duplicated references;
- generated contract-facing artifacts over hidden implementation assumptions;
- Core-owned structured surfaces over downstream semantic inference;
- clean interfaces over premature integrations;
- mission data chain modeling before runtime-facing, ground-facing, introspection, entity indexing, relationship manifests and plugin generation.
