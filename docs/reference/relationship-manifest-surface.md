# Relationship Manifest Surface

Status: Stable v1.0 surface for admitted relationship families  
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

In v1.0.0, the surface is stable for the admitted relationship families documented on this page.

The `manifest_version` value remains `0.1-candidate` as the report format identifier. That value is not the release status of the surface.

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

## Admitted relationship families

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

These relationship families are admitted only because they can be derived from explicit loaded Mission Model fields.

No relationship family is admitted from naming conventions, ID prefixes, generated documentation, CLI text, downstream UI state or private downstream assumptions.

---

## Admitted derivation sources

Every relationship record must be derived from an explicit field already present in the loaded Mission Model.

Admitted derivation sources are:

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

## Demo mission shape

For `examples/demo-3u/mission`, the manifest contains 46 relationship records.

The demo mission emits seventeen relationship families because its only data product is produced by a payload, not by a subsystem, and its recovery intents are fault-based rather than event-based.

The demo count is:

```json
{
  "total_relationships": 46,
  "relationship_types": {
    "autonomous_action_dispatches_command": 2,
    "command_emits_event": 4,
    "command_targets_subsystem": 4,
    "commandability_rule_constrains_command": 1,
    "data_product_produced_by_payload": 1,
    "downlink_flow_includes_data_product": 1,
    "event_sourced_from_subsystem": 8,
    "fault_emits_event": 3,
    "fault_sourced_from_subsystem": 3,
    "packet_includes_telemetry": 5,
    "payload_accepts_command": 2,
    "payload_belongs_to_subsystem": 1,
    "payload_generates_event": 2,
    "payload_may_raise_fault": 1,
    "payload_produces_telemetry": 1,
    "recovery_intent_reacts_to_fault": 2,
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
| `command_emits_event` | Command emits an indexed event. | `commands[].emits` |
| `command_targets_subsystem` | Command targets an indexed subsystem. | `commands[].target` |
| `commandability_rule_constrains_command` | Commandability rule constrains an indexed command. | `commandability.rules[].command` |
| `data_product_produced_by_payload` | Data product is produced by an indexed payload. | `data_products[].producer` with `producer_type == payload` |
| `data_product_produced_by_subsystem` | Data product is produced by an indexed subsystem. | `data_products[].producer` with `producer_type == subsystem` |
| `downlink_flow_includes_data_product` | Downlink flow includes an indexed data product. | `downlink_flows[].eligible_data_products` |
| `event_sourced_from_subsystem` | Event is sourced from an indexed subsystem. | `events[].source` |
| `fault_emits_event` | Fault emits an indexed event. | `faults[].emits` |
| `fault_sourced_from_subsystem` | Fault is sourced from an indexed subsystem. | `faults[].source` |
| `packet_includes_telemetry` | Packet includes indexed telemetry. | `packets[].telemetry` |
| `payload_accepts_command` | Payload accepts an indexed command. | `payloads[].commands.accepted` |
| `payload_belongs_to_subsystem` | Payload belongs to an indexed subsystem. | `payloads[].subsystem` |
| `payload_generates_event` | Payload generates an indexed event. | `payloads[].events.generated` |
| `payload_may_raise_fault` | Payload may raise an indexed fault. | `payloads[].faults.possible` |
| `payload_produces_telemetry` | Payload produces indexed telemetry. | `payloads[].telemetry.produced` |
| `recovery_intent_reacts_to_event` | Recovery intent reacts to an indexed event. | `commandability.recovery_intents[].event` |
| `recovery_intent_reacts_to_fault` | Recovery intent reacts to an indexed fault. | `commandability.recovery_intents[].fault` |
| `telemetry_sourced_from_subsystem` | Telemetry is sourced from an indexed subsystem. | `telemetry[].source` |

These are contract relationships.

They do not execute commands, evaluate policies, dispatch actions, monitor faults, schedule runtime behavior, expose ground behavior, expose Studio API behavior or expose plugin API behavior.

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
```

No relationship may be added merely because two identifiers look related.

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
model_summary.json -> domain navigation
entity_index.json -> entity navigation
relationship_manifest.json -> relationship navigation
```

Studio may consume admitted Core relationship records.

Studio must not invent missing relationship types or graph edges.

---

## Future relationship families

Additional relationship families may be considered only when they can be derived from explicit loaded Mission Model fields without weakening the current boundary.

No relationship family is accepted until documented in an implementation PR.

---

## Non-goals

The stable v1.0 relationship manifest surface does not introduce:

```text
relationship inference
relationship graph
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
```

It also does not introduce storage relationships, downlink policy relationships, subsystem behavior, packet-generation behavior, runtime routing behavior, ground routing behavior, fault monitoring behavior, autonomous action execution behavior, trigger evaluation behavior, dispatch behavior, commandability evaluation behavior, authorization behavior, security policy behavior, recovery policy evaluation behavior, mode transition behavior or recovery execution behavior.

---

## Acceptance criteria for future relationship records

A future implementation PR that admits additional relationship records must satisfy all of the following:

```text
admit a concrete relationship type
prove deterministic derivation from explicit loaded Mission Model fields
add unit tests for emitted relationships
add tests for deterministic ordering
add tests proving entity_index nodes are referenced, not duplicated
add tests proving forbidden heuristics are not used
add CLI smoke tests for emitted relationships if the CLI output changes
add documentation for every emitted relationship type
keep boundary flags explicit
keep Studio-specific behavior out of Core
```

---

## Final position

The Relationship Manifest Surface is a stable v1.0 Core-owned read-only inspection surface for the admitted relationship families documented on this page.

Additional relationship families may be added only if Core can derive them deterministically from explicit Mission Model semantics.
