# Relationship Manifest Surface

Status: Stable v1.0 surface for original admitted relationship families, with documented additive post-v1 FDIR families  
Surface version: `0.1-candidate`  
Default path: `generated/reports/relationship_manifest.json`

---

## Purpose

The Relationship Manifest Surface is an OrbitFabric Core-owned structured report.

It describes Core-owned relationships between Mission Model entities already exposed by the Entity Index Surface.

It answers:

```text
How are indexed mission contract entities related?
```

The Mission Model remains the source of truth.

The relationship manifest is a derived, read-only inspection artifact.

The original v1.0.0 stable surface admits nineteen deliberately narrow relationship families. Later minor-release development may add relationship families when the new family is derived deterministically from an explicit loaded Mission Model field and the compatibility impact is documented.

The current development surface adds seven FDIR-oriented relationship families under that additive rule.

The `manifest_version` value remains `0.1-candidate` as the report-format identifier because the envelope and relationship-record shape are unchanged. That value is not the release status of the surface and must not be used as a closed enumeration of every relationship type a later compatible consumer may encounter.

---

## Compatibility posture

The original nineteen v1.0.0 relationship families remain stable compatibility commitments.

The seven FDIR families documented below are an explicit additive extension. They do not rename, remove or change the meaning of any original v1 relationship family.

A downstream consumer should therefore:

```text
recognize the manifest kind and format identifier
consume relationship types it explicitly supports
preserve or safely ignore unknown additive relationship types
never assign guessed semantics to an unknown relationship type
```

A downstream consumer must not treat the set of relationship types as a permanently closed enum unless it intentionally pins itself to a specific release contract.

The v1 golden regression remains fixed on the original relationship-family contract. Separate tests cover additive families.

---

## Surface chain

OrbitFabric Core exposes these machine-readable inspection surfaces:

```text
model_summary.json          -> What contract domains are present?
entity_index.json           -> What contract entities are defined?
relationship_manifest.json  -> How are indexed mission contract entities related?
```

`model_summary.json` is domain-level.

`entity_index.json` is entity-level.

`relationship_manifest.json` is relationship-level.

`entity_index.json` contains entities, not relationships.

The relationship manifest contains Core-owned relationship records derived from explicit Mission Model references.

---

## Original v1.0.0 admitted relationship families

The v1.0.0 stable surface admits nineteen deliberately narrow relationship families:

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

These original relationship families remain unchanged.

---

## Additive FDIR relationship families

The current development extension admits seven additional relationship families:

```text
autonomous_action_triggered_by_fault
autonomous_action_uses_command_source
fault_observes_telemetry
fault_recovery_dispatches_command
fault_recovery_targets_mode
recovery_intent_includes_command
recovery_intent_targets_mode
```

They are admitted because each maps directly to an explicit loaded Mission Model field.

No family is added merely because two objects look related or appear together in a scenario.

A deliberate naming distinction is preserved:

```text
fault_recovery_dispatches_command
```

is appropriate for `faults[].recovery.auto_commands`, which declares automatic recovery commands, while:

```text
recovery_intent_includes_command
```

is used for `commandability.recovery_intents[].commands` because a recovery intent declares commands as part of its intent and the field does not itself assert runtime dispatch.

---

## Admitted derivation sources

Every relationship record must be derived from an explicit field already present in the loaded Mission Model.

Original v1.0 derivation sources are:

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

The additive FDIR extension admits:

```text
commandability.autonomous_actions[].trigger.fault
commandability.autonomous_actions[].dispatches.source
faults[].condition.telemetry
faults[].recovery.auto_commands
faults[].recovery.mode_transition
commandability.recovery_intents[].commands
commandability.recovery_intents[].target_mode
```

`data_products[].producer` admits two distinct relationship families, depending on the explicit `producer_type` value:

```text
producer_type == payload    -> data_product_produced_by_payload
producer_type == subsystem -> data_product_produced_by_subsystem
```

---

## CLI export

The manifest can be exported with:

```bash
orbitfabric export relationship-manifest examples/demo-3u/mission
```

The default output path is:

```text
generated/reports/relationship_manifest.json
```

A custom output file can be selected with:

```bash
orbitfabric export relationship-manifest examples/demo-3u/mission \
  --json generated/reports/relationship_manifest.json
```

The command does not infer relationships.

It does not generate a graph.

It does not expose plugin behavior.

---

## Demo mission shape with the additive FDIR extension

For `examples/demo-3u/mission`, the current development manifest contains 63 relationship records across 24 emitted relationship families.

The complete admitted family set is larger because the demo does not exercise `data_product_produced_by_subsystem` or `recovery_intent_reacts_to_event`.

The demo count is:

```json
{
  "total_relationships": 63,
  "relationship_types": {
    "autonomous_action_dispatches_command": 2,
    "autonomous_action_triggered_by_fault": 2,
    "autonomous_action_uses_command_source": 2,
    "command_emits_event": 4,
    "command_targets_subsystem": 4,
    "commandability_rule_constrains_command": 1,
    "data_product_produced_by_payload": 1,
    "downlink_flow_includes_data_product": 1,
    "event_sourced_from_subsystem": 8,
    "fault_emits_event": 3,
    "fault_observes_telemetry": 3,
    "fault_recovery_dispatches_command": 3,
    "fault_recovery_targets_mode": 3,
    "fault_sourced_from_subsystem": 3,
    "packet_includes_telemetry": 5,
    "payload_accepts_command": 2,
    "payload_belongs_to_subsystem": 1,
    "payload_generates_event": 2,
    "payload_may_raise_fault": 1,
    "payload_produces_telemetry": 1,
    "recovery_intent_includes_command": 2,
    "recovery_intent_reacts_to_fault": 2,
    "recovery_intent_targets_mode": 2,
    "telemetry_sourced_from_subsystem": 5
  }
}
```

The admitted `data_product_produced_by_subsystem` family is exercised by richer examples such as `examples/spacelab-inspired-communications-minislice/mission`.

The admitted `recovery_intent_reacts_to_event` family is not emitted by the demo mission because the demo recovery intents are fault-based.

---

## Boundary flags

The manifest declares boundary flags equivalent to:

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

These flags are part of the boundary definition.

They do not make the manifest a graph, dependency graph, Studio API or plugin API.

---

## Relationship record shape

Each relationship record has this conceptual shape:

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

Relationship records must refer to entities already represented by the Entity Index Surface.

They must not create independent synthetic nodes.

If Core cannot resolve an endpoint to an indexed entity, the relationship type must either not be emitted, be emitted only under an explicitly documented unresolved endpoint policy, or remain unsupported.

---

## Relationship family semantics

Each admitted relationship type has a narrow meaning:

| Relationship type | Meaning | Derived from |
|---|---|---|
| `autonomous_action_dispatches_command` | Autonomous action dispatches an indexed command. | `commandability.autonomous_actions[].dispatches.command` |
| `autonomous_action_triggered_by_fault` | Autonomous action declares an indexed fault as its trigger. | `commandability.autonomous_actions[].trigger.fault` |
| `autonomous_action_uses_command_source` | Autonomous action dispatch declaration uses an indexed command source. | `commandability.autonomous_actions[].dispatches.source` |
| `command_emits_event` | Command emits an indexed event. | `commands[].emits` |
| `command_targets_subsystem` | Command targets an indexed subsystem. | `commands[].target` |
| `commandability_rule_constrains_command` | Commandability rule constrains an indexed command. | `commandability.rules[].command` |
| `data_product_produced_by_payload` | Data product is produced by an indexed payload. | `data_products[].producer` with `producer_type == payload` |
| `data_product_produced_by_subsystem` | Data product is produced by an indexed subsystem. | `data_products[].producer` with `producer_type == subsystem` |
| `downlink_flow_includes_data_product` | Downlink flow includes an indexed eligible data product. | `downlink_flows[].eligible_data_products` |
| `event_sourced_from_subsystem` | Event is sourced from an indexed subsystem. | `events[].source` |
| `fault_emits_event` | Fault emits an indexed event. | `faults[].emits` |
| `fault_observes_telemetry` | Fault condition explicitly observes indexed telemetry. | `faults[].condition.telemetry` |
| `fault_recovery_dispatches_command` | Fault recovery declares an indexed automatic recovery command. | `faults[].recovery.auto_commands` |
| `fault_recovery_targets_mode` | Fault recovery explicitly targets an indexed mode. | `faults[].recovery.mode_transition` |
| `fault_sourced_from_subsystem` | Fault is sourced from an indexed subsystem. | `faults[].source` |
| `packet_includes_telemetry` | Packet includes indexed telemetry. | `packets[].telemetry` |
| `payload_accepts_command` | Payload accepts an indexed command. | `payloads[].commands.accepted` |
| `payload_belongs_to_subsystem` | Payload belongs to an indexed subsystem. | `payloads[].subsystem` |
| `payload_generates_event` | Payload generates an indexed event. | `payloads[].events.generated` |
| `payload_may_raise_fault` | Payload may raise an indexed fault. | `payloads[].faults.possible` |
| `payload_produces_telemetry` | Payload produces indexed telemetry. | `payloads[].telemetry.produced` |
| `recovery_intent_includes_command` | Recovery intent explicitly includes an indexed command. | `commandability.recovery_intents[].commands` |
| `recovery_intent_reacts_to_event` | Recovery intent reacts to an indexed event. | `commandability.recovery_intents[].event` |
| `recovery_intent_reacts_to_fault` | Recovery intent reacts to an indexed fault. | `commandability.recovery_intents[].fault` |
| `recovery_intent_targets_mode` | Recovery intent explicitly targets an indexed mode. | `commandability.recovery_intents[].target_mode` |
| `telemetry_sourced_from_subsystem` | Telemetry is sourced from an indexed subsystem. | `telemetry[].source` |

These are contract relationships.

They do not prove that the relationship was exercised in a scenario or observed in a run.

In particular:

```text
fault_observes_telemetry
```

does not mean that a fault actually triggered, and:

```text
fault_recovery_dispatches_command
```

does not constitute run evidence that the command was dispatched.

That distinction belongs to structured scenario/run evidence.

The manifest does not execute commands, evaluate policies, monitor faults, schedule runtime behavior, expose ground behavior, expose Studio API behavior or expose plugin API behavior.

---

## Important semantic distinctions

### Telemetry limits are not fault conditions

A telemetry warning or critical limit does not imply that a fault observes that telemetry or uses the same threshold.

`fault_observes_telemetry` is emitted only from:

```text
faults[].condition.telemetry
```

Studio or any other consumer must not derive the relationship from numeric-limit coincidence.

### Recovery intent commands are declarative

`recovery_intent_includes_command` states that a command is explicitly listed by the recovery intent.

It does not assert that the command was dispatched during a run.

### Declared relationship is not observed evidence

Two relationship endpoints appearing in the same scenario or simulation report do not prove that a relationship was exercised.

Observed relationship evidence requires a separate Core-owned structured correlation.

---

## Forbidden derivation sources

A relationship manifest must not derive relationship records from:

```text
naming conventions
string similarity
ID prefixes
source file names
YAML file ordering
YAML formatting
generated Markdown
generated runtime files
generated ground files
human-oriented CLI output
stdout text
stderr text
Studio UI state
React component state
private downstream assumptions
scenario co-occurrence
simulation-record co-occurrence
```

No relationship may be added merely because two identifiers look related or occur together.

---

## Relationship manifest is not a graph

A relationship manifest is a set of Core-owned relationship records.

It is not:

```text
a graph engine
a dependency graph
a visualization format
a Studio API
a layout format
a runtime routing table
a ground routing table
a scheduler input
a command dispatcher input
```

A downstream tool may render a graph from relationship records.

The semantic meaning of every rendered edge must still come from Core.

---

## Relationship manifest and plugins

A relationship manifest is not a plugin API.

Plugins must not silently inject relationship records into a Core-owned relationship manifest.

If future plugins are allowed to contribute diagnostics or reports, their outputs must be clearly separated from Core output.

A future plugin-contributed relationship-like artifact must be marked as plugin output, not Core relationship data.

---

## Relationship manifest and Studio

OrbitFabric Studio must not infer relationships privately.

The intended downstream chain is:

```text
mission_snapshot.json       -> complete loaded contract inspection
entity_index.json           -> normalized entity navigation
relationship_manifest.json  -> explicit relationship navigation
```

Studio may consume admitted Core relationship records.

Studio may construct local indexes and presentation graphs from those records.

Studio must not invent missing relationship types, graph edges, causal links or observed execution claims.

---

## Future relationship families

Additional relationship families may be considered only when they can be derived from explicit loaded Mission Model fields without weakening the current boundary.

A future family must be:

```text
semantically narrow
explicitly named
deterministically derived
endpoint-resolvable through Entity Index
documented as compatibility-sensitive additive evolution
covered by tests independent from the original v1 golden
```

No relationship family is accepted until documented in an implementation PR.

---

## Non-goals

The Relationship Manifest Surface does not introduce:

```text
relationship inference
relationship graph engine
relationship dependency analysis
source line tracking
source column tracking
YAML AST export
plugin API
plugin discovery
plugin loader
Studio API
runtime behavior
ground behavior
observed relationship evidence
```

The additive FDIR families expose declared Mission Model relationships only. They do not evaluate trigger conditions, execute recovery behavior, dispatch commands at runtime or prove that recovery occurred.

---

## Acceptance criteria for future relationship records

A future implementation PR that admits additional relationship records must satisfy all of the following:

```text
admit a concrete relationship type
prove deterministic derivation from explicit loaded Mission Model fields
add unit tests for emitted relationships
add tests for deterministic ordering
add tests proving Entity Index nodes are referenced, not duplicated
add tests proving forbidden heuristics are not used
add CLI smoke tests if CLI-visible counts or behavior change
add documentation for every emitted relationship type
preserve the original stable-family golden contract
keep boundary flags explicit
keep Studio-specific behavior out of Core
```

---

## Final position

The Relationship Manifest Surface remains a Core-owned read-only inspection surface.

The original v1.0 relationship families remain stable.

The current FDIR extension adds seven explicit families without changing the existing relationship record shape or inventing any graph or execution semantics.

Additional relationship families may be added only if Core can derive them deterministically from explicit Mission Model semantics and the compatibility impact is explicit, reviewed and documented.
