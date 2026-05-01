# ADR-0007 — Mission Data Chain Before Runtime Generation

Status: Accepted  
Date: 2026-05-01

---

## Context

OrbitFabric is a model-first Mission Data Contract framework for small spacecraft.

The project already demonstrates a coherent early vertical slice:

```text
Mission Model
        -> structural validation
        -> semantic lint
        -> generated documentation
        -> scenario validation
        -> deterministic scenario execution
        -> JSON reports and logs
```

The Payload / IOD Payload Contract Model extends this foundation by making mission-specific payload behavior explicit, lintable, documentable and scenario-aware.

The next obvious technical temptation is generated runtime skeletons.

That would be premature.

A small spacecraft mission data contract is not only a set of telemetry, commands, events, faults, modes and packets.

For the onboard-to-ground chain to be architecturally meaningful, the model must also express how mission data is produced, preserved, prioritized, made available for downlink and consumed by future ground-facing artifacts.

Without that layer, generated runtime skeletons would be derived from an incomplete contract.

---

## Decision

OrbitFabric will introduce Mission Data Chain modeling before generated runtime skeletons.

The roadmap therefore places these model-first milestones before runtime generation:

```text
Data Product and Storage Contracts
Contact Windows and Downlink Flow Contracts
Commandability and Autonomy Contracts
End-to-End Mission Data Flow Evidence
```

Generated runtime skeletons are deferred until after these concepts are clear enough to be represented in the Mission Data Contract.

The intended chain is:

```text
Payload or subsystem activity
        -> generated telemetry and data products
        -> onboard storage and retention intent
        -> downlink queue and priority intent
        -> contact window assumptions
        -> commandability and autonomy constraints
        -> end-to-end scenario evidence
        -> future runtime and ground artifacts
```

This decision reinforces the existing OrbitFabric principles:

```text
model before generator
lint before runtime
docs from model
no hidden semantics
small working slice before broad scope
```

---

## Rationale

Generated code is only useful if the model behind it is strong.

If OrbitFabric generated runtime skeletons before modeling data products, storage intent, contact assumptions and downlink priorities, the generated artifacts would reflect an incomplete view of the mission.

For CubeSat and small spacecraft missions, the value of a payload is not limited to command acceptance or telemetry generation.

The relevant engineering questions are broader:

- What data products are produced?
- Which payload or subsystem produces them?
- How large are they expected to be?
- How long should they be retained onboard?
- What happens when storage is full?
- Which products are prioritized for downlink?
- What contact assumptions are used?
- Which commands require ground contact?
- Which commands may be dispatched autonomously?
- What recovery behavior is expected after faults?
- Which scenarios prove the expected end-to-end behavior?

These are Mission Data Contract questions.

They are not flight runtime implementation details.

---

## Scope

Mission Data Chain modeling may introduce contract-level descriptions for:

```text
data products
product producers
estimated product size
product priority
storage class
retention policy
overflow policy
downlink intent
downlink queue assumptions
contact windows
contact profiles
link profiles
command source constraints
requires-contact constraints
expected command effects
timeout expectations
recovery command references
autonomy expectations
scenario evidence for data flow
```

These concepts must remain declarative, synthetic and clean-room.

---

## Non-Goals

This decision does not authorize OrbitFabric to implement:

```text
real onboard storage software
file systems
compression engines
payload processing pipelines
RF link simulation
orbit propagation
antenna pointing
live downlink services
live command uplink services
operator consoles
Yamcs or OpenC3 as embedded services
flight-ready autonomy
real command authentication or authorization
qualified flight runtime
```

Those are outside the core scope.

They may become future integration targets, generated artifacts or plugin outputs only after the contract is clear.

---

## Consequences

The roadmap changes from:

```text
Payload Contracts
        -> Generated Runtime Skeletons
        -> Ground Integration Artifacts
```

to:

```text
Payload Contracts
        -> Mission Data Chain Contracts
        -> End-to-End Mission Data Flow Evidence
        -> Generated Runtime Skeletons
        -> Ground Integration Artifacts
```

This delays runtime skeleton generation, but it makes it more valuable.

The generated runtime artifacts will eventually be able to reflect payloads, data products, storage policies, downlink priorities and commandability constraints, not only IDs and basic command/telemetry structures.

The ground integration artifacts will also be stronger, because they will be derived from a richer contract that already includes data products and downlink assumptions.

---

## Expected Roadmap Impact

The roadmap includes these milestones before runtime generation:

```text
v0.3 Data Product and Storage Contracts
v0.4 Contact Windows and Downlink Flow Contracts
v0.5 Commandability and Autonomy Contracts
v0.6 End-to-End Mission Data Flow Evidence
```

Generated runtime skeletons are placed later:

```text
v0.7 Generated Runtime Skeletons
```

Ground integration artifacts follow after the model contains enough ground-facing semantics:

```text
v0.8 Ground Integration Artifacts
```

Plugin and extensibility work remains after the core model has matured:

```text
v0.9 Plugin and Extensibility Layer
```

---

## Acceptance Criteria for This Decision

This ADR is satisfied when:

- the roadmap explicitly places Mission Data Chain modeling before runtime skeleton generation;
- the Project Charter explains Mission Data Chain as part of OrbitFabric's direction;
- generated runtime skeletons are no longer the immediate next implementation milestone;
- future data product, storage, downlink, contact, commandability and autonomy concepts are described as contracts, not runtime implementations;
- non-goals remain explicit.

---

## Final Position

OrbitFabric must not generate code from an immature mission contract.

It must first model the mission data chain.

That is the architectural step that turns OrbitFabric from a useful mission-model tool into a credible Mission Data Fabric.
