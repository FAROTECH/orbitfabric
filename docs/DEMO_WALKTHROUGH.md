# Demo Walkthrough

This page explains the current OrbitFabric demo mission:

```text
examples/demo-3u/
```

The demo is synthetic and clean-room.

Current project release:

```text
v1.2.0 - Core Integration Input Consolidation
```

The stable Mission Data Contract commitment originated with:

```text
v1.0.0 - Stable Mission Data Contract
```

v1.2.0 extends the stable Core boundary additively without changing Mission Model semantics.

---

## 1. Demo purpose

The `demo-3u` mission demonstrates the OrbitFabric vertical slice:

```text
Define once. Validate. Simulate. Test. Document. Integrate.
```

The goal is not to model a real CubeSat.

The goal is to show how one Mission Data Contract can be reused across linting, documentation, deterministic scenario execution, runtime-facing contract bindings, ground-facing integration artifacts, stable Core-owned structured surfaces, a coherent external-integration input set, candidate inspection surfaces, golden signatures and compatibility governance.

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

The selected demonstration chain is:

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
        -> mission_snapshot.json
        -> selected golden signatures protecting stable Core-owned surface fields
```

This demonstrates Mission Data Contract continuity.

It does not demonstrate flight readiness, ground readiness, protocol compliance or operational completeness.

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

The simulation JSON reports include additive v1.1.0 structured expectation accounting while preserving the legacy top-level `failed_expectations` compatibility list. Those additions remain candidate after v1.2.0.

---

## 5. Export stable Core-owned structured surfaces

The stable Core-owned inspection chain is:

```text
mission_snapshot.json       -> What complete Mission Model did Core load?
model_summary.json          -> What contract domains are present?
entity_index.json           -> What contract entities are defined?
relationship_manifest.json  -> Which admitted explicit relationships connect them?
```

Export the stable surfaces:

```bash
orbitfabric export mission-snapshot examples/demo-3u/mission/ \
  --json examples/demo-3u/generated/reports/mission_snapshot.json

orbitfabric export model-summary examples/demo-3u/mission/ \
  --json examples/demo-3u/generated/reports/model_summary.json

orbitfabric export entity-index examples/demo-3u/mission/ \
  --json examples/demo-3u/generated/reports/entity_index.json

orbitfabric export relationship-manifest examples/demo-3u/mission/ \
  --json examples/demo-3u/generated/reports/relationship_manifest.json
```

The seven FDIR relationship families admitted in v1.2.0 are additive stable-compatible families derived from explicit Mission Model fields. Unknown additive family semantics must never be guessed.

These reports are read-only Core-owned structured surfaces. They do not expose graph behavior, plugin execution, runtime behavior, ground behavior or Studio-specific APIs.

---

## 6. Export the stable Core Integration Input Set

The production-facing Core-to-external-integration boundary is:

```bash
orbitfabric export integration-input-set examples/demo-3u/mission/ \
  --output-dir examples/demo-3u/generated/reports/integration_input
```

The coherent set contains:

```text
integration_input_manifest.json
mission_snapshot.json
entity_index.json
relationship_manifest.json
lint_report.json
model_summary.json
```

The manifest records exact surface roles, availability, kind/version identity and SHA-256 digests plus a deterministic RFC 8785/JCS-based `input_set_sha256`.

The manifest is published last. Without a valid manifest, a directory of files is not a coherent Integration Input Set.

An external adapter must reject incompatible required surfaces and must not reconstruct semantics from raw Mission Model YAML.

---

## 7. Export candidate v1.1.0 Core-owned inspection surfaces

The candidate Core-owned inspection chain remains:

```text
dashboard_summary.json       -> Dashboard-ready aggregation of existing Core facts
scenario_run_index.json      -> Index of Core simulation JSON report runs
coverage_summary.json        -> Limited coverage derived from Core structured outputs
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

These surfaces remain candidate after v1.2.0. They do not make OrbitFabric Core a dashboard backend, Studio API, graph engine, runtime framework or ground segment.

---

## 8. Generate runtime-facing contract bindings

```bash
orbitfabric gen runtime examples/demo-3u/mission/
```

Validate the generated C++17 host-build smoke target:

```bash
cmake -S examples/demo-3u/generated/runtime/cpp17 -B examples/demo-3u/generated/runtime/cpp17/build
cmake --build examples/demo-3u/generated/runtime/cpp17/build
```

The generated C++17 files expose deterministic identifiers, metadata registries, command argument structs and abstract adapter interfaces.

They do not implement command dispatch, telemetry polling, scheduling, HAL, drivers, storage, downlink or flight behavior.

---

## 9. Generate ground-facing integration artifacts

```bash
orbitfabric gen ground examples/demo-3u/mission/
```

Default omitted output path:

```text
examples/demo-3u/generated/ground/generic/
```

These artifacts expose the Mission Data Contract to ground-side review and downstream integration workflows.

They do not implement a ground segment, decoder, telemetry archive, database, operator console, command uplink service, Yamcs integration, OpenC3 integration or XTCE-compliant mission database.

---

## 10. Generate mission documentation

```bash
orbitfabric gen docs examples/demo-3u/mission/
```

Default omitted output path:

```text
examples/demo-3u/generated/docs/
```

A dedicated data-flow generator is also available:

```bash
orbitfabric gen data-flow examples/demo-3u/mission/ \
  --output-file examples/demo-3u/generated/docs/data_flow.md
```

Generated documentation describes the contract; it does not implement runtime behavior.

---

## 11. Review stability and compatibility references

The current classification is documented through:

```text
Stability and Compatibility Contract
Mission Model Stability Contract
Release Compatibility Policy
v1.0 Stable Surface Decision
v1.0 Demo Evidence Chain
v1.0 Compatibility and Migration Notes
Golden Output and Regression Confidence Policy
v1.2 Integration Input Stability Decision
Post-v1 Integration Surface Classification
Mission Snapshot Surface
Core Integration Input Contract
Relationship Manifest Surface
Projection Profile Contract
Integration Result Contract
Integration Package and Adapter Execution Contract
```

The Projection Profile, Integration Result and Integration Package / Adapter Execution contracts remain extension-owned `0.1-candidate` contracts after v1.2.0.

---

## 12. What this proves

The demo proves that OrbitFabric can:

- load and structurally validate a multi-file YAML Mission Model;
- run semantic lint rules;
- execute deterministic host-side scenario evidence;
- record contract-level data-flow evidence;
- export stable Core-owned structured surfaces;
- export a stable coherent Core Integration Input Set;
- emit additive stable-compatible FDIR relationship families;
- produce candidate downstream inspection surfaces;
- generate runtime-facing contract bindings;
- validate generated C++17 bindings with a host-build smoke target;
- generate ground-facing contract artifacts;
- protect selected stable surface fields with golden signatures.

The wider project additionally reference-proves the Core input boundary through an external OpenOBSW/OpenSVF Integration Package and independent OrbitFabric Studio consumption.

---

## 13. What this does not prove

The demo does not prove:

- flight readiness or real-time behavior;
- hardware integration;
- real onboard storage/downlink execution;
- real contact scheduling;
- orbit propagation or RF link budget simulation;
- CCSDS/PUS/CFDP compliance;
- generic compatibility with cFS, F Prime, Yamcs or OpenC3;
- XTCE compliance;
- binary decoder/encoder behavior;
- command uplink, telemetry archive, database or operator-console behavior;
- HAL or RTOS integration;
- relationship/dependency graph behavior;
- Core plugin discovery/loading/execution;
- qualification for operational spacecraft use.

Those are intentionally outside the current Core scope.
