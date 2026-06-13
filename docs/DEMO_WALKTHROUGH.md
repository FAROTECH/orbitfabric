# Demo Walkthrough

This page explains the current OrbitFabric demo mission:

```text
examples/demo-3u/
```

The demo is synthetic and clean-room.

Current project release:

```text
v1.1.0 - Candidate Integration Surface Consolidation
```

Stable Mission Data Contract baseline:

```text
v1.0.0 - Stable Mission Data Contract
```

---

## 1. Demo purpose

The `demo-3u` mission demonstrates the OrbitFabric vertical slice:

```text
Define once. Validate. Simulate. Test. Document. Integrate.
```

The goal is not to model a real CubeSat.

The goal is to show how a Mission Data Contract can define mission data and operational behavior once, then reuse it across linting, documentation, deterministic scenario execution, runtime-facing contract bindings, ground-facing integration artifacts, stable Core-owned structured surfaces, candidate Core-owned integration surfaces, golden signatures and compatibility governance references.

---

## 2. Demo structure

The demo lives under:

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

The `mission/` directory contains the Mission Model.

The `scenarios/` directory contains executable host-side operational scenarios.

---

## 3. Scenario evidence chain

The selected v1.0 demonstration chain is:

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

This demonstrates Mission Data Contract continuity.

It does not demonstrate flight readiness, ground readiness, protocol compliance, tool-specific integration or operational completeness.

---

## 4. Run the scenarios

Battery-low recovery:

```bash
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml
```

Payload data-flow evidence:

```bash
orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml
```

Expected result:

```text
Result: PASSED
```

Generate scenario JSON reports and logs:

```bash
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml \
  --json examples/demo-3u/generated/reports/battery_low_during_payload_report.json \
  --log examples/demo-3u/generated/logs/battery_low_during_payload.log

orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml \
  --json examples/demo-3u/generated/reports/payload_data_flow_evidence_report.json \
  --log examples/demo-3u/generated/logs/payload_data_flow_evidence.log
```

The simulation JSON reports include additive v1.1.0 structured expectation accounting while preserving the legacy top-level `failed_expectations` compatibility list.

---

## 5. Export stable v1.0.0 Core-owned structured surfaces

The stable Core-owned structured surface chain is:

```text
model_summary.json          -> What contract domains are present?
entity_index.json           -> What contract entities are defined?
relationship_manifest.json  -> How are indexed contract entities related?
```

Export the stable surfaces:

```bash
orbitfabric export model-summary examples/demo-3u/mission/ \
  --json examples/demo-3u/generated/reports/model_summary.json

orbitfabric export entity-index examples/demo-3u/mission/ \
  --json examples/demo-3u/generated/reports/entity_index.json

orbitfabric export relationship-manifest examples/demo-3u/mission/ \
  --json examples/demo-3u/generated/reports/relationship_manifest.json
```

These reports are read-only Core-owned structured surfaces.

They do not expose relationship graph behavior, dependency graph behavior, plugin APIs, plugin execution, runtime behavior, ground behavior or Studio-specific APIs.

---

## 6. Export candidate v1.1.0 Core-owned integration surfaces

The candidate Core-owned integration surface chain is:

```text
dashboard_summary.json      -> Dashboard-ready aggregation of existing Core facts
scenario_run_index.json     -> Index of Core simulation JSON report runs
coverage_summary.json       -> Limited coverage derived from Core structured outputs
simulation JSON expectations -> Additive structured expectation accounting
```

Export the candidate surfaces:

```bash
orbitfabric export dashboard-summary examples/demo-3u/mission/

orbitfabric export scenario-run-index \
  --simulation-reports examples/demo-3u/generated/reports \
  --json examples/demo-3u/generated/reports/scenario_run_index.json

orbitfabric export coverage-summary examples/demo-3u/mission/
```

With omitted output paths, mission-based commands write under:

```text
examples/demo-3u/generated/reports/
```

Expected candidate outputs include:

```text
examples/demo-3u/generated/reports/dashboard_summary.json
examples/demo-3u/generated/reports/scenario_run_index.json
examples/demo-3u/generated/reports/coverage_summary.json
```

These surfaces are Core-owned and candidate.

They are not part of the original v1.0.0 stable surface.

They do not make OrbitFabric Core a dashboard backend, Studio API, OpenOBSW/OpenSVF-specific generator, graph engine, runtime framework or ground segment.

---

## 7. Generate runtime-facing contract bindings

Generate runtime-facing contract bindings for the same `demo-3u` Mission Model:

```bash
orbitfabric gen runtime examples/demo-3u/mission/
```

Validate the generated C++17 host-build smoke target:

```bash
cmake -S examples/demo-3u/generated/runtime/cpp17 -B examples/demo-3u/generated/runtime/cpp17/build
cmake --build examples/demo-3u/generated/runtime/cpp17/build
```

The generated C++17 files expose the contract surface as deterministic identifiers, metadata registries, command argument structs and abstract adapter interfaces.

They do not implement command dispatch, telemetry polling, scheduling, HAL, drivers, storage, downlink or flight behavior.

---

## 8. Generate ground-facing integration artifacts

Generate ground-facing integration artifacts for the same `demo-3u` Mission Model:

```bash
orbitfabric gen ground examples/demo-3u/mission/
```

Default omitted output path:

```text
examples/demo-3u/generated/ground/generic/
```

These artifacts expose the mission data contract to ground-side review and downstream integration workflows.

They do not implement a ground segment, decoder, telemetry archive, database, operator console, command uplink service, Yamcs integration, OpenC3 integration or XTCE-compliant mission database.

---

## 9. Generate mission documentation

```bash
orbitfabric gen docs examples/demo-3u/mission/
```

Default omitted output path:

```text
examples/demo-3u/generated/docs/
```

A dedicated generator is also available:

```bash
orbitfabric gen data-flow examples/demo-3u/mission/ \
  --output-file examples/demo-3u/generated/docs/data_flow.md
```

None of these pages describes runtime behavior.

---

## 10. Review stability and compatibility references

v1.0.0 defines the stable Mission Data Contract posture through these references:

```text
Stability and Compatibility Contract
Mission Model Stability Contract
CLI Contract v1
Generated Surfaces Stability
Lint Rule Code Stability
JSON Report Compatibility
Scenario Evidence Stability
Release Compatibility Policy
v1.0 Stable Surface Decision
v1.0 Demo Evidence Chain
v1.0 Compatibility and Migration Notes
Golden Output and Regression Confidence Policy
Extensibility Boundary Contract
```

v1.1.0 candidate integration surfaces are documented through:

```text
Post-v1 Candidate Integration Surfaces
Dashboard Summary Surface
Scenario Run Index Surface
Coverage Summary Surface
```

These references classify stable and candidate surfaces. They do not add Mission Model semantics, YAML fields, runtime behavior, ground behavior or plugin execution.

---

## 11. What this proves

The demo proves that OrbitFabric can:

- load a multi-file YAML Mission Model;
- validate Mission Model structure;
- run semantic lint rules;
- execute deterministic host-side scenario evidence;
- record contract-level data-flow evidence;
- produce stable v1.0.0 Core-owned structured surfaces;
- produce candidate v1.1.0 Core-owned integration surfaces;
- generate runtime-facing contract bindings;
- validate generated C++17 bindings with a host-build smoke target;
- generate ground-facing contract artifacts;
- protect selected stable surface fields with golden signatures.

---

## 12. What this does not prove

The demo does not prove:

- flight readiness;
- real-time behavior;
- hardware integration;
- real onboard storage execution;
- real downlink execution;
- real contact scheduling;
- orbit propagation;
- RF link budget simulation;
- CCSDS, PUS or CFDP compliance;
- compatibility with cFS, F Prime, Yamcs or OpenC3;
- XTCE compliance;
- binary decoder behavior;
- command uplink behavior;
- telemetry archive behavior;
- database behavior;
- operator console behavior;
- command dispatch runtime behavior;
- telemetry polling runtime behavior;
- HAL or RTOS integration;
- relationship graph behavior;
- dependency graph behavior;
- plugin API behavior;
- plugin discovery behavior;
- plugin loading behavior;
- plugin execution behavior;
- qualification for operational spacecraft use.

Those are intentionally outside the current scope.
