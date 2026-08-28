# Commandability and Autonomy Contract Model

Status: Implemented since v0.5.0 and part of the stable Mission Model contract from v1.0.0  
Scope: Commandability and Autonomy Contract definition

## Purpose

The Commandability and Autonomy Contract Model defines declared commandability, autonomy and recovery assumptions.

It answers a contract-level question:

> Given the declared commands, modes, contact assumptions, mission conditions and recovery expectations, is the intended use of commands and autonomous actions coherent?

The model does not execute commands, authenticate operators, authorize commands, implement live uplink, implement onboard autonomy or implement a real FDIR system.

## Relationship with Commands

The Command model defines command identity and command-level behavior such as target, arguments, allowed modes, preconditions, acknowledgement intent, timeout, risk, emitted events and expected effects.

The Commandability and Autonomy Contract adds assumptions about how commands are intended to be sourced, constrained and used in autonomous or recovery contexts.

```text
Command Definition
    -> Command Source Assumption
    -> Commandability Rule
    -> Autonomous Action Assumption
    -> Recovery Intent
```

This remains declarative. It does not imply runtime dispatch, onboard scheduling, operator workflow or live routing.

## Relationship with Contact and Downlink Contracts

A command source may reference contact assumptions when contract-level consistency requires it.

For example:

```text
requires_contact: true
contact_profile: primary_ground_contact
```

This states that a ground command source depends on a declared contact assumption. It does not create an uplink runtime, contact scheduler or RF model.

## What the model may describe

The model may describe:

```text
command source identity and type
whether a source requires contact
optional contact profile reference
commandability rule identity
referenced command
allowed source assumptions
mode availability refinement
confirmation intent
autonomous trigger assumption
autonomously dispatched command assumption
expected event or telemetry evidence
recovery intent
safing-oriented target mode assumption
```

## What the model does not describe

The model does not implement:

```text
real command authentication
real command authorization
operator accounts or roles
cryptographic keys or encryption
live uplink
live command routing
real command queues
operator consoles
mission control services
flight autonomy runtime
onboard scheduling
onboard command dispatch
real FDIR implementation
real safing logic
Yamcs or OpenC3 runtime services
```

## YAML shape

Commandability and autonomy assumptions are defined in the optional file:

```text
mission/commandability.yaml
```

Representative shape:

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

This domain is part of the stable documented Mission Model contract from v1.0.0 onward. Its documented fields, meanings, controlled values, identifiers and cross-reference rules are compatibility-sensitive.

Compatible additive evolution remains possible under the Mission Model Stability Contract. Existing documented meaning must not change silently.

## Command sources

A command source describes an abstract source class for command-dispatch intent.

Examples:

```text
ground_operator
onboard_autonomy
scenario_driver
maintenance_session
```

A command source is not a user account, authorization role or transport endpoint.

## Commandability rules

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

It complements the existing command definition. It must not silently contradict or replace command-level semantics.

## Autonomous Action Contracts

An autonomous action declares an expected relationship between an explicit trigger and an autonomous command or recovery-oriented action.

It may reference events, faults, telemetry items, dispatched commands, command sources and expected evidence.

This is contract-level intent, not autonomy software.

## Recovery intents

A recovery intent describes a declared recovery or safing response and may reference:

```text
fault
event
target mode
commands
expected evidence
```

A recovery intent is not runtime FDIR implementation.

## Validation and linting

Current validation and linting cover reference integrity and obvious consistency issues, including:

```text
unknown command references
unknown mode references
unknown command sources
missing contact assumptions for ground sources
unknown contact profiles
unknown autonomous trigger references
unknown recovery references
high-risk command confirmation ambiguity
autonomous recovery evidence ambiguity
```

Warnings expose engineering ambiguity without pretending to solve routing, scheduling or autonomy execution.

## Relationship Manifest integration

The commandability domain contributes explicit Core-owned relationship records when a relationship is directly declared by a loaded Mission Model field.

Examples include:

```text
autonomous_action_dispatches_command
autonomous_action_triggered_by_fault
autonomous_action_uses_command_source
commandability_rule_constrains_command
recovery_intent_reacts_to_event
recovery_intent_reacts_to_fault
recovery_intent_includes_command
recovery_intent_targets_mode
```

These relationships are declarative contract relationships. They do not prove that an action or command was observed during a run.

## Generated documentation and scenario evidence

When this domain is present, OrbitFabric generates:

```text
generated/docs/commandability.md
```

Scenario execution may exercise commandability, autonomy and recovery declarations as deterministic host-side evidence.

Generated documentation and scenario evidence remain derived outputs. They do not become command runtime or FDIR runtime.

## Current boundary

The Commandability and Autonomy Contract Model is a stable declarative Mission Model domain.

The correct boundary is:

```text
Command Definition
    -> Commandability Contract
    -> Autonomy and Recovery Intent
    -> Core validation and lint
    -> generated documentation
    -> host-side scenario evidence
    -> runtime-facing contract bindings
```

The model must not drift into:

```text
command uplink runtime
operator console
scheduler
command dispatcher
autonomy runtime
real FDIR system
```
