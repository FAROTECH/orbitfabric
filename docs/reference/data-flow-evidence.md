# Data Flow Evidence

Status: Development preview  
Scope: Introduced in OrbitFabric v0.6.0 and retained in the v0.7.0 baseline

---

## 1. Purpose

Data Flow Evidence is the contract-level link between command behavior and mission data movement assumptions.

It lets OrbitFabric trace a declared path from a command to a data product and then to the storage, downlink and contact assumptions already present in the Mission Model.

The core evidence chain is:

```text
command expected effect
        -> data product
        -> storage intent
        -> downlink intent
        -> eligible downlink flow
        -> matching contact window
```

This keeps the Mission Data Chain explicit before runtime-facing contract bindings or ground integration artifacts consume it.

---

## 2. Source of truth

The source of truth remains the Mission Model and scenario YAML.

Data-flow evidence is derived from:

```text
commands.yaml
        expected_effects.data_products

data_products.yaml
        storage intent
        downlink intent

contacts.yaml
        downlink flows
        contact windows

scenarios/*.yaml
        expect.data_flow assertions
```

Generated documentation and JSON reports are derived artifacts.

They are not the source of truth.

---

## 3. Command-declared data product effects

A command may declare that it is expected to produce or trigger one or more data products:

```yaml
expected_effects:
  data_products:
    - payload.radiation_histogram
```

OrbitFabric validates this field through command lint rules.

The field must be a list of data product IDs declared in `data_products.yaml`.

Relevant diagnostics:

```text
OF-CMD-008 expected_effects.data_products must be a list / contain only strings
OF-CMD-009 expected_effects references unknown data product
```

---

## 4. Scenario data-flow assertions

Scenarios may assert that data-flow evidence exists and matches declared contract assumptions.

Example:

```yaml
expect:
  data_flow:
    data_product: payload.radiation_histogram
    triggered_by_command: payload.start_acquisition
    storage_intent_declared: true
    downlink_intent_declared: true
    eligible_downlink_flow: science_next_available_contact
    contact_window: demo_contact_001
```

The scenario loader validates references before execution.

Relevant diagnostics:

```text
OF-SCN-014 unknown data product in data-flow expectation
OF-SCN-015 unknown command in data-flow expectation
OF-SCN-016 unknown downlink flow in data-flow expectation
OF-SCN-017 unknown contact window in data-flow expectation
```

---

## 5. Simulation evidence

During deterministic host-side scenario execution, OrbitFabric records data-flow evidence when an accepted command declares data product effects.

The simulator records evidence such as:

```text
DATA_PRODUCT payload.radiation_histogram CONTRACT_EVIDENCE_RECORDED
DATA_FLOW payload.radiation_histogram EXPECTATION_MET
```

The evidence is held in simulator state and exported into the simulation JSON report.

---

## 6. JSON report evidence

Simulation reports include:

```json
{
  "summary": {
    "data_flow_evidence": 1
  },
  "data_flow_evidence": [
    {
      "t": 5,
      "data_product_id": "payload.radiation_histogram",
      "producer": "demo_iod_payload",
      "producer_type": "payload",
      "triggered_by_command": "payload.start_acquisition",
      "storage_intent": {
        "declared": true,
        "class": "science",
        "retention": "7d",
        "overflow_policy": "drop_oldest"
      },
      "downlink_intent": {
        "declared": true,
        "policy": "next_available_contact"
      },
      "eligible_downlink_flows": [
        "science_next_available_contact"
      ],
      "contact_windows": [
        "demo_contact_001"
      ]
    }
  ]
}
```

See also:

```text
Reference -> JSON Reports v0.1
```

---

## 7. Generated data-flow documentation

The standard documentation generator produces:

```text
generated/docs/data_flow.md
```

through:

```bash
orbitfabric gen docs examples/demo-3u/mission/
```

A dedicated generator is also available:

```bash
orbitfabric gen data-flow examples/demo-3u/mission/ \
  --output-file generated/docs/data_flow.md
```

The generated page summarizes declared command-to-data-product paths and renders:

```text
Command
Data Product
Producer
Storage Intent
Downlink Intent
Eligible Downlink Flows
Matching Contact Windows
```

---

## 8. Demo scenario

The canonical data-flow evidence demo scenario is:

```text
examples/demo-3u/scenarios/payload_data_flow_evidence.yaml
```

It demonstrates:

```text
payload.start_acquisition
        -> payload.radiation_histogram
        -> storage intent declared
        -> downlink intent declared
        -> science_next_available_contact
        -> demo_contact_001
```

Run it with:

```bash
orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml \
  --json generated/reports/payload_data_flow_evidence_report.json \
  --log generated/logs/payload_data_flow_evidence.log
```

---

## 9. Boundary

Data Flow Evidence does not implement:

```text
real payload file generation
onboard storage writes
file-system behavior
compression
onboard queues
real downlink execution
contact scheduling
RF behavior
ground station operations
CCSDS/PUS/CFDP behavior
runtime behavior
```

It is deterministic contract-level evidence.

It proves that declared Mission Model assumptions are connected and inspectable.

It does not prove that real flight or ground software exists.

---

## 10. Architectural meaning

v0.6 completed the first end-to-end Mission Data Chain evidence slice:

```text
Payload Contract
        -> Data Product Contract
        -> Storage Intent
        -> Downlink Intent
        -> Contact Window Assumption
        -> Downlink Flow Contract
        -> Commandability and Autonomy Contract
        -> End-to-End Mission Data Flow Evidence
```

v0.7 builds on this by deriving runtime-facing contract bindings from the same validated Mission Model.

Data Flow Evidence remains a contract-level precondition for meaningful runtime-facing and ground-facing generated artifacts.
