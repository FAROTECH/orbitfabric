# ADR-0012 - Ground Integration Artifacts Boundary

Status: Accepted for v0.8.0 planning  
Date: 2026-05-11

---

## Context

OrbitFabric is a model-first Mission Data Contract framework for small spacecraft.

The v0.7.0 baseline introduced Generated Runtime Skeletons, defined precisely as runtime-facing contract bindings.

That milestone created a controlled software-facing generation path:

```text
Mission Model
        -> validation and linting
        -> RuntimeContract
        -> generated runtime-facing contract bindings
        -> host-build smoke validation
        -> user implementation outside generated/
```

The next roadmap step is `v0.8.0 - Ground Integration Artifacts`.

This step is architecturally sensitive.

Ground-side terminology can easily imply a live ground segment, a mission control system, a telemetry archive, a telecommand uplink service, a decoder, a database, a Yamcs integration, an OpenC3 integration or an XTCE-compliant mission database.

OrbitFabric must not make those claims in v0.8.0.

The source of truth must remain the Mission Model.

Generated ground artifacts must be downstream, reproducible, inspectable and disposable.

---

## Decision

OrbitFabric v0.8.0 introduces Ground Integration Artifacts as deterministic, inspectable, tool-neutral ground-facing contract exports derived from the validated Mission Model.

The preferred architectural interpretation is:

```text
Mission Model
        -> validated MissionModel
        -> GroundContract intermediate model
        -> generic ground-facing dictionaries
        -> JSON / Markdown / CSV exports
```

The forbidden interpretation is:

```text
Mission Model
        -> generated ground segment
        -> generated mission control system
        -> generated operator console
        -> generated telemetry archive
        -> generated command uplink service
        -> generated Yamcs/OpenC3/XTCE integration
```

The preferred internal term is:

```text
Ground-facing mission data package
```

The public milestone name remains:

```text
Ground Integration Artifacts
```

---

## Core Principle

OrbitFabric v0.8.0 does not implement ground behavior.

It generates the contract-aligned ground-facing data package that ground software teams can review, adapt or consume outside OrbitFabric.

This principle is mandatory.

Every v0.8.0 feature must be evaluated against it.

---

## GroundContract Intermediate Model

v0.8.0 introduces a GroundContract intermediate model.

Ground-facing generators must not read raw YAML in scattered places.

The required dependency direction is:

```text
CLI
        -> Mission Model loading and validation
        -> GroundContract builder
        -> profile-specific ground exporter
        -> generated files
```

The disallowed dependency direction is:

```text
profile-specific ground exporter
        -> raw YAML files
        -> simulator internals
        -> runtime generator internals
        -> generated runtime files
```

GroundContract is not a replacement for RuntimeContract.

RuntimeContract is software-facing.

GroundContract is ground-facing.

Both are derived from the validated Mission Model.

Neither is the source of truth.

---

## Initial Generation Profile

The first supported ground generation profile is:

```text
generic
```

The generated output root is:

```text
generated/ground/generic/
```

The planned v0.8.0 output is:

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

The `generic` profile is deliberately tool-neutral.

It is not a Yamcs profile.

It is not an OpenC3 profile.

It is not an XTCE profile.

Tool-specific profiles may be considered only after their semantics are implemented and tested explicitly.

---

## Generated Artifact Semantics

Generated ground artifacts are reproducible outputs.

They are not the source of truth.

The source of truth remains:

```text
mission/*.yaml
```

Generated artifacts are disposable.

They may be overwritten on every generation.

User integration code, ground adapters, database imports, operator displays, decoder implementations and ground runtime configuration must live outside the generated OrbitFabric output tree unless they are explicitly generated as future tool-specific profiles.

---

## Dictionary Scope

The v0.8.0 ground-facing package may include dictionaries for:

```text
telemetry
commands
events
faults
data products
packets
```

These dictionaries expose contract metadata already declared in the Mission Model.

They do not introduce new ground behavior.

They do not reinterpret the Mission Model.

They do not infer protocol-specific semantics that are not declared.

---

## Telemetry Dictionary Boundary

Telemetry dictionary artifacts may expose:

```text
telemetry identity
name
type
unit
source subsystem
sampling declaration
criticality
persistence
downlink priority
limits
enum values
quality policy
description
```

They must not implement:

```text
telemetry decoding runtime
sensor reading
packet parsing
raw-to-engineering conversion
calibration curves
archive storage
alarm runtime
operator display generation
```

---

## Command Dictionary Boundary

Command dictionary artifacts may expose:

```text
command identity
target subsystem
arguments
argument type and constraints
allowed modes
preconditions
ack requirement
timeout
risk
emitted events
expected effects
related data products when declared
```

They must not implement:

```text
telecommand uplink
command encoding
command authentication
command authorization
command queueing
operator workflow
transport sessions
runtime ACK handling
retry behavior
```

The existing command `risk` field may be exported because it is already part of the Mission Model.

No new security model is introduced in v0.8.0.

---

## Event and Fault Dictionary Boundary

Event and fault dictionary artifacts may expose:

```text
event identity
source
severity
persistence
downlink priority
fault identity
fault condition metadata
emitted events
recovery intent metadata
```

They must not implement:

```text
event routing runtime
fault detection runtime
fault recovery runtime
FDIR implementation
operator alarm engine
```

---

## Data Product Dictionary Boundary

Data product dictionary artifacts may expose:

```text
data product identity
producer
producer type
product type
estimated size
priority
payload reference
storage intent
downlink intent
retention intent
overflow policy
```

They must not implement:

```text
payload file creation
payload data processing
compression
onboard storage writes
retention execution
downlink queues
contact scheduling
ground file ingestion
science processing pipeline
```

---

## Packet Dictionary Boundary

The current Mission Model supports packet membership dictionaries.

A packet dictionary may expose:

```text
packet identity
packet name
abstract packet type
maximum payload size
period
telemetry membership
```

It must not be described as a complete decoder specification.

The current Mission Model does not define:

```text
byte offsets
bit offsets
endianness
scaling rules
calibration curves
APID / VCID mapping
CCSDS headers
PUS service/subservice mapping
framing
transport
```

Therefore v0.8.0 must not generate binary packet decoders or claim CCSDS/PUS/CFDP behavior.

---

## Manifest Boundary Flags

The generated ground manifest must explicitly state what it does not contain.

The manifest should include boundary flags such as:

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

These flags are part of the public boundary of v0.8.0.

---

## Non-Goals

v0.8.0 must not introduce:

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

These are not missing features of v0.8.0.

They are intentionally outside the milestone boundary.

---

## Relationship with Security Assumptions

v0.8.0 must not introduce the future Security Assumptions / Command Criticality Contracts layer.

The existing command `risk` metadata may be exported in command dictionaries.

That export does not imply authentication, authorization, access control, audit runtime, cryptography, key management or security enforcement.

Security assumptions remain tracked separately.

---

## Testing Direction

v0.8.0 should include tests for:

```text
GroundContract construction
deterministic ordering
deterministic JSON output
manifest boundary flags
telemetry dictionary content
command dictionary content
event dictionary content
fault dictionary content
data product dictionary content
packet dictionary content
CSV headers and row stability
Markdown boundary statement
CLI success path
CLI abort on lint errors
unsupported profile failure
```

The required local checks remain:

```bash
ruff check .
pytest
mkdocs build --strict
```

---

## Consequences

This decision creates a controlled bridge from Mission Data Contracts to ground-facing integration artifacts.

It makes OrbitFabric useful to ground software teams without turning OrbitFabric into their ground system.

It enables future tool-specific exporters only after the generic contract package is stable.

It also creates a clear review boundary for v0.8.0 work:

```text
Does this artifact expose ground-facing contract metadata?
Or does it implement ground behavior?
```

Only the first category belongs in v0.8.0.

---

## Acceptance Criteria for This Decision

This ADR is satisfied when:

- Ground Integration Artifacts are defined as ground-facing contract exports;
- GroundContract is selected as the mandatory intermediate model;
- the `generic` profile is the only v0.8.0 ground profile;
- generated artifacts are deterministic, inspectable and disposable;
- the generated manifest declares the ground-runtime boundary;
- tool-specific compatibility claims are excluded from v0.8.0;
- packet outputs are bounded to packet membership dictionaries;
- decoder, transport, database and console behavior are excluded;
- security enforcement is excluded;
- testing expectations are documented.

---

## Final Position

Ground Integration Artifacts are valuable only if they preserve OrbitFabric's identity.

The v0.8.0 milestone generates the ground-facing mission data package derived from the Mission Model.

It does not generate the ground system that consumes that package.
