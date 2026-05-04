# Diagnostics and Lint Rules

This page documents the diagnostics and lint rules currently implemented by OrbitFabric.

Current documented baseline:

```text
v0.4.0 — Contact Windows and Downlink Flow Contracts
```

OrbitFabric diagnostics are intentionally actionable. A diagnostic should tell the user:

- what is wrong;
- where it was found;
- which Mission Model domain is affected;
- how to fix it.

Diagnostics may be produced by different layers:

- the Mission Model loader;
- the semantic lint engine;
- the scenario loader;
- scenario reference validation.

Not every diagnostic listed here is produced by the same command.

---

## Severity levels

| Severity | Meaning |
|---|---|
| `ERROR` | The model, scenario or operation is invalid and the command must fail. |
| `WARNING` | The model is structurally valid, but an engineering concern was found. |
| `INFO` | Informational diagnostic. Currently reserved for future use. |

Default lint behavior:

```text
ERROR   -> lint fails
WARNING -> lint passes with warnings
INFO    -> lint passes
```

With:

```bash
orbitfabric lint <mission-dir> --warnings-as-errors
```

warning-level findings also make lint fail.

---

## Diagnostic shape

OrbitFabric diagnostics expose a common diagnostic shape across Mission Model loading, scenario loading, scenario reference validation and semantic lint findings.

| Field | Meaning |
|---|---|
| `severity` | Diagnostic severity. |
| `code` | Stable diagnostic or rule identifier. |
| `file` | File where the issue was found, when known. |
| `domain` | Mission Model or scenario domain. |
| `object_id` | Object affected by the diagnostic, when known. |
| `message` | Human-readable explanation. |
| `suggestion` | Suggested fix, when available. |

The `suggestion` field is intentionally optional, but it should be provided whenever OrbitFabric can recommend a clear and safe corrective action.

---

## Rule families

| Prefix | Family |
|---|---|
| `OF-SYN-*` | YAML syntax, file loading and file shape diagnostics. |
| `OF-STR-*` | Structural Mission Model diagnostics. |
| `OF-ID-*` | Identifier uniqueness diagnostics. |
| `OF-REF-*` | Cross-reference diagnostics. |
| `OF-TLM-*` | Telemetry engineering lint rules. |
| `OF-CMD-*` | Command engineering lint rules. |
| `OF-EVT-*` | Event engineering lint rules. |
| `OF-FLT-*` | Fault engineering lint rules. |
| `OF-MODE-*` | Mode and mode-transition diagnostics. |
| `OF-PKT-*` | Packet engineering lint rules. |
| `OF-PAY-*` | Payload Contract lint rules. |
| `OF-DP-*` | Data Product Contract lint rules. |
| `OF-CON-*` | Contact assumption rules. |
| `OF-DL-*` | Downlink flow assumption rules. |
| `OF-SCN-*` | Scenario loading and scenario reference diagnostics. |

---

## `OF-SYN-*` — Syntax and file loading diagnostics

These diagnostics are produced while loading a Mission Model directory.

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-SYN-001` | `ERROR` | mission path | Mission path does not exist or is not a directory. | Pass an existing Mission Model directory. |
| `OF-SYN-002` | `ERROR` | mission file | A required Mission Model file is missing. | Add the required YAML file. |
| `OF-SYN-003` | `ERROR` | YAML | A YAML file is syntactically invalid. | Fix YAML syntax. |
| `OF-SYN-004` | `ERROR` | YAML | A YAML file is empty. | Add the required top-level content. |
| `OF-SYN-005` | `ERROR` | YAML | A YAML file does not contain a top-level mapping. | Use a YAML mapping at the top level. |

Current required Mission Model files:

```text
spacecraft.yaml
subsystems.yaml
modes.yaml
telemetry.yaml
commands.yaml
events.yaml
faults.yaml
packets.yaml
policies.yaml
```

Current optional Mission Model files:

```text
payloads.yaml
data_products.yaml
```

---

## `OF-STR-*` — Structural diagnostics

These diagnostics are produced during Mission Model structural validation.

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-STR-001` | `ERROR` | top-level key | A required top-level key is missing from a Mission Model YAML file. | Add the expected top-level key. |
| `OF-STR-002` | `ERROR` | top-level key | An unexpected top-level key was found in a Mission Model YAML file. | Remove or rename the unexpected key. |
| `OF-STR-003` | `ERROR` | typed model validation | Pydantic model validation failed. | Fix the field type, required field or invalid value. |

---

## `OF-ID-*` — Identifier diagnostics

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-ID-001` | `ERROR` | model domain | Duplicate IDs are not allowed within the same domain. | Rename or remove the duplicate object. |

Domains currently checked for duplicate IDs:

```text
subsystems
modes
telemetry
commands
events
faults
packets
payloads
data_products
```

---

## `OF-REF-*` — Cross-reference diagnostics

These rules check that Mission Model objects reference existing objects.

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-REF-001` | `ERROR` | telemetry | Telemetry source does not reference an existing subsystem. | Add the subsystem or fix telemetry `source`. |
| `OF-REF-002` | `ERROR` | commands | Command target does not reference an existing subsystem. | Add the subsystem or fix command `target`. |
| `OF-REF-003` | `ERROR` | events | Event source does not reference an existing subsystem. | Add the subsystem or fix event `source`. |
| `OF-REF-004` | `ERROR` | faults | Fault source does not reference an existing subsystem. | Add the subsystem or fix fault `source`. |
| `OF-REF-005` | `ERROR` | faults | Fault condition references unknown telemetry. | Add the telemetry item or fix the fault condition. |
| `OF-REF-006` | `ERROR` | commands | Command emits an unknown event. | Add the event or fix command `emits`. |
| `OF-REF-007` | `ERROR` | faults | Fault emits an unknown event. | Add the event or fix fault `emits`. |
| `OF-REF-008` | `ERROR` | commands | Command allowed mode does not reference an existing mode. | Add the mode or fix `allowed_modes`. |
| `OF-REF-009` | `ERROR` | faults | Fault recovery references an unknown target mode. | Add the mode or fix `recovery.mode_transition`. |
| `OF-REF-010` | `ERROR` | packets | Packet references unknown telemetry. | Add the telemetry item or fix packet `telemetry`. |

---

## `OF-TLM-*` — Telemetry rules

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-TLM-001` | `ERROR` | telemetry | High or critical numeric telemetry must define operational limits. | Add warning or critical limits. |
| `OF-TLM-006` | `ERROR` | telemetry | Enum telemetry must define enum values. | Add a non-empty `enum` list. |
| `OF-TLM-007` | `WARNING` | telemetry | Telemetry quality policy should be defined. | Add a `quality` policy with required/default fields. |

Numeric telemetry types currently checked by `OF-TLM-001`:

```text
uint8
uint16
uint32
int8
int16
int32
float32
float64
```

---

## `OF-CMD-*` — Command rules

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-CMD-005` | `WARNING` | commands | Command should define `timeout_ms`. | Add `timeout_ms` to make command behavior testable. |
| `OF-CMD-006` | `WARNING` | commands | Command should define expected effects. | Add `expected_effects` or explicitly justify no expected effects. |
| `OF-CMD-007` | `ERROR` | commands | A medium, high or critical-risk command is allowed in `SAFE` mode. | Remove `SAFE` from `allowed_modes` or lower the command risk. |

---

## `OF-EVT-*` — Event rules

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-EVT-002` | `WARNING` | events | Event should define downlink priority. | Add `downlink_priority`. |
| `OF-EVT-003` | `WARNING` | events | Event should define persistence policy. | Add `persistence`. |

---

## `OF-FLT-*` — Fault rules

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-FLT-003` | `ERROR` | faults | Fault must emit at least one event. | Add at least one event ID to the fault `emits` list. |
| `OF-FLT-005` | `ERROR` | faults | Fault recovery references an unknown command. | Add the command or fix `recovery.auto_commands`. |

---

## `OF-MODE-*` — Mode rules

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-MODE-001` | `ERROR` | modes | Exactly one initial mode must be defined. | Set `initial: true` on exactly one mode. |
| `OF-MODE-003` | `ERROR` | mode transitions | Mode transition source or target is not a known mode. | Add the referenced mode or fix the transition. |

---

## `OF-PKT-*` — Packet rules

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-PKT-002` | `ERROR` | packets | Packet must not be empty. | Add at least one telemetry item to the packet. |
| `OF-PKT-003` | `ERROR` | packets | Packet `max_payload_bytes` must be positive. | Set `max_payload_bytes` to a positive integer. |

---

## `OF-PAY-*` — Payload Contract rules

These rules validate optional Payload / IOD Payload Contracts.

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-PAY-001` | `ERROR` | payloads | Payload subsystem reference must exist. | Add the subsystem or fix `payload.subsystem`. |
| `OF-PAY-002` | `ERROR` | payloads | Payload subsystem must have type `payload`. | Link the payload contract to a payload subsystem. |
| `OF-PAY-003` | `ERROR` | payloads | Payload lifecycle must define an initial state. | Add `lifecycle.initial_state`. |
| `OF-PAY-004` | `ERROR` | payloads | Payload lifecycle initial state must exist in lifecycle states. | Add the state or fix `initial_state`. |
| `OF-PAY-005` | `ERROR` | payloads | Payload telemetry reference must exist. | Add the telemetry or fix the reference. |
| `OF-PAY-006` | `ERROR` | payloads | Payload command reference must exist. | Add the command or fix the reference. |
| `OF-PAY-007` | `ERROR` | payloads | Payload event reference must exist. | Add the event or fix the reference. |
| `OF-PAY-008` | `ERROR` | payloads | Payload fault reference must exist. | Add the fault or fix the reference. |
| `OF-PAY-009` | `ERROR` | commands | Command payload lifecycle precondition references an unknown payload or state. | Fix the payload lifecycle precondition. |
| `OF-PAY-010` | `ERROR` | commands | Command expected payload lifecycle effect references an unknown payload or state. | Fix the expected payload lifecycle effect. |

Payload rules are contract-level rules. They do not validate payload firmware, drivers, buses or physical payload behavior.

---

## `OF-DP-*` — Data Product Contract rules

These rules validate optional Data Product and Storage Contracts.

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-DP-002` | `ERROR` | data_products | Data product producer reference must exist. | Add the producer payload/subsystem or fix `producer`. |
| `OF-DP-003` | `ERROR` | data_products | Optional data product payload reference must exist. | Add the payload contract or fix `payload`. |
| `OF-DP-006` | `WARNING` | data_products | Data product storage intent should define retention. | Set `storage.retention` or remove storage intent if not retained. |
| `OF-DP-007` | `WARNING` | data_products | Data product storage intent should define overflow policy. | Set `storage.overflow_policy` for retained data products. |
| `OF-DP-008` | `WARNING` | data_products | High or critical priority data product should define downlink intent. | Set `downlink.policy`. |

Structural validation covers additional data product constraints such as duplicate IDs, positive estimated size and known literal values for product type, storage class, overflow policy and downlink policy.

Data Product rules are contract-level rules. They do not validate real storage, compression, contact scheduling or downlink runtime behavior.

---

## `OF-CON-*` — Contact assumption rules

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-CON-001` | `ERROR` | contact_windows | Contact window references an unknown contact profile. | Add the contact profile or fix `contact_window.contact_profile`. |
| `OF-CON-002` | `ERROR` | contact_windows | Contact window references an unknown link profile. | Add the link profile or fix `contact_window.link_profile`. |

---

## `OF-DL-*` — Downlink flow assumption rules

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-DL-001` | `ERROR` | downlink_flows | Downlink flow references an unknown contact profile. | Add the contact profile or fix `downlink_flow.contact_profile`. |
| `OF-DL-002` | `ERROR` | downlink_flows | Downlink flow references an unknown link profile. | Add the link profile or fix `downlink_flow.link_profile`. |
| `OF-DL-003` | `ERROR` | downlink_flows | Downlink flow references an unknown eligible data product. | Add the data product or fix `downlink_flow.eligible_data_products`. |
| `OF-DL-004` | `WARNING` | data_products | High-priority data product has downlink intent but is not eligible in any downlink flow. | Add the data product to a downlink flow or revise its downlink intent. |
| `OF-DL-005` | `WARNING` | downlink_flows | Estimated eligible data product volume may exceed declared contact capacity. | Increase capacity, reduce eligible volume or split the flow. |

---

## `OF-SCN-*` — Scenario diagnostics

These diagnostics are produced while loading or validating an OrbitFabric scenario.

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-SCN-000` | `ERROR` | scenario path | Scenario path does not exist or is not a file. | Pass an existing scenario YAML file. |
| `OF-SCN-001` | `ERROR` | scenario | Scenario command or expected command references an unknown command. | Use a command defined in `commands.yaml`. |
| `OF-SCN-002` | `ERROR` | scenario | Scenario event expectation references an unknown event. | Use an event defined in `events.yaml`. |
| `OF-SCN-003` | `ERROR` | scenario | Scenario mode expectation references an unknown mode. | Use a mode defined in `modes.yaml`. |
| `OF-SCN-004` | `ERROR` | scenario | Scenario telemetry injection or expectation references unknown telemetry. | Use telemetry defined in `telemetry.yaml`. |
| `OF-SCN-005` | `ERROR` | scenario | Scenario timeline must be monotonic. | Sort scenario steps by non-decreasing time. |
| `OF-SCN-006` | `ERROR` | scenario | Scenario initial mode references unknown mode. | Use a mode defined in `modes.yaml`. |
| `OF-SCN-007` | `ERROR` | scenario | Scenario initial telemetry references unknown telemetry. | Use telemetry defined in `telemetry.yaml`. |
| `OF-SCN-008` | `ERROR` | scenario YAML | Scenario YAML is syntactically invalid. | Fix YAML syntax. |
| `OF-SCN-009` | `ERROR` | scenario YAML | Scenario YAML file is empty. | Add scenario content. |
| `OF-SCN-010` | `ERROR` | scenario YAML | Scenario YAML does not contain a top-level mapping. | Use a YAML mapping at the top level. |
| `OF-SCN-011` | `ERROR` | scenario | A required scenario top-level key is missing. | Add the required key. |
| `OF-SCN-012` | `ERROR` | scenario | An unexpected scenario top-level key was found. | Remove or rename the unexpected key. |
| `OF-SCN-013` | `ERROR` | scenario model validation | Scenario typed model validation failed. | Fix the invalid field, missing field or invalid value. |

Required scenario top-level keys:

```text
scenario
mission
initial_state
steps
```

---

## Current command coverage

Current behavior:

| Command | Diagnostics produced |
|---|---|
| `orbitfabric lint <mission-dir>` | Mission Model loading diagnostics, structural diagnostics, semantic lint findings. |
| `orbitfabric gen docs <mission-dir>` | Mission Model loading diagnostics; generation aborts if lint errors exist. |
| `orbitfabric sim <scenario-file>` | Scenario loading diagnostics, Mission Model loading diagnostics, scenario reference diagnostics and scenario execution failures. |

---

## Notes for contributors

When adding a new diagnostic or lint rule:

1. assign a stable `OF-*` code;
2. choose the correct family prefix;
3. use `ERROR` only when the model or scenario is invalid;
4. use `WARNING` for engineering concerns that are valid but risky or incomplete;
5. provide an actionable message;
6. provide a suggested fix where possible;
7. add or update tests;
8. update this rule catalog.

Do not document a rule as implemented until it exists in code and is covered by tests.
