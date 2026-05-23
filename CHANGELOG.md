# Changelog

All notable changes to OrbitFabric will be documented in this file.

This project follows a lightweight changelog style for the Mission Model, contract layers, generated artifacts and CLI.

---

## [Unreleased]

### Added

- Added the candidate `dashboard_summary.json` Core-owned structured surface.
- Added `orbitfabric export dashboard-summary <mission_dir> --json <path>`.
- Added the Dashboard Summary Surface reference page and MkDocs navigation entry.
- Added tests for dashboard summary identity, boundaries, inventory, coverage-unavailable posture, deterministic JSON writing and CLI export.

### Compatibility impact

No Mission Data Contract semantic impact.

This change does not add, remove or rename Mission Model fields, model domains, controlled values, reference rules, lint diagnostics or scenario expectations.

The new dashboard summary is an additive candidate post-v1 Core-owned structured surface. It does not change the v1.0.0 stable surface.

The dashboard summary does not introduce coverage metrics, model completeness scoring, mission health scoring, runtime behavior, ground behavior, relationship graph behavior, plugin execution or Studio-specific APIs.

---

## [v1.0.0] - Stable Mission Data Contract

### Added

- Added v1.0.0 release notes.
- Added the v1.0.0 release notes page to the MkDocs Releases navigation.
- Added the v1.0 Stable Surface Decision reference.
- Added the v1.0 Stable Surface Decision page to the MkDocs Reference navigation.
- Added explicit v1.0 classification for stable surfaces, public preview surfaces, generated disposable artifacts, internal implementation details and out-of-scope topics.
- Added the selected v1.0 demonstration use-case boundary for Mission Data Contract continuity.
- Added contract-significant golden signatures for the demo-3u Core-owned structured surfaces: `model_summary.json`, `entity_index.json` and `relationship_manifest.json`.
- Added regression tests comparing generated Core-owned structured surfaces against those golden signatures.
- Added the v1.0 Demo Evidence Chain reference.
- Added the v1.0 Demo Evidence Chain page to the MkDocs Reference navigation.

### Changed

- Updated the package and CLI version to `1.0.0`.
- Updated the package classifier from pre-alpha to beta.
- Marked `v1.0.0 - Stable Mission Data Contract` as completed in the roadmap.
- Aligned README, public documentation homepage, roadmap, quickstart, development guide, architecture and project charter with the v1.0.0 release baseline.
- Aligned the v1.0 Compatibility and Migration Notes reference with the current v1.0 stable posture after the stable surface decision, golden signatures and demo evidence chain.
- Documented that no migration is required from the v0.12.0 release candidate hardening baseline to v1.0.0.

### Compatibility impact

v1.0.0 establishes the first stable narrow Mission Data Contract surface.

The release has no Mission Data Contract semantic migration impact from v0.12.0.

It does not add, remove or rename Mission Model fields, model domains, controlled values, reference rules, lint diagnostics, scenario expectations, JSON report fields, generated surfaces or CLI workflows beyond version reporting.

The expected CLI version is now:

```text
orbitfabric 1.0.0
```

### Stable surface

The v1.0.0 stable surface includes:

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

### Boundaries

v1.0.0 intentionally does not introduce:

- new Mission Model semantics relative to v0.12.0;
- new YAML fields;
- new model domains;
- new CLI behavior beyond version reporting;
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

Generated runtime-facing and ground-facing artifacts remain reproducible and disposable unless explicitly classified otherwise.

The v1.0 golden signatures protect selected contract-significant fields of existing Core-owned structured surfaces.

They do not freeze full generated JSON files, absolute paths, human-oriented output, Markdown wording, generated runtime bindings, generated ground dictionaries or disposable artifact formatting.

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

See `docs/releases/v0.11.0.md` for release details.

---

## [v0.10.1] - Documentation and Published Site Consistency

See `docs/releases/v0.10.1.md` for release details.

---

## [v0.10.0] - Stability and Compatibility Contract

See `docs/releases/v0.10.0.md` for release details.

---

## [v0.9.0] - Relationship Manifest Surface and Extensibility Boundary

See `docs/releases/v0.9.0.md` for release details.

---

## [v0.8.2] - Entity Index Surface

See `docs/releases/v0.8.2.md` for release details.

---

## [v0.8.1] - Contract Introspection Surface

See `docs/releases/v0.8.1.md` for release details.

---

## [Initial development preview]

Initial repository structure, Python package skeleton, Mission Model loader, validation, linting, documentation generation, scenario execution, JSON reports, synthetic demo mission, project charter, clean-room policy, architecture documentation, roadmap documentation, Mission Model v0.1 reference, ADR-0001 through ADR-0005 and CI workflow.
