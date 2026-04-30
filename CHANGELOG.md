# Changelog

All notable changes to OrbitFabric will be documented in this file.

This project follows a lightweight pre-1.0 changelog style while the Mission Model and CLI stabilize.

---

## [Unreleased]

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
ruff check .  -> passing
pytest        -> 34 tests passing
lint          -> passing
gen docs      -> passing
sim           -> passing
```