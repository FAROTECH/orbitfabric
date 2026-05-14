# Changelog

All notable changes to OrbitFabric will be documented in this file.

This project follows a lightweight pre-1.0 changelog style while the Mission Model, contract layers, generated artifacts and CLI stabilize.

---

## [Unreleased]

### Next

- Prepare `v0.9 - Plugin and Extensibility Layer` as the next controlled extension milestone after Core-owned introspection and entity index surfaces.

---

## [v0.8.2] - Entity Index Surface

### Added

- Added `entity_index_to_dict(model, mission_dir)`.
- Added `write_entity_index(model, mission_dir, output_file)`.
- Added deterministic `entity_index.json` generation.
- Added the `orbitfabric export entity-index` command.
- Added `index_version 0.1` for the entity index surface.
- Added `kind orbitfabric.entity_index` for the entity index report.
- Added entity-level records derived from the loaded Mission Model.
- Added per-domain entity counts.
- Added per-domain model counts.
- Added source file metadata for entity records and domain summaries.
- Added required/present domain status for the entity index surface.
- Added indexed/not-indexed domain status.
- Added explicit boundary flags for the entity index report.
- Added entity index export tests.
- Added entity index CLI tests.
- Added Entity Index Surface reference documentation.
- Added v0.8.2 release notes.

### Changed

- Updated the package and CLI version to `0.8.2`.
- Extended the Core-owned structured surfaces from domain-level model summary to entity-level indexing.
- Aligned the public roadmap so `v0.8.2 - Entity Index Surface` is completed and `v0.9 - Plugin and Extensibility Layer` is the next milestone.
- Updated README, architecture, project charter, quickstart, development guide, contributing guide and versioning documentation for v0.8.2.
- Reinforced that downstream tools should consume Core-generated structured surfaces instead of reconstructing Mission Model entities from YAML, generated files or textual CLI output.
- Clarified the relationship between `model_summary.json` and `entity_index.json`.

### Boundaries

The Entity Index Surface intentionally does not introduce:

- new Mission Model semantics;
- relationship manifest export implementation;
- relationship graph;
- dependency graph;
- source line or column tracking;
- YAML AST export;
- plugin API;
- plugin discovery;
- Studio-specific API;
- runtime behavior;
- ground behavior.

---

## [v0.8.1] - Contract Introspection Surface

### Added

- Added the `orbitfabric.export` package.
- Added `model_summary_to_dict(model, mission_dir)`.
- Added `write_model_summary(model, mission_dir, output_file)`.
- Added the `orbitfabric export model-summary` command.
- Added deterministic `model_summary.json` generation.
- Added the first Core-owned read-only Contract Introspection Surface.
- Added domain-level contract counts.
- Added domain source file metadata.
- Added required/present domain status.
- Added explicit boundary flags for the model summary report.
- Added Contract Introspection Surface reference documentation.
- Added v0.8.1 release notes.

### Changed

- Updated the package and CLI version to `0.8.1`.
- Aligned the public roadmap so `v0.8.1 - Contract Introspection Surface` is completed and `v0.8.2 - Entity Index Surface` is the next milestone.
- Reinforced that downstream tools should consume Core-generated structured surfaces instead of reconstructing Mission Model semantics from YAML, generated files or textual CLI output.

### Boundaries

The Contract Introspection Surface intentionally does not introduce:

- new Mission Model semantics;
- entity index export implementation;
- entity-level records;
- relationship manifest export implementation;
- relationship graph;
- source line or column tracking;
- YAML AST export;
- plugin API;
- plugin discovery;
- Studio-specific API;
- runtime behavior;
- ground behavior.

---

## [v0.8.0] - Ground Integration Artifacts

### Added

- Added the `GroundContract` intermediate model for ground-facing generation.
- Added the `orbitfabric gen ground` command.
- Added the initial `generic` ground generation profile.
- Added `ground_contract_manifest.json` generation.
- Added JSON ground dictionaries for telemetry, commands, events, faults, data products and packets.
- Added CSV ground dictionaries for review workflows.
- Added generated `README.md` for the ground artifact directory.
- Added generated `ground_dictionaries.md` for human engineering review.
- Added manifest boundary flags for ground runtime, operator console, transport, database, Yamcs, OpenC3 and XTCE claims.
- Added Ground Integration Artifacts reference documentation.
- Added ADR-0012 for the Ground Integration Artifacts boundary.
- Added v0.8.0 release notes.

### Changed

- Extended the public documentation baseline from v0.7.0 to v0.8.0.
- Extended the Mission Data Chain from runtime-facing contract bindings to ground-facing contract exports.
- Updated README, architecture, roadmap, quickstart, development guide, contributing guide, versioning documentation and demo walkthrough for v0.8.0.
- Updated the package and CLI version to `0.8.0`.
- Marked `v0.9 - Plugin and Extensibility Layer` as the next roadmap milestone.

### Boundaries

The Ground Integration Artifacts slice intentionally does not introduce:

- live ground segment;
- mission control system;
- operator console;
- telemetry archive;
- telemetry database;
- command uplink service;
- telecommand transport;
- telemetry downlink runtime;
- network/session/routing behavior;
- command authentication or authorization;
- security enforcement;
- Yamcs integration;
- OpenC3 integration;
- XTCE compliance;
- CCSDS/PUS/CFDP implementation;
- binary packet decoder;
- binary telecommand encoder;
- offset/bitfield layout model;
- calibration model;
- RF/link-budget behavior;
- pass scheduling;
- station automation.

Ground Integration Artifacts in v0.8.0 are ground-facing contract exports only.

---

## [v0.7.0] - Generated Runtime Skeletons

### Added

- Added the `RuntimeContract` intermediate model for software-facing generation.
- Added deterministic runtime naming and symbol generation.
- Added deterministic generated numeric identifiers with `Invalid = 0` reserved per enum domain.
- Added the `orbitfabric gen runtime` command.
- Added the initial `cpp17` runtime generation profile.
- Added `runtime_contract_manifest.json` generation.
- Added generated C++17 mission identifier headers through `mission_ids.hpp`.
- Added generated C++17 runtime value enums through `mission_enums.hpp`.
- Added generated C++17 static metadata registries through `mission_registries.hpp`.
- Added generated C++17 command argument structs through `command_args.hpp`.
- Added generated C++17 abstract adapter interfaces through `adapter_interfaces.hpp`.
- Added generated C++17 host-build smoke files through `CMakeLists.txt` and `src/orbitfabric_runtime_contract_smoke.cpp`.
- Added host-build smoke validation for generated runtime-facing contract bindings.
- Added Runtime Contract Bindings reference documentation.
- Added v0.7.0 release notes.

### Changed

- Extended the public documentation baseline from v0.6.0 to v0.7.0.
- Extended the Mission Data Chain from data-flow evidence to runtime-facing contract bindings.
- Updated README, architecture, roadmap, quickstart, development guide, contributing guide and versioning documentation for v0.7.0.
- Updated the package and CLI version to `0.7.0`.
- Marked `v0.8 - Ground Integration Artifacts` as the next roadmap milestone.

### Boundaries

The Generated Runtime Skeletons slice intentionally does not introduce:

- flight-ready runtime;
- complete OBC framework;
- command dispatch runtime;
- command queues;
- telemetry polling runtime;
- event routing runtime;
- fault manager runtime;
- scheduler;
- HAL;
- drivers;
- RTOS abstraction;
- binary serialization;
- CCSDS/PUS/CFDP behavior;
- storage runtime;
- downlink runtime;
- user-code merge;
- protected regions;
- flight-ready software.

Generated Runtime Skeletons in v0.7.0 are runtime-facing contract bindings only.

---

## [v0.6.0] - End-to-End Mission Data Flow Evidence

### Added

- Added command-declared data product effects through `expected_effects.data_products`.
- Added `OF-CMD-008` and `OF-CMD-009` diagnostics for command data product effects.
- Added simulation data-flow evidence records.
- Added `data_flow_evidence` to simulation JSON reports.
- Added `summary.data_flow_evidence` to simulation JSON reports.
- Added scenario `expect.data_flow` assertions.
- Added `OF-SCN-014` through `OF-SCN-017` diagnostics for scenario data-flow expectation references.
- Added the synthetic `payload_data_flow_evidence` demo scenario.
- Added generated `data_flow.md` documentation output.
- Added the `orbitfabric gen data-flow` command.
- Added a dedicated Data Flow Evidence reference page.
- Added v0.6.0 release notes.

### Changed

- Extended the standard `orbitfabric gen docs` output to include `generated/docs/data_flow.md`.
- Extended the synthetic `demo-3u` mission evidence chain from commandability/autonomy to contract-level data-flow evidence.
- Updated public documentation, architecture, roadmap, quickstart, demo walkthrough and report references for v0.6.0.
- Bumped package and CLI version to `0.6.0`.

### Boundaries

The End-to-End Mission Data Flow Evidence slice intentionally does not introduce:

- real payload file generation;
- real onboard storage runtime;
- file-system behavior;
- compression behavior;
- real downlink queue execution;
- real contact scheduling;
- RF behavior;
- live ground integration;
- CCSDS/PUS/CFDP runtime behavior;
- runtime skeleton generation;
- flight-ready software.

---

## [v0.5.0] - Commandability and Autonomy Contracts

### Added

- Added the Commandability and Autonomy Contract Model as an optional mission model domain.
- Added optional `mission/commandability.yaml` loading.
- Added command sources.
- Added commandability rules.
- Added autonomous action contracts.
- Added recovery intents.
- Added semantic lint rules for commandability/autonomy consistency.
- Added `OF-CAB-*`, `OF-AUT-*` and `OF-REC-*` lint rule families.
- Added generated Commandability and Autonomy Contract documentation.
- Added generated `commandability.md` documentation output.
- Added one synthetic commandability/autonomy slice to the `demo-3u` mission.

### Changed

- Extended the synthetic `demo-3u` mission with contract-level commandability and recovery assumptions.
- Extended generated mission documentation to include commandability/autonomy references when commandability contracts are present.
- Extended the Mission Data Chain from contact/downlink assumptions to commandability, autonomy and recovery assumptions.

### Boundaries

The Commandability and Autonomy Contract slice intentionally does not introduce:

- real command authentication;
- real command authorization;
- live uplink services;
- operator consoles;
- command queues;
- onboard schedulers;
- autonomy runtime;
- real FDIR or safing behavior;
- Yamcs/OpenC3 runtime services;
- real spacecraft operations.

---

## [v0.4.0] - Contact Windows and Downlink Flow Contracts

### Added

- Added the Contact Windows and Downlink Flow Contract Model as an optional mission model domain.
- Added optional `mission/contacts.yaml` loading.
- Added contact profiles.
- Added link profiles.
- Added contact windows with declared capacity assumptions.
- Added downlink flow contracts.
- Added data product eligibility for downlink flows.
- Added Mission Model ID helpers for contact/downlink domains.
- Added duplicate ID validation for contact profiles, link profiles, contact windows and downlink flows.
- Added semantic lint rules for contact/downlink references and downlink flow consistency.
- Added `OF-CON-*` lint rules for contact assumptions.
- Added `OF-DL-*` lint rules for downlink flow assumptions.
- Added generated Contact and Downlink Contract documentation.
- Added generated `contacts.md` documentation output.
- Added one synthetic contact/downlink slice to the `demo-3u` mission.
- Added ADR-0009 for Contact Windows and Downlink Flow Contracts.
- Added reference documentation for the Contact and Downlink Contract Model.

### Changed

- Extended the synthetic `demo-3u` mission with contract-level contact/downlink assumptions.
- Extended generated mission documentation to include contact/downlink references when contact contracts are present.
- Extended the Mission Data Chain from downlink intent to declared contact and downlink flow assumptions.
- Reinforced the boundary between contract assumptions and runtime/ground behavior.

### Boundaries

The Contact Windows and Downlink Flow Contract slice intentionally does not introduce:

- orbit propagation;
- TLE parsing;
- ground track computation;
- antenna pointing;
- RF link budget simulation;
- real contact scheduling;
- real downlink execution;
- onboard downlink queues;
- live ground links;
- CCSDS/PUS/CFDP implementation;
- Yamcs/OpenC3 runtime integration;
- runtime skeleton generation;
- ground export generation;
- real spacecraft operations.

---

## [v0.3.0] - Data Product and Storage Contracts

### Added

- Added the Data Product Contract Model as an optional mission model domain.
- Added optional `mission/data_products.yaml` loading.
- Added the `DataProductContract` model.
- Added data product producer type support.
- Added data product type support.
- Added estimated data product size support.
- Added data product priority support.
- Added storage intent fields.
- Added storage class support.
- Added retention intent support.
- Added overflow policy support.
- Added downlink intent fields.
- Added downlink policy support.
- Added semantic lint rules for Data Product Contracts.
- Added data product producer reference checks.
- Added optional payload reference checks.
- Added storage intent warnings for missing retention and overflow policy.
- Added downlink intent warnings for high-priority data products.
- Added generated data product documentation.
- Added generated `data_products.md` documentation output.
- Added invalid data product fixtures and tests.
- Added one synthetic data product to the `demo-3u` mission.
- Added ADR-0008 for Data Product and Storage Contracts.

### Changed

- Extended the synthetic `demo-3u` mission with a clean-room payload data product.
- Extended generated mission documentation to include Data Product Contract references when data products are present.
- Reinforced the Mission Data Chain direction introduced by ADR-0007.
- Moved OrbitFabric one step further from payload behavior modeling toward explicit mission data chain modeling.

### Boundaries

The Data Product and Storage Contract slice intentionally does not introduce:

- real onboard storage runtime;
- file-system abstraction;
- compression engines;
- payload data processing pipelines;
- contact window modeling;
- RF link modeling;
- downlink runtime;
- ground segment export;
- runtime skeleton generation;
- real payload data.

---

## [v0.2.2] - Payload Contract Release Alignment

### Changed

- Aligned README, public documentation, roadmap, changelog, release notes and package version around the Payload Contract Model.
- Documented `v0.2.2` as the Payload Contract Release Alignment baseline.
- Added release notes for `v0.2.2`.
- Prepared public communication material for the Payload Contract Model.

---

## [v0.2.1] - Payload Contract Model

### Added

- Added the Payload / IOD Payload Contract Model as an optional mission model domain.
- Added optional `mission/payloads.yaml` loading.
- Added the `PayloadContract` model.
- Added payload profile support.
- Added minimal payload lifecycle support.
- Added payload contract semantic linting.
- Added payload lint rules `OF-PAY-001` through `OF-PAY-010`.
- Added payload reference checks for linked subsystems, telemetry, commands, events and faults.
- Added generated payload contract documentation.
- Added generated `payloads.md` documentation output.
- Added minimal payload-aware scenario behavior.
- Added nominal payload lifecycle simulation for `READY -> ACQUIRING -> READY`.
- Added invalid payload contract fixtures.
- Added negative tests for mutated payload contract fixtures.
- Added ADR-0006 for the Payload Contract Model.

### Changed

- Extended the synthetic `demo-3u` mission with a clean-room IOD payload contract.
- Extended the demo scenario to include payload lifecycle behavior during `battery_low_during_payload`.
- Reinforced OrbitFabric's positioning as a Mission Data Contract Layer.

### Boundaries

The Payload Contract Model intentionally does not introduce:

- payload firmware;
- payload drivers;
- payload runtime execution;
- physical payload simulation;
- hardware bus integration;
- payload data processing pipelines;
- ground segment implementation.

---

## [Initial development preview]

### Added

- Initial repository structure.
- Python package skeleton with `orbitfabric` CLI.
- Mission Model YAML loader.
- Typed Mission Model validation with Pydantic.
- Structural validation for canonical multi-file mission directories.
- Semantic lint engine.
- Cross-reference lint rules.
- Engineering lint rules for telemetry, commands, events, faults and packets.
- JSON lint report generation.
- Markdown documentation generator.
- Scenario YAML model and loader.
- Scenario reference validation.
- Deterministic scenario execution runtime.
- Simulation JSON report generation.
- Simulation plain-text log generation.
- Synthetic clean-room `demo-3u` mission.
- Synthetic `battery_low_during_payload` scenario.
- Project charter.
- Clean-room policy.
- Architecture documentation.
- Roadmap documentation.
- Mission Model v0.1 reference.
- ADR-0001 through ADR-0005.
- CI workflow.

### Current Verified Baseline

```text
ruff check .
-> passing

pytest
-> passing

lint
-> passing

gen docs
-> passing

sim
-> passing
```
