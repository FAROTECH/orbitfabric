# Changelog

All notable changes to OrbitFabric will be documented in this file.

This project follows a lightweight changelog style for the Mission Model, contract layers, generated artifacts and CLI.

---

## [Unreleased]

### Added

- Added the Core-owned Adapter Manager M0 candidate lifecycle for exact adapter installation, inspection, verification, execution and removal.
- Added `orbitfabric adapter install`, `list`, `inspect`, `verify`, `execute` and `remove`.
- Added the Adapter Release Descriptor `0.1-candidate` JSON Schema and Core conformance validation.
- Added the explicit exact-release source lane and SHA-256 artifact verification.
- Added the first Python wheel installation backend using a dedicated managed Python environment and an absolute environment-local adapter endpoint.
- Added a user-scoped Core-owned Installed Adapter Inventory with install-record publication last and removal-record deletion last.
- Added ADR-0017 and the Adapter Manager M0 reference documentation.
- Added regression coverage for Release Descriptor conformance, lifecycle transaction ordering, installed-state drift detection and generic `orbitfabric.adapter_cli.v1` execution.

### Changed

- Moved `jsonschema` into the base runtime dependencies because integration and Adapter Release conformance are required by Adapter Manager lifecycle operations.

### Compatibility impact

Adapter Manager M0 is an additive Core product capability and does not introduce a Mission Model semantic migration.

No Mission Model fields, domains, controlled values, identifier rules, reference meanings, lint diagnostic semantics or scenario expectation semantics are removed, renamed or redefined.

The existing Integration Package Manifest `0.2-candidate`, `orbitfabric.adapter_cli.v1` and Integration Result `0.2-candidate` execution lane is reused unchanged. Adapter Manager does not introduce a second runtime adapter protocol.

The Adapter Release Descriptor `0.1-candidate` and the `orbitfabric adapter` lifecycle CLI remain candidate surfaces. Raw Installed Adapter Inventory persistence, local instance identifiers, managed-environment layout and backend receipts remain implementation-private.

M0 does not introduce public registry discovery, Adapter Project Lock IO, automatic updates, publisher administration, non-Python backends or Studio lifecycle UX.

## [v1.2.0] - 2026-08-28

### Added

- Added the Core-owned `mission_snapshot.json` read-only inspection surface for the complete loaded Mission Model.
- Added `orbitfabric export mission-snapshot <mission_dir> --json <path>` with structured load-failure diagnostics and no partial semantic Mission Model on structural failure.
- Added seven explicit FDIR-oriented relationship families to `relationship_manifest.json`:
  - `autonomous_action_triggered_by_fault`;
  - `autonomous_action_uses_command_source`;
  - `fault_observes_telemetry`;
  - `fault_recovery_dispatches_command`;
  - `fault_recovery_targets_mode`;
  - `recovery_intent_includes_command`;
  - `recovery_intent_targets_mode`.
- Added the generic Core Integration Input Contract, Projection Profile Contract, Integration Result Contract and Integration Package / Adapter Execution Contract reference documents extracted from the OpenOBSW/OpenSVF PoC.
- Added the coherent Core Integration Input Set producer and public `orbitfabric export integration-input-set <mission_dir> [--output-dir <dir>]` workflow.
- Added `integration_input_manifest.json` with explicit required/companion roles, surface status, kind/version identity, SHA-256 digests, load/lint state and an RFC 8785/JCS-based coherent input-set fingerprint.
- Added regression coverage for one-load/one-lint production, manifest-last completeness, structural/lint/generation failure states and deterministic input-set identity.
- Added a selected Mission Snapshot golden signature protecting contract-significant envelope, boundary and representative serialization invariants without freezing the complete serialized Mission Model.
- Added the accepted v1.2 Integration Input Stability Decision and v1.2.0 release notes.

### Changed

- Updated package and CLI version to `1.2.0`.
- Promoted `mission_snapshot.json` to a stable Core-owned integration/inspection surface for its documented envelope, failure behavior and serialization role.
- Promoted the coherent Core Integration Input Set to the stable Core-to-external-integration input boundary.
- Classified the seven FDIR relationship families as additive stable-compatible Relationship Manifest families derived deterministically from explicit Mission Model fields.
- Kept the original v1 Relationship Manifest golden signature unchanged; dedicated FDIR tests protect the additive families.
- Preserved existing Mission Snapshot and Integration Input Set format identifiers (`0.1-candidate`) because stability classification is independent from format-version text and changing the identifiers would create needless consumer incompatibility.
- Aligned README, roadmap, release documentation and stability references with the v1.2.0 classification.

### Compatibility impact

No Mission Data Contract semantic migration is introduced by v1.2.0.

No Mission Model fields, domains, controlled values, identifier rules, reference meanings, lint diagnostic semantics or scenario expectation semantics are removed, renamed or redefined.

`mission_snapshot.json` is a stable additive Core-owned surface. Its `model` payload remains a faithful serialization of the loaded Mission Model and follows Mission Model compatibility rules; compatible consumers must tolerate additive fields where those rules permit them.

The coherent Integration Input Set is now the stable supported Core input boundary for external Integration Packages. Required surface incompatibility blocks semantic projection; raw-YAML semantic fallback remains forbidden.

The seven FDIR relationship families are additive. They do not rename, remove or change the meaning of original v1 relationship families. Compatible consumers must tolerate unknown additive relationship types and must not guess unknown semantics.

The v1.1.0 dashboard summary, scenario run index, coverage summary and structured expectation additions remain candidate unless separately promoted.

Projection Profile, Integration Result and Integration Package / Adapter Execution remain independently versioned `0.1-candidate` extension contracts. Their presence in the Core repository documentation does not make them stable Core Mission Data Contract surfaces.

v1.2.0 does not introduce plugin execution, runtime behavior, ground behavior, relationship graph behavior, dependency graph behavior or OpenOBSW/OpenSVF/YAMCS-specific semantics into Core.

## [v1.1.0] - 2026-06-13

### Changed

- Consolidated post-v1 candidate integration surface documentation across README, active reference contracts, contribution/security guidance and release documentation with the merged v1.2 baseline while preserving stable/candidate ownership boundaries and historical records.
- Added a dedicated post-v1 candidate integration surfaces index page to keep stable, candidate, Core-owned and downstream-owned boundaries explicit.
- Reclassified the Dashboard and Coverage Foundation reference from a proposed future boundary to the implemented post-v1 candidate surface boundary.

### Fixed

- Fixed generated artifact default paths for mission-based CLI commands so omitted output paths resolve under the mission workspace instead of the current working directory.
- Documented that explicit user-provided output paths are preserved unchanged.

### Added

- Added the candidate `dashboard_summary.json` Core-owned structured surface.
- Added `orbitfabric export dashboard-summary <mission_dir> --json <path>`.
- Added the Dashboard Summary Surface reference page and MkDocs navigation entry.
- Added tests for dashboard summary identity, boundaries, inventory, coverage-unavailable posture, deterministic JSON writing and CLI export.
- Added the candidate `scenario_run_index.json` Core-owned structured surface.
- Added `orbitfabric export scenario-run-index --simulation-reports <dir> --json <path>`.
- Added the Scenario Run Index Surface reference page and MkDocs navigation entry.
- Added tests for scenario run index identity, boundaries, filtering of non-simulation JSON reports, deterministic JSON writing and CLI export.
- Added additive structured expectation accounting to simulation JSON reports.
- Added `summary.expectations`, `summary.passed_expectations` and the structured top-level `expectations` object to simulation JSON reports.
- Added tests covering passed expectation accounting, failed expectation accounting and legacy `failed_expectations` compatibility.
- Added the candidate `coverage_summary.json` Core-owned structured surface.
- Added `orbitfabric export coverage-summary <mission_dir> --entity-index <path> --relationship-manifest <path> --scenario-run-index <path> --json <path>`.
- Added the Coverage Summary Surface reference page and MkDocs navigation entry.
- Added tests for coverage summary identity, boundaries, entity coverage, expectation coverage, relationship coverage, deterministic JSON writing and CLI export.

### Compatibility impact

No Mission Data Contract semantic impact.

This change does not add, remove or rename Mission Model fields, model domains, controlled values, reference rules, lint diagnostics or scenario expectations.

The new dashboard summary, scenario run index and coverage summary are additive candidate post-v1 Core-owned structured surfaces. They do not change the v1.0.0 stable surface.

The dashboard summary does not introduce coverage metrics, model completeness scoring, mission health scoring, runtime behavior, ground behavior, relationship graph behavior, plugin execution or Studio-specific APIs.

The scenario run index is derived from simulation JSON reports only. It does not parse plain-text logs and does not introduce coverage metrics, structured expectation accounting, runtime behavior, ground behavior, relationship graph behavior, plugin execution or Studio-specific APIs.

The structured expectation accounting fields are additive simulation JSON report fields. They preserve the legacy top-level `failed_expectations` array for compatibility.

The structured expectation accounting fields do not introduce formal verification, coverage metrics, runtime behavior, ground behavior, relationship graph behavior, plugin execution or Studio-specific APIs.

The coverage summary is derived only from Core-owned structured outputs: `entity_index.json`, `relationship_manifest.json`, `scenario_run_index.json` and simulation JSON reports referenced by the scenario run index.

The coverage summary does not read plain-text logs, scan raw YAML, compute mission health, compute model completeness, introduce formal verification, introduce runtime behavior, introduce ground behavior, introduce relationship graph behavior, introduce plugin execution or introduce Studio-specific APIs.

---

## [v1.0.0] - Stable Mission Data Contract

### Added

- Added v1.0.0 release notes.
- Added the v1.0.0 release notes page to the MkDocs Releases navigation.
- Added the v1.0 Stable Surface Decision reference.
- Added the v1.0 Stable Surface Decision page to the MkDocs Reference navigation.
- Added explicit v1.0 classification for stable surfaces, public preview surfaces, generated disposable artifacts, internal implementation details and out-of-scope topics.
- Added explicit documentation that the v1.0 stable surface is narrow and deliberately excludes candidate preview surfaces unless separately promoted.
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
