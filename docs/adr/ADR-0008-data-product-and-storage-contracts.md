# ADR-0008 — Data Product and Storage Contracts

Status: Accepted  
Date: 2026-05-01

---

## Context

OrbitFabric is a model-first Mission Data Contract framework for small spacecraft.

The Payload / IOD Payload Contract Model introduced a first-class way to describe mission-specific payload behavior as a declarative contract.

That model can describe payload telemetry, commands, events, faults, lifecycle states, preconditions and expected effects.

However, a payload does not only expose telemetry or accept commands.

In many small spacecraft and IOD missions, a payload produces mission data objects that must be preserved, prioritized and eventually delivered to the ground.

Examples include:

```text
image frames
radiation histograms
science sample batches
AIS capture windows
IoT receiver bursts
diagnostic dumps
compressed payload products
```

These objects are not the same as telemetry fields.

They are also not the same as packets.

OrbitFabric needs a contract-level way to describe them before runtime skeletons, downlink models or ground integration artifacts are generated.

---

## Decision

OrbitFabric introduces Data Product and Storage Contracts as the next model-first slice after Payload Contracts.

A data product is a declared mission-data object produced by a payload or subsystem.

A data product contract may describe:

```text
data product identity
producer reference
producer type
optional payload reference
product type
estimated size
priority
storage class
retention intent
overflow policy
downlink intent
```

Storage and downlink fields represent declared intent.

They do not represent real storage implementation, file-system behavior, compression, contact-window simulation or downlink runtime behavior.

The first implementation slice is intentionally narrow and is introduced as an optional model domain:

```text
mission/data_products.yaml
```

---

## Terminology

OrbitFabric must keep these concepts distinct.

```text
Telemetry
    A state, measurement or status value exposed by the Mission Model.

Packet
    A declared grouping or transport-oriented representation of mission data.

Data Product
    A mission or payload output object that may require storage, retention,
    prioritization and eventual downlink.
```

This distinction is essential.

A payload may produce telemetry such as `payload.acquisition.active` while also producing a data product such as `payload.radiation_histogram`.

The telemetry describes operational state.

The data product describes a mission output object.

---

## Minimal Shape

The first data product slice uses a shape similar to:

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

This is implemented in v0.3.0, but it is not a frozen v1.0 schema.

---

## Initial Scope

The first vertical slice includes:

```text
optional data_products.yaml loading
typed DataProductContract model
producer reference validation
optional payload reference validation
estimated size validation
priority validation
storage intent fields
downlink intent fields
semantic lint rules
generated data product documentation
invalid fixtures and tests
one synthetic demo data product
```

The slice proves this relationship:

```text
Payload Contract
        -> Data Product Contract
        -> Storage Intent
        -> Downlink Intent
```

---

## Non-Goals

This decision must not introduce:

```text
real onboard storage runtime
file-system abstraction
compression engine
payload data processing pipeline
contact window model
RF link model
downlink runtime
ground segment export
runtime skeleton generation
real payload data
private mission-specific data products
```

These are not missing pieces of the first data product slice.

They are intentionally outside the scope of this ADR.

Contact windows and downlink flow contracts belong to a later milestone.

Runtime skeletons and ground integration artifacts must remain deferred until the contract is mature.

---

## Linting Direction

Data Product and Storage Contracts are lintable from the beginning.

Implemented lint direction includes:

```text
ERROR: data product references an unknown producer.
ERROR: data product references an unknown payload contract.
WARNING: retained data product has no retention policy.
WARNING: retained data product has no overflow policy.
WARNING: high-priority data product has no downlink intent.
```

Structural validation covers duplicate IDs, positive estimated size and known literal values.

The principle is fixed:

> If a data product can become operationally ambiguous, the ambiguity must be visible before runtime or ground artifacts are generated.

---

## Documentation Direction

Generated documentation exposes data products from the validated Mission Model.

The generated file is:

```text
generated/docs/data_products.md
```

The generated page makes clear that storage and downlink fields are contract intent, not executable runtime behavior.

---

## Consequences

This decision extends OrbitFabric from payload behavior modeling toward mission data chain modeling.

It makes the first post-payload step explicit:

```text
payload behavior
        -> data product produced
        -> storage intent declared
        -> downlink intent declared
```

This strengthens future milestones.

Runtime skeletons will eventually be able to include data product identifiers and storage/downlink policy enumerations.

Ground artifacts will eventually be able to export not only telemetry and command dictionaries, but also data product dictionaries and downlink policy information.

---

## Acceptance Criteria for This Decision

This ADR is satisfied when:

- the scope of Data Product and Storage Contracts is documented;
- data products are clearly distinguished from telemetry and packets;
- storage and downlink fields are described as intent, not implementation;
- non-goals are explicit;
- the public documentation exposes the contract scope;
- implementation is covered by model loading, lint rules, invalid fixtures, generated documentation and one synthetic demo data product.

---

## Final Position

OrbitFabric should not jump from payload contracts directly to runtime generation.

The next correct step is to model the mission data objects produced by payloads and subsystems, together with their storage and downlink intent.

That is the first concrete layer of the Mission Data Chain.
