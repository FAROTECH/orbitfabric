# Changelog

All notable changes to OrbitFabric will be documented in this file.

This project follows a lightweight pre-1.0 changelog style while the Mission Model, Payload Contract Model and CLI stabilize.

---

## [Unreleased]

### Changed

- Public documentation, roadmap and release alignment work for the Payload Contract Model is ongoing under `v0.2.2 — Payload Contract Release Alignment`.

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
