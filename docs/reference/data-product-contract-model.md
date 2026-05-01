# Data Product Contract Model

Status: Implemented in OrbitFabric v0.3.0  
Scope: Data Product and Storage Contract definition

## Purpose

The Data Product Contract Model extends OrbitFabric with an optional model domain for mission data objects produced by payloads or subsystems.

A data product contract describes what mission data object is expected to be produced, who produces it, how large it is expected to be, how important it is, how it should be retained and how it should be prepared for future downlink planning.

The model is contract-level only.

It does not implement onboard storage, payload processing, compression, contact windows, downlink execution or ground export.

## Why Data Products Are Separate

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

For example, a payload may expose telemetry indicating that acquisition is active while also producing a histogram, image, sample batch or diagnostic dump.

The telemetry describes operational state.

The data product describes the mission output object.

## What a Data Product Contract May Describe

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

These fields make the first part of the Mission Data Chain explicit:

```text
Payload or subsystem activity
        -> data product produced
        -> storage intent declared
        -> downlink intent declared
```

## What a Data Product Contract Does Not Describe

A data product contract does not describe:

- real onboard storage software;
- file-system implementation;
- compression engines;
- payload data processing pipelines;
- physical payload simulation;
- contact window modeling;
- RF link modeling;
- downlink runtime;
- ground segment implementation;
- runtime skeleton generation.

Those are intentionally outside the v0.3.0 scope.

## YAML Shape

Data products are defined in the optional file:

```text
mission/data_products.yaml
```

Current shape:

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

This shape is implemented in v0.3.0, but OrbitFabric is still pre-1.0 and the schema may evolve.

## Relationship with Payload Contracts

Payload Contracts describe expected payload behavior.

Data Product Contracts describe mission data objects produced by that behavior.

The relationship is:

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

The reference remains declarative.

It does not imply payload runtime execution or data processing.

## Storage Intent

Storage fields describe policy intent.

Examples include:

- storage class;
- retention duration;
- overflow policy.

They do not implement storage.

They make it possible to validate that a produced mission object has a declared preservation strategy before later milestones introduce contact windows, downlink flow or runtime skeletons.

## Downlink Intent

Downlink fields describe future delivery intent.

Examples include:

- next available contact;
- priority-based downlink;
- deferred downlink;
- manual or operator-selected downlink.

The first data product slice does not implement contact windows or downlink simulation.

Those belong to later Mission Data Chain milestones.

## Implemented Lint Rules

Data Product Contracts are linted semantically.

Implemented rule families include:

```text
OF-DP-002  producer reference must be known
OF-DP-003  optional payload reference must be known
OF-DP-006  storage intent should define retention
OF-DP-007  storage intent should define overflow_policy
OF-DP-008  high-priority data product should define downlink intent
```

Structural validation also covers duplicate IDs, positive estimated size and known literal values for product type, storage class, overflow policy and downlink policy.

## Generated Documentation

When data products are present, OrbitFabric can generate data product documentation from the validated Mission Model.

Current generated output:

```text
generated/docs/data_products.md
```

The generated page exposes data product identity, producer, type, estimated size, priority, storage intent and downlink intent.

## Current Status

This page documents the implemented v0.3.0 Data Product Contract Model.

The model remains development-preview and pre-1.0.

Future milestones will add contact windows, downlink flow contracts, commandability contracts and end-to-end mission data flow evidence before runtime skeletons or ground artifacts are introduced.
