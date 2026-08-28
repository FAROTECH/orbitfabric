# Contact and Downlink Contract Model

Status: Implemented since v0.4.0 and part of the stable Mission Model contract from v1.0.0  
Scope: Contact Windows and Downlink Flow Contract definition

## Purpose

The Contact and Downlink Contract Model defines declared contact and downlink assumptions at Mission Data Contract level.

Its purpose is to answer a contract question:

> Given the declared data products, priorities, storage policies, downlink intent and contact assumptions, is the mission data flow coherent?

The model does not execute downlink, compute orbital passes, simulate RF performance or implement a ground segment.

## Relationship with Data Products

The Data Product Contract Model describes mission data objects produced by payloads or subsystems.

The Contact and Downlink Contract Model describes assumptions used to reason about how those products are intended to become eligible for downlink.

```text
Data Product Contract
    -> Storage Intent
    -> Downlink Intent
    -> Contact Window Assumption
    -> Downlink Flow Contract
```

A data product may declare downlink intent. A downlink flow may declare which data products are eligible for a given abstract contact and link path.

This remains declarative. It does not imply runtime queue execution or file transfer.

## What the model describes

The model may describe:

```text
contact profile identity
abstract contact target
link profile identity
abstract data-rate assumption
contact window identity
contact window start
contact window duration
declared downlink capacity
downlink flow identity
queue-policy intent
eligible data products
```

These fields support validation, linting, scenario evidence and generated documentation.

## What the model does not describe

The model does not implement:

```text
orbit propagation
ground-track computation
TLE ingestion
antenna pointing
RF link budget
modulation and coding behavior
real contact scheduling
real ground station operations
live downlink execution
onboard downlink queues
file-transfer protocols
CCSDS, PUS or CFDP implementation
Yamcs or OpenC3 runtime integration
operator consoles
```

## YAML shape

Contact and downlink assumptions are defined in the optional file:

```text
mission/contacts.yaml
```

Representative shape:

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
      description: Abstract nominal downlink assumption for contract-level reasoning.

  contact_windows:
    - id: demo_contact_001
      contact_profile: primary_ground_contact
      link_profile: uhf_downlink_nominal
      start: "2026-01-01T00:00:00Z"
      duration_seconds: 600
      assumed_capacity_bytes: 512000
      description: Synthetic contact window used to demonstrate downlink flow assumptions.

  downlink_flows:
    - id: science_next_available_contact
      contact_profile: primary_ground_contact
      link_profile: uhf_downlink_nominal
      queue_policy: priority_then_age
      eligible_data_products:
        - payload.radiation_histogram
      description: Synthetic science downlink flow used by the demo mission.
```

This domain is part of the stable documented Mission Model contract from v1.0.0 onward. Its documented fields, meanings, controlled values, identifier rules and cross-reference behavior are compatibility-sensitive.

Compatible additive evolution remains possible under the Mission Model Stability Contract. Existing documented meaning must not change silently.

## Contact profiles

A contact profile describes an abstract contact target or class.

Examples:

```text
primary_ground_contact
backup_ground_contact
commercial_ground_network
lab_emulated_contact
```

A contact profile is not a real ground station configuration. It is a contract-level target referenced by windows and flows.

## Link profiles

A link profile describes an abstract link assumption.

Examples:

```text
uhf_downlink_nominal
s_band_downlink_nominal
lab_downlink_emulated
```

A link profile may include an assumed data rate used for contract reasoning. That value is not an RF budget or measured link performance.

## Contact windows

A contact window describes an assumed contact opportunity and may reference:

```text
contact profile
link profile
start time
duration
declared capacity
```

Declared capacity is an engineering assumption used for validation and evidence. It does not imply orbital or physical link simulation.

## Downlink Flow Contracts

A downlink flow describes how data products are intended to become eligible for downlink.

It may reference:

```text
contact profile
link profile
queue-policy intent
eligible data products
```

Queue policy is declarative intent only.

Examples include:

```text
priority_then_age
oldest_first
manual_selection
critical_first
```

OrbitFabric does not implement a runtime queue from these declarations.

## Validation and linting

Lint rules focus on reference integrity and obvious contract consistency.

Implemented rules include:

```text
OF-CON-001  contact window references unknown contact profile
OF-CON-002  contact window references unknown link profile
OF-DL-001   downlink flow references unknown contact profile
OF-DL-002   downlink flow references unknown link profile
OF-DL-003   downlink flow references unknown data product
OF-DL-004   high-priority data product has downlink intent but no eligible downlink flow
OF-DL-005   estimated data product volume may exceed declared contact capacity
```

Warnings expose engineering ambiguity without pretending to solve scheduling or RF behavior.

## Generated documentation and evidence

When contact and downlink contracts are present, OrbitFabric generates:

```text
generated/docs/contacts.md
```

The generated page exposes contact profiles, link profiles, windows, declared capacities, downlink flows and eligible data products.

Scenario Data Flow Evidence can also correlate declared command effects with data products, storage intent, downlink intent, eligible flows and matching contact windows.

This is contract evidence, not observed ground operations.

## Current boundary

The Contact and Downlink Contract Model is a stable declarative Mission Model domain.

The correct boundary is:

```text
Data Product Contract
    -> Downlink Intent
    -> Contact and Downlink Contract
    -> Core validation and lint
    -> generated documentation and host-side evidence
```

The model must not drift into:

```text
orbit simulator
RF simulator
ground segment
downlink runtime
contact scheduler
```
