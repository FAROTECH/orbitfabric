# ADR-0009 — Contact Windows and Downlink Flow Contracts

Status: Accepted  
Date: 2026-05-04

---

## Context

OrbitFabric is a model-first Mission Data Contract framework for small spacecraft.

The Data Product and Storage Contract Model introduced a contract-level way to describe mission data objects, their producers, estimated size, priority, storage intent, retention intent, overflow policy and downlink intent.

That slice intentionally stopped before contact windows and downlink flow modeling.

However, a data product with downlink intent is still incomplete unless the mission contract can also express the assumptions used to reason about delivery to the ground.

OrbitFabric therefore needs a narrow contract-level model for:

```text
Data Product Contract
        -> Storage Intent
        -> Downlink Intent
        -> Contact Window Assumptions
        -> Downlink Flow Contract
```

This is a Mission Data Contract concern.

It is not a ground segment concern, not an orbit propagation concern, not an RF simulation concern and not a downlink runtime concern.

---

## Decision

OrbitFabric will introduce Contact Windows and Downlink Flow Contracts as the next Mission Data Chain slice.

The model will describe declared assumptions about contacts, links and downlink flows so that OrbitFabric can reason about consistency before runtime skeletons, ground integration artifacts or end-to-end mission data flow evidence are introduced.

The first implementation slice should be optional and narrow.

The preferred model entry point is:

```text
mission/contacts.yaml
```

The model may contain:

```text
contact profiles
link profiles
contact windows
downlink flow contracts
declared downlink capacity assumptions
data product downlink eligibility
```

These concepts are declarative.

They do not execute contacts, schedule passes, propagate orbits, model RF behavior, transmit data or integrate with live ground systems.

---

## Terminology

OrbitFabric must keep these concepts distinct.

```text
Contact Profile
    A declared abstract target or class of contact used by the mission contract.

Link Profile
    A declared abstract link assumption used for downlink reasoning.

Contact Window
    A declared availability window or assumed opportunity for contact.

Downlink Flow Contract
    A declared policy describing how eligible data products are intended to be downlinked.

Declared Capacity
    A contract-level capacity assumption used for linting and documentation.
```

A contact window is not an orbit pass computed by OrbitFabric.

A link profile is not an RF link budget.

A downlink flow contract is not a runtime queue implementation.

---

## Minimal Shape

The first slice should use a shape similar to:

```yaml
contacts:
  contact_profiles:
    - id: primary_ground_contact
      target: synthetic_ground_station
      description: Synthetic primary ground contact used by the demo mission.

  link_profiles:
    - id: uhf_downlink_nominal
      direction: downlink
      assumed_rate_bps: 9600
      description: Abstract nominal downlink assumption.

  contact_windows:
    - id: demo_contact_001
      contact_profile: primary_ground_contact
      link_profile: uhf_downlink_nominal
      start: "2026-01-01T00:00:00Z"
      duration_seconds: 600
      assumed_capacity_bytes: 512000

  downlink_flows:
    - id: science_next_available_contact
      contact_profile: primary_ground_contact
      link_profile: uhf_downlink_nominal
      queue_policy: priority_then_age
      eligible_data_products:
        - payload.radiation_histogram
```

This shape is a proposed v0.4.0 contract shape.

It is not a frozen v1.0 schema.

---

## Initial Scope

The first vertical slice should include:

```text
optional contacts.yaml loading
typed contact/downlink model objects
contact profile identity validation
link profile identity validation
contact window identity validation
downlink flow identity validation
reference validation between contact windows, profiles and link profiles
reference validation from downlink flows to data products
declared capacity linting direction
generated contact/downlink documentation
one synthetic demo contact/downlink slice
```

The slice should prove this relationship:

```text
Data Product Contract
        -> Downlink Intent
        -> Contact Assumption
        -> Downlink Flow Contract
```

---

## Non-Goals

This decision must not introduce:

```text
orbit propagation
TLE parsing
ground track computation
antenna pointing
RF link budget simulation
modulation or coding simulation
live ground links
real contact scheduling
real downlink execution
onboard downlink queues
file transfer protocols
CCSDS implementation
PUS implementation
CFDP implementation
Yamcs runtime integration
OpenC3 runtime integration
ground station operations
operator consoles
runtime skeleton generation
ground export generation
private mission-specific contact data
```

These are not missing pieces of v0.4.0.

They are intentionally outside the scope of this ADR.

---

## Linting Direction

Contact Windows and Downlink Flow Contracts must be lintable from the beginning.

Initial linting direction should include:

```text
ERROR: contact window references an unknown contact profile.
ERROR: contact window references an unknown link profile.
ERROR: downlink flow references an unknown contact profile.
ERROR: downlink flow references an unknown link profile.
ERROR: downlink flow references an unknown data product.
WARNING: high-priority data product has downlink intent but no eligible downlink flow.
WARNING: estimated data volume may exceed declared contact capacity.
```

The principle is fixed:

> If a downlink assumption can become operationally ambiguous, the ambiguity must be visible before runtime or ground artifacts are generated.

---

## Documentation Direction

Generated documentation should expose contact and downlink assumptions from the validated Mission Model.

The expected generated file is:

```text
generated/docs/contacts.md
```

The generated page should make clear that contacts, link profiles, capacity and downlink flows are contract assumptions only.

---

## Consequences

This decision extends OrbitFabric from data product and storage intent modeling toward declared onboard-to-ground flow reasoning.

It makes the next Mission Data Chain step explicit:

```text
payload or subsystem produces data product
        -> data product declares storage intent
        -> data product declares downlink intent
        -> contact/downlink assumptions define expected delivery path
```

This strengthens later milestones.

End-to-End Mission Data Flow Evidence will be able to reason about produced, retained, queued, eligible and downlinked data products at contract level.

Runtime skeletons and ground integration artifacts will eventually be derived from a stronger model.

---

## Acceptance Criteria for This Decision

This ADR is satisfied when:

- the scope of Contact Windows and Downlink Flow Contracts is documented;
- contact profiles, link profiles, contact windows and downlink flows are defined as contract assumptions;
- non-goals are explicit;
- the model remains optional;
- contact/downlink concepts are connected to Data Product Contracts;
- initial linting direction is documented;
- generated documentation direction is documented;
- implementation remains narrow, synthetic and clean-room.

---

## Final Position

OrbitFabric must not jump from data product downlink intent directly to runtime or ground integration.

The next correct step is to model the contact and downlink assumptions used to reason about the mission data chain.

That model must stay declarative.
