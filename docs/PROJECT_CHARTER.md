# OrbitFabric — Project Charter

Version: 0.1-draft  
Status: Draft  
Scope: MVP foundation  

---

## 1. Project Vision

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

Its purpose is to let small spacecraft teams define telemetry, commands, events, faults, operational modes, packets and operational scenarios once, in a single mission contract, and then use that contract to validate consistency, generate documentation, run simulations, support tests and prepare integration artifacts for onboard and ground systems.

OrbitFabric is not intended to be another flight software framework, another CubeSat tutorial or another ground segment tool.

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
- persistence and downlink policies;
- operational scenarios;
- validation and linting rules.

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
- payload-specific integration notes.

This creates drift.

A command may be accepted by a simulator but rejected onboard. A telemetry field may exist in flight software but be missing in documentation. A fault may be described in a document but implemented differently in code. A packet may exceed its expected size without being detected early. A mode may forbid an operation in principle, while the command router still accepts it in practice.

OrbitFabric addresses this by making the mission data model explicit, validated, executable and reusable.

---

## 4. Target Users

The initial target users are:

- advanced makers working on serious spacecraft-like systems;
- university CubeSat and PicoSat teams;
- aerospace students building mission software prototypes;
- embedded engineers entering the small spacecraft domain;
- small space startups and technical teams needing disciplined mission-data organization;
- research labs needing repeatable mission simulations and test scenarios.

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

The runtime, simulator, documentation and ground artifacts must be derived from the model, not the other way around.

### 6.2 Contract Before Code

The first valuable artifact is the contract.

Code generation, runtime execution and integration bridges are secondary and must not be designed before the model has sufficient clarity.

### 6.3 Linting as Engineering Judgment

OrbitFabric linting must not be limited to YAML syntax validation.

It must perform mission consistency analysis.

Examples:

- high-criticality telemetry without limits is an error;
- a command allowed in SAFE mode despite operational risk is an error;
- a fault emitting an unknown event is an error;
- a packet referencing unknown telemetry is an error;
- a command without timeout is at least a warning;
- an event without downlink priority is at least a warning.

The lint system is a core feature, not a utility.

### 6.4 Scenario-First Testing

Operational scenarios must be first-class artifacts.

A mission scenario should be expressible as structured data and executable by the simulator.

The simulator must be able to answer a practical engineering question:

> Given this mission model and this scenario, does the system behave as expected?

### 6.5 Ground by Construction

OrbitFabric must not become a full ground segment.

However, it must generate artifacts useful for ground integration:

- Markdown or HTML documentation;
- JSON mission database exports;
- packet descriptions;
- decoder skeletons;
- future Yamcs/OpenC3/XTCE exports.

### 6.6 Clean-Room Development

OrbitFabric must be developed from scratch using public knowledge, synthetic examples and generic engineering concepts.

It must not contain proprietary mission details, real non-public architectures, private protocols, real bus maps, real pinouts, real logs, real payload data or any information under NDA.

### 6.7 Small Core, Extensible Edges

The core must stay small.

Extensibility should come through plugins, generators, custom lint rules and adapters, not through a bloated core.

### 6.8 Practical Before Perfect

OrbitFabric must favor useful, testable, well-documented behavior over broad but shallow standard compliance.

CCSDS, PUS, CFDP, XTCE, Yamcs, OpenC3, cFS, F Prime and Basilisk integrations are future extensions, not v0.1 requirements.

---

## 7. MVP v0.1 Scope

The goal of v0.1 is to demonstrate the complete OrbitFabric philosophy with a small but coherent vertical slice.

v0.1 must include:

- Mission Model YAML files;
- model loading;
- structural validation;
- semantic linting;
- generated Markdown documentation;
- simple simulation runtime;
- scenario runner;
- mock EPS subsystem;
- mock Payload subsystem;
- minimal telemetry registry;
- minimal command router;
- minimal event bus;
- minimal mode manager;
- minimal fault monitor;
- readable logs;
- JSON reports;
- one complete demo mission named `demo-3u`.

v0.1 must support these commands:

```bash
orbitfabric lint examples/demo-3u/mission/
orbitfabric gen docs examples/demo-3u/mission/
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml
```

---

## 8. MVP v0.1 Non-Goals

v0.1 must not include:

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
- Yamcs integration;
- OpenC3 integration;
- Basilisk integration;
- formal verification;
- advanced security;
- real mission operations procedures;
- proprietary mission examples.

These items may become future work only after the Mission Model, lint engine and scenario runner prove valuable.

---

## 9. Demo Mission

The initial demo mission is `demo-3u`.

It is a synthetic 3U CubeSat-like mission used only to demonstrate OrbitFabric concepts.

It contains:

- OBC;
- EPS mock;
- Payload mock;
- optional Radio mock;
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
- one scenario where the payload is active, battery voltage degrades, a warning event is emitted, the spacecraft transitions to DEGRADED and the payload is automatically stopped.

The expected scenario narrative is:

```text
[00:00] MODE=NOMINAL
[00:05] COMMAND payload.start_acquisition -> ACCEPTED
[00:06] EVENT payload.acquisition_started
[00:30] INJECT eps.battery.voltage=6.7
[00:33] EVENT eps.battery_low severity=WARNING
[00:35] MODE TRANSITION PAYLOAD_ACTIVE -> DEGRADED
[00:36] COMMAND payload.stop_acquisition -> AUTO_DISPATCHED
[00:37] EVENT payload.acquisition_stopped
[00:40] SCENARIO PASSED
```

---

## 10. Initial Technical Direction

The recommended technical baseline for v0.1 is:

- Python 3.11 or newer;
- YAML for the Mission Model;
- Pydantic v2 for typed model validation;
- Typer for the command-line interface;
- PyYAML or ruamel.yaml for YAML loading;
- pytest for tests;
- ruff for formatting and linting;
- MkDocs Material for documentation;
- GitHub Actions for CI;
- Apache-2.0 license.

The future onboard runtime may use C++17, but C++ generation is explicitly out of scope for v0.1.

---

## 11. Repository Philosophy

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

## 12. Success Criteria for v0.1

OrbitFabric v0.1 is successful if a user can:

1. inspect the `demo-3u` Mission Model;
2. run mission linting;
3. receive meaningful semantic errors and warnings;
4. run the battery degradation scenario;
5. see events, faults, mode transitions and auto-dispatched commands in the log;
6. generate Markdown documentation from the same Mission Model;
7. understand the project positioning from the README in less than one minute;
8. extend the demo mission with one telemetry item, one command or one event without modifying the simulator internals.

A minimal but strong v0.1 is better than a broad, fragile and unfinished v0.1.

---

## 13. Clean-Room Policy Summary

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
- clean-room code written from scratch.

If a design choice risks being too close to a private mission, it must be generalized or removed.

---

## 14. Governance Principles

Until the project reaches a usable v0.1, technical decisions should optimize for clarity, minimalism and architectural coherence.

The project should prefer:

- explicit models over implicit behavior;
- small examples over large fake missions;
- readable YAML over clever DSLs;
- deterministic simulation over realism;
- semantic lint rules over superficial validation;
- generated documentation over manually duplicated references;
- clean interfaces over premature integrations.

The project should reject:

- speculative feature expansion;
- premature standard compliance;
- hardware-specific shortcuts;
- hidden behavior not represented in the Mission Model;
- undocumented assumptions;
- private mission-derived examples.

---

## 15. Immediate Next Artifacts

After this Project Charter, the next required artifacts are:

```text
docs/CLEAN_ROOM_POLICY.md
docs/ROADMAP.md
docs/ARCHITECTURE.md
docs/adr/ADR-0001-mission-model-first.md
docs/adr/ADR-0002-python-toolchain-first.md
docs/adr/ADR-0003-yaml-multifile-mission-model.md
docs/adr/ADR-0004-no-flight-runtime-in-v0.1.md
docs/adr/ADR-0005-lint-as-core-feature.md
docs/reference/mission-model-v0.1.md
```

The next highest-priority artifact is:

```text
docs/adr/ADR-0001-mission-model-first.md
```

---

## 16. Final Position

OrbitFabric must begin as a disciplined Mission Data Contract framework.

The project should not try to look large. It should try to be coherent.

The first version must prove one thing convincingly:

> A small spacecraft mission can be described once, validated semantically, simulated operationally, tested through scenarios and documented automatically from a single source of truth.

That is the core of OrbitFabric.

