# Changelog

All notable changes to OrbitFabric will be documented in this file.

This project follows a lightweight pre-1.0 changelog style while the Mission Model, Payload Contract Model, Data Product Contract Model and CLI stabilize.

---

## [Unreleased]

### Changed

- Next development focus: `v0.5 — Commandability and Autonomy Contracts`.

---

## [v0.4.0] — Contact Windows and Downlink Flow Contracts

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

## [v0.3.0] — Data Product and Storage Contracts

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

## [v0.2.2] — Payload Contract Release Alignment

### Changed

- Aligned README, public documentation, roadmap, changelog, release notes and package version around the Payload Contract Model.
- Documented `v0.2.2` as the Payload Contract Release Alignment baseline.
- Added release notes for `v0.2.2`.
- Prepared public communication material for the Payload Contract Model.

---

## [v0.2.1] — Payload Contract Model

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
- Added nominal payload lifecycle simulation for `READY → ACQUIRING → READY`.
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
