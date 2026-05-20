# Demo Walkthrough

This page explains the current OrbitFabric demo mission:

```text
examples/demo-3u/
```

The demo is synthetic and clean-room. It is not based on a real spacecraft, private mission, proprietary bus map, private payload or operational log.

---

## 1. Demo purpose

The `demo-3u` mission demonstrates the OrbitFabric vertical slice:

```text
Define once. Validate. Simulate. Test. Document. Integrate.
```

The goal is not to model a real CubeSat.

The goal is to show how a Mission Data Contract can define mission data and operational behavior once, then reuse it across linting, documentation, deterministic scenario execution, runtime-facing contract bindings, ground-facing integration artifacts, Core-owned introspection surfaces, entity index surfaces, relationship manifest surfaces, golden signatures and v1.0 compatibility governance references.

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

## 3. Mission Model files

The Mission Model defines the synthetic spacecraft, subsystems, modes, telemetry, commands, events, faults, packets and policies.

It also defines contract domains:

```text
payloads.yaml          -> synthetic IOD payload contract
data_products.yaml     -> synthetic payload data product contract
contacts.yaml          -> synthetic contact/downlink assumptions
commandability.yaml    -> synthetic commandability/autonomy assumptions
```

The key declared data product is:

```text
payload.radiation_histogram
        producer: demo_iod_payload
        type: histogram
        estimated size: 4096 bytes
        priority: high
        storage class: science
        retention: 7d
        overflow policy: drop_oldest
        downlink policy: next_available_contact
```

The key declared downlink path is:

```text
primary_ground_contact
        link: uhf_downlink_nominal
        window: demo_contact_001
        flow: science_next_available_contact
        eligible data product: payload.radiation_histogram
```

The key commandability slice is:

```text
ground_operator
        -> payload.start_acquisition commandability rule

onboard_autonomy
        -> stop payload on low/critical battery faults
        -> recovery intents toward DEGRADED and SAFE
```

These are contract assumptions only. They do not implement live uplink, operator authentication, real onboard storage, real downlink queues, real contact scheduling, RF behavior, ground operations or recovery execution behavior.

---

## 4. Scenarios

The demo includes:

```text
examples/demo-3u/scenarios/battery_low_during_payload.yaml
examples/demo-3u/scenarios/nominal_payload_acquisition.yaml
examples/demo-3u/scenarios/payload_data_flow_evidence.yaml
```

`battery_low_during_payload.yaml` demonstrates a degraded recovery path.

`nominal_payload_acquisition.yaml` demonstrates a nominal payload lifecycle path.

`payload_data_flow_evidence.yaml` demonstrates the contract-level data-flow evidence path.

---

## 5. Scenario: battery low during payload operation

The battery-low scenario demonstrates this host-side sequence:

```text
payload.start_acquisition
-> payload.acquisition_started
-> NOMINAL -> PAYLOAD_ACTIVE
-> battery voltage degradation
-> eps.battery_low
-> PAYLOAD_ACTIVE -> DEGRADED
-> payload.stop_acquisition AUTO_DISPATCHED
-> payload.acquisition_stopped
-> payload.acquisition.active = false
-> SCENARIO PASSED
```

This remains a deterministic host-side operational scenario.

It does not execute storage, downlink, live uplink or autonomy runtime behavior.

---

## 6. Scenario: payload data-flow evidence

The data-flow evidence scenario demonstrates the contract chain:

```text
payload.start_acquisition
-> payload.acquisition_started
-> payload lifecycle ACQUIRING
-> payload.acquisition.active = true
-> DATA_PRODUCT payload.radiation_histogram CONTRACT_EVIDENCE_RECORDED
-> DATA_FLOW payload.radiation_histogram EXPECTATION_MET
-> payload.stop_acquisition
-> payload.acquisition_stopped
-> payload lifecycle READY
-> payload.acquisition.active = false
-> SCENARIO PASSED
```

The scenario checks that the command-declared data product effect is traceable to:

```text
payload.start_acquisition
        -> payload.radiation_histogram
        -> storage intent declared
        -> downlink intent declared
        -> science_next_available_contact
        -> demo_contact_001
```

This is deterministic contract-level evidence generated from the Mission Model and scenario expectations.

It is not real payload file generation, onboard storage, downlink queue execution or contact scheduling.

---

## 7. Export Core-owned structured surfaces

The stable Core-owned structured surface chain is:

```text
model_summary.json          -> What contract domains are present?
entity_index.json           -> What contract entities are defined?
relationship_manifest.json  -> How are indexed contract entities related?
```

Export the model summary:

```bash
orbitfabric export model-summary examples/demo-3u/mission/ \
  --json generated/reports/model_summary.json
```

Export the entity index:

```bash
orbitfabric export entity-index examples/demo-3u/mission/ \
  --json generated/reports/entity_index.json
```

Export the relationship manifest:

```bash
orbitfabric export relationship-manifest examples/demo-3u/mission/ \
  --json generated/reports/relationship_manifest.json
```

For `demo-3u`, the relationship manifest emits 46 relationship records across 17 emitted relationship families.

The stable v1.0 relationship manifest surface admits 19 deliberately narrow relationship families documented in `docs/reference/relationship-manifest-surface.md`.

These reports are read-only Core-owned structured surfaces.

They do not expose relationship graph behavior, dependency graph behavior, plugin APIs, plugin execution, runtime behavior, ground behavior or Studio-specific APIs.

---

## 8. Review stability and compatibility references

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

These references classify the current Mission Model, CLI, JSON reports, lint diagnostics, generated surfaces, scenario evidence and release compatibility expectations.

They do not add Mission Model semantics, YAML fields, generated surfaces, CLI behavior, report fields, lint diagnostics, scenario behavior, runtime behavior, ground behavior or plugin execution.

---

## 9. Generate runtime-facing contract bindings

Generate runtime-facing contract bindings for the same `demo-3u` Mission Model:

```bash
orbitfabric gen runtime examples/demo-3u/mission/
```

Generated files:

```text
generated/runtime/cpp17/
├── runtime_contract_manifest.json
├── CMakeLists.txt
├── include/orbitfabric/generated/
│   ├── mission_ids.hpp
│   ├── mission_enums.hpp
│   ├── mission_registries.hpp
│   ├── command_args.hpp
│   └── adapter_interfaces.hpp
└── src/
    └── orbitfabric_runtime_contract_smoke.cpp
```

The generated C++17 files expose the contract surface as deterministic identifiers, metadata registries, command argument structs and abstract adapter interfaces.

They do not implement command dispatch, telemetry polling, scheduling, HAL, drivers, storage, downlink or flight behavior.

They remain public preview disposable generated artifacts in v1.0.0.

---

## 10. Validate the generated C++17 host-build smoke target

After generating runtime bindings, run:

```bash
cmake -S generated/runtime/cpp17 -B generated/runtime/cpp17/build
cmake --build generated/runtime/cpp17/build
```

This confirms that the generated contract-binding surface is syntactically valid and host-buildable as C++17.

It does not validate flight behavior.

---

## 11. Generate ground-facing integration artifacts

Generate ground-facing integration artifacts for the same `demo-3u` Mission Model:

```bash
orbitfabric gen ground examples/demo-3u/mission/
```

Generated files:

```text
generated/ground/generic/
├── ground_contract_manifest.json
├── README.md
├── dictionaries/
│   ├── telemetry_dictionary.json
│   ├── command_dictionary.json
│   ├── event_dictionary.json
│   ├── fault_dictionary.json
│   ├── data_product_dictionary.json
│   └── packet_dictionary.json
├── csv/
│   ├── telemetry_dictionary.csv
│   ├── command_dictionary.csv
│   ├── event_dictionary.csv
│   ├── fault_dictionary.csv
│   ├── data_product_dictionary.csv
│   └── packet_dictionary.csv
└── ground_dictionaries.md
```

These artifacts expose the mission data contract to ground-side review and downstream integration workflows.

They remain public preview disposable generated artifacts in v1.0.0.

They do not implement a ground segment, decoder, telemetry archive, database, operator console, command uplink service, Yamcs integration, OpenC3 integration or XTCE-compliant mission database.

---

## 12. Run the scenarios

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

---

## 13. Generate scenario outputs

Battery-low recovery outputs:

```bash
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml \
  --json generated/reports/battery_low_during_payload_report.json \
  --log generated/logs/battery_low_during_payload.log
```

Data-flow evidence outputs:

```bash
orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml \
  --json generated/reports/payload_data_flow_evidence_report.json \
  --log generated/logs/payload_data_flow_evidence.log
```

Generated files:

```text
generated/reports/battery_low_during_payload_report.json
generated/logs/battery_low_during_payload.log
generated/reports/payload_data_flow_evidence_report.json
generated/logs/payload_data_flow_evidence.log
```

---

## 14. Generate mission documentation

```bash
orbitfabric gen docs examples/demo-3u/mission/
```

Generated files:

```text
generated/docs/
├── telemetry.md
├── commands.md
├── events.md
├── faults.md
├── modes.md
├── packets.md
├── payloads.md
├── data_products.md
├── contacts.md
├── commandability.md
└── data_flow.md
```

A dedicated generator is also available:

```bash
orbitfabric gen data-flow examples/demo-3u/mission/ \
  --output-file generated/docs/data_flow.md
```

None of these pages describes runtime behavior.

---

## 15. What the simulator checks

During execution, OrbitFabric checks that:

- commands exist in the Mission Model;
- commands are allowed in the current mode;
- expected command effects are applied;
- payload lifecycle preconditions are respected;
- events are emitted;
- telemetry injections update simulation state;
- fault conditions are evaluated;
- mode transitions occur;
- auto-dispatched recovery commands are recorded;
- command-declared data product effects record data-flow evidence;
- data-flow expectations match recorded evidence;
- storage intent declaration is inspectable;
- downlink intent declaration is inspectable;
- eligible downlink flow evidence is inspectable;
- matching contact window evidence is inspectable;
- scenario expectations pass.

The simulator does not execute real storage, real downlink, live uplink, contact scheduling or autonomy runtime behavior.

---

## 16. Expected final state

At the end of the battery-low scenario:

```text
mode = DEGRADED
payload lifecycle = READY
payload.acquisition.active = false
scenario_status = PASSED
```

At the end of the data-flow evidence scenario:

```text
mode = PAYLOAD_ACTIVE
payload lifecycle = READY
payload.acquisition.active = false
data_flow_evidence contains payload.radiation_histogram
scenario_status = PASSED
```

The important contract-level behavior is the evidence path:

```text
command accepted
  -> payload lifecycle and telemetry effects applied
  -> data product evidence recorded
  -> storage/downlink/contact intent checked
  -> scenario evidence produced
  -> runtime-facing bindings generated from the same model
  -> ground-facing artifacts generated from the same model
  -> model summary exported from the same model
  -> entity index exported from the same model
  -> relationship manifest exported from the same model
  -> v1.0 compatibility governance explains current surface stability
```

---

## 17. Clean-room boundary

This demo is deliberately synthetic.

It must not include:

- real mission names;
- private subsystem architectures;
- private bus maps;
- private payload protocols;
- real thresholds from private missions;
- real operational procedures;
- real telemetry logs;
- real anomaly sequences;
- real payload data;
- real storage or downlink policies;
- real ground station details;
- real RF assumptions.

The demo exists to prove OrbitFabric's architecture, not to approximate a real spacecraft.
