# OrbitFabric — Project Charter

Version: 0.7
Status: Draft
Scope: Mission Data Contract foundation, Mission Data Chain and generated contract-facing artifacts

---

## 1. Project Vision

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

Its purpose is to let small spacecraft teams define telemetry, commands, events, faults, operational modes, packets, payload contracts, data products, storage intent, downlink assumptions, commandability/autonomy assumptions, operational scenarios and runtime-facing contract bindings once, in a single mission contract, and then use that contract to validate consistency, generate documentation, run simulations, support tests and prepare integration artifacts for onboard and ground systems.

OrbitFabric is not intended to be another flight software framework, another CubeSat tutorial, another ground segment tool or a payload runtime framework.

It is the contract layer between mission design, onboard software, simulation, testing, documentation and ground integration.

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
- runtime-facing generated contract bindings.

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
- generated integration code.

This creates drift.

A command may be accepted by a simulator but rejected onboard. A telemetry field may exist in flight software but be missing in documentation. A fault may be described in a document but implemented differently in code. A packet may exceed its expected size without being detected early. A mode may forbid an operation in principle, while the command router still accepts it in practice. A payload may produce data products that have no storage policy, retention rule or downlink path. A ground dictionary may describe data that the onboard design does not actually preserve or prioritize. A generated software boundary may diverge from the mission model it was supposed to represent.

OrbitFabric addresses this by making the mission data model explicit, validated, executable, documented and reusable.

---

## 4. Target Users

The initial target users are:

- advanced makers working on serious spacecraft-like systems;
- university CubeSat and PicoSat teams;
- aerospace students building mission software prototypes;
- embedded engineers entering the small spacecraft domain;
- small space startups and technical teams needing disciplined mission-data organization;
- research labs needing repeatable mission simulations and test scenarios;
- space software architects who need a coherent contract between payload behavior, onboard data handling and ground-facing artifacts.

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

OrbitFabric starts from the Mission Model, not from the onboard runtime.

The runtime-facing bindings, simulator, documentation and ground artifacts must be derived from the model, not the other way around.

### 6.2 Contract Before Code

The first valuable artifact is the contract.

Code generation, runtime execution and integration bridges are secondary and must not be designed before the model has sufficient clarity.

### 6.3 Mission Data Chain Before Runtime-Facing Bindings

OrbitFabric must make the mission data chain explicit before generating software-facing artifacts.

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
```

Only after these concepts are sufficiently clear should OrbitFabric derive ground integration artifacts from them.

### 6.4 Generated Code Is Disposable

Generated runtime-facing contract bindings are reproducible outputs.

They are not the source of truth.

Users must not place handwritten implementation code inside generated files.

User implementation code must live outside `generated/` and integrate through generated identifiers, descriptors, typed structures and abstract interfaces.

### 6.5 Linting as Engineering Judgment

OrbitFabric linting must not be limited to YAML syntax validation.

It must perform mission consistency analysis.

Examples:

- high-criticality telemetry without limits is an error;
- a command allowed in SAFE mode despite operational risk is an error;
- a fault emitting an unknown event is an error;
- a packet referencing unknown telemetry is an error;
- a command without timeout is at least a warning;
- an event without downlink priority is at least a warning;
- an incomplete data product storage intent is at least a warning;
- a high-priority data product without downlink intent is at least a warning;
- a contact profile referenced by downlink policy but missing from the model is an error.

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

- Markdown or HTML documentation;
- JSON mission database exports;
- packet descriptions;
- decoder skeletons;
- data product dictionaries;
- downlink policy descriptions;
- future Yamcs/OpenC3/XTCE exports.

### 6.8 Clean-Room Development

OrbitFabric must be developed from scratch using public knowledge, synthetic examples and generic engineering concepts.

It must not contain proprietary mission details, real non-public architectures, private protocols, real bus maps, real pinouts, real logs, real payload data or any information under NDA.

### 6.9 Small Core, Extensible Edges

The core must stay small.

Extensibility should come through plugins, generators, custom lint rules and adapters, not through a bloated core.

### 6.10 Practical Before Perfect

OrbitFabric must favor useful, testable, well-documented behavior over broad but shallow standard compliance.

CCSDS, PUS, CFDP, XTCE, Yamcs, OpenC3, cFS, F Prime and Basilisk integrations are future extensions, not early-version requirements.

---

## 7. Completed Early Scope

The current v0.7.0 baseline includes:

- Mission Model YAML files;
- model loading;
- structural validation;
- semantic linting;
- generated Markdown documentation;
- simple deterministic host-side scenario simulation;
- scenario runner;
- payload contract model;
- data product contract model;
- contact/downlink contract model;
- commandability/autonomy contract model;
- end-to-end mission data flow evidence;
- RuntimeContract intermediate model;
- generated C++17 runtime-facing contract bindings;
- C++17 host-build smoke validation;
- generated payload documentation;
- generated data product documentation;
- generated contact/downlink documentation;
- generated commandability/autonomy documentation;
- generated data-flow documentation;
- readable logs;
- JSON reports;
- one complete demo mission named `demo-3u`.

The current baseline supports these commands:

```bash
orbitfabric lint examples/demo-3u/mission/
orbitfabric gen docs examples/demo-3u/mission/
orbitfabric gen data-flow examples/demo-3u/mission/
orbitfabric gen runtime examples/demo-3u/mission/
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml
orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml
```

---

## 8. Payload Contract Direction

The Payload / IOD Payload Contract Model makes mission-specific payload behavior explicit without turning OrbitFabric into a payload runtime framework.

A payload contract may describe:

- payload identity;
- payload profile;
- linked subsystem;
- lifecycle states;
- telemetry references;
- command references;
- event references;
- fault references;
- command preconditions;
- expected effects;
- scenario-level behavior;
- generated documentation.

A payload contract must not describe:

- payload firmware;
- payload drivers;
- hardware buses;
- physical payload simulation;
- scientific data processing pipelines;
- real payload acquisition implementation.

Payload contracts are part of the Mission Data Contract.

They are the foundation for later data product, storage and downlink modeling.

---

## 9. Mission Data Chain Direction

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
        -> future ground artifacts
```

This direction is essential for small spacecraft and CubeSat missions because the value of mission data depends on the full path from onboard generation to ground consumption.

OrbitFabric must model the contract of that path.

It must not implement the physical, flight or operational stack behind that path.

---

## 10. Early Non-Goals

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
- Basilisk integration as a dynamics simulator;
- formal verification;
- advanced security;
- real mission operations procedures;
- proprietary mission examples;
- payload firmware support;
- payload driver support;
- physical payload simulation;
- live ground operations.

These items may become future integration targets, generated artifacts or external consumers only after the Mission Model, lint engine, scenario runner, mission data chain contracts and generated contract-facing artifacts prove valuable.

---

## 11. Demo Mission

The initial demo mission is `demo-3u`.

It is a synthetic 3U CubeSat-like mission used only to demonstrate OrbitFabric concepts.

It contains:

- OBC;
- EPS mock;
- Payload mock;
- Radio mock;
- operational modes:
  - BOOT;
  - NOMINAL;
  - PAYLOAD_ACTIVE;
  - DEGRADED;
  - SAFE;
  - MAINTENANCE;
- battery-voltage telemetry;
- payload acquisition state telemetry;
- payload start/stop commands;
- EPS status command;
- battery warning fault;
- battery critical fault;
- payload contract `demo_iod_payload`;
- data product contract `payload.radiation_histogram`;
- contact profile `primary_ground_contact`;
- link profile `uhf_downlink_nominal`;
- contact window `demo_contact_001`;
- downlink flow `science_next_available_contact`;
- command sources `ground_operator` and `onboard_autonomy`;
- commandability rule `payload_start_ground_rule`;
- autonomous actions for low/critical battery recovery assumptions;
- recovery intents toward DEGRADED and SAFE;
- one nominal payload acquisition scenario;
- one scenario where the payload is active, battery voltage degrades, a warning event is emitted, the spacecraft transitions to DEGRADED and the payload is automatically stopped;
- one scenario demonstrating contract-level data-flow evidence;
- generated runtime-facing contract bindings derived from the same model.

The expected battery-low scenario narrative is:

```text
[00:00] MODE=NOMINAL
[00:05] COMMAND payload.start_acquisition -> ACCEPTED
[00:05] EVENT payload.acquisition_started
[00:05] PAYLOAD demo_iod_payload LIFECYCLE=ACQUIRING
[00:32] EVENT eps.battery_low severity=WARNING
[00:32] MODE TRANSITION PAYLOAD_ACTIVE -> DEGRADED
[00:32] COMMAND payload.stop_acquisition -> AUTO_DISPATCHED
[00:32] PAYLOAD demo_iod_payload LIFECYCLE=READY
[00:40] SCENARIO PASSED
```

The demo also includes synthetic contact/downlink, commandability/autonomy, data-flow and runtime-binding slices.

Those assumptions remain generic and do not encode private mission details, real ground station data, real orbit data or real RF behavior.

---

## 12. Initial Technical Direction

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
- GitHub Actions for CI;
- Apache-2.0 license.

The generated C++17 surface is intentionally contract-facing and host-buildable.

It is not a flight runtime.

---

## 13. Repository Philosophy

OrbitFabric should use a monorepo at the beginning.

The repository should contain:

- framework source code;
- documentation;
- examples;
- tests;
- generated artifacts examples;
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

## 14. Success Criteria for the Early Public Preview

OrbitFabric is successful in the early public preview if a user can:

1. inspect the `demo-3u` Mission Model;
2. run mission linting;
3. receive meaningful semantic errors and warnings;
4. run the battery degradation scenario;
5. see events, faults, mode transitions and auto-dispatched commands in the log;
6. generate Markdown documentation from the same Mission Model;
7. generate runtime-facing C++17 contract bindings from the same Mission Model;
8. validate those generated bindings through a host-side C++17 smoke build;
9. understand the project positioning from the README in less than one minute;
10. extend the demo mission with one telemetry item, one command or one event without modifying the simulator internals;
11. understand how payload contracts fit into the Mission Data Contract;
12. understand how data products, storage intent, downlink intent, contact assumptions, commandability constraints, recovery expectations and runtime-facing bindings fit into the roadmap before ground artifacts.

A minimal but strong preview is better than a broad, fragile and unfinished feature set.

---

## 15. Clean-Room Policy Summary

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

## 16. Governance Principles

Technical decisions should optimize for clarity, minimalism and architectural coherence.

The project should prefer:

- explicit models over implicit behavior;
- small examples over large fake missions;
- readable YAML over clever DSLs;
- deterministic simulation over realism;
- semantic lint rules over superficial validation;
- generated documentation over manually duplicated references;
- generated contract-facing artifacts over hidden implementation assumptions;
- clean interfaces over premature integrations;
- mission data chain modeling before runtime-facing and ground-facing generation.

The project should reject:

- speculative feature expansion;
- premature standard compliance;
- hardware-specific shortcuts;
- hidden behavior not represented in the Mission Model;
- undocumented assumptions;
- private mission-derived examples;
- flight runtime generation from an immature model;
- ground integration exports before the contract they export is clear.

---

## 17. Final Position

OrbitFabric must remain a disciplined Mission Data Contract framework.

The project should not try to look large. It should try to be coherent.

The first versions must prove one thing convincingly:

> A small spacecraft mission can be described once, validated semantically, simulated operationally, tested through scenarios, documented automatically and exposed through generated contract-facing artifacts from a single source of truth.

The next versions must extend that proof to the ground-facing side:

> Payload behavior, data products, onboard storage intent, downlink priorities, contact assumptions, commandability constraints, recovery expectations and runtime-facing contract bindings can feed ground integration artifacts without duplicating or redefining the mission contract.

That is the core of OrbitFabric.
