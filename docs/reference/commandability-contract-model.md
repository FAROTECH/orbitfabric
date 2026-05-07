# Commandability and Autonomy Contract Model

Status: Proposed for OrbitFabric v0.5.0  
Scope: Commandability and Autonomy Contract definition

---

## Purpose

The Commandability and Autonomy Contract Model extends OrbitFabric with an optional model domain for declared commandability and autonomy assumptions.

Its purpose is to answer a contract-level question:

> Given the declared commands, modes, contact/downlink assumptions, mission conditions and recovery expectations, is the intended use of commands and autonomous actions coherent?

The model does not execute commands.

It does not authenticate operators.

It does not authorize commands.

It does not implement live uplink.

It does not implement onboard autonomy.

It does not implement a real FDIR system.

---

## Relationship with Commands

The existing Command model describes command identity and basic command definition.

A command may already define:

```text
command id
target subsystem
arguments
allowed modes
preconditions
ack requirement
timeout
risk
emitted events
expected effects
```

The Commandability and Autonomy Contract Model describes the assumptions used to reason about how commands are intended to be dispatched, constrained and used in recovery or autonomous contexts.

The relationship is:

```text
Command Definition
        -> Command Source Assumption
        -> Commandability Rule
        -> Autonomous Action Assumption
        -> Recovery Intent
```

This is declarative.

It does not imply runtime dispatch, onboard scheduling, operator workflow or live command routing.

---

## Relationship with Contact and Downlink Contracts

Contact and Downlink Contracts describe declared assumptions about contact opportunities and data delivery paths.

Commandability Contracts may reference contact assumptions only where this is useful for contract-level consistency.

For example, a ground command source may declare:

```text
requires_contact: true
contact_profile: primary_ground_contact
```

This means only that the command source depends on a declared contact assumption.

It does not create an uplink runtime.

It does not turn OrbitFabric into a contact scheduler.

It does not require RF simulation.

---

## What the Model May Describe

A commandability/autonomy contract may describe:

```text
command source identity
command source type
whether a source requires contact
optional contact profile reference
commandability rule identity
referenced command
allowed source assumptions
mode availability refinement
confirmation intent
autonomous trigger assumption
autonomously dispatched command assumption
expected event evidence
expected telemetry or mode effects
recovery intent
safing-oriented target mode assumption
```

These fields exist to support validation, linting and generated documentation.

---

## What the Model Must Not Describe

A commandability/autonomy contract must not describe:

```text
real command authentication
real command authorization
operator accounts
user roles
cryptographic keys
encryption
live uplink
live command routing
real command queue
operator console
mission control system
flight autonomy runtime
onboard scheduler
onboard command dispatcher
real FDIR implementation
real safing logic
Yamcs/OpenC3 runtime services
runtime skeleton generation
ground export artifacts
```

Those are intentionally outside the v0.5.0 scope.

---

## YAML Shape

Commandability and autonomy assumptions are expected to be defined in the optional file:

```text
mission/commandability.yaml
```

Proposed shape:

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
        fault: eps.battery_warning
      dispatches:
        command: payload.stop_acquisition
        source: onboard_autonomy
      expected_events:
        - payload.acquisition_stopped
      description: Contract-level autonomous recovery assumption for battery warning.

  recovery_intents:
    - id: payload_battery_warning_recovery
      fault: eps.battery_warning
      target_mode: DEGRADED
      commands:
        - payload.stop_acquisition
      description: Declared recovery intent for payload activity during battery warning.
```

This shape is intentionally minimal.

OrbitFabric is still pre-1.0 and the schema may evolve before stabilization.

---

## Command Sources

A command source describes an abstract source class for command dispatch intent.

Examples:

```text
ground_operator
onboard_autonomy
scenario_driver
maintenance_session
```

A command source may define:

```text
id
type
requires_contact
optional contact profile reference
description
```

A command source is not a user account.

It is not an authorization role.

It is not a transport endpoint.

---

## Commandability Rules

A commandability rule describes when a command is intended to be usable under declared assumptions.

It may reference:

```text
command
sources
allowed modes
confirmation intent
timeout expectation
expected evidence
```

This should complement, not replace, the existing command definition.

If the existing command declares `allowed_modes`, the commandability rule should be consistent with that declaration.

---

## Autonomous Action Contracts

An autonomous action contract describes a declared assumption that an event, fault, telemetry condition or mode context may lead to an autonomous command dispatch or recovery-oriented action.

It may reference:

```text
trigger event
trigger fault
trigger telemetry item
dispatched command
source
expected events
expected effects
```

This is not autonomy software.

It is contract-level documentation and lintable intent.

---

## Recovery Intents

A recovery intent describes a declared recovery or safing-oriented response.

It may reference:

```text
fault
event
target mode
commands
expected evidence
```

A recovery intent is not FDIR implementation.

It exists to make recovery assumptions explicit before future scenario evidence and runtime skeletons consume them.

---

## Initial Lint Direction

Initial lint rules should focus on reference integrity and obvious consistency issues.

Expected rule direction:

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

Warnings should expose engineering ambiguity without pretending to solve command routing, scheduling or autonomy execution.

---

## Generated Documentation

When commandability/autonomy contracts are present, OrbitFabric should generate Markdown documentation from the validated Mission Model.

Expected generated output:

```text
generated/docs/commandability.md
```

The generated page should expose:

```text
command sources
commandability rules
autonomous action assumptions
recovery intents
referenced commands
referenced modes
referenced events, faults and telemetry
```

Generated documentation must state that these are contract assumptions, not runtime behavior.

---

## Current Boundary

The v0.5.0 model must remain narrow.

It should strengthen the Mission Data Chain without introducing command runtime or autonomy runtime behavior.

The correct v0.5.0 outcome is:

```text
Command Definition
        -> Commandability Contract
        -> Autonomy/Recovery Contract Assumption
        -> Lintable Consistency
        -> Generated Documentation
```

The incorrect v0.5.0 outcome is:

```text
command uplink runtime
operator console
scheduler
command dispatcher
autonomy runtime
real FDIR system
```

That boundary is strict.
