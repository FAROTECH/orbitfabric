# OrbitFabric

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

Its central artifact is the Mission Data Contract: a structured Mission Model that defines mission data semantics once and lets OrbitFabric Core validate, exercise, document and export those semantics through explicit engineering boundaries.

The Mission Model remains the semantic source of truth.

## What OrbitFabric covers

The stable Mission Model includes documented contracts for:

```text
spacecraft and subsystems
operational modes and transitions
telemetry
commands
events
faults
packets and policies
payloads
data products, storage and retention intent
contact and downlink assumptions
commandability
autonomy and recovery intent
```

Operational scenarios are separate host-side evidence inputs.

From the validated Mission Model, Core can:

- perform structural validation and semantic linting;
- execute deterministic scenario evidence;
- generate mission and data-flow documentation;
- generate C++17 runtime-facing contract bindings;
- generate generic ground-facing contract artifacts;
- export machine-readable Core-owned inspection surfaces;
- produce one coherent Integration Input Set for external ecosystem integrations;
- manage exact installed external adapter releases through a provider-neutral candidate lifecycle.

Generated runtime and ground artifacts are contract-facing outputs, not flight software or a ground segment.

## Current Core version

```text
v1.3.0 - Adapter Management Foundation
```

The stable Mission Data Contract commitment started with v1.0.0.

v1.2.0 extended the stable Core boundary with:

```text
mission_snapshot.json
Core Integration Input Set
seven additive stable-compatible FDIR Relationship Manifest families
```

v1.3.0 preserves those stable semantics and adds candidate operation-input and Adapter Management capabilities. It introduces no new Mission Model semantics.

The coherent Integration Input Set is generated from one logical Core load/lint operation and includes:

```text
integration_input_manifest.json
mission_snapshot.json
entity_index.json
relationship_manifest.json
lint_report.json
model_summary.json
```

External adapters must consume the documented Core boundary and must not reconstruct Mission Data Contract semantics by reparsing raw YAML as a fallback.

## Stability at a glance

### Stable v1.x Core surface

```text
Mission Model documented semantics
Core structural validation
Core semantic lint policy
scenario YAML evidence inputs
lint JSON report
simulation JSON report
model_summary.json
entity_index.json
relationship_manifest.json for admitted families
mission_snapshot.json
Core Integration Input Set
documented stable CLI workflows
compatibility and extensibility governance
```

### Candidate Core inspection surfaces

The following v1.1 additions remain candidate:

```text
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
simulation JSON structured expectation accounting
```

### Candidate integration and Adapter Management surfaces

The generic Integration Framework and v1.3 Adapter Management foundation include candidate contracts and product surfaces:

```text
Projection Profile
Integration Result
Integration Package / Adapter Execution
operation-input v1 contract lane
Adapter Release Descriptor
Adapter Project Lock
Adapter Manager lifecycle
explicit-source install-from-lock
source-neutral resolved-release attachment
Adapter Catalog model and CLI
```

These remain independently versioned or explicitly classified candidate surfaces. They are not automatically part of the stable Mission Data Contract merely because the Core package version is 1.3.0.

## Architecture in one view

```text
Mission Model
    -> OrbitFabric Core
        -> validation and lint
        -> scenario evidence
        -> documentation
        -> runtime-facing bindings
        -> ground-facing artifacts
        -> Core-owned structured surfaces
        -> coherent Core Integration Input Set
            -> Projection Profile
            -> external Integration Package / Adapter
            -> Integration Result
            -> Studio / CI / other consumers
```

Adapter lifecycle ownership is separate but connected:

```text
Adapter Project Lock
    -> exact Adapter Catalog selection
    -> provider-specific Release Source outside Core
    -> ResolvedAdapterRelease
    -> Core Adapter Manager
    -> Installed Adapter State
```

Ownership remains explicit:

```text
Core owns mission semantics.
Core owns exact adapter identity, desired/actual state and lifecycle semantics.
Projection Profiles own authored target-specific intent.
External adapters own target-specific validation and generation.
Provider-specific Release Sources own provider acquisition.
Integration Results own explicit integration outputs and provenance.
Downstream tools consume and present explicit records.
```

Core does not import ecosystem-specific adapter code in-process and does not contain provider-specific acquisition logic.

## Start here

Choose the path that matches what you need.

### I want to run OrbitFabric

Start with [Quickstart](QUICKSTART.md).

It covers environment setup, CLI validation, stable exports, candidate inspection surfaces, generators and demo scenarios.

### I want to understand the project

Read [Project Charter](PROJECT_CHARTER.md) and [Architecture](ARCHITECTURE.md).

The Charter defines the problem, target users, scope and positioning. Architecture defines semantic ownership, stable boundaries, integration ownership and explicit non-goals.

### I want an end-to-end example

Use [Demo Walkthrough](DEMO_WALKTHROUGH.md).

The built-in `demo-3u` mission demonstrates a synthetic Mission Data Chain from payload command through data product, storage intent, downlink intent, contact assumptions, scenario evidence, generated artifacts and Core-owned surfaces.

### I want compatibility rules

Read these references:

- [Mission Model Stability Contract](reference/mission-model-stability-contract.md)
- [Stability and Compatibility Contract](reference/stability-compatibility-contract.md)
- [Release Compatibility Policy](reference/release-compatibility-policy.md)
- [CLI Contract v1](reference/cli-contract-v1.md)
- [JSON Report Compatibility](reference/json-report-compatibility.md)
- [Generated Surfaces Stability](reference/generated-surfaces-stability.md)
- [Golden Output and Regression Confidence Policy](reference/golden-output-regression-confidence.md)

### I want the external integration boundary

Read:

- [Mission Snapshot Surface](reference/mission-snapshot-surface.md)
- [Core Integration Input Contract](reference/core-integration-input-contract.md)
- [v1.2 Integration Input Stability Decision](reference/v1.2-integration-input-stability-decision.md)
- [Projection Profile Contract](reference/projection-profile-contract.md)
- [Projection Profile Integration Schema Publication](reference/projection-profile-schema-publication.md)
- [Integration Package and Adapter Execution Contract](reference/integration-package-adapter-execution-contract.md)
- [Integration Operation-Input Contract v1](reference/integration-contract-v1.md)
- [Integration Result Contract](reference/integration-result-contract.md)

The Core input boundary is stable from v1.2. The Profile, Package, operation-input and Result contracts remain candidate extension contracts.

### I want the Adapter Management boundary

Read:

- [Adapter Manager M0](reference/adapter-manager-m0.md)
- [Adapter Project Lock M1](reference/adapter-project-lock-m1.md)
- [Explicit-Source Install from Adapter Project Lock](reference/adapter-install-from-lock-explicit-source.md)
- [Adapter Catalog CLI](reference/adapter-catalog-cli.md)
- [ADR-0020 Source-Neutral Release Attachment Seam](adr/ADR-0020-source-neutral-release-attachment-seam.md)
- [ADR-0021 Adapter Catalog Exact Selection Boundary](adr/ADR-0021-adapter-catalog-exact-selection-boundary.md)

The Core boundary is provider-neutral. Provider-specific Release Sources remain external products and hand verified exact releases into Core through `ResolvedAdapterRelease`.

### I want to contribute

Read the repository [Contributing Guide](https://github.com/FAROTECH/orbitfabric/blob/main/CONTRIBUTING.md) and [Clean-Room Policy](CLEAN_ROOM_POLICY.md).

## Project boundaries

OrbitFabric is not:

```text
a flight software framework
a ground segment
a mission control system
a command uplink service
a telemetry archive
a spacecraft dynamics simulator
a hardware abstraction layer
a CCSDS/PUS/CFDP implementation
a relationship or dependency graph engine
a Core in-process plugin execution platform
a provider-specific package registry client
a Studio-specific backend
```

Those boundaries are deliberate. OrbitFabric is valuable because it provides a narrow, explicit contract and lifecycle layer that other engineering systems can consume.

## Quality and reproducibility

The main repository gates are:

```bash
ruff check .
pytest
mkdocs build --strict
```

CI validates Python 3.11 and Python 3.12 and regenerates representative mission evidence.

Selected stable fields are protected by golden signatures. Golden tests protect contract meaning rather than freezing every byte of generated output.

## Clean-room policy

OrbitFabric is independent open-source work.

Public examples must be synthetic or based only on material that can legally be used and redistributed. Proprietary mission data, private packet formats, employer-owned code, customer-owned details, operational logs, export-controlled material and NDA-protected information are prohibited.

See [Clean-Room Policy](CLEAN_ROOM_POLICY.md).

## Release notes

The current release notes are in [v1.3.0 Adapter Management Foundation](releases/v1.3.0.md).

The complete release history is available under the **Releases** section of this documentation site and in the repository `CHANGELOG.md`.
