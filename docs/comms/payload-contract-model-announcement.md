# Payload Contract Model Announcement

Status: communication draft  
Scope: OrbitFabric v0.2.2 — Payload Contract Release Alignment  
Audience: GitHub, LinkedIn, technical network

---

## Purpose

This document prepares the public communication for the Payload / IOD Payload Contract Model introduced in OrbitFabric.

The goal is to explain the value of the feature without overstating the current scope of the project.

The key message is simple:

> OrbitFabric can now describe mission-specific and IOD payload behavior as part of the Mission Data Contract.

---

## Core Message

OrbitFabric is a model-first Mission Data Contract framework for small spacecraft.

With the Payload Contract Model, OrbitFabric can now treat mission-specific and IOD payloads as first-class contract elements.

A payload contract can describe payload telemetry, commands, events, faults, lifecycle states, preconditions and expected effects in a declarative, lintable and documentable way.

This strengthens OrbitFabric as the contract layer between mission design, onboard software, simulation, test, documentation and ground integration.

---

## What Is New

The Payload Contract Model adds:

- optional `mission/payloads.yaml`;
- `PayloadContract` model support;
- payload profile support;
- minimal payload lifecycle support;
- payload semantic lint rules;
- payload reference checks;
- generated `payloads.md`;
- payload-aware scenario behavior;
- minimal lifecycle simulation;
- invalid payload fixtures and negative tests;
- public documentation and release alignment.

The first lifecycle vertical slice demonstrates:

```text
READY → ACQUIRING → READY
```

---

## What This Is Not

The Payload Contract Model is not:

- payload firmware;
- a payload driver framework;
- payload runtime execution;
- hardware bus integration;
- physical payload simulation;
- payload scientific processing;
- a ground segment implementation;
- a flight software framework.

This boundary is intentional.

OrbitFabric describes the contract.  
It does not implement the payload.

---

## GitHub Announcement Draft

OrbitFabric `v0.2.2` is now aligned around the new Payload / IOD Payload Contract Model.

This update consolidates the first payload contract vertical slice and makes payloads part of the Mission Data Contract.

OrbitFabric can now describe optional mission-specific and IOD payload behavior through `mission/payloads.yaml`, including:

- payload telemetry references;
- payload command references;
- payload event and fault references;
- lifecycle states;
- command preconditions;
- expected effects;
- generated payload documentation;
- payload-aware scenario behavior.

The initial lifecycle slice is intentionally narrow:

```text
READY → ACQUIRING → READY
```

The goal is not to turn OrbitFabric into a payload runtime, driver framework or physical simulator.

The goal is to make payload behavior explicit, lintable, documentable and testable at mission-contract level.

This reinforces OrbitFabric's core positioning:

> Define once. Validate. Simulate. Test. Document. Integrate.

OrbitFabric remains a model-first Mission Data Contract framework for small spacecraft.

---

## LinkedIn Post Draft

I have just completed another important step in OrbitFabric, my open-source model-first framework for small spacecraft mission data contracts.

The new milestone introduces the first Payload / IOD Payload Contract Model vertical slice.

The idea is simple but important: mission-specific payloads should not live as scattered assumptions across documents, test scripts and software modules.

They should be modeled explicitly.

With this update, OrbitFabric can now describe optional payload contracts through `mission/payloads.yaml`, including:

- telemetry produced by the payload;
- commands accepted by the payload;
- events and faults related to payload behavior;
- lifecycle states;
- command preconditions;
- expected effects;
- generated payload documentation;
- payload-aware scenario behavior.

The first lifecycle slice is intentionally narrow:

```text
READY → ACQUIRING → READY
```

This is not payload firmware.  
It is not a driver framework.  
It is not physical instrument simulation.

It is the contract layer.

The goal of OrbitFabric remains:

> Define once. Validate. Simulate. Test. Document. Integrate.

This strengthens the project direction: OrbitFabric is not trying to replace flight software frameworks, ground segments or simulators.

It is designed to sit between mission design, onboard software, simulation, test, documentation and ground integration as a Mission Data Contract Layer.

Repository: https://github.com/FAROTECH/orbitfabric

---

## Short LinkedIn Version

OrbitFabric now includes the first vertical slice of a Payload / IOD Payload Contract Model.

This means mission-specific payload behavior can be described as part of the Mission Data Contract:

- telemetry;
- commands;
- events;
- faults;
- lifecycle states;
- preconditions;
- expected effects;
- generated documentation;
- scenario behavior.

The first lifecycle slice is deliberately minimal:

```text
READY → ACQUIRING → READY
```

This is not payload firmware or hardware simulation.

It is a declarative contract layer for small spacecraft missions.

Repository: https://github.com/FAROTECH/orbitfabric

---

## Suggested Positioning Sentence

OrbitFabric now models not only spacecraft subsystems, but also mission-specific and IOD payload contracts as first-class Mission Data Contract elements.

---

## Do Not Claim

Avoid claiming that OrbitFabric currently provides:

- flight-ready software;
- payload runtime support;
- payload driver generation;
- CCSDS/PUS/CFDP implementation;
- physical payload simulation;
- ground segment operation;
- hardware integration;
- mission qualification;
- production spacecraft deployment.

---

## Suggested Hashtags

```text
#OrbitFabric
#OpenSource
#SpaceSoftware
#SmallSat
#CubeSat
#MissionEngineering
#ModelBasedEngineering
#SystemsEngineering
#SpaceTech
```
