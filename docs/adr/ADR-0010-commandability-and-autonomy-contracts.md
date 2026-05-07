# ADR-0010 — Commandability and Autonomy Contracts

Status: Accepted / Implemented  
Date: 2026-05-07

---

## Context

OrbitFabric is a model-first Mission Data Contract framework for small spacecraft.

The v0.4.0 baseline introduced Contact Windows and Downlink Flow Contracts as declared assumptions for onboard-to-ground data flow reasoning.

The current Mission Data Chain is:

```text
Payload Contract
        -> Data Product Contract
        -> Storage Intent
        -> Downlink Intent
        -> Contact Window Assumption
        -> Downlink Flow Contract
```

That chain describes what mission data exists, how it is intended to be retained, and under which declared contact/downlink assumptions it can become eligible for delivery.

However, a mission contract also needs to describe whether the commands and autonomous actions that affect this chain are coherent.

Examples:

```text
A payload acquisition command may be ground-dispatched only in selected modes.
A recovery command may be auto-dispatched after a declared fault.
A high-risk command may require an explicit confirmation intent.
An autonomous action may expect events or telemetry effects to be declared.
A command may require a contact assumption before it is considered commandable from ground.
```

These are Mission Data Contract concerns.

They are not command uplink runtime, not command authentication, not command authorization, not an operator console, not an onboard scheduler, not a flight autonomy runtime and not a real FDIR implementation.

---

## Decision

OrbitFabric will introduce Commandability and Autonomy Contracts as the next Mission Data Chain slice.

The model will describe declared assumptions about command sources, command dispatch intent, commandability constraints, autonomous action assumptions and recovery intent so that OrbitFabric can reason about consistency before runtime skeletons, ground integration artifacts or end-to-end mission data flow evidence are introduced.

The first implementation slice must be optional and narrow.

The preferred model entry point is:

```text
mission/commandability.yaml
```

This name is intentional.

It communicates that the domain describes whether commands are commandable under declared assumptions.

It does not imply a mission operations system, command policy engine, security model, scheduler or autonomy runtime.

The model may contain:

```text
command source assumptions
commandability rules
autonomous action contracts
recovery intent declarations
```

These concepts are declarative.

They do not execute commands, queue commands, authenticate users, schedule onboard actions, run autonomy logic or perform real safing.

---

## Naming Decision

The selected first-slice file name is:

```text
mission/commandability.yaml
```

Rejected names:

```text
operations.yaml
command_policy.yaml
autonomy.yaml
```

Rationale:

- `operations.yaml` is too broad and suggests mission operations procedures or an operator console.
- `command_policy.yaml` suggests security, authorization or a runtime policy engine.
- `autonomy.yaml` over-emphasizes autonomy and risks implying a flight autonomy runtime.

A two-file split such as `commandability.yaml` plus `autonomy.yaml` is also deferred.

The first slice should remain small enough to validate the concept without creating premature domain fragmentation.

---

## Terminology

OrbitFabric must keep these concepts distinct.

```text
Command Source
    A declared origin class for command dispatch intent.
    Examples: ground, onboard, autonomous.

Commandability Rule
    A declared rule describing when a command is intended to be usable.
    It complements the existing command definition without duplicating it.

Autonomous Action Contract
    A declared assumption that a command or action may be triggered by a modeled event, fault, telemetry condition or mode context.

Recovery Intent
    A declared recovery or safing-oriented intent that references existing commands, modes, faults or events.
```

A command source is not a user account.

A commandability rule is not runtime authorization.

An autonomous action contract is not autonomy software.

A recovery intent is not FDIR implementation.

---

## Minimal Shape

The first slice should use a shape similar to:

```yaml
commandability:
  sources:
    - id: ground_operator
      type: ground
      requires_contact: true
      contact_profile: primary_ground_contact
      description: Abstract ground-originated command source.

    - id: onboard_autonomy
      type: autonomous
      requires_contact: false
      description: Abstract onboard autonomous command source.

  rules:
    - id: payload_start_ground_rule
      command: payload.start_acquisition
      sources:
        - ground_operator
      allowed_modes:
        - NOMINAL
      confirmation: required
      description: Payload acquisition may be commanded from ground in nominal mode.

  autonomous_actions:
    - id: stop_payload_on_battery_warning
      trigger:
        fault: eps.battery_low_fault
      dispatches:
        command: payload.stop_acquisition
        source: onboard_autonomy
      expected_events:
        - payload.acquisition_stopped
      description: Contract-level autonomous recovery assumption for low battery conditions.

  recovery_intents:
    - id: payload_battery_warning_recovery
      fault: eps.battery_low_fault
      target_mode: DEGRADED
      commands:
        - payload.stop_acquisition
      description: Declared recovery intent for payload activity during low battery conditions.
```

This shape is the implemented current v0.5 development contract shape.

It is not a frozen v1.0 schema.

---

## Relationship with Existing Commands

The existing `commands.yaml` domain remains the source of truth for command identity and basic command definition.

Commandability Contracts must not duplicate the command model.

They should reference existing commands and add declared assumptions around:

```text
source
mode availability refinement
contact requirement
confirmation intent
autonomous dispatch intent
recovery intent
expected evidence
```

The existing command fields remain relevant:

```text
allowed_modes
requires_ack
timeout_ms
risk
emits
expected_effects
```

The v0.5 model should cross-check commandability assumptions against those existing command fields.

---

## Initial Scope

The first vertical slice should include:

```text
optional commandability.yaml loading
typed commandability model objects
command source identity validation
commandability rule identity validation
autonomous action identity validation
recovery intent identity validation
reference validation to existing commands
reference validation to existing modes
reference validation to existing events, faults and telemetry where used
optional reference validation to contact profiles when ground source requires contact
minimal semantic lint rules
generated commandability documentation
one synthetic demo commandability/autonomy slice
```

The slice should prove this relationship:

```text
Command Definition
        -> Command Source Assumption
        -> Commandability Rule
        -> Autonomous Action Assumption
        -> Recovery Intent
        -> Lintable Consistency
        -> Generated Documentation
```

---

## Non-Goals

This decision must not introduce:

```text
real command authentication
real command authorization
user roles or permissions
encryption
key management
live uplink
live command routing
real command queue
operator console
mission control system
Yamcs runtime integration
OpenC3 runtime integration
flight autonomy runtime
onboard scheduler
onboard command dispatcher
real FDIR implementation
real safing logic
runtime skeleton generation
ground export generation
private mission operations procedures
```

These are not missing pieces of v0.5.0.

They are intentionally outside the scope of this ADR.

---

## Linting Direction

Commandability and Autonomy Contracts must be lintable from the beginning.

Initial linting direction should include:

```text
ERROR: commandability rule references an unknown command.
ERROR: commandability rule references an unknown mode.
ERROR: commandability rule references an unknown source.
WARNING: ground command source requires contact but no contact profile is referenced.
ERROR: ground command source references an unknown contact profile.
ERROR: autonomous action dispatches an unknown command.
ERROR: autonomous action references an unknown source.
ERROR: autonomous action trigger references an unknown event, fault or telemetry item.
ERROR: recovery intent references an unknown command.
ERROR: recovery intent references an unknown fault, event or mode.
WARNING: high-risk command lacks explicit confirmation intent.
WARNING: autonomous recovery command lacks expected events or effects.
```

The principle is fixed:

> If command use or autonomous behavior can become operationally ambiguous, the ambiguity must be visible before runtime or ground artifacts are generated.

---

## Documentation Direction

Generated documentation should expose commandability and autonomy assumptions from the validated Mission Model.

The expected generated file is:

```text
generated/docs/commandability.md
```

The generated page should make clear that sources, commandability rules, autonomous actions and recovery intents are contract assumptions only.

---

## Consequences

This decision extends OrbitFabric from declared onboard-to-ground data flow reasoning toward declared command and recovery reasoning.

It makes the next Mission Data Chain step explicit:

```text
contact/downlink assumptions
        -> command source assumptions
        -> commandability rules
        -> autonomous action assumptions
        -> recovery intent
        -> future end-to-end mission data flow evidence
```

This strengthens later milestones.

End-to-End Mission Data Flow Evidence will be able to reason about whether a scenario is not only data-flow coherent, but also commandability coherent.

Runtime skeletons and ground integration artifacts will eventually be derived from a stronger model.

---

## Acceptance Criteria for This Decision

This ADR is satisfied when:

- the scope of Commandability and Autonomy Contracts is documented;
- `mission/commandability.yaml` is selected as the first-slice model entry point;
- command sources, commandability rules, autonomous actions and recovery intents are defined as contract assumptions;
- non-goals are explicit;
- the model remains optional;
- commandability concepts are connected to existing commands, modes, events, faults, telemetry and contact assumptions where appropriate;
- initial linting direction is documented;
- generated documentation direction is documented;
- implementation remains narrow, synthetic and clean-room.

---

## Final Position

OrbitFabric must not jump from contact/downlink contracts directly to runtime or ground integration.

The next correct step is to model the commandability and autonomy assumptions used to reason about the mission contract.

That model must stay declarative.
