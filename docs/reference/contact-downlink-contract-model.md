# Contact and Downlink Contract Model

Status: Proposed for OrbitFabric v0.4.0  
Scope: Contact Windows and Downlink Flow Contract definition

---

## Purpose

The Contact and Downlink Contract Model extends OrbitFabric with an optional model domain for declared contact and downlink assumptions.

Its purpose is to answer a contract-level question:

> Given the declared data products, priorities, storage policies, downlink intent and contact assumptions, is the mission data flow coherent?

The model does not execute downlink.

It does not compute orbital passes.

It does not simulate RF performance.

It does not implement a ground segment.

---

## Relationship with Data Products

The Data Product Contract Model describes mission data objects produced by payloads or subsystems.

The Contact and Downlink Contract Model describes the assumptions used to reason about how those data products are expected to become eligible for downlink.

The relationship is:

```text
Data Product Contract
        -> Storage Intent
        -> Downlink Intent
        -> Contact Window Assumption
        -> Downlink Flow Contract
```

A data product may declare downlink intent.

A downlink flow contract may declare which data products are eligible for a given abstract contact/link path.

This is declarative.

It does not imply runtime queue execution or file transfer.

---

## What the Model May Describe

A contact/downlink contract may describe:

```text
contact profile identity
abstract contact target
link profile identity
abstract downlink rate assumption
contact window identity
contact window start
contact window duration
declared downlink capacity
downlink flow identity
queue policy intent
eligible data products
```

These fields exist to support validation, linting and generated documentation.

---

## What the Model Does Not Describe

A contact/downlink contract does not describe:

```text
orbit propagation
ground track computation
TLE ingestion
antenna pointing
RF link budget
modulation and coding behavior
real contact scheduling
real ground station operations
live downlink execution
onboard downlink queues
file transfer protocols
CCSDS/PUS/CFDP implementation
Yamcs/OpenC3 runtime integration
operator consoles
runtime skeletons
ground export artifacts
```

Those are intentionally outside the v0.4.0 scope.

---

## YAML Shape

Contact and downlink assumptions are expected to be defined in the optional file:

```text
mission/contacts.yaml
```

Proposed shape:

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

This shape is intentionally minimal.

OrbitFabric is still pre-1.0 and the schema may evolve before stabilization.

---

## Contact Profiles

A contact profile describes an abstract contact target or contact class.

Examples:

```text
primary_ground_contact
backup_ground_contact
commercial_ground_network
lab_emulated_contact
```

A contact profile is not a real ground station configuration.

It is a contract-level target used by contact windows and downlink flows.

---

## Link Profiles

A link profile describes an abstract link assumption.

Examples:

```text
uhf_downlink_nominal
s_band_downlink_nominal
lab_downlink_emulated
```

A link profile may include an assumed data rate.

That rate is a declared assumption used for linting and documentation.

It is not an RF budget.

---

## Contact Windows

A contact window describes an assumed contact opportunity.

A contact window may reference:

```text
contact profile
link profile
start time
duration
declared capacity
```

The declared capacity may be explicit or derived later from declared rate and duration.

In the first v0.4.0 slice, explicit `assumed_capacity_bytes` is preferred because it avoids pretending to perform physical link simulation.

---

## Downlink Flow Contracts

A downlink flow contract describes how data products are intended to become eligible for downlink.

It may reference:

```text
contact profile
link profile
queue policy intent
eligible data products
```

Queue policy is intent only.

Examples:

```text
priority_then_age
oldest_first
manual_selection
critical_first
```

The model does not implement a runtime queue.

---

## Initial Lint Direction

Initial lint rules should focus on reference integrity and obvious consistency issues.

Expected rule direction:

```text
ERROR: contact window references an unknown contact profile.
ERROR: contact window references an unknown link profile.
ERROR: downlink flow references an unknown contact profile.
ERROR: downlink flow references an unknown link profile.
ERROR: downlink flow references an unknown data product.
WARNING: high-priority data product has downlink intent but no eligible downlink flow.
WARNING: estimated data volume may exceed declared contact capacity.
```

Warnings should expose engineering ambiguity without pretending to solve scheduling.

---

## Generated Documentation

When contact/downlink contracts are present, OrbitFabric should generate Markdown documentation from the validated Mission Model.

Expected generated output:

```text
generated/docs/contacts.md
```

The generated page should expose:

```text
contact profiles
link profiles
contact windows
declared capacities
downlink flows
eligible data products
```

Generated documentation must state that these are contract assumptions, not runtime behavior.

---

## Current Boundary

The v0.4.0 model must remain narrow.

It should strengthen the Mission Data Chain without introducing runtime behavior.

The correct v0.4.0 outcome is:

```text
Data Product Contract
        -> Downlink Intent
        -> Contact/Downlink Contract
        -> Lintable consistency
        -> Generated documentation
```

The incorrect v0.4.0 outcome is:

```text
orbit simulator
RF simulator
ground segment
downlink runtime
contact scheduler
```

That boundary is strict.
