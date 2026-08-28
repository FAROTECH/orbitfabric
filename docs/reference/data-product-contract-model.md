# Data Product Contract Model

Status: Implemented since v0.3.0 and part of the stable Mission Model contract from v1.0.0  
Scope: Data Product and Storage Contract definition

## Purpose

The Data Product Contract Model defines mission data objects produced by payloads or subsystems.

A data product contract describes what mission data object is expected to be produced, who produces it, how large it is expected to be, how important it is, how it should be retained and how it is intended to enter the downlink path.

The model is contract-level only.

It does not implement onboard storage, payload processing, compression, contact scheduling, downlink execution or ground runtime.

## Relationship to telemetry and packets

OrbitFabric keeps telemetry, packets and data products distinct.

```text
Telemetry
  A state, measurement or status value exposed by the Mission Model.

Packet
  A declared grouping or transport-oriented representation of mission data.

Data Product
  A mission or payload output object that may require storage, retention,
  prioritization and eventual downlink.
```

A payload may expose telemetry showing that acquisition is active while also producing an image, histogram, sample batch or diagnostic dump.

Telemetry describes operational state. A data product describes the mission output object.

## What a Data Product Contract may describe

A data product contract may describe:

- data product identity;
- producer reference;
- producer type;
- optional payload reference;
- product type;
- estimated size;
- priority;
- storage class;
- retention intent;
- overflow policy;
- downlink intent.

These fields make part of the Mission Data Chain explicit:

```text
payload or subsystem activity
    -> data product produced
    -> storage intent declared
    -> downlink intent declared
```

## What it does not describe

A Data Product Contract does not implement:

- real onboard storage software;
- file-system behavior;
- compression engines;
- payload data processing pipelines;
- physical payload simulation;
- contact scheduling;
- RF link modeling;
- downlink runtime;
- ground segment behavior;
- flight runtime behavior.

## YAML shape

Data products are defined in the optional file:

```text
mission/data_products.yaml
```

Representative shape:

```yaml
data_products:
  - id: payload.radiation_histogram
    producer: demo_iod_payload
    producer_type: payload
    type: histogram
    estimated_size_bytes: 4096
    priority: high
    storage:
      class: science
      retention: 7d
      overflow_policy: drop_oldest
    downlink:
      policy: next_available_contact
```

This domain is part of the stable documented Mission Model contract from v1.0.0 onward. Its documented field names, meanings, identifier and reference rules, controlled values and required/optional behavior are compatibility-sensitive.

Compatible additive evolution remains possible under the Mission Model Stability Contract. Existing documented meaning must not change silently.

## Relationship with Payload Contracts

Payload Contracts describe expected payload behavior.

Data Product Contracts describe mission data objects produced by that behavior.

```text
Payload Contract
    -> produced telemetry
    -> accepted commands
    -> generated events
    -> possible faults
    -> lifecycle behavior
    -> Data Product Contracts
```

A data product may reference a payload contract as its producer.

The relationship remains declarative. It does not imply payload runtime execution or data processing.

## Storage intent

Storage fields describe policy intent.

Examples include:

- storage class;
- retention duration;
- overflow policy.

They do not implement storage.

Their purpose is to make preservation expectations explicit before later contract layers reason about data flow, runtime-facing bindings or ground-facing artifacts.

## Downlink intent

Downlink fields describe delivery intent.

Examples include next available contact, priority-based downlink, deferred downlink or manual selection.

They do not implement scheduling, queueing or transfer.

Contact and Downlink Contracts provide the separate model domain for contact assumptions and downlink-flow intent.

## Validation and linting

Data Product Contracts are structurally validated and semantically linted.

Implemented rule families include:

```text
OF-DP-002  producer reference must be known
OF-DP-003  optional payload reference must be known
OF-DP-006  storage intent should define retention
OF-DP-007  storage intent should define overflow_policy
OF-DP-008  high-priority data product should define downlink intent
```

Structural validation also covers duplicate IDs, positive estimated size and documented controlled values for product type, storage class, overflow policy and downlink policy.

Diagnostic behavior is Core-owned. Downstream tools must not replace or privately reinterpret Core lint findings.

## Generated documentation

When data products are present, OrbitFabric generates data product documentation from the validated Mission Model.

Current generated output:

```text
generated/docs/data_products.md
```

The generated page exposes data product identity, producer, type, estimated size, priority, storage intent and downlink intent.

Generated documentation is derived and reproducible. It is not the source of truth.

## Relationship with data-flow evidence and generated bindings

Data Product Contracts are consumed by later OrbitFabric layers.

Data Flow Evidence can trace declared command effects through:

```text
command
    -> data product
    -> storage intent
    -> downlink intent
    -> eligible downlink flow
    -> contact window
```

Runtime-facing bindings expose data products as software-facing identifiers and registry metadata.

Ground-facing artifacts expose contract information for downstream integration and review.

All of these uses remain contract-level. They do not implement data product generation, storage, compression or downlink execution.

## Current boundary

The Data Product Contract Model is a stable declarative Mission Model domain.

Its stable status does not convert intent into runtime behavior.

The boundary remains:

```text
Mission Model declares the data product and its intent.
Core validates and exports that meaning.
Generated and downstream artifacts consume the declared contract.
Runtime storage, processing and downlink remain outside Core.
```
