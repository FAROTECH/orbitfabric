<div align="center">
  <img src="assets/brand/orbitfabric-logo-horizontal-light.png" alt="OrbitFabric" width="760">
</div>

<br>

<div align="center">

**Model-first Mission Data Fabric for small spacecraft**

Define mission data once. Validate it. Simulate it. Document it. Generate deterministic contract-facing artifacts from the same source of truth.

</div>

---

## Overview

OrbitFabric is a **model-first Mission Data Fabric** for small spacecraft.

It lets teams define a Mission Data Contract once, using a structured Mission Model, and reuse that contract across validation, documentation, testing, scenario evidence, runtime-facing bindings, ground-facing integration artifacts and Core-owned structured surfaces.

OrbitFabric is not a flight software framework, not a ground segment and not a spacecraft dynamics simulator.

It is the contract layer between:

```text
mission design
onboard software
simulation
testing
documentation
runtime-facing integration
ground integration
downstream inspection tools
future extension-owned outputs
```

> Define once. Validate. Simulate. Test. Document. Integrate.

---

## Current Status

OrbitFabric is currently released at:

```text
v1.1.0 - Candidate Integration Surface Consolidation
```

v1.1.0 consolidates the post-v1 candidate Core-owned integration surfaces while preserving the deliberately narrow v1.0.0 Stable Mission Data Contract.

The stable surface is intentionally limited.

OrbitFabric v1.1.0 is not a flight software framework, not a ground segment, not a mission control system, not a spacecraft dynamics simulator, not a plugin execution platform and not a tool-specific integration layer.

The stable Core-owned structured surface chain is:

```text
model_summary.json          -> What contract domains are present?
entity_index.json           -> What contract entities are defined?
relationship_manifest.json  -> How are indexed contract entities related?
```

The post-v1 candidate Core-owned integration surface chain is:

```text
dashboard_summary.json      -> Dashboard-ready aggregation of existing Core facts
scenario_run_index.json     -> Index of Core simulation JSON report runs
coverage_summary.json       -> Limited coverage derived from Core structured outputs
simulation JSON expectations -> Additive structured expectation accounting
```

These post-v1 surfaces are **candidate**, not part of the original v1.0.0 stable surface.

They are Core-owned read-only structured outputs intended for downstream inspection tools.

They do not make OrbitFabric Core a dashboard backend, flight software framework, ground segment, runtime framework, graph engine, Studio API or OpenOBSW/OpenSVF-specific generator.

The ownership boundary is:

```text
Core defines, computes and emits contract-significant structured surfaces.
Studio and other downstream tools consume, link, navigate and render them.
Downstream tools must not invent private coverage, health or completeness semantics.
```

Generated artifact default paths are mission-workspace relative for mission-based commands.

For example:

```bash
orbitfabric gen ground examples/demo-3u/mission/
```

writes to:

```text
examples/demo-3u/generated/ground/generic/
```

Explicit user-provided output paths are preserved unchanged.

The stable v1.0 posture is:

```text
Mission Model remains the source of truth.
Core owns Mission Data Contract semantics.
Core-owned structured surfaces are derived from the validated Mission Model.
Downstream tools consume Core-owned structured surfaces.
Generated runtime-facing and ground-facing artifacts remain reproducible and disposable unless explicitly classified otherwise.
Plugin execution remains out of scope.
```

The v1.0 golden signatures protect selected contract-significant fields of existing Core-owned structured surfaces.

They do not freeze full generated JSON files, absolute paths, human-oriented output, Markdown wording, generated runtime bindings, generated ground dictionaries or disposable artifact formatting.

The v1.0 demo evidence chain proves Mission Data Contract continuity from one validated Mission Model across scenario evidence, generated review artifacts and Core-owned structured surfaces.

It does not prove flight readiness, ground readiness, protocol compliance, tool-specific integration or operational completeness.

---

## What OrbitFabric Is

OrbitFabric is a Mission Data Contract framework.

It models:

- telemetry;
- commands;
- events;
- faults;
- operational modes;
- packets;
- scenarios;
- optional Payload / IOD Payload Contracts;
- optional Data Product and Storage Contracts;
- optional Contact Windows and Downlink Flow Contracts;
- optional Commandability and Autonomy Contracts;
- contract-level Mission Data Flow Evidence;
- generated runtime-facing contract bindings;
- generated ground-facing integration artifacts;
- Core-owned contract introspection surfaces;
- Core-owned entity index surfaces;
- Core-owned relationship manifest surfaces;
- stability and compatibility classifications;
- extensibility boundary rules;
- v1.0 stable Mission Data Contract governance references.

The structured surface chain is:

```text
Mission Model
        -> canonical loader
        -> validated MissionModel
        -> model_summary.json
        -> entity_index.json
        -> relationship_manifest.json
        -> downstream tools and future extensions consume Core-owned structured surfaces
```

---

## What OrbitFabric Is Not

OrbitFabric is not:

- a flight-ready onboard runtime;
- a replacement for cFS or F Prime;
- a replacement for Yamcs or OpenC3;
- a spacecraft physics simulator;
- a CCSDS/PUS/CFDP implementation;
- a hardware abstraction layer;
- a ground segment;
- a mission control system;
- an operator console;
- a telemetry archive;
- a command uplink service;
- a relationship graph;
- a dependency graph;
- a plugin execution layer;
- a plugin loader;
- a plugin discovery mechanism;
- a plugin API;
- a metadata schema;
- a Studio-specific backend API;
- schema migration tooling;
- a JSON Schema publication layer;
- a tool-specific integration layer.

Generated Runtime Skeletons are runtime-facing contract bindings.

Ground Integration Artifacts are ground-facing contract exports.

Contract Introspection, Entity Index and Relationship Manifest surfaces are Core-derived read-only structured surfaces.

Stability, compatibility, extensibility and v1.0 references are governance and documentation surfaces.

None of them is flight software, ground software, plugin execution or a visual modeling tool.

---

## Demo Mission: `demo-3u`

The repository includes a synthetic clean-room demo mission:

```text
examples/demo-3u/
├── mission/
│   ├── spacecraft.yaml
│   ├── subsystems.yaml
│   ├── modes.yaml
│   ├── telemetry.yaml
│   ├── commands.yaml
│   ├── events.yaml
│   ├── faults.yaml
│   ├── packets.yaml
│   ├── policies.yaml
│   ├── payloads.yaml
│   ├── data_products.yaml
│   ├── contacts.yaml
│   └── commandability.yaml
└── scenarios/
    ├── battery_low_during_payload.yaml
    ├── nominal_payload_acquisition.yaml
    └── payload_data_flow_evidence.yaml
```

The v1.0 demo evidence chain focuses on:

```text
payload.start_acquisition
        -> payload.acquisition_started
        -> payload.radiation_histogram data product evidence
        -> storage intent declared
        -> downlink intent declared
        -> science_next_available_contact downlink flow
        -> demo_contact_001 contact window
        -> scenario JSON evidence
        -> runtime-facing contract bindings
        -> ground-facing dictionaries
        -> model_summary.json
        -> entity_index.json
        -> relationship_manifest.json
        -> golden signatures protecting selected Core-owned surface fields
```

---

## Local Development

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Verify the CLI:

```bash
orbitfabric --version
orbitfabric --help
```

Expected current package version:

```text
orbitfabric 1.0.0
```

Run checks:

```bash
ruff check .
pytest
mkdocs build --strict
```

---

## Common Commands

Mission-based commands write omitted generated artifact paths under the mission workspace.

For `examples/demo-3u/mission/`, omitted report outputs resolve under:

```text
examples/demo-3u/generated/reports/
```

Pass `--json`, `--output-dir` or `--output-file` explicitly when a different destination is required.

```bash
orbitfabric lint examples/demo-3u/mission/ \
  --json generated/reports/lint_report.json

orbitfabric export model-summary examples/demo-3u/mission/ \
  --json generated/reports/model_summary.json

orbitfabric export entity-index examples/demo-3u/mission/ \
  --json generated/reports/entity_index.json

orbitfabric export relationship-manifest examples/demo-3u/mission/ \
  --json generated/reports/relationship_manifest.json

orbitfabric export dashboard-summary examples/demo-3u/mission/

orbitfabric export scenario-run-index \
  --simulation-reports generated/reports \
  --json generated/reports/scenario_run_index.json

orbitfabric export coverage-summary examples/demo-3u/mission/

orbitfabric gen docs examples/demo-3u/mission/

orbitfabric gen runtime examples/demo-3u/mission/
cmake -S generated/runtime/cpp17 -B generated/runtime/cpp17/build
cmake --build generated/runtime/cpp17/build

orbitfabric gen ground examples/demo-3u/mission/

orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml \
  --json generated/reports/battery_low_during_payload_report.json \
  --log generated/logs/battery_low_during_payload.log

orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml \
  --json generated/reports/payload_data_flow_evidence_report.json \
  --log generated/logs/payload_data_flow_evidence.log
```

Expected command result for the demo mission:

```text
Result: PASSED
```

Generated artifacts are reproducible outputs. They are not the source of truth.

The source of truth remains:

```text
examples/demo-3u/mission/*.yaml
examples/demo-3u/scenarios/*.yaml
```

---

## Example Mission Slices

The repository includes public, clean-room example slices:

- `examples/demo-3u/`, synthetic clean-room demo mission;
- `examples/university-cubesat-minislice/`, generic university CubeSat minislice;
- `examples/oresat-inspired-minislice/`, public-material-derived low-power, beacon and constrained-downlink minislice;
- `examples/finch-inspired-minislice/`, public-material-derived imaging acquisition, ADCS readiness, compression and constrained-downlink minislice;
- `examples/spacelab-inspired-communications-minislice/`, public-material-derived TT&C, OBDH, beacon, telecommanded data-request and decoder-evidence minislice.

The `*-inspired-*` examples are conceptual public demos. They are not official models, not endorsed by the original project teams, and do not imply adoption of OrbitFabric by those teams.

---

## Documentation

Published documentation is available at:

```text
https://farotech.github.io/orbitfabric/
```

Useful entry points:

- `docs/PROJECT_CHARTER.md`
- `docs/ARCHITECTURE.md`
- `docs/ROADMAP.md`
- `docs/DEVELOPMENT.md`
- `docs/QUICKSTART.md`
- `docs/DEMO_WALKTHROUGH.md`
- `docs/reference/v1-stable-surface-decision.md`
- `docs/reference/v1-demo-evidence-chain.md`
- `docs/reference/v1-compatibility-migration-notes.md`
- `docs/reference/golden-output-regression-confidence.md`
- `docs/reference/extensibility-boundary-contract.md`
- `docs/reference/post-v1-candidate-integration-surfaces.md`
- `docs/reference/dashboard-summary-surface.md`
- `docs/reference/scenario-run-index-surface.md`
- `docs/reference/coverage-summary-surface.md`
- `docs/releases/v1.0.0.md`

Build the documentation site locally:

```bash
mkdocs build --strict
```

---

## Clean-Room Policy

OrbitFabric is developed as a clean-room open-source project.

Do not add private, confidential, proprietary, restricted or non-public mission material to this repository.
