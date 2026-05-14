# Diagnostics and Lint Rules

This page documents the diagnostics and lint rules currently implemented by OrbitFabric.

Current documented baseline:

```text
v0.8.2 - Entity Index Surface
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

The `orbitfabric export model-summary` command consumes the already loaded Mission Model and reports loader diagnostics if the model cannot be loaded. It does not introduce a dedicated lint rule family in v0.8.1.

The `orbitfabric export entity-index` command consumes the already loaded Mission Model and reports loader diagnostics if the model cannot be loaded. It does not introduce a dedicated lint rule family in v0.8.2.

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
| `OF-CAB-*` | Commandability rule diagnostics. |
| `OF-AUT-*` | Autonomous action diagnostics. |
| `OF-REC-*` | Recovery intent diagnostics. |
| `OF-SCN-*` | Scenario loading and scenario reference diagnostics. |

---

## `OF-SYN-*` - Syntax and file loading diagnostics

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
contacts.yaml
commandability.yaml
```

---

## `OF-STR-*` - Structural diagnostics

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-STR-001` | `ERROR` | top-level key | A required top-level key is missing from a Mission Model YAML file. | Add the expected top-level key. |
| `OF-STR-002` | `ERROR` | top-level key | An unexpected top-level key was found in a Mission Model YAML file. | Remove or rename the unexpected key. |
| `OF-STR-003` | `ERROR` | typed model validation | Pydantic model validation failed. | Fix the field type, required field or invalid value. |

---

## `OF-ID-*` - Identifier diagnostics

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
contact_profiles
link_profiles
contact_windows
downlink_flows
command_sources
commandability_rules
autonomous_actions
recovery_intents
```

---

## `OF-REF-*` - Cross-reference diagnostics

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

## `OF-TLM-*` - Telemetry rules

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-TLM-001` | `ERROR` | telemetry | High or critical numeric telemetry must define operational limits. | Add warning or critical limits. |
| `OF-TLM-006` | `ERROR` | telemetry | Enum telemetry must define enum values. | Add a non-empty `enum` list. |
| `OF-TLM-007` | `WARNING` | telemetry | Telemetry quality policy should be defined. | Add a `quality` policy with required/default fields. |

---

## `OF-CMD-*` - Command rules

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-CMD-005` | `WARNING` | commands | Command should define `timeout_ms`. | Add `timeout_ms` to make command behavior testable. |
| `OF-CMD-006` | `WARNING` | commands | Command should define expected effects. | Add `expected_effects` or explicitly justify no expected effects. |
| `OF-CMD-007` | `ERROR` | commands | A medium, high or critical-risk command is allowed in `SAFE` mode. | Remove `SAFE` from `allowed_modes` or lower the command risk. |
| `OF-CMD-008` | `ERROR` | commands | `expected_effects.data_products` is not a list or contains a non-string entry. | Set `expected_effects.data_products` to a list of data product IDs declared in `data_products.yaml`. |
| `OF-CMD-009` | `ERROR` | commands | Command expected effects reference an unknown data product. | Add the data product to `data_products.yaml` or fix `expected_effects.data_products`. |

The data-flow evidence path starts from command expected effects such as:

```yaml
expected_effects:
  data_products:
    - payload.radiation_histogram
```

These rules ensure that the command-to-data-product link is explicit and valid before scenario evidence, generated data-flow documentation, runtime-facing contract bindings, ground-facing artifacts or Core-owned structured surfaces depend on it.

---

## `OF-EVT-*` - Event rules

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-EVT-002` | `WARNING` | events | Event should define downlink priority. | Add `downlink_priority`. |
| `OF-EVT-003` | `WARNING` | events | Event should define persistence policy. | Add `persistence`. |

---

## `OF-FLT-*` - Fault rules

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-FLT-003` | `ERROR` | faults | Fault must emit at least one event. | Add at least one event ID to the fault `emits` list. |
| `OF-FLT-005` | `ERROR` | faults | Fault recovery references an unknown command. | Add the command or fix `recovery.auto_commands`. |

---

## `OF-MODE-*` - Mode rules

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-MODE-001` | `ERROR` | modes | Exactly one initial mode must be defined. | Set `initial: true` on exactly one mode. |
| `OF-MODE-003` | `ERROR` | mode transitions | Mode transition source or target is not a known mode. | Add the referenced mode or fix the transition. |

---

## `OF-PKT-*` - Packet rules

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-PKT-002` | `ERROR` | packets | Packet must not be empty. | Add at least one telemetry item to the packet. |
| `OF-PKT-003` | `ERROR` | packets | Packet `max_payload_bytes` must be positive. | Set `max_payload_bytes` to a positive integer. |

---

## `OF-PAY-*` - Payload Contract rules

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

## `OF-DP-*` - Data Product Contract rules

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

## `OF-CON-*` - Contact assumption rules

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-CON-001` | `ERROR` | contact_windows | Contact window references an unknown contact profile. | Add the contact profile or fix `contact_window.contact_profile`. |
| `OF-CON-002` | `ERROR` | contact_windows | Contact window references an unknown link profile. | Add the link profile or fix `contact_window.link_profile`. |

---

## `OF-DL-*` - Downlink flow assumption rules

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-DL-001` | `ERROR` | downlink_flows | Downlink flow references an unknown contact profile. | Add the contact profile or fix `downlink_flow.contact_profile`. |
| `OF-DL-002` | `ERROR` | downlink_flows | Downlink flow references an unknown link profile. | Add the link profile or fix `downlink_flow.link_profile`. |
| `OF-DL-003` | `ERROR` | downlink_flows | Downlink flow references an unknown eligible data product. | Add the data product or fix `downlink_flow.eligible_data_products`. |
| `OF-DL-004` | `WARNING` | data_products | High-priority data product has downlink intent but is not eligible in any downlink flow. | Add the data product to a downlink flow or revise its downlink intent. |
| `OF-DL-005` | `WARNING` | downlink_flows | Estimated eligible data product volume may exceed declared contact capacity. | Increase capacity, reduce eligible volume or split the flow. |

---

## `OF-CAB-*` - Commandability rule diagnostics

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-CAB-001` | `ERROR` | commandability_rules | Commandability rule references an unknown command. | Add the command to `commands.yaml` or fix `rule.command`. |
| `OF-CAB-002` | `ERROR` | commandability_rules | Commandability rule references an unknown mode. | Add the mode to `modes.yaml` or fix `rule.allowed_modes`. |
| `OF-CAB-003` | `ERROR` | commandability_rules | Commandability rule references an unknown source. | Add the source to `commandability.sources` or fix `rule.sources`. |
| `OF-CAB-004` | `WARNING` | command_sources | Ground command source requires contact but has no contact profile. | Set `contact_profile` or set `requires_contact` to false. |
| `OF-CAB-005` | `ERROR` | command_sources | Command source references an unknown contact profile. | Add the contact profile to `contacts.yaml` or fix `source.contact_profile`. |
| `OF-CAB-006` | `ERROR` | commandability_rules | Commandability rule references an unknown expected event. | Add the event to `events.yaml` or fix `rule.expected_events`. |
| `OF-CAB-007` | `WARNING` | commandability_rules | Risky command lacks explicit required confirmation intent. | Add a commandability rule with `confirmation: required`, or lower the command risk if appropriate. |

---

## `OF-AUT-*` - Autonomous action diagnostics

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-AUT-001` | `ERROR` | autonomous_actions | Autonomous action dispatches an unknown command. | Add the command to `commands.yaml` or fix `dispatches.command`. |
| `OF-AUT-002` | `ERROR` | autonomous_actions | Autonomous action references an unknown source. | Add the source to `commandability.sources` or fix `dispatches.source`. |
| `OF-AUT-003` | `ERROR` | autonomous_actions | Autonomous action trigger references an unknown event, fault, telemetry item or mode. | Add the referenced object to the Mission Model or fix `action.trigger`. |
| `OF-AUT-004` | `ERROR` | autonomous_actions | Autonomous action references an unknown expected event. | Add the event to `events.yaml` or fix `expected_events`. |
| `OF-AUT-005` | `WARNING` | autonomous_actions | Autonomous action lacks expected events or effects. | Add `expected_events` or `expected_effects` to make the assumption testable. |

---

## `OF-REC-*` - Recovery intent diagnostics

| Rule | Severity | Domain | Description | Suggested fix |
|---|---|---|---|---|
| `OF-REC-001` | `ERROR` | recovery_intents | Recovery intent references an unknown command. | Add the command to `commands.yaml` or fix `recovery_intent.commands`. |
| `OF-REC-002` | `ERROR` | recovery_intents | Recovery intent references an unknown fault, event or mode. | Add the referenced object to the Mission Model or fix `recovery_intent`. |
| `OF-REC-003` | `ERROR` | recovery_intents | Recovery intent references an unknown expected event. | Add the event to `events.yaml` or fix `recovery_intent.expected_events`. |

---

## `OF-SCN-*` - Scenario diagnostics

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
| `OF-SCN-014` | `ERROR` | scenario | Scenario data-flow expectation references an unknown data product. | Use a data product defined in `data_products.yaml`. |
| `OF-SCN-015` | `ERROR` | scenario | Scenario data-flow expectation references an unknown command. | Use a command defined in `commands.yaml`. |
| `OF-SCN-016` | `ERROR` | scenario | Scenario data-flow expectation references an unknown downlink flow. | Use a downlink flow defined in `contacts.yaml`. |
| `OF-SCN-017` | `ERROR` | scenario | Scenario data-flow expectation references an unknown contact window. | Use a contact window defined in `contacts.yaml`. |

Required scenario top-level keys:

```text
scenario
mission
initial_state
steps
```

Data-flow expectations use this shape:

```yaml
expect:
  data_flow:
    data_product: payload.radiation_histogram
    triggered_by_command: payload.start_acquisition
    storage_intent_declared: true
    downlink_intent_declared: true
    eligible_downlink_flow: science_next_available_contact
    contact_window: demo_contact_001
```

These expectations validate contract-level evidence only. They do not execute real storage, downlink, contact scheduling or ground integration behavior.

---

## Current command coverage

Current behavior:

| Command | Diagnostics produced |
|---|---|
| `orbitfabric lint <mission-dir>` | Mission Model loading diagnostics, structural diagnostics, semantic lint findings. |
| `orbitfabric export model-summary <mission-dir>` | Mission Model loading diagnostics before exporting the model summary report. |
| `orbitfabric export entity-index <mission-dir>` | Mission Model loading diagnostics before exporting the entity index report. |
| `orbitfabric gen docs <mission-dir>` | Mission Model loading diagnostics; generation aborts if lint errors exist. |
| `orbitfabric gen data-flow <mission-dir>` | Mission Model loading diagnostics; generation aborts if lint errors exist. |
| `orbitfabric gen runtime <mission-dir>` | Mission Model loading diagnostics; generation aborts if lint errors exist. |
| `orbitfabric gen ground <mission-dir>` | Mission Model loading diagnostics; generation aborts if lint errors exist. |
| `orbitfabric sim <scenario-file>` | Scenario loading diagnostics, Mission Model loading diagnostics, scenario reference diagnostics and scenario execution failures. |

Ground artifact generation consumes the already validated Mission Model and aborts when lint errors exist. It does not add a dedicated ground-specific diagnostic family in v0.8.0.

Model summary export consumes the loaded Mission Model and does not add a dedicated export-specific diagnostic family in v0.8.1.

Entity index export consumes the loaded Mission Model and does not add a dedicated export-specific diagnostic family in v0.8.2.

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
