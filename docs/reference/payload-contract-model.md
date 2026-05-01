# Payload Contract Model

Status: Development preview  
Scope: OrbitFabric v0.2.x model hardening

## Purpose

The Payload Contract Model extends OrbitFabric with an optional model domain for mission-specific and IOD payloads.

A payload contract describes what a payload is expected to expose at mission-data level: telemetry, commands, events, faults, lifecycle states, preconditions and expected behavior.

It keeps payload behavior explicit, lintable, documentable and scenario-aware without turning OrbitFabric into a payload runtime or hardware framework.

## What a Payload Contract Describes

A payload contract may describe or reference:

- payload identity;
- payload profile;
- linked spacecraft subsystem;
- lifecycle states;
- payload telemetry;
- payload commands;
- payload events;
- payload faults;
- command preconditions;
- expected effects;
- scenario-level behavior;
- generated payload documentation.

Payload contracts are part of the Mission Data Contract.

## What a Payload Contract Does Not Describe

A payload contract does not describe:

- payload firmware;
- payload drivers;
- hardware buses;
- onboard services;
- payload runtime execution;
- payload data processing pipelines;
- physical instrument simulation;
- thermal, optical or scientific payload simulation;
- ground segment implementation.

These are intentionally outside the scope of the current Payload Contract Model.

## Relationship with the Mission Model

Payload contracts are optional.

When present, they are defined in:

```text
mission/payloads.yaml
```

The rest of the mission model remains valid without `payloads.yaml`.

A payload contract references existing mission model elements such as:

- subsystem IDs;
- telemetry IDs;
- command IDs;
- event IDs;
- fault IDs.

This keeps payload-specific behavior connected to the rest of the mission model instead of scattering it across unrelated YAML domains.

## Current Lifecycle Model

The current lifecycle model is intentionally minimal:

```text
OFF
READY
ACQUIRING
FAULT
```

The first demo vertical slice uses:

```text
READY → ACQUIRING → READY
```

Additional states such as `STANDBY`, `WARMUP`, `PROCESSING` or `DOWNLINK_PENDING` are not part of the current slice and should only be introduced after the model is stable.

## Generated Documentation

When payload contracts are present, OrbitFabric can generate payload-specific Markdown documentation.

The generated file is:

```text
generated/docs/payloads.md
```

This page documents the declared payload contracts and makes payload-specific mission behavior visible without requiring manual documentation duplication.

## Scenario Behavior

Payload contracts can participate in scenario execution.

The current demo mission includes a nominal payload lifecycle sequence where the payload transitions from `READY` to `ACQUIRING` and back to `READY`.

The scenario also demonstrates how payload behavior can interact with spacecraft-level conditions, such as EPS degradation and automatic command dispatch.

## Current Boundary

The current implementation is a deliberately narrow vertical slice.

It is meant to validate the model shape, lint rules, generated documentation and minimal scenario behavior.

It is not a commitment to payload runtime execution, payload hardware integration or physical payload simulation.
