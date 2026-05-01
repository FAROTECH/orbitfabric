# Data Product Contract Model

Status: Proposed for OrbitFabric v0.3  
Scope: Data Product and Storage Contract definition

## Purpose

The Data Product Contract Model extends OrbitFabric with a proposed model domain for mission data objects produced by payloads or subsystems.

A data product contract describes what mission data object is expected to be produced, who produces it, how large it is expected to be, how important it is, how it should be retained and how it should be prepared for future downlink planning.

The model is contract-level only.

It does not implement onboard storage, payload processing, compression, contact windows, downlink execution or ground export.

## Why Data Products Are Separate

OrbitFabric must keep telemetry, packets and data products distinct.

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

Those are intentionally outside the proposed v0.3 scope.

## Candidate YAML Shape

The first implementation slice may introduce an optional file:

```text
mission/data_products.yaml
```

A candidate shape is:

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

This is a proposed shape for the v0.3 design direction.

It is not yet a stable schema.

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

The reference must remain declarative.

It must not imply payload runtime execution or data processing.

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

The first data product slice should not implement contact windows or downlink simulation.

Those belong to later Mission Data Chain milestones.

## Linting Direction

Data Product Contracts should be linted semantically.

Candidate findings include:

```text
ERROR: data product id is duplicated.
ERROR: data product references an unknown producer.
ERROR: data product references an unknown payload contract.
ERROR: estimated size must be positive.
WARNING: retained data product has no retention policy.
WARNING: retained data product has no overflow policy.
WARNING: high-priority data product has no downlink intent.
```

Exact rule IDs and severities should be defined during implementation.

## Generated Documentation Direction

When data products are present, OrbitFabric should be able to generate data product documentation from the validated Mission Model.

Candidate output:

```text
generated/docs/data_products.md
```

The generated page should expose data product identity, producer, type, estimated size, priority, storage intent and downlink intent.

## Current Status

This page defines proposed v0.3 scope only.

It does not document an implemented schema yet.

Implementation should proceed through small follow-up issues covering model loading, lint rules, invalid fixtures, generated documentation and one synthetic demo data product.
