# Relationship Manifest Surface

Status: Stable v1.x surface for admitted relationship families  
Surface version: `0.1-candidate`  
Default path: `generated/reports/relationship_manifest.json`

## Purpose

The Relationship Manifest is an OrbitFabric Core-owned read-only structured surface describing explicit relationships between Mission Model entities already represented by the Entity Index.

It answers:

```text
How are indexed mission contract entities explicitly related?
```

The Mission Model remains the semantic source of truth.

The manifest does not infer relationships and does not implement a graph engine.

## Compatibility posture

The original nineteen relationship families admitted in v1.0.0 remain stable compatibility commitments.

v1.2.0 adds seven FDIR-oriented families as additive stable-compatible relationships. They do not rename, remove or redefine an original v1 family.

The report-format identifier remains:

```text
manifest_version = 0.1-candidate
```

That token identifies the existing envelope and relationship record format. It is not the release maturity class and it must not be interpreted as a permanently closed enumeration of relationship types.

A compatible consumer should:

```text
recognize the manifest kind and format identifier
consume relationship types it explicitly understands
preserve or safely ignore unknown additive relationship types
never guess the meaning of an unknown relationship type
```

A consumer that intentionally requires a closed relationship-type set must pin that expectation to a specific release contract.

## Surface chain

```text
model_summary.json          What contract domains are present?
entity_index.json           What contract entities are defined?
relationship_manifest.json  Which explicit admitted relationships connect them?
mission_snapshot.json       What complete Mission Model did Core load?
```

The Entity Index contains entities, not relationships.

The Relationship Manifest contains relationship records whose endpoints resolve to indexed Core entities.

## Original v1.0 relationship families

The original stable family set is:

```text
autonomous_action_dispatches_command
command_emits_event
command_targets_subsystem
commandability_rule_constrains_command
data_product_produced_by_payload
data_product_produced_by_subsystem
downlink_flow_includes_data_product
event_sourced_from_subsystem
fault_emits_event
fault_sourced_from_subsystem
packet_includes_telemetry
payload_accepts_command
payload_belongs_to_subsystem
payload_generates_event
payload_may_raise_fault
payload_produces_telemetry
recovery_intent_reacts_to_event
recovery_intent_reacts_to_fault
telemetry_sourced_from_subsystem
```

These families remain unchanged.

## v1.2 additive FDIR relationship families

The seven additional stable-compatible families are:

```text
autonomous_action_triggered_by_fault
autonomous_action_uses_command_source
fault_observes_telemetry
fault_recovery_dispatches_command
fault_recovery_targets_mode
recovery_intent_includes_command
recovery_intent_targets_mode
```

Each family is admitted because it maps directly to an explicit loaded Mission Model field.

No family is emitted merely because two objects look related or appear together in a scenario.

A deliberate semantic distinction is preserved:

```text
fault_recovery_dispatches_command
```

is used for `faults[].recovery.auto_commands`, which explicitly declares automatic recovery commands, while:

```text
recovery_intent_includes_command
```

is used for `commandability.recovery_intents[].commands`, which states that a recovery intent includes a command without itself asserting runtime dispatch.

## Admitted derivation sources

Original v1 sources include:

```text
commands[].emits
commands[].target
commandability.autonomous_actions[].dispatches.command
commandability.recovery_intents[].event
commandability.recovery_intents[].fault
commandability.rules[].command
data_products[].producer
downlink_flows[].eligible_data_products
events[].source
faults[].emits
faults[].source
packets[].telemetry
payloads[].commands.accepted
payloads[].subsystem
payloads[].events.generated
payloads[].faults.possible
payloads[].telemetry.produced
telemetry[].source
```

v1.2 additionally admits:

```text
commandability.autonomous_actions[].trigger.fault
commandability.autonomous_actions[].dispatches.source
faults[].condition.telemetry
faults[].recovery.auto_commands
faults[].recovery.mode_transition
commandability.recovery_intents[].commands
commandability.recovery_intents[].target_mode
```

`data_products[].producer` can produce either:

```text
producer_type == payload     -> data_product_produced_by_payload
producer_type == subsystem  -> data_product_produced_by_subsystem
```

## Relationship record shape

A relationship record has the conceptual shape:

```json
{
  "relationship_id": "<from-domain>:<from-id>-><relationship-type>:<to-domain>:<to-id>",
  "relationship_type": "<relationship-type>",
  "from": {
    "domain": "<from-domain>",
    "id": "<from-id>"
  },
  "to": {
    "domain": "<to-domain>",
    "id": "<to-id>"
  },
  "derived_from": {
    "model_field": "<explicit-loaded-model-field>"
  }
}
```

Relationship endpoints must resolve to entities represented by the Entity Index.

The manifest must not create independent synthetic nodes.

## Relationship semantics

| Relationship type | Meaning | Derived from |
|---|---|---|
| `autonomous_action_dispatches_command` | Autonomous action declares dispatch of an indexed command. | `commandability.autonomous_actions[].dispatches.command` |
| `autonomous_action_triggered_by_fault` | Autonomous action declares an indexed fault trigger. | `commandability.autonomous_actions[].trigger.fault` |
| `autonomous_action_uses_command_source` | Autonomous action dispatch declaration references an indexed command source. | `commandability.autonomous_actions[].dispatches.source` |
| `command_emits_event` | Command declares an indexed emitted event. | `commands[].emits` |
| `command_targets_subsystem` | Command targets an indexed subsystem. | `commands[].target` |
| `commandability_rule_constrains_command` | Commandability rule constrains an indexed command. | `commandability.rules[].command` |
| `data_product_produced_by_payload` | Data product declares an indexed payload producer. | `data_products[].producer` with payload type |
| `data_product_produced_by_subsystem` | Data product declares an indexed subsystem producer. | `data_products[].producer` with subsystem type |
| `downlink_flow_includes_data_product` | Downlink flow declares an indexed eligible data product. | `downlink_flows[].eligible_data_products` |
| `event_sourced_from_subsystem` | Event declares an indexed subsystem source. | `events[].source` |
| `fault_emits_event` | Fault declares an indexed emitted event. | `faults[].emits` |
| `fault_observes_telemetry` | Fault condition explicitly observes indexed telemetry. | `faults[].condition.telemetry` |
| `fault_recovery_dispatches_command` | Fault recovery declares an indexed automatic recovery command. | `faults[].recovery.auto_commands` |
| `fault_recovery_targets_mode` | Fault recovery declares an indexed target mode. | `faults[].recovery.mode_transition` |
| `fault_sourced_from_subsystem` | Fault declares an indexed subsystem source. | `faults[].source` |
| `packet_includes_telemetry` | Packet declares indexed telemetry membership. | `packets[].telemetry` |
| `payload_accepts_command` | Payload declares an indexed accepted command. | `payloads[].commands.accepted` |
| `payload_belongs_to_subsystem` | Payload declares an indexed subsystem. | `payloads[].subsystem` |
| `payload_generates_event` | Payload declares an indexed generated event. | `payloads[].events.generated` |
| `payload_may_raise_fault` | Payload declares an indexed possible fault. | `payloads[].faults.possible` |
| `payload_produces_telemetry` | Payload declares indexed produced telemetry. | `payloads[].telemetry.produced` |
| `recovery_intent_includes_command` | Recovery intent explicitly includes an indexed command. | `commandability.recovery_intents[].commands` |
| `recovery_intent_reacts_to_event` | Recovery intent declares an indexed event. | `commandability.recovery_intents[].event` |
| `recovery_intent_reacts_to_fault` | Recovery intent declares an indexed fault. | `commandability.recovery_intents[].fault` |
| `recovery_intent_targets_mode` | Recovery intent declares an indexed target mode. | `commandability.recovery_intents[].target_mode` |
| `telemetry_sourced_from_subsystem` | Telemetry declares an indexed subsystem source. | `telemetry[].source` |

## Declared relationship versus observed evidence

A relationship record describes the contract.

It does not prove that the relationship was exercised during a scenario or observed during an operational run.

For example, `fault_observes_telemetry` does not mean that the fault triggered, and `fault_recovery_dispatches_command` does not prove that the command was dispatched in a run.

Observed evidence belongs to scenario or external verification evidence layers.

## Important semantic distinctions

### Telemetry limits are not fault conditions

A telemetry warning or critical limit does not imply that a fault observes that telemetry or uses the same threshold.

`fault_observes_telemetry` is emitted only from the explicit fault condition reference.

### Recovery intent commands are declarative

`recovery_intent_includes_command` means the command is explicitly listed by the recovery intent. It does not assert runtime dispatch.

### Scenario co-occurrence is not a relationship

Two entities appearing in the same scenario or report do not prove that a Core relationship exists between them.

## Boundary flags

The surface declares boundaries equivalent to:

```json
{
  "source_of_truth": "mission_model",
  "core_derived_report": true,
  "read_only": true,
  "contains_entity_index": false,
  "contains_entity_records": false,
  "contains_relationship_manifest": true,
  "contains_relationship_records": true,
  "contains_relationship_graph": false,
  "contains_dependency_graph": false,
  "contains_yaml_ast": false,
  "contains_source_locations": false,
  "contains_plugin_api": false,
  "contains_studio_api": false,
  "contains_runtime_behavior": false,
  "contains_ground_behavior": false
}
```

These flags are part of the public boundary. They do not turn the manifest into a graph, runtime table or Studio API.

## Forbidden derivation sources

Core relationship records must not be derived from:

```text
naming conventions
string similarity
ID prefixes
source filenames
YAML ordering or formatting
generated Markdown
generated runtime files
generated ground files
terminal output
Studio UI state
private downstream assumptions
scenario co-occurrence
simulation-record co-occurrence
```

## Relationship Manifest is not a graph

The surface is a set of explicit relationship records.

It is not:

```text
a graph engine
a dependency graph
a visualization format
a layout format
a scheduler input
a runtime routing table
a ground routing table
```

A downstream tool may render a graph from these records. Every rendered semantic edge must still trace back to a documented Core relationship record.

## Relationship Manifest and extensions

Extensions and plugins must not silently inject records into the Core-owned Relationship Manifest.

Extension-owned relationship-like output must remain explicitly extension-owned.

OrbitFabric Studio may consume Core relationship records, build local presentation indexes and render relationship views. It must not invent missing relationship types, causal links or execution claims.

## CLI export

```bash
orbitfabric export relationship-manifest examples/demo-3u/mission
```

Custom path:

```bash
orbitfabric export relationship-manifest examples/demo-3u/mission \
  --json generated/reports/relationship_manifest.json
```

## Demo coverage

The `demo-3u` mission exercises most admitted relationship families, including the v1.2 FDIR additions.

Some admitted families require richer examples and may not appear in the demo. A family remains valid because its semantics are documented and tested, not because one fixture happens to exercise it.

## Regression protection

The original v1 Relationship Manifest golden signature remains unchanged.

Dedicated regression tests protect the v1.2 additive FDIR families.

This keeps the historical original-v1 compatibility anchor separate from later additive evolution.

## Future relationship families

A future Core relationship family requires explicit review and must be:

```text
semantically narrow
explicitly named
deterministically derived from a loaded Mission Model field
endpoint-resolvable through Entity Index
documented as compatibility-sensitive additive evolution
covered by tests independent from the original v1 golden
```

No relationship family should be created merely because it would make a visualization convenient.

## Non-goals

The Relationship Manifest does not introduce:

```text
relationship inference
relationship graph execution
dependency analysis
YAML AST export
source-location tracking
plugin API
plugin execution
runtime behavior
ground behavior
Studio semantic authority
```

## Final statement

The Relationship Manifest is a stable Core-owned set of explicit contract relationships.

v1.2.0 extends the admitted family set additively for FDIR without changing the original v1 meanings, the record envelope or Core's prohibition on inferred relationships.
