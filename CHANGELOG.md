# Changelog

All notable changes to OrbitFabric will be documented in this file.

This project follows a lightweight pre-1.0 changelog style while the Mission Model, contract layers, generated artifacts and CLI stabilize.

---

## [Unreleased]

### Added

- Added the v1.0 Stable Surface Decision reference.
- Added the v1.0 Stable Surface Decision page to the MkDocs Reference navigation.
- Added explicit v1.0 classification for stable surfaces, public preview surfaces, generated disposable artifacts, internal implementation details and out-of-scope topics.
- Added the selected v1.0 demonstration use-case boundary for Mission Data Contract continuity.
- Added contract-significant golden signatures for the demo-3u Core-owned structured surfaces: `model_summary.json`, `entity_index.json` and `relationship_manifest.json`.
- Added regression tests comparing generated Core-owned structured surfaces against those golden signatures.

### Compatibility impact

This change has no Mission Data Contract semantic impact.

It does not add, remove or rename Mission Model fields, model domains, controlled values, reference rules, lint diagnostics, scenario expectations, JSON report fields, generated surfaces or CLI behavior.

It documents the proposed narrow v1.0 stable surface selected from existing OrbitFabric Core behavior and surfaces.

The golden signatures protect selected contract-significant fields for existing Core-owned structured surfaces.

They do not introduce new generated surfaces or new report fields.

### Boundaries

This change intentionally does not introduce:

- new Mission Model semantics;
- new YAML fields;
- new model domains;
- new CLI behavior;
- new JSON report fields;
- new generated Core surfaces;
- new lint diagnostics;
- new scenario behavior;
- schema migration tooling;
- JSON Schema publication;
- XTCE export;
- Yamcs integration;
- OpenC3 integration;
- F Prime mapping;
- cFS integration;
- CCSDS/PUS/CFDP implementation;
- Mission Model security domain;
- security YAML fields;
- security enforcement semantics;
- plugin discovery;
- plugin loading;
- plugin execution;
- relationship graph;
- dependency graph;
- runtime behavior;
- ground behavior;
- Studio-specific API.

The new golden signatures do not freeze full generated JSON files, absolute paths, human-oriented output, Markdown wording, generated runtime bindings, generated ground dictionaries or disposable artifact formatting.

---

## [v0.12.0] - v1.0 Release Candidate Hardening

### Added

- Added the v1.0 Candidate Surface Inventory reference.
- Added the Golden Output and Regression Confidence Policy reference.
- Added the v1.0 Compatibility and Migration Notes reference.
- Added all three v0.12.0 hardening references to the MkDocs Reference navigation.
- Added v0.12.0 release notes.
- Added the v0.12.0 release notes page to the MkDocs Releases navigation.
- Added explicit documentation that v0.12.0 hardening references are review and governance surfaces, not new Mission Data Contract semantics.
- Added explicit documentation that candidate, preview and generated surfaces do not become stable v1.0 automatically.
- Added explicit disposition for security assumptions and command criticality contracts: valid future exploration, not a v1.0.0 blocker, deferred beyond v1.0.0 unless separately scoped.

### Changed

- Updated the package and CLI version to `0.12.0`.
- Marked `v0.12.0 - v1.0 Release Candidate Hardening` as completed in the roadmap.
- Marked `v1.0.0 - Stable Mission Data Contract` as the next milestone.
- Aligned README with the v0.12.0 release baseline.
- Aligned the public documentation homepage with the v0.12.0 release baseline.
- Aligned Quickstart, Development Guide, Contributing Guide and Versioning Model with the v0.12.0 release baseline.
- Aligned Architecture and Project Charter headers with the v0.12.0 release candidate hardening baseline.
- Clarified the release candidate hardening path before v1.0.0.
- Clarified that current CI artifacts are not committed golden-output baselines.
- Clarified that golden-output baselines require separate future PRs and explicit scope.
- Clarified compatibility and migration note discipline before v1.0.0.
- Clarified that security assumptions and command criticality contracts remain outside v0.12.0 and v1.0.0 implementation scope.

### Compatibility impact

v0.12.0 has no Mission Data Contract semantic impact.

It does not add, remove or rename Mission Model fields, model domains, controlled values, reference rules, lint diagnostics, scenario expectations, JSON report fields or generated surfaces.

The only CLI-visible behavior change is the reported package version:

```text
orbitfabric 0.12.0
```

No migration is required from v0.11.0 to v0.12.0.

### Boundaries

The v0.12.0 release candidate hardening slice intentionally does not introduce:

- new Mission Model semantics;
- new YAML fields;
- new model domains;
- new CLI behavior beyond version reporting;
- new JSON report fields;
- new generated Core surfaces;
- new lint diagnostics;
- new scenario behavior;
- new golden files;
- new snapshot tests;
- new CI jobs;
- schema migration tooling;
- migration commands;
- compatibility scanners;
- JSON Schema publication;
- Mission Model security domain;
- security YAML fields;
- security enforcement semantics;
- plugin discovery;
- plugin loading;
- plugin execution;
- metadata schema;
- metadata parser;
- metadata loader;
- metadata validator;
- relationship graph;
- dependency graph;
- runtime behavior;
- ground behavior;
- Studio-specific API;
- stable v1.0 compatibility guarantee.

v0.12.0 is a release candidate hardening and release-alignment milestone only.

---

## [v0.11.0] - Extensibility Boundary Contract, no execution

### Added

- Added ADR-0015 for the Extensibility Boundary Contract, No Execution.
- Added the Extensibility Boundary Contract reference page.
- Added the Extensibility Boundary Contract page to the MkDocs Reference navigation.
- Added v0.11.0 release notes.
- Added the v0.11.0 release notes page to the MkDocs Releases navigation.
- Added non-normative guidance for future descriptive extension metadata.
- Added explicit Core ownership rules for Mission Data Contract semantics.
- Added explicit extension ownership rules for future extension-owned outputs.
- Added provenance expectations for future extension-owned artifacts.
- Added a semantic override ban for future extensions.
- Added explicit downstream consumer rules for Core-owned surfaces and extension-owned artifacts.
- Added compatibility-sensitive extensibility boundary expectations before v1.0.0.

### Changed

- Updated the package and CLI version to `0.11.0`.
- Marked `v0.11.0 - Extensibility Boundary Contract, no execution` as completed in the roadmap.
- Marked `v0.12.0 - v1.0 Release Candidate Hardening` as the next milestone.
- Aligned README with the v0.11.0 release baseline.
- Aligned the public documentation homepage with the v0.11.0 release baseline.
- Aligned Quickstart, Development Guide, Contributing Guide and Versioning Model with the v0.11.0 release baseline.
- Aligned Architecture and Project Charter headers with the v0.11.0 extensibility boundary baseline.

### Boundaries

The v0.11.0 extensibility boundary slice intentionally does not introduce:

- new Mission Model semantics;
- new YAML fields;
- new model domains;
- new CLI behavior beyond version reporting;
- new JSON report fields;
- new generated Core surfaces;
- new lint diagnostics;
- new scenario behavior;
- metadata schema;
- JSON metadata shape;
- metadata manifest format;
- metadata parser;
- metadata loader;
- metadata validator;
- new extension command;
- plugin discovery;
- plugin loading;
- plugin execution;
- custom lint plugin execution;
- custom generator plugin execution;
- dynamic extension runtime;
- third-party code execution;
- remote plugin registry;
- plugin marketplace;
- extension installation;
- extension dependency resolution;
- relationship graph;
- dependency graph;
- runtime behavior;
- ground behavior;
- Studio-specific API;
- schema migration tooling;
- JSON Schema publication;
- stable v1.0 compatibility guarantee.

v0.11.0 is an extensibility boundary and release-alignment milestone only.

---

## [v0.10.1] - Documentation and Published Site Consistency

### Added

- Added v0.10.1 release notes.
- Added the v0.10.1 release notes page to the MkDocs navigation.

### Changed

- Updated the package and CLI version to `0.10.1`.
- Marked `v0.10.1 - Documentation and Published Site Consistency` as completed in the roadmap.
- Marked `v0.11.0 - Extensibility Boundary Contract, no execution` as the next milestone.
- Clarified README wording around Relationship Manifest family counts.
- Aligned the public documentation homepage with the v0.10.1 release baseline.
- Preserved the v0.10.0 stability and compatibility classification baseline as the current compatibility foundation before v1.0.0.

### Boundaries

The v0.10.1 documentation consistency slice intentionally does not introduce:

- new Mission Model semantics;
- new YAML fields;
- new model domains;
- new CLI behavior beyond version reporting;
- new JSON report fields;
- new generated surfaces;
- new lint diagnostics;
- new scenario behavior;
- schema migration tooling;
- JSON Schema publication;
- plugin execution;
- plugin discovery;
- plugin loader;
- relationship graph;
- dependency graph;
- runtime behavior;
- ground behavior;
- Studio-specific API;
- stable v1.0 compatibility guarantee.

v0.10.1 is a documentation consistency and release-alignment milestone only.

---

## [v0.10.0] - Stability and Compatibility Contract

### Added

- Added the Stability and Compatibility Contract reference.
- Added the Mission Model Stability Contract reference.
- Added the CLI Contract v1 Preview reference.
- Added the Generated Surfaces Stability reference.
- Added the Lint Rule Code Stability reference.
- Added the JSON Report Compatibility reference.
- Added the Scenario Evidence Stability reference.
- Added the Release Compatibility Policy reference.
- Added v0.10.0 release notes.

### Changed

- Updated the package and CLI version to `0.10.0`.
- Marked `v0.10.0 - Stability and Compatibility Contract` as completed in the roadmap.
- Marked `v0.10.1 - Documentation and Published Site Consistency` as the next milestone.
- Classified Mission Model, CLI, JSON report, lint diagnostic, generated surface, scenario evidence and release compatibility expectations before v1.0.0.
- Clarified which surfaces are public preview, candidate contract, internal implementation detail or disposable generated artifacts.
- Clarified that compatibility-sensitive changes must be explicit, reviewed and documented before v1.0.0.

### Boundaries

The v0.10.0 stability and compatibility slice intentionally does not introduce:

- new Mission Model semantics;
- new YAML fields;
- new model domains;
- new CLI behavior;
- new JSON report fields;
- new generated surfaces;
- new lint diagnostics;
- new scenario behavior;
- schema migration tooling;
- JSON Schema publication;
- plugin execution;
- plugin discovery;
- plugin loader;
- relationship graph;
- dependency graph;
- runtime behavior;
- ground behavior;
- Studio-specific API;
- stable v1.0 compatibility guarantee.

v0.10.0 is a classification and release-alignment milestone only.

---

## [v0.9.0] - Relationship Manifest Surface and Extensibility Boundary

### Added

- Added `relationship_manifest_to_dict(model, mission_dir)`.
- Added `write_relationship_manifest(model, mission_dir, output_file)`.
- Added deterministic `relationship_manifest.json` generation.
- Added the `orbitfabric export relationship-manifest` command.
- Added `manifest_version 0.1-candidate` for the relationship manifest surface.
- Added `kind orbitfabric.relationship_manifest` for the relationship manifest report.
- Added Core-owned relationship records derived from explicit loaded Mission Model fields.
- Added relationship type records and relationship type counts.
- Added explicit relationship derivation policy.
- Added explicit boundary flags for the relationship manifest report.
- Added 19 admitted relationship families to the candidate relationship manifest surface.
- Added relationship manifest export tests.
- Added relationship manifest CLI tests.
- Added Relationship Manifest Surface reference documentation.
- Added v0.9.0 release notes.

### Changed

- Updated the package and CLI version to `0.9.0`.
- Extended Core-owned structured surfaces from domain-level and entity-level reports to relationship-level reports.
- Extended the public documentation baseline from `v0.8.2 - Entity Index Surface` to `v0.9.0 - Relationship Manifest Surface and Extensibility Boundary`.
- Aligned README, site homepage, roadmap, architecture, project charter, quickstart, development guide, contributing guide and demo walkthrough with the relationship manifest surface.
- Clarified the structured surface chain: `model_summary.json -> entity_index.json -> relationship_manifest.json`.
- Reinforced that downstream tools should consume Core-owned structured surfaces instead of reconstructing Mission Model relationships from YAML, generated files, textual CLI output or UI state.

### Boundaries

The v0.9.0 relationship manifest slice intentionally does not introduce:

- new Mission Model semantics;
- relationship inference;
- relationship graph;
- dependency graph;
- source line or column tracking;
- YAML AST export;
- plugin API;
- plugin discovery;
- plugin loader;
- plugin execution;
- custom lint plugin support;
- custom generator plugin support;
- Studio-specific API;
- runtime behavior;
- ground behavior.

Relationship Manifest Surface in v0.9.0 is a Core-owned read-only candidate relationship report only.

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
