# OrbitFabric Mission Model v0.1

Status: Draft
Scope: OrbitFabric MVP v0.1
Model version: 0.1.0

This page documents the core v0.1 Mission Model surface. Optional extension domains added after v0.1, including Payload Contracts, Data Product Contracts, Contact/Downlink Contracts and Commandability/Autonomy Contracts, are documented in their dedicated reference pages.

---

## 1. Purpose

The OrbitFabric Mission Model is the canonical Mission Data Contract for a small spacecraft mission.

It defines, in a structured and machine-readable form:

- spacecraft metadata;
- subsystems;
- operational modes;
- mode transitions;
- telemetry;
- commands;
- events;
- faults;
- packets;
- mission policies;
- operational scenarios.

The Mission Model is the single source of truth for:

- semantic linting;
- generated documentation;
- host-side scenario simulation;
- JSON reports;
- future runtime skeleton generation;
- future ground integration artifacts.

OrbitFabric v0.1 intentionally keeps the model small but coherent.

---

## 2. Canonical Directory Layout

A mission is represented as a directory named `mission/` containing domain-specific YAML files.

```text
mission/
├── spacecraft.yaml
├── subsystems.yaml
├── modes.yaml
├── telemetry.yaml
├── commands.yaml
├── events.yaml
├── faults.yaml
├── packets.yaml
└── policies.yaml
```

Scenarios are stored separately:

```text
scenarios/
├── battery_low_during_payload.yaml
└── nominal_payload_acquisition.yaml
```

For the canonical demo:

```text
examples/demo-3u/
├── mission/
│   ├── spacecraft.yaml
│   ├── subsystems.yaml
│   ├── modes.yaml
│   ├── telemetry.yaml
│   ├── commands.yaml
│   ├── events.yaml
│   ├── faults.yaml
│   ├── packets.yaml
│   ├── policies.yaml
│   ├── payloads.yaml
│   ├── data_products.yaml
│   ├── contacts.yaml
│   └── commandability.yaml
└── scenarios/
    ├── battery_low_during_payload.yaml
    └── nominal_payload_acquisition.yaml
```

Each YAML file must contain exactly one top-level domain key. The core v0.1 files remain required for the demo; `payloads.yaml`, `data_products.yaml`, `contacts.yaml` and `commandability.yaml` are optional extension domains described by later reference pages.

---

## 3. Identifier Rules

OrbitFabric uses dotted identifiers.

Examples:

```text
eps.battery.voltage
payload.start_acquisition
eps.battery_low_fault
payload.acquisition_started
```

### 3.1 Identifier Format

Recommended format:

```text
[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)*
```

Rules:

- lowercase only;
- segments separated by dots;
- each segment starts with a letter;
- digits and underscores are allowed after the first character;
- spaces are not allowed;
- hyphens are not allowed in identifiers;
- identifiers must be stable once published.

### 3.2 Identifier Scope

IDs must be unique within their domain.

Domains include:

- subsystem IDs;
- telemetry IDs;
- command IDs;
- event IDs;
- fault IDs;
- packet IDs;
- scenario IDs.

Cross-domain duplicate IDs should be avoided but are not forbidden in v0.1 unless ambiguity is created.

### 3.3 Related Lint Rules

```text
OF-ID-001 duplicate IDs are not allowed within a domain
OF-ID-002 IDs must follow canonical dotted identifier format
OF-ID-003 reserved identifiers must not be redefined
```

---

## 4. Common Controlled Values

### 4.1 Criticality

Allowed values:

```text
low
medium
high
critical
```

Meaning:

- `low`: useful but not operationally important;
- `medium`: relevant for operations or diagnosis;
- `high`: important for spacecraft health or mission execution;
- `critical`: directly relevant to survival, safety or essential operation.

### 4.2 Severity

Allowed values:

```text
info
warning
error
critical
```

Meaning:

- `info`: operational information;
- `warning`: abnormal condition requiring attention;
- `error`: serious malfunction or failed operation;
- `critical`: condition requiring immediate protective action.

### 4.3 Downlink Priority

Allowed values:

```text
low
medium
high
critical
```

Meaning:

- `low`: downlink when convenient;
- `medium`: regular operational visibility;
- `high`: prioritize in constrained windows;
- `critical`: highest priority, health/safety relevant.

### 4.4 Persistence Policy

Allowed values:

```text
none
store
downlink_only
store_and_downlink
```

Meaning:

- `none`: do not persist and do not downlink by default;
- `store`: persist locally;
- `downlink_only`: downlink but do not persist locally;
- `store_and_downlink`: persist and make available for downlink.

### 4.5 Risk

Allowed values:

```text
low
medium
high
critical
```

Meaning:

- `low`: safe diagnostic or status command;
- `medium`: can affect subsystem operation;
- `high`: can affect spacecraft state, payload or power budget;
- `critical`: can affect survival, safety, irreversible configuration or essential functions.

---

## 5. `spacecraft.yaml`

### 5.1 Purpose

Defines mission identity and high-level spacecraft metadata.

### 5.2 Top-Level Key

```yaml
spacecraft:
```

### 5.3 Schema

| Field | Type | Required | Description |
|---|---:|---:|---|
| `id` | string | yes | Stable spacecraft/mission identifier. |
| `name` | string | yes | Human-readable spacecraft name. |
| `class` | string | yes | Spacecraft class, for example `cubesat`, `picosat`, `smallsat`. |
| `form_factor` | string | no | Physical form factor, for example `1U`, `3U`, `6U`. |
| `mission_type` | string | no | Mission category, for example `technology_demonstrator`. |
| `model_version` | string | yes | Mission Model contract version declared by this mission. |

### 5.4 Example

```yaml
spacecraft:
  id: demo-3u
  name: Demo 3U Spacecraft
  class: cubesat
  form_factor: 3U
  mission_type: technology_demonstrator
  model_version: 0.1.0
```

### 5.5 Lint Rules

```text
OF-STR-001 spacecraft.id is required
OF-STR-002 spacecraft.name is required
OF-STR-003 spacecraft.model_version is required
OF-ID-002 spacecraft.id should follow identifier rules
```

---

## 6. `subsystems.yaml`

### 6.1 Purpose

Defines the spacecraft subsystem inventory.

Subsystems are referenced by telemetry, commands, events and faults.

### 6.2 Top-Level Key

```yaml
subsystems:
```

### 6.3 Schema

Each subsystem entry has:

| Field | Type | Required | Description |
|---|---:|---:|---|
| `id` | string | yes | Stable subsystem identifier. |
| `name` | string | yes | Human-readable name. |
| `type` | string | yes | Subsystem category. |
| `criticality` | enum | yes | Operational criticality. |
| `description` | string | no | Optional description. |

### 6.4 Recommended `type` Values

```text
core
subsystem
payload
communication
software
other
```

v0.1 does not enforce a strict subsystem type taxonomy beyond structural validation, but unknown values may produce warnings in future versions.

### 6.5 Example

```yaml
subsystems:
  - id: obc
    name: On-Board Computer
    type: core
    criticality: critical

  - id: eps
    name: Electrical Power System
    type: subsystem
    criticality: critical

  - id: payload
    name: Demo Payload
    type: payload
    criticality: medium

  - id: radio
    name: Communication System
    type: communication
    criticality: high
```

### 6.6 Lint Rules

```text
OF-ID-001 duplicate subsystem IDs are not allowed
OF-ID-002 subsystem IDs must follow identifier rules
OF-STR-010 subsystem.name is required
OF-STR-011 subsystem.criticality is required
```

---

## 7. `modes.yaml`

### 7.1 Purpose

Defines operational modes and allowed mode transitions.

Modes constrain command execution and describe high-level spacecraft operational state.

### 7.2 Top-Level Keys

```yaml
modes:
mode_transitions:
```

For v0.1, both keys may live in `modes.yaml`.

### 7.3 `modes` Schema

`modes` is a mapping from mode name to mode definition.

| Field | Type | Required | Description |
|---|---:|---:|---|
| `description` | string | yes | Human-readable mode description. |
| `initial` | bool | no | Marks the initial mode. Exactly one mode must be initial. |

### 7.4 Mode Name Rules

Mode names use uppercase snake case.

Examples:

```text
BOOT
NOMINAL
PAYLOAD_ACTIVE
DEGRADED
SAFE
MAINTENANCE
```

### 7.5 `mode_transitions` Schema

Each transition has:

| Field | Type | Required | Description |
|---|---:|---:|---|
| `from` | string | yes | Source mode. |
| `to` | string | yes | Target mode. |
| `reason` | string | yes | Machine-readable transition reason. |
| `description` | string | no | Human-readable explanation. |

### 7.6 Example

```yaml
modes:
  BOOT:
    description: Initial boot and system initialization
    initial: true

  NOMINAL:
    description: Standard operational mode

  PAYLOAD_ACTIVE:
    description: Payload acquisition is active

  DEGRADED:
    description: Reduced capability mode after non-critical fault

  SAFE:
    description: Safe mode with payload disabled

  MAINTENANCE:
    description: Ground-controlled maintenance mode

mode_transitions:
  - from: BOOT
    to: NOMINAL
    reason: boot_completed

  - from: NOMINAL
    to: PAYLOAD_ACTIVE
    reason: payload_acquisition_started

  - from: PAYLOAD_ACTIVE
    to: DEGRADED
    reason: eps_warning_fault

  - from: DEGRADED
    to: SAFE
    reason: critical_fault

  - from: SAFE
    to: MAINTENANCE
    reason: ground_authorized
```

### 7.7 Lint Rules

```text
OF-MODE-001 exactly one initial mode must be defined
OF-MODE-003 mode transitions must reference known modes
OF-MODE-004 unreachable modes should be reported
OF-ID-001 duplicate mode names are not allowed
OF-STR-020 mode.description is required
```

---

## 8. `telemetry.yaml`

### 8.1 Purpose

Defines telemetry items.

Telemetry is not just a driver value. It is an operationally meaningful data point with source, type, unit, sampling, criticality, limits, persistence and downlink behavior.

### 8.2 Top-Level Key

```yaml
telemetry:
```

### 8.3 Schema

Each telemetry item has:

| Field | Type | Required | Description |
|---|---:|---:|---|
| `id` | string | yes | Stable telemetry identifier. |
| `name` | string | yes | Human-readable name. |
| `type` | enum | yes | Data type. |
| `unit` | string | yes | Unit or `none`. |
| `source` | string | yes | Source subsystem ID. |
| `sampling` | string | yes | Sampling policy, for example `1Hz`, `10s`, `on_change`. |
| `criticality` | enum | yes | Operational criticality. |
| `persistence` | enum | yes | Persistence policy. |
| `downlink_priority` | enum | yes | Downlink priority. |
| `limits` | object | no | Warning/critical limits. |
| `enum` | list[string] | conditional | Required if `type` is `enum`. |
| `quality` | object | no | Quality flag policy. |
| `description` | string | no | Human-readable description. |

### 8.4 Supported Types v0.1

```text
bool
uint8
uint16
uint32
int8
int16
int32
float32
float64
enum
string
```

### 8.5 Limits Schema

For numeric telemetry, `limits` may include:

| Field | Type | Description |
|---|---:|---|
| `warning_low` | number | Lower warning threshold. |
| `critical_low` | number | Lower critical threshold. |
| `warning_high` | number | Upper warning threshold. |
| `critical_high` | number | Upper critical threshold. |

### 8.6 Quality Schema

| Field | Type | Required | Description |
|---|---:|---:|---|
| `required` | bool | no | Whether a quality flag is expected. |
| `default` | string | no | Default quality state. |

Recommended quality states:

```text
good
suspect
invalid
unknown
```

### 8.7 Example

```yaml
telemetry:
  - id: eps.battery.voltage
    name: Battery Voltage
    type: float32
    unit: V
    source: eps
    sampling: 1Hz
    criticality: high
    persistence: store_and_downlink
    downlink_priority: high
    limits:
      warning_low: 6.8
      critical_low: 6.4
    quality:
      required: true
      default: good

  - id: payload.acquisition.active
    name: Payload Acquisition Active
    type: bool
    unit: none
    source: payload
    sampling: on_change
    criticality: medium
    persistence: store_and_downlink
    downlink_priority: medium
    quality:
      required: true
      default: good
```

### 8.8 Lint Rules

```text
OF-ID-001 duplicate telemetry IDs are not allowed
OF-ID-002 telemetry IDs must follow identifier rules
OF-REF-001 telemetry source must reference an existing subsystem
OF-TLM-001 high-criticality telemetry must define operational limits
OF-TLM-002 telemetry must define persistence policy
OF-TLM-003 telemetry must define downlink priority
OF-TLM-004 telemetry sampling must be defined
OF-TLM-005 telemetry type must be supported
OF-TLM-006 enum telemetry must define enum values
OF-TLM-007 telemetry quality policy should be defined
```

---

## 9. `commands.yaml`

### 9.1 Purpose

Defines telecommands.

A command is not only an opcode or function call. It has target, arguments, allowed modes, preconditions, timeout, acknowledgment behavior, operational risk, emitted events and expected effects.

### 9.2 Top-Level Key

```yaml
commands:
```

### 9.3 Schema

Each command has:

| Field | Type | Required | Description |
|---|---:|---:|---|
| `id` | string | yes | Stable command identifier. |
| `target` | string | yes | Target subsystem ID. |
| `description` | string | yes | Human-readable description. |
| `arguments` | list | yes | Command arguments. Empty list allowed. |
| `allowed_modes` | list[string] | yes | Modes where command is allowed. |
| `preconditions` | list/object | no | Additional conditions required before execution. |
| `requires_ack` | bool | yes | Whether acknowledgment is required. |
| `timeout_ms` | integer | recommended | Timeout in milliseconds. |
| `risk` | enum | yes | Operational risk. |
| `emits` | list[string] | no | Events emitted by successful command execution. |
| `expected_effects` | object | no | Expected telemetry or mode effects. |

### 9.4 Argument Schema

Each argument has:

| Field | Type | Required | Description |
|---|---:|---:|---|
| `name` | string | yes | Argument name. |
| `type` | enum | yes | Argument type. |
| `min` | number | no | Minimum value for numeric arguments. |
| `max` | number | no | Maximum value for numeric arguments. |
| `enum` | list[string] | conditional | Allowed values for enum arguments. |
| `default` | any | no | Optional default value. |
| `description` | string | no | Human-readable description. |

Supported command argument types follow telemetry scalar types where applicable.

### 9.5 Expected Effects Schema

v0.1 supports:

```yaml
expected_effects:
  telemetry:
    payload.acquisition.active: true
  mode_transition:
    to: PAYLOAD_ACTIVE
```

The simulator may use this information for simple behavior checks.

### 9.6 Example

```yaml
commands:
  - id: payload.start_acquisition
    target: payload
    description: Start demo payload acquisition
    arguments:
      - name: duration_s
        type: uint16
        min: 1
        max: 600
    allowed_modes:
      - NOMINAL
    requires_ack: true
    timeout_ms: 1000
    risk: medium
    emits:
      - payload.acquisition_started
    expected_effects:
      telemetry:
        payload.acquisition.active: true
      mode_transition:
        to: PAYLOAD_ACTIVE

  - id: payload.stop_acquisition
    target: payload
    description: Stop demo payload acquisition
    arguments: []
    allowed_modes:
      - PAYLOAD_ACTIVE
      - DEGRADED
      - SAFE
    requires_ack: true
    timeout_ms: 1000
    risk: low
    emits:
      - payload.acquisition_stopped
    expected_effects:
      telemetry:
        payload.acquisition.active: false
```

### 9.7 Lint Rules

```text
OF-ID-001 duplicate command IDs are not allowed
OF-ID-002 command IDs must follow identifier rules
OF-REF-002 command target must reference an existing subsystem
OF-REF-006 command emitted events must reference existing events
OF-REF-008 command allowed modes must reference existing modes
OF-CMD-001 command must define allowed modes
OF-CMD-002 command must define risk level
OF-CMD-003 command emitted events must exist
OF-CMD-004 command arguments must define valid types and ranges when applicable
OF-CMD-005 command should define timeout_ms
OF-CMD-006 command should define expected effects
OF-CMD-007 medium/high/critical-risk commands must not be allowed in SAFE mode unless explicitly justified
```

---

## 10. `events.yaml`

### 10.1 Purpose

Defines operational events.

Events are first-class mission artifacts. They are not just logs.

Events may drive:

- fault management;
- storage;
- downlink prioritization;
- diagnostics;
- scenario assertions;
- mission timeline reconstruction;
- generated documentation.

### 10.2 Top-Level Key

```yaml
events:
```

### 10.3 Schema

Each event has:

| Field | Type | Required | Description |
|---|---:|---:|---|
| `id` | string | yes | Stable event identifier. |
| `source` | string | yes | Source subsystem ID. |
| `severity` | enum | yes | Event severity. |
| `description` | string | yes | Human-readable description. |
| `downlink_priority` | enum | recommended | Downlink priority. |
| `persistence` | enum | recommended | Persistence policy. |

### 10.4 Example

```yaml
events:
  - id: payload.acquisition_started
    source: payload
    severity: info
    description: Payload acquisition started
    downlink_priority: medium
    persistence: store_and_downlink

  - id: eps.battery_low
    source: eps
    severity: warning
    description: Battery voltage below warning threshold
    downlink_priority: high
    persistence: store_and_downlink

  - id: eps.battery_critical
    source: eps
    severity: critical
    description: Battery voltage below critical threshold
    downlink_priority: critical
    persistence: store_and_downlink
```

### 10.5 Lint Rules

```text
OF-ID-001 duplicate event IDs are not allowed
OF-ID-002 event IDs must follow identifier rules
OF-REF-003 event source must reference an existing subsystem
OF-EVT-001 event severity must be defined
OF-EVT-002 event should define downlink priority
OF-EVT-003 event should define persistence policy
OF-EVT-004 warning/error/critical events should be referenced by a fault, command or scenario
```

---

## 11. `faults.yaml`

### 11.1 Purpose

Defines fault detection and minimal recovery behavior.

Faults must not be hidden as scattered `if` statements in code. In OrbitFabric, a fault is a model element.

### 11.2 Top-Level Key

```yaml
faults:
```

### 11.3 Schema

Each fault has:

| Field | Type | Required | Description |
|---|---:|---:|---|
| `id` | string | yes | Stable fault identifier. |
| `source` | string | yes | Source subsystem ID. |
| `severity` | enum | yes | Fault severity. |
| `description` | string | yes | Human-readable description. |
| `condition` | object | yes | Detection condition. |
| `emits` | list[string] | yes | Events emitted when fault triggers. |
| `recovery` | object | no | Minimal recovery policy. |

### 11.4 Telemetry Condition Schema

```yaml
condition:
  telemetry: eps.battery.voltage
  operator: <
  value: 6.8
  debounce_samples: 3
```

Fields:

| Field | Type | Required | Description |
|---|---:|---:|---|
| `telemetry` | string | yes | Telemetry item to evaluate. |
| `operator` | enum | yes | Comparison operator. |
| `value` | number/string/bool | yes | Comparison value. |
| `debounce_samples` | integer | no | Required consecutive samples before trigger. |

Supported operators v0.1:

```text
<
<=
>
>=
==
!=
```

### 11.5 Event Occurrence Condition Schema

v0.1 may support event occurrence conditions, but they are optional for the first implementation.

```yaml
condition:
  event: payload.command_timeout
  occurrences: 3
  window_s: 60
```

### 11.6 Recovery Schema

v0.1 supports only simple recovery actions:

```yaml
recovery:
  mode_transition: DEGRADED
  auto_commands:
    - payload.stop_acquisition
```

Fields:

| Field | Type | Required | Description |
|---|---:|---:|---|
| `mode_transition` | string | no | Target mode after fault trigger. |
| `auto_commands` | list[string] | no | Commands automatically dispatched after fault trigger. |

### 11.7 Example

```yaml
faults:
  - id: eps.battery_low_fault
    source: eps
    severity: warning
    description: Battery voltage below warning threshold
    condition:
      telemetry: eps.battery.voltage
      operator: <
      value: 6.8
      debounce_samples: 3
    emits:
      - eps.battery_low
    recovery:
      mode_transition: DEGRADED
      auto_commands:
        - payload.stop_acquisition

  - id: eps.battery_critical_fault
    source: eps
    severity: critical
    description: Battery voltage below critical threshold
    condition:
      telemetry: eps.battery.voltage
      operator: <
      value: 6.4
      debounce_samples: 2
    emits:
      - eps.battery_critical
    recovery:
      mode_transition: SAFE
      auto_commands:
        - payload.stop_acquisition
```

### 11.8 Lint Rules

```text
OF-ID-001 duplicate fault IDs are not allowed
OF-ID-002 fault IDs must follow identifier rules
OF-REF-004 fault source must reference an existing subsystem
OF-REF-005 fault condition telemetry must reference an existing telemetry item
OF-REF-007 fault emitted events must reference existing events
OF-REF-009 recovery mode transitions must reference existing modes
OF-FLT-001 fault must define a condition
OF-FLT-002 fault condition must reference known telemetry or known event
OF-FLT-003 fault must emit at least one event
OF-FLT-004 fault severity must be compatible with emitted event severity
OF-FLT-005 fault recovery commands must reference known commands
OF-FLT-006 fault recovery mode transition must reference a known mode
```

---

## 12. `packets.yaml`

### 12.1 Purpose

Defines telemetry packet groupings.

v0.1 does not implement a real packet protocol. Packets are logical groupings used for documentation, linting and future exports.

### 12.2 Top-Level Key

```yaml
packets:
```

### 12.3 Schema

Each packet has:

| Field | Type | Required | Description |
|---|---:|---:|---|
| `id` | string | yes | Stable packet identifier. |
| `name` | string | yes | Human-readable packet name. |
| `type` | enum | yes | Packet representation type. |
| `max_payload_bytes` | integer | yes | Maximum allowed payload size. |
| `period` | string | no | Expected production period. |
| `telemetry` | list[string] | yes | Telemetry included in the packet. |
| `description` | string | no | Optional description. |

### 12.4 Supported Packet Types v0.1

```text
json
binary_compact
ccsds_like
```

Only `json` is expected to be implemented in the v0.1 simulator/logging path.

`binary_compact` and `ccsds_like` are reserved logical labels for future work and may trigger warnings if used without a generator.

### 12.5 Example

```yaml
packets:
  - id: hk_fast
    name: Fast Housekeeping Packet
    type: json
    max_payload_bytes: 512
    period: 1s
    telemetry:
      - eps.battery.voltage
      - eps.battery.current
      - obc.mode

  - id: payload_status
    name: Payload Status Packet
    type: json
    max_payload_bytes: 512
    period: 10s
    telemetry:
      - payload.acquisition.active
```

### 12.6 Lint Rules

```text
OF-ID-001 duplicate packet IDs are not allowed
OF-ID-002 packet IDs must follow identifier rules
OF-REF-010 packet telemetry entries must reference existing telemetry items
OF-PKT-001 packet telemetry entries must exist
OF-PKT-002 packet must not be empty
OF-PKT-003 packet max_payload_bytes must be positive
OF-PKT-004 estimated packet payload should not exceed max_payload_bytes
OF-PKT-005 high-priority telemetry should appear in at least one packet or have a downlink policy
```

---

## 13. `policies.yaml`

### 13.1 Purpose

Defines controlled vocabularies and reusable mission-level policy values.

v0.1 keeps policies simple.

### 13.2 Top-Level Key

```yaml
policies:
```

### 13.3 Schema

| Field | Type | Required | Description |
|---|---:|---:|---|
| `persistence.allowed_values` | list[string] | yes | Allowed persistence values. |
| `downlink_priority.allowed_values` | list[string] | yes | Allowed downlink priorities. |
| `command_risk.allowed_values` | list[string] | yes | Allowed risk values. |

### 13.4 Example

```yaml
policies:
  persistence:
    allowed_values:
      - none
      - store
      - downlink_only
      - store_and_downlink

  downlink_priority:
    allowed_values:
      - low
      - medium
      - high
      - critical

  command_risk:
    allowed_values:
      - low
      - medium
      - high
      - critical
```

### 13.5 Lint Rules

```text
OF-POL-001 policy allowed values must not be empty
OF-POL-002 referenced policy values must be known
```

---

## 14. Scenario Model

### 14.1 Purpose

Scenarios describe operational sequences and expected behavior.

They are used by `orbitfabric sim` to validate that the Mission Model behaves as expected under a defined timeline.

Scenarios are not part of the static mission directory but are closely linked to it.

### 14.2 Top-Level Keys

```yaml
scenario:
initial_state:
steps:
```

### 14.3 Scenario Metadata Schema

```yaml
scenario:
  id: battery_low_during_payload
  name: Battery degradation during payload operation
  description: Payload is active while EPS battery voltage drops below warning threshold.
```

| Field | Type | Required | Description |
|---|---:|---:|---|
| `id` | string | yes | Stable scenario identifier. |
| `name` | string | yes | Human-readable scenario name. |
| `description` | string | no | Scenario description. |

### 14.4 Initial State Schema

```yaml
initial_state:
  mode: NOMINAL
  telemetry:
    eps.battery.voltage: 7.4
    eps.battery.current: 0.4
    payload.acquisition.active: false
```

| Field | Type | Required | Description |
|---|---:|---:|---|
| `mode` | string | yes | Initial operational mode. |
| `telemetry` | mapping | no | Initial telemetry values. |

### 14.5 Step Schema

Each step must define `t`.

` t ` is scenario time in seconds from scenario start.

Supported step types v0.1:

- command dispatch;
- telemetry injection;
- expected event;
- expected mode;
- expected command;
- expected scenario status.

### 14.6 Command Step

```yaml
- t: 5
  command: payload.start_acquisition
  args:
    duration_s: 300
  expect:
    command_status: ACCEPTED
```

### 14.7 Telemetry Injection Step

```yaml
- t: 30
  inject:
    telemetry: eps.battery.voltage
    value: 6.7
```

### 14.8 Expected Event Step

```yaml
- t: 33
  expect_event: eps.battery_low
```

### 14.9 Expected Mode Step

```yaml
- t: 35
  expect_mode: DEGRADED
```

### 14.10 Expected Command Step

```yaml
- t: 36
  expect_command:
    id: payload.stop_acquisition
    dispatch: AUTO
```

### 14.11 Scenario Status Step

```yaml
- t: 40
  expect:
    scenario_status: PASSED
```

### 14.12 Complete Example

```yaml
scenario:
  id: battery_low_during_payload
  name: Battery degradation during payload operation
  description: Payload is active while EPS battery voltage drops below warning threshold.

initial_state:
  mode: NOMINAL
  telemetry:
    eps.battery.voltage: 7.4
    eps.battery.current: 0.4
    payload.acquisition.active: false

steps:
  - t: 5
    command: payload.start_acquisition
    args:
      duration_s: 300
    expect:
      command_status: ACCEPTED

  - t: 6
    expect_event: payload.acquisition_started

  - t: 7
    expect_mode: PAYLOAD_ACTIVE

  - t: 30
    inject:
      telemetry: eps.battery.voltage
      value: 6.7

  - t: 31
    inject:
      telemetry: eps.battery.voltage
      value: 6.7

  - t: 32
    inject:
      telemetry: eps.battery.voltage
      value: 6.7

  - t: 33
    expect_event: eps.battery_low

  - t: 35
    expect_mode: DEGRADED

  - t: 36
    expect_command:
      id: payload.stop_acquisition
      dispatch: AUTO

  - t: 37
    expect_event: payload.acquisition_stopped

  - t: 40
    expect:
      scenario_status: PASSED
```

### 14.13 Lint Rules

```text
OF-SCN-001 scenario command references must exist
OF-SCN-002 scenario event expectations must reference known events
OF-SCN-003 scenario mode expectations must reference known modes
OF-SCN-004 scenario telemetry injections must reference known telemetry
OF-SCN-005 scenario timeline must be monotonic
OF-SCN-006 scenario initial mode must reference a known mode
OF-SCN-007 scenario initial telemetry must reference known telemetry
```

---

## 15. Cross-File Reference Rules

The loader and lint engine must resolve references across files.

Required reference checks:

| Source | Reference | Target Domain | Rule |
|---|---|---|---|
| telemetry.source | subsystem ID | subsystems | OF-REF-001 |
| command.target | subsystem ID | subsystems | OF-REF-002 |
| event.source | subsystem ID | subsystems | OF-REF-003 |
| fault.source | subsystem ID | subsystems | OF-REF-004 |
| fault.condition.telemetry | telemetry ID | telemetry | OF-REF-005 |
| command.emits | event ID | events | OF-REF-006 |
| fault.emits | event ID | events | OF-REF-007 |
| command.allowed_modes | mode name | modes | OF-REF-008 |
| recovery.mode_transition | mode name | modes | OF-REF-009 |
| packet.telemetry | telemetry ID | telemetry | OF-REF-010 |

Unknown references are errors.

---

## 16. Loader Requirements

The v0.1 loader must:

1. accept a mission directory path;
2. locate all canonical YAML files;
3. parse YAML files;
4. verify top-level domain keys;
5. build typed domain objects;
6. build identifier indexes;
7. detect duplicate IDs;
8. resolve cross-file references;
9. return a complete Mission Model object;
10. emit diagnostics with file and domain context.

The loader must not silently ignore unknown top-level keys.

Unknown fields may be warnings in v0.1, but should become stricter as the model matures.

---

## 17. Minimal Mission Model Object

Internally, the validated model should conceptually expose:

```text
MissionModel
├── spacecraft
├── subsystems
├── modes
├── mode_transitions
├── telemetry
├── commands
├── events
├── faults
├── packets
└── policies
```

Each domain should be indexable by ID.

Example conceptual access:

```text
model.telemetry["eps.battery.voltage"]
model.commands["payload.start_acquisition"]
model.events["eps.battery_low"]
model.modes["SAFE"]
```

---

## 18. v0.1 Required Demo Coverage

The `demo-3u` model must include at least:

- one spacecraft;
- four subsystems:
  - `obc`;
  - `eps`;
  - `payload`;
  - `radio`;
- six modes:
  - `BOOT`;
  - `NOMINAL`;
  - `PAYLOAD_ACTIVE`;
  - `DEGRADED`;
  - `SAFE`;
  - `MAINTENANCE`;
- at least four telemetry items;
- at least three commands;
- at least six events;
- at least two faults;
- at least two packets;
- one scenario: `battery_low_during_payload`.

---

## 19. Out of Scope for Mission Model v0.1

The following are explicitly out of scope:

- CCSDS packet standard compliance;
- PUS service modeling;
- CFDP entities;
- authentication and authorization;
- cryptographic command protection;
- real-time scheduling;
- hardware bus description;
- pinout description;
- electrical interface modeling;
- detailed ADCS dynamics;
- orbital dynamics;
- resource budgeting;
- power simulation;
- thermal simulation;
- full requirements traceability;
- formal verification semantics;
- flight qualification metadata.

These may be future extensions, but they must not enter v0.1.

---

## 20. Compatibility and Evolution

Mission Model v0.1 is intentionally small.

Future versions may add:

- dedicated mission manifest;
- includes/imports;
- subsystem-specific model extensions;
- custom type definitions;
- calibration metadata;
- packet encoding rules;
- XTCE export metadata;
- Yamcs/OpenC3 export metadata;
- generated C++ runtime metadata;
- plugin-defined model sections;
- rule severity profiles;
- mission constraints;
- requirements traceability.

Backward compatibility should be considered after v0.1 becomes useful.

Before that, clarity is more important than compatibility.

---

## 21. Final Rule

The Mission Model is the contract.

If behavior matters to mission consistency, it should be represented in the Mission Model.

If behavior exists only in Python code, documentation or simulator internals, it is not yet part of the contract.

OrbitFabric must always prefer explicit model semantics over hidden implementation assumptions.

