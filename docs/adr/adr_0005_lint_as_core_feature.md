# ADR-0005 — Lint as a Core Feature

Status: Accepted  
Date: 2026-04-29  
Scope: OrbitFabric MVP v0.1  

---

## Context

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

The central artifact is the Mission Model: a machine-readable contract describing telemetry, commands, events, faults, modes, packets, policies and operational scenarios.

A basic implementation could validate only syntax and structure:

- YAML parses correctly;
- required fields are present;
- values have the expected type;
- lists and dictionaries are well-formed.

That is necessary, but not sufficient.

The real problem in small spacecraft projects is not only invalid syntax.

The real problem is inconsistency across mission data, operational assumptions and derived artifacts.

Examples:

- a high-criticality telemetry item has no operational limits;
- a command emits an event that is not defined;
- a fault references telemetry that does not exist;
- a command is allowed in SAFE mode even though it has medium or high operational risk;
- a packet references telemetry that does not exist;
- a packet may exceed its maximum payload size;
- an event has no downlink priority;
- a command has no timeout;
- a scenario expects a mode that is not defined;
- a recovery action dispatches a command that is not allowed in the resulting mode.

These are mission consistency problems, not syntax problems.

OrbitFabric must detect them early.

---

## Decision

OrbitFabric shall treat linting as a core feature, not as an optional utility.

The command:

```bash
orbitfabric lint <mission-directory>
```

shall perform both:

1. structural validation;
2. semantic mission consistency analysis.

Structural validation ensures that the Mission Model is well-formed.

Semantic linting ensures that the Mission Model is coherent, operationally meaningful and internally consistent.

The lint engine shall be one of the primary value propositions of OrbitFabric v0.1.

---

## Rationale

A Mission Data Contract is useful only if it can be trusted.

Trust requires more than parsing.

A YAML file can be syntactically valid and still represent an unsafe, incomplete or contradictory mission model.

OrbitFabric must therefore encode engineering judgment into lint rules.

This is what makes OrbitFabric different from:

- a YAML schema;
- a documentation generator;
- a packet dictionary;
- a simulator configuration file;
- a simple code generator.

The lint engine is the mechanism by which OrbitFabric becomes opinionated and valuable.

---

## Types of Validation

OrbitFabric shall distinguish at least three levels of validation.

### 1. Syntax Validation

Checks whether files can be parsed.

Examples:

- invalid YAML;
- malformed indentation;
- duplicate YAML keys if detectable;
- unsupported document structure.

### 2. Structural Validation

Checks whether the parsed data matches the expected model shape.

Examples:

- missing required field;
- invalid type;
- invalid enum value;
- malformed command argument;
- malformed fault condition;
- malformed packet definition.

### 3. Semantic Linting

Checks whether the Mission Model makes engineering sense.

Examples:

- unknown cross-reference;
- high-criticality telemetry without limits;
- command without timeout;
- risky command allowed in SAFE mode;
- fault with no emitted event;
- event with no persistence or downlink policy;
- packet containing unknown telemetry;
- scenario expecting undefined behavior.

All three levels are required for a serious v0.1.

---

## Severity Levels

Lint findings shall use explicit severity levels.

Initial severity levels:

```text
ERROR
WARNING
INFO
```

### ERROR

An error means the Mission Model is inconsistent or unsafe enough that downstream generation or simulation should not proceed by default.

Examples:

- unknown telemetry reference;
- unknown event reference;
- unknown command reference;
- unknown mode reference;
- duplicate IDs;
- invalid command mode reference;
- fault condition references missing telemetry;
- packet references missing telemetry.

### WARNING

A warning means the Mission Model is valid enough to load, but contains questionable or incomplete engineering information.

Examples:

- telemetry without limits;
- command without timeout;
- event without downlink priority;
- packet period slower than expected telemetry sampling;
- command without expected effects;
- telemetry without quality policy.

### INFO

An info message provides non-blocking guidance.

Examples:

- unused event;
- unused telemetry;
- packet could be split for clarity;
- command risk defaults to low.

---

## Rule Codes

Every lint rule shall have a stable rule code.

Rule codes make diagnostics searchable, documentable and testable.

Initial rule code families:

```text
OF-SYN-*   syntax and file parsing
OF-STR-*   structural validation
OF-ID-*    identifier and uniqueness rules
OF-REF-*   cross-reference rules
OF-TLM-*   telemetry rules
OF-CMD-*   command rules
OF-EVT-*   event rules
OF-FLT-*   fault rules
OF-MODE-*  mode and transition rules
OF-PKT-*   packet rules
OF-SCN-*   scenario rules
OF-POL-*   policy rules
```

Example diagnostics:

```text
ERROR   OF-REF-001 faults.yaml eps.battery_low_fault references unknown telemetry eps.battery.vbat
ERROR   OF-CMD-003 commands.yaml payload.start_acquisition emits unknown event payload.started
WARNING OF-CMD-005 commands.yaml payload.start_acquisition has no timeout_ms
ERROR   OF-MODE-002 commands.yaml payload.start_acquisition is allowed in SAFE mode but risk is medium
WARNING OF-EVT-002 events.yaml payload.data_ready has no downlink priority
ERROR   OF-PKT-001 packets.yaml hk_fast references unknown telemetry adcs.mode
```

---

## Initial v0.1 Rule Set

The v0.1 lint engine shall implement a small but meaningful rule set.

### Identifier Rules

```text
OF-ID-001 duplicate IDs are not allowed within a domain
OF-ID-002 IDs must follow canonical dotted identifier format
OF-ID-003 reserved identifiers must not be redefined
```

### Cross-Reference Rules

```text
OF-REF-001 telemetry source must reference an existing subsystem
OF-REF-002 command target must reference an existing subsystem
OF-REF-003 event source must reference an existing subsystem
OF-REF-004 fault source must reference an existing subsystem
OF-REF-005 fault condition telemetry must reference an existing telemetry item
OF-REF-006 command emitted events must reference existing events
OF-REF-007 fault emitted events must reference existing events
OF-REF-008 command allowed modes must reference existing modes
OF-REF-009 recovery mode transitions must reference existing modes
OF-REF-010 packet telemetry entries must reference existing telemetry items
```

### Telemetry Rules

```text
OF-TLM-001 high-criticality telemetry must define operational limits
OF-TLM-002 telemetry must define persistence policy
OF-TLM-003 telemetry must define downlink priority
OF-TLM-004 telemetry source sampling must be defined
OF-TLM-005 telemetry type must be supported
OF-TLM-006 enum telemetry must define enum values
OF-TLM-007 telemetry quality policy should be defined
```

### Command Rules

```text
OF-CMD-001 command must define allowed modes
OF-CMD-002 command must define risk level
OF-CMD-003 command emitted events must exist
OF-CMD-004 command arguments must define valid types and ranges when applicable
OF-CMD-005 command should define timeout_ms
OF-CMD-006 command should define expected effects
OF-CMD-007 medium/high/critical-risk commands must not be allowed in SAFE mode unless explicitly justified
```

### Event Rules

```text
OF-EVT-001 event severity must be defined
OF-EVT-002 event should define downlink priority
OF-EVT-003 event should define persistence policy
OF-EVT-004 warning/error/critical events should be referenced by a fault, command or scenario
```

### Fault Rules

```text
OF-FLT-001 fault must define a condition
OF-FLT-002 fault condition must reference known telemetry or known event
OF-FLT-003 fault must emit at least one event
OF-FLT-004 fault severity must be compatible with emitted event severity
OF-FLT-005 fault recovery commands must reference known commands
OF-FLT-006 fault recovery mode transition must reference a known mode
```

### Mode Rules

```text
OF-MODE-001 exactly one initial mode must be defined
OF-MODE-002 risky commands must not be allowed in SAFE mode unless explicitly justified
OF-MODE-003 mode transitions must reference known modes
OF-MODE-004 unreachable modes should be reported
OF-MODE-005 recovery transitions should be present for critical faults
```

### Packet Rules

```text
OF-PKT-001 packet telemetry entries must exist
OF-PKT-002 packet must not be empty
OF-PKT-003 packet max_payload_bytes must be positive
OF-PKT-004 estimated packet payload should not exceed max_payload_bytes
OF-PKT-005 high-priority telemetry should appear in at least one packet or have a downlink policy
```

### Scenario Rules

```text
OF-SCN-001 scenario command references must exist
OF-SCN-002 scenario event expectations must reference known events
OF-SCN-003 scenario mode expectations must reference known modes
OF-SCN-004 scenario telemetry injections must reference known telemetry
OF-SCN-005 scenario timeline must be monotonic
```

---

## Lint Output Requirements

The lint command shall produce readable terminal output.

Example:

```text
OrbitFabric Mission Lint v0.1

Mission: demo-3u
Model version: 0.1.0

Loaded:
  spacecraft: 1
  subsystems: 4
  modes: 6
  telemetry: 4
  commands: 3
  events: 7
  faults: 2
  packets: 2

Findings:
  ERROR   OF-REF-005 faults.yaml eps.battery_low_fault references unknown telemetry eps.battery.vbat
  WARNING OF-CMD-005 commands.yaml payload.start_acquisition has no timeout_ms

Summary:
  errors: 1
  warnings: 1
  info: 0

Result: FAILED
```

When no blocking errors exist:

```text
OrbitFabric Mission Lint v0.1

Mission: demo-3u
Model version: 0.1.0

Findings:
  WARNING OF-TLM-001 telemetry eps.battery.current has no limits

Summary:
  errors: 0
  warnings: 1
  info: 0

Result: PASSED WITH WARNINGS
```

---

## JSON Report Requirements

The lint command should be able to produce a machine-readable JSON report.

Initial report structure:

```json
{
  "tool": "orbitfabric-lint",
  "version": "0.1.0",
  "mission": "demo-3u",
  "model_version": "0.1.0",
  "result": "failed",
  "summary": {
    "errors": 1,
    "warnings": 1,
    "info": 0
  },
  "findings": [
    {
      "severity": "ERROR",
      "code": "OF-REF-005",
      "file": "faults.yaml",
      "domain": "faults",
      "object_id": "eps.battery_low_fault",
      "message": "fault references unknown telemetry eps.battery.vbat"
    }
  ]
}
```

This allows future CI integration.

---

## CI Behavior

In CI, linting shall fail on errors.

Warnings shall not fail CI by default in v0.1.

Future versions may support stricter policies:

```bash
orbitfabric lint mission/ --warnings-as-errors
orbitfabric lint mission/ --rule OF-CMD-005=error
orbitfabric lint mission/ --disable-rule OF-EVT-004
```

These options are useful but not required for the first implementation.

---

## Relationship with Schema Validation

Schema validation is required but insufficient.

Pydantic or JSON Schema can verify that fields exist and have correct types.

They cannot fully verify mission semantics.

Examples that require semantic linting:

- checking whether a referenced event exists;
- checking whether a command is unsafe in SAFE mode;
- checking whether a fault recovery command is valid in the target mode;
- checking whether high-criticality telemetry has meaningful limits;
- checking whether packets contain valid telemetry entries.

Therefore, the lint engine shall sit above structural validation.

---

## Implementation Guidance

The lint engine shall be implemented under:

```text
src/orbitfabric/lint/
```

Suggested structure:

```text
src/orbitfabric/lint/
├── engine.py
├── finding.py
├── rule.py
├── registry.py
├── rules_identifiers.py
├── rules_references.py
├── rules_telemetry.py
├── rules_commands.py
├── rules_events.py
├── rules_faults.py
├── rules_modes.py
├── rules_packets.py
└── rules_scenarios.py
```

The engine shall operate on validated Mission Model objects, not raw YAML dictionaries.

Each rule should be testable independently.

Each finding should include:

- severity;
- rule code;
- message;
- domain;
- object ID where applicable;
- file where applicable;
- optional suggestion.

---

## Rule Design Principles

Lint rules should be:

- deterministic;
- documented;
- testable;
- specific;
- actionable;
- stable enough to reference in documentation and CI.

Bad lint message:

```text
Command is bad.
```

Good lint message:

```text
ERROR OF-CMD-007 commands.yaml payload.start_acquisition is allowed in SAFE mode but risk is medium. Remove SAFE from allowed_modes or add an explicit justification.
```

Every rule should help the user improve the Mission Model.

---

## What Lint Must Not Become in v0.1

The lint engine must not become:

- a formal verification engine;
- a theorem prover;
- a full safety analysis tool;
- a replacement for mission review;
- a substitute for flight qualification;
- a full requirements-management system;
- a hidden runtime simulator.

It is an engineering consistency checker.

It finds contradictions, omissions and suspicious modeling choices early.

---

## Future Extensions

Future versions may add:

- custom lint rule plugins;
- mission-specific lint profiles;
- severity override configuration;
- CI output formats;
- SARIF export;
- HTML lint reports;
- autofix suggestions;
- rule documentation pages;
- integration with generated documentation;
- linting of generated artifacts;
- comparison between two Mission Model versions.

These extensions are valuable, but v0.1 must remain focused.

---

## Architectural Rule

No OrbitFabric artifact generation should proceed from an invalid Mission Model by default.

The normal flow shall be:

```text
load mission
validate structure
run semantic lint
if errors exist: stop
if only warnings exist: allow generation and simulation with warning summary
```

This rule protects downstream artifacts from being generated from inconsistent mission data.

---

## Decision Summary

`orbitfabric lint` is a core feature of OrbitFabric.

It must perform semantic mission consistency analysis, not just syntax or schema validation.

The lint engine is one of the main r