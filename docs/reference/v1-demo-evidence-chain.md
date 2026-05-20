# v1.0 Demo Evidence Chain

Status: Accepted in v1.0.0  
Scope: documentation-only evidence map for the `demo-3u` Mission Model  
Applies to: OrbitFabric Core `v1.0.0 - Stable Mission Data Contract`

This page records the selected v1.0 demonstration evidence chain for OrbitFabric Core.

It explains how the existing `examples/demo-3u` Mission Model demonstrates Mission Data Contract continuity across validation, scenario evidence, generated artifacts and Core-owned structured surfaces.

This page does not introduce new Mission Model semantics, new YAML fields, new CLI behavior, new generated surfaces, new scenario behavior or new compatibility guarantees beyond the v1.0.0 stable release boundary.

---

## 1. Purpose

The v1.0 demo proves one thing clearly:

```text
A single validated Mission Model can carry the same mission-data meaning across commands, events, payloads, data products, storage/downlink intent, scenario evidence, generated artifacts and Core-owned structured surfaces.
```

The demo is not intended to prove flight readiness, ground readiness, protocol compliance or tool-specific integration.

The selected proof path is deliberately narrow and already present in the repository.

---

## 2. Source of truth

The source of truth is:

```text
examples/demo-3u/mission/
```

The evidence scenario is:

```text
examples/demo-3u/scenarios/payload_data_flow_evidence.yaml
```

The supporting generated and exported surfaces are:

```text
generated/reports/payload_data_flow_evidence_report.json
generated/reports/model_summary.json
generated/reports/entity_index.json
generated/reports/relationship_manifest.json
generated/runtime/cpp17/
generated/ground/generic/
generated/docs/
```

Generated files remain disposable.

The Mission Model remains authoritative.

---

## 3. Selected evidence chain

The v1.0 demo evidence chain is:

```text
payload.start_acquisition
        -> payload.acquisition_started
        -> payload lifecycle ACQUIRING
        -> payload.acquisition.active = true
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

This chain demonstrates contract continuity.

It does not demonstrate operational execution.

---

## 4. Mission Model declarations used by the chain

The chain is rooted in existing Mission Model declarations.

| Chain element | Mission Model source | Contract meaning |
|---|---|---|
| `payload.start_acquisition` | `commands.yaml` | Command that starts synthetic payload acquisition. |
| `payload.acquisition_started` | `events.yaml` | Event emitted by the payload acquisition command. |
| `demo_iod_payload` | `payloads.yaml` | Synthetic IOD payload contract. |
| `payload.acquisition.active` | `telemetry.yaml` | Telemetry effect showing payload acquisition state. |
| `payload.radiation_histogram` | `data_products.yaml` | Synthetic payload data product produced by the demo payload. |
| `science_next_available_contact` | `contacts.yaml` | Downlink flow that includes the payload data product. |
| `demo_contact_001` | `contacts.yaml` | Synthetic contact window used to demonstrate downlink assumptions. |
| `primary_ground_contact` | `contacts.yaml` | Synthetic ground contact profile. |
| `uhf_downlink_nominal` | `contacts.yaml` | Abstract downlink link profile. |
| `payload_start_ground_rule` | `commandability.yaml` | Commandability rule for the payload start command. |

These declarations are contract declarations only.

They are not runtime services.

---

## 5. Scenario evidence

The scenario:

```text
examples/demo-3u/scenarios/payload_data_flow_evidence.yaml
```

checks that the declared command effect is traceable to the declared data product and downlink assumptions.

The expected evidence path is:

```text
payload.start_acquisition
        -> payload.radiation_histogram
        -> storage intent declared
        -> downlink intent declared
        -> science_next_available_contact
        -> demo_contact_001
```

The produced JSON report is a machine-readable scenario evidence surface.

The plain-text log remains human-oriented and non-contractual.

---

## 6. Runtime-facing generated artifacts

The same Mission Model can generate runtime-facing C++17 contract bindings:

```bash
orbitfabric gen runtime examples/demo-3u/mission/
```

The generated runtime-facing artifacts expose contract identifiers, registries, command argument structures and adapter interfaces.

They do not implement:

```text
command dispatch
telemetry polling
scheduling
storage
downlink
HAL
drivers
RTOS integration
flight behavior
```

For the v1.0 demo, their role is to show that the same contract can be projected toward runtime-facing code boundaries without becoming flight software.

---

## 7. Ground-facing generated artifacts

The same Mission Model can generate ground-facing generic dictionaries:

```bash
orbitfabric gen ground examples/demo-3u/mission/
```

The generated ground-facing artifacts expose telemetry, command, event, fault, data product and packet dictionaries for review and downstream integration workflows.

They do not implement:

```text
ground segment
mission control
telemetry archive
operator console
command uplink
telemetry decoder
telecommand encoder
Yamcs integration
OpenC3 integration
XTCE mission database
```

For the v1.0 demo, their role is to show that the same contract can be projected toward ground-facing review artifacts without becoming a ground segment.

---

## 8. Core-owned structured surfaces

The same Mission Model can export Core-owned structured surfaces:

```bash
orbitfabric export model-summary examples/demo-3u/mission/ \
  --json generated/reports/model_summary.json

orbitfabric export entity-index examples/demo-3u/mission/ \
  --json generated/reports/entity_index.json

orbitfabric export relationship-manifest examples/demo-3u/mission/ \
  --json generated/reports/relationship_manifest.json
```

These surfaces answer three different questions:

```text
model_summary.json
        What contract domains are present?

entity_index.json
        What contract entities are defined?

relationship_manifest.json
        How are indexed contract entities related?
```

They are Core-owned, read-only and derived from the validated Mission Model.

They are not a second source of truth.

---

## 9. Relationship evidence selected for v1.0

The `relationship_manifest.json` surface is important for the demo because it shows that the chain is not just a narrative.

It exposes relationship records such as:

```text
commands:payload.start_acquisition
        -> command_emits_event
        -> events:payload.acquisition_started

commands:payload.start_acquisition
        -> command_targets_subsystem
        -> subsystems:payload

payloads:demo_iod_payload
        -> payload_accepts_command
        -> commands:payload.start_acquisition

payloads:demo_iod_payload
        -> payload_produces_telemetry
        -> telemetry:payload.acquisition.active

data_products:payload.radiation_histogram
        -> data_product_produced_by_payload
        -> payloads:demo_iod_payload

downlink_flows:science_next_available_contact
        -> downlink_flow_includes_data_product
        -> data_products:payload.radiation_histogram
```

These records are derived from explicit loaded Mission Model fields.

They are not inferred from naming conventions, YAML scanning or downstream assumptions.

---

## 10. Golden signature protection

The v1.0 release includes golden signatures for selected Core-owned structured surface fields:

```text
tests/golden/demo_3u_core_surfaces/model_summary_contract_signature.json
tests/golden/demo_3u_core_surfaces/entity_index_contract_signature.json
tests/golden/demo_3u_core_surfaces/relationship_manifest_contract_signature.json
```

The related test file is:

```text
tests/test_v1_golden_core_surfaces.py
```

These golden signatures protect contract-significant fields such as:

```text
surface kind
surface version
mission identity
boundary flags
domain counts
entity identifiers
relationship family counts
selected relationship records
```

They do not freeze:

```text
absolute paths
full generated JSON files
human-oriented terminal output
Markdown wording
generated runtime bindings
generated ground dictionaries
disposable artifact formatting
```

---

## 11. Validation command sequence

The v1.0 demo evidence chain can be exercised with:

```bash
ruff check .
pytest
mkdocs build --strict

orbitfabric lint examples/demo-3u/mission/

orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml \
  --json generated/reports/payload_data_flow_evidence_report.json \
  --log generated/logs/payload_data_flow_evidence.log

orbitfabric export model-summary examples/demo-3u/mission/ \
  --json generated/reports/model_summary.json

orbitfabric export entity-index examples/demo-3u/mission/ \
  --json generated/reports/entity_index.json

orbitfabric export relationship-manifest examples/demo-3u/mission/ \
  --json generated/reports/relationship_manifest.json

orbitfabric gen runtime examples/demo-3u/mission/
cmake -S generated/runtime/cpp17 -B generated/runtime/cpp17/build
cmake --build generated/runtime/cpp17/build

orbitfabric gen ground examples/demo-3u/mission/
orbitfabric gen docs examples/demo-3u/mission/
```

This validates the contract chain as a host-side, deterministic engineering workflow.

It does not validate flight execution or ground execution.

---

## 12. Explicit non-claims

The v1.0 demo evidence chain must not be described as:

```text
flight-ready
ground-segment-ready
mission-control-ready
XTCE-compatible
Yamcs-ready
OpenC3-ready
F Prime-compatible
cFS-compatible
CCSDS-compliant
PUS-compliant
security-enforcing
plugin-executing
relationship graph behavior
```

The correct claim is narrower:

```text
The demo proves Mission Data Contract continuity from one validated Mission Model across scenario evidence, generated review artifacts and Core-owned structured surfaces.
```

---

## 13. Final position

The v1.0 demo is a proof of engineering continuity, not operational completeness.

The stable message is:

```text
Define the contract once.
Validate it.
Exercise scenario evidence.
Generate review artifacts.
Export Core-owned structured surfaces.
Protect selected stable surface fields with golden signatures.
Keep the Mission Model as the source of truth.
```

That is the v1.0 demonstration posture for OrbitFabric Core.
