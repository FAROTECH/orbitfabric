# Ground Integration Artifacts

Status: Introduced in v0.8.0  
Scope: Ground-facing Mission Data Contract exports

---

## Purpose

Ground Integration Artifacts are generated ground-facing outputs derived from the validated OrbitFabric Mission Model.

Their purpose is to help ground software teams review, adapt and integrate the mission data contract before configuring or implementing their actual ground system.

They are not a ground segment.

They are not a mission control system.

They are not an operator console.

They are not a telemetry archive.

They are not a command uplink service.

They are not a Yamcs, OpenC3 or XTCE integration.

---

## Implemented Flow

The v0.8.0 flow is:

```text
Mission Model
        -> validation and linting
        -> GroundContract
        -> generic ground-facing dictionaries
        -> JSON / Markdown / CSV exports
        -> downstream ground-system integration outside OrbitFabric
```

The source of truth remains the Mission Model.

Generated ground artifacts are reproducible and disposable.

---

## Target User

The primary target user is not the operator of a physical ground station antenna.

The primary target user is a ground segment software engineer, mission control engineer, ground system integrator or test engineer who needs a clear and machine-readable description of the mission data contract.

Typical questions include:

```text
What telemetry can arrive from the spacecraft?
What commands can be issued?
What command arguments and constraints are declared?
Which events and faults may be reported?
Which data products are expected?
Which packet memberships are declared?
Which priority, persistence, storage and downlink intent metadata exists?
Which assumptions remain external implementation concerns?
```

---

## Generated Package

The generic output package is:

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

This package is intended for engineering review and downstream integration.

It is not intended to be executed.

---

## Command

Ground artifacts are generated with:

```bash
orbitfabric gen ground examples/demo-3u/mission/
```

Default output:

```text
generated/ground/generic/
```

The currently supported generation profile is:

```text
generic
```

---

## GroundContract

GroundContract is the v0.8.0 intermediate model for ground-facing generation.

It is derived from the validated Mission Model.

It is not loaded from generated runtime files.

It is not the source of truth.

The dependency direction is:

```text
MissionModel
        -> GroundContract builder
        -> generic ground exporter
        -> generated package
```

GroundContract exists to prevent ground exporters from directly reading raw YAML or reinterpreting unrelated generator outputs.

---

## Generic Profile

The first ground generation profile is:

```text
generic
```

The generic profile is tool-neutral.

It does not claim compatibility with any ground framework.

Future tool-specific profiles may be considered only when their outputs are implemented and tested explicitly.

---

## Telemetry Dictionary

The telemetry dictionary exposes:

```text
model_id
name
value_type
unit
source
sampling
criticality
persistence
downlink_priority
limits
enum_values
quality
description
```

It does not implement telemetry decoding, telemetry polling, alarm runtime, archive storage or operator displays.

---

## Command Dictionary

The command dictionary exposes:

```text
model_id
target
description
arguments
allowed_modes
preconditions
requires_ack
timeout_ms
risk
emits
expected_effects
```

It does not implement command encoding, command uplink, authentication, authorization, queuing, routing, retry logic or runtime ACK handling.

The existing command `risk` metadata is exported because it is already part of the Mission Model.

This does not create a security model.

---

## Event Dictionary

The event dictionary exposes:

```text
model_id
source
severity
description
downlink_priority
persistence
```

It does not implement event routing, event storage, alerting or operator notification behavior.

---

## Fault Dictionary

The fault dictionary exposes:

```text
model_id
source
severity
description
condition
emits
recovery
```

It does not implement fault detection, FDIR, safing behavior, command dispatch or ground alarm handling.

---

## Data Product Dictionary

The data product dictionary exposes:

```text
model_id
producer
producer_type
type
estimated_size_bytes
priority
payload
storage
downlink
description
```

It does not implement payload processing, file creation, compression, storage, retention, downlink execution or ground ingestion.

---

## Packet Dictionary

The packet dictionary exposes:

```text
model_id
name
type
max_payload_bytes
period
telemetry
description
```

This is a packet membership dictionary.

It is not a binary decoder specification.

The current Mission Model does not define byte offsets, bit offsets, endianness, scaling rules, calibration curves, APID, VCID, CCSDS headers, PUS service/subservice fields, framing or transport.

Therefore v0.8.0 does not claim decoder generation, CCSDS compliance, PUS compliance or CFDP behavior.

---

## Manifest

The generated manifest explicitly describes the generated package and its boundary.

Boundary flags include:

```json
{
  "kind": "orbitfabric.ground_contract_manifest",
  "manifest_version": "0.1",
  "generation": {
    "profile": "generic",
    "generated_artifacts_are_disposable": true,
    "contains_ground_runtime": false,
    "contains_operator_console": false,
    "contains_transport": false,
    "contains_database": false,
    "claims_yamcs_compatibility": false,
    "claims_openc3_compatibility": false,
    "claims_xtce_compliance": false
  }
}
```

These flags are deliberate.

They prevent generated dictionaries from being mistaken for live ground software.

---

## JSON, CSV and Markdown Outputs

The generic profile writes three review layers:

```text
JSON dictionaries  -> machine-readable contract artifacts
CSV dictionaries   -> spreadsheet-style review artifacts
Markdown documents -> human-reviewable engineering artifacts
```

The generated Markdown avoids HTML table line-break tags so that it remains readable in common Markdown editors.

---

## Non-Goals

Ground Integration Artifacts do not implement:

```text
live ground segment
mission control system
operator console
telemetry archive
telemetry database
command uplink service
telecommand transport
telemetry downlink runtime
network/session/routing behavior
command authentication or authorization
security enforcement
Yamcs integration
OpenC3 integration
XTCE compliance
CCSDS/PUS/CFDP implementation
binary packet decoder
binary telecommand encoder
offset/bitfield layout model
calibration model
RF/link-budget behavior
pass scheduling
station automation
```

These are not missing pieces of v0.8.0.

They are intentionally outside scope.

---

## Relationship with RuntimeContract

RuntimeContract and GroundContract serve different consumers.

```text
RuntimeContract -> software-facing contract bindings
GroundContract  -> ground-facing contract dictionaries
```

Both derive from the validated Mission Model.

Neither should read from the other's generated artifacts.

Neither should bypass Mission Model validation.

---

## Relationship with Security Assumptions

v0.8.0 exports existing command `risk` metadata.

It does not introduce security assumptions, command authorization, authentication, audit runtime, cryptography, key management or enforcement behavior.

Security assumptions are a separate future contract-model topic.

---

## Architectural Meaning

Ground Integration Artifacts make OrbitFabric useful to ground software teams without making OrbitFabric a ground system.

They provide a deterministic, reviewable and machine-readable mission data contract package.

The downstream ground system remains responsible for real decoding, storage, displays, transport, operator workflow, security and live operations.
