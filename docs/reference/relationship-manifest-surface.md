# Relationship Manifest Surface

Status: Candidate  
Surface version: 0.1-candidate  
Default path: `generated/reports/relationship_manifest.json`

---

## Purpose

The Relationship Manifest Surface is a candidate OrbitFabric Core report.

Its purpose is to describe Core-owned relationships between Mission Model entities that are already exposed by the Entity Index Surface.

It is intended to answer:

```text
How are indexed mission contract entities related?
```

The Mission Model remains the source of truth.

The relationship manifest is a derived, read-only inspection artifact.

---

## Current status

OrbitFabric Core currently exposes these machine-readable inspection surfaces:

```text
model_summary.json
entity_index.json
relationship_manifest.json
```

`model_summary.json` is domain-level.

It answers:

```text
What contract domains are present in this mission?
```

`entity_index.json` is entity-level.

It answers:

```text
What contract entities are defined in this mission?
```

`relationship_manifest.json` is relationship-level.

It answers:

```text
How are indexed mission contract entities related?
```

`entity_index.json` contains nodes, not edges.

The relationship manifest contains Core-owned edge records derived from explicit Mission Model references.

---

## Admitted relationship families

At the current baseline, the surface admits nineteen deliberately narrow relationship families:

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

## Currently admitted derivation sources

Every relationship record must be derived from an explicit field already present in the loaded Mission Model.

Currently admitted derivation sources are:

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

`data_products[].producer` currently admits two distinct relationship families, depending on the explicit `producer_type` value:

```text
producer_type == payload    -> data_product_produced_by_payload
producer_type == subsystem -> data_product_produced_by_subsystem
```

---

## CLI export

The candidate manifest can be exported with:

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

For `examples/demo-3u/mission`, the current manifest contains 46 relationship records.

The demo mission currently emits seventeen relationship families because its only data product is produced by a payload, not by a subsystem, and its recovery intents are fault-based rather than event-based.

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

The admitted `data_product_produced_by_subsystem` family is exercised by richer examples such as `examples/spacelab-inspired-communications-minislice/mission`, where seven data products are produced by indexed subsystems.

The admitted `payload_may_raise_fault` family is exercised by the demo mission through `payloads[].faults.possible` for `demo_iod_payload`.

The admitted `commandability_rule_constrains_command` family is exercised by the demo mission through `commandability.rules[].command` for `payload_start_ground_rule`.

The admitted `autonomous_action_dispatches_command` family is exercised by the demo mission through `commandability.autonomous_actions[].dispatches.command` for `stop_payload_on_battery_low` and `stop_payload_on_battery_critical`.

The admitted `recovery_intent_reacts_to_fault` family is exercised by the demo mission through `commandability.recovery_intents[].fault` for `payload_battery_low_recovery` and `payload_battery_critical_recovery`.

The admitted `recovery_intent_reacts_to_event` family is not emitted by the demo mission because the demo recovery intents are fault-based.

---

## Boundary flags

The candidate manifest declares boundary flags equivalent to:

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

## Admitted relationship types

### autonomous_action_dispatches_command

This relationship states that an autonomous action dispatches an indexed command.

It is derived from:

```text
commandability.autonomous_actions[].dispatches.command
```

Endpoints:

```text
from: autonomous_actions.<id>
to: commands.<id>
```

It is emitted only when `commandability.autonomous_actions[].dispatches.command` resolves to an indexed command.

Conceptual record shape:

```json
{
  "relationship_id": "autonomous_actions:stop_payload_on_battery_low->autonomous_action_dispatches_command:commands:payload.stop_acquisition",
  "relationship_type": "autonomous_action_dispatches_command",
  "from": {
    "domain": "autonomous_actions",
    "id": "stop_payload_on_battery_low"
  },
  "to": {
    "domain": "commands",
    "id": "payload.stop_acquisition"
  },
  "derived_from": {
    "model_field": "commandability.autonomous_actions[].dispatches.command"
  }
}
```

This is a direct autonomous action contract reference.

It is not derived from action ID prefixes, command ID prefixes, trigger fields, source fields, expected events, expected effects, recovery intents or command targets.

It does not execute autonomous actions, dispatch commands, evaluate triggers, implement recovery behavior, authorize commands, implement security policy behavior, schedule runtime behavior, expose ground behavior, expose Studio API behavior or expose plugin API behavior.

### command_emits_event

This relationship states that a command emits an event.

It is derived from:

```text
commands[].emits
```

Endpoints:

```text
from: commands.<id>
to: events.<id>
```

This is a direct command contract reference.

It is not derived from command ID prefixes, event ID prefixes, command targets or expected effects.

### command_targets_subsystem

This relationship states that a command targets an indexed subsystem.

It is derived from:

```text
commands[].target
```

Endpoints:

```text
from: commands.<id>
to: subsystems.<id>
```

It is emitted only when `commands[].target` resolves to an indexed subsystem.

It is not derived from command ID prefixes, subsystem naming conventions or payload contract references.

### commandability_rule_constrains_command

This relationship states that a commandability rule constrains an indexed command.

It is derived from:

```text
commandability.rules[].command
```

Endpoints:

```text
from: commandability_rules.<id>
to: commands.<id>
```

It is emitted only when `commandability.rules[].command` resolves to an indexed command.

Conceptual record shape:

```json
{
  "relationship_id": "commandability_rules:payload_start_ground_rule->commandability_rule_constrains_command:commands:payload.start_acquisition",
  "relationship_type": "commandability_rule_constrains_command",
  "from": {
    "domain": "commandability_rules",
    "id": "payload_start_ground_rule"
  },
  "to": {
    "domain": "commands",
    "id": "payload.start_acquisition"
  },
  "derived_from": {
    "model_field": "commandability.rules[].command"
  }
}
```

This is a direct commandability contract reference.

It is not derived from command ID prefixes, rule ID prefixes, allowed modes, expected events, expected effects, source IDs or command targets.

It does not implement runtime commandability evaluation, command authorization, security policy evaluation, dispatch behavior, scheduler behavior, ground behavior, Studio API behavior or plugin API behavior.

### data_product_produced_by_payload

This relationship states that a data product is produced by an indexed payload.

It is derived from:

```text
data_products[].producer
```

Endpoints:

```text
from: data_products.<id>
to: payloads.<id>
```

It is emitted only when `data_products[].producer_type` is `payload` and `data_products[].producer` resolves to an indexed payload.

It is not derived from data product ID prefixes, payload naming conventions, storage policy or downlink policy.

### data_product_produced_by_subsystem

This relationship states that a data product is produced by an indexed subsystem.

It is derived from:

```text
data_products[].producer
```

Endpoints:

```text
from: data_products.<id>
to: subsystems.<id>
```

It is emitted only when `data_products[].producer_type` is `subsystem` and `data_products[].producer` resolves to an indexed subsystem.

Conceptual record shape:

```json
{
  "relationship_id": "data_products:critical_housekeeping_packet->data_product_produced_by_subsystem:subsystems:obdh",
  "relationship_type": "data_product_produced_by_subsystem",
  "from": {
    "domain": "data_products",
    "id": "critical_housekeeping_packet"
  },
  "to": {
    "domain": "subsystems",
    "id": "obdh"
  },
  "derived_from": {
    "model_field": "data_products[].producer"
  }
}
```

This is a direct data product contract reference.

It is not derived from data product ID prefixes, subsystem naming conventions, storage policy, downlink policy, packet membership or telemetry sources.

### downlink_flow_includes_data_product

This relationship states that a downlink flow includes an indexed data product as an eligible product.

It is derived from:

```text
downlink_flows[].eligible_data_products
```

Endpoints:

```text
from: downlink_flows.<id>
to: data_products.<id>
```

It is emitted only when a `downlink_flows[].eligible_data_products` entry resolves to an indexed data product.

It is not derived from data product ID prefixes, downlink flow naming conventions, storage policy, downlink policy, contact profiles, link profiles or contact windows.

### event_sourced_from_subsystem

This relationship states that an event is sourced from an indexed subsystem.

It is derived from:

```text
events[].source
```

Endpoints:

```text
from: events.<id>
to: subsystems.<id>
```

It is emitted only when `events[].source` resolves to an indexed subsystem.

It is not derived from event ID prefixes, subsystem naming conventions, command emissions, fault emissions or payload event declarations.

### fault_emits_event

This relationship states that a fault emits an event.

It is derived from:

```text
faults[].emits
```

Endpoints:

```text
from: faults.<id>
to: events.<id>
```

This is a direct fault contract reference.

It is not derived from fault ID prefixes, event ID prefixes, fault conditions, source fields or recovery actions.

### fault_sourced_from_subsystem

This relationship states that a fault is sourced from an indexed subsystem.

It is derived from:

```text
faults[].source
```

Endpoints:

```text
from: faults.<id>
to: subsystems.<id>
```

It is emitted only when `faults[].source` resolves to an indexed subsystem.

It is not derived from fault ID prefixes, subsystem naming conventions, fault emissions, fault conditions or recovery actions.

### packet_includes_telemetry

This relationship states that a packet includes a telemetry item.

It is derived from:

```text
packets[].telemetry
```

Endpoints:

```text
from: packets.<id>
to: telemetry.<id>
```

This is a direct model reference.

It is not derived from naming conventions.

### payload_accepts_command

This relationship states that a payload accepts a command.

It is derived from:

```text
payloads[].commands.accepted
```

Endpoints:

```text
from: payloads.<id>
to: commands.<id>
```

This is a direct payload contract reference.

It is not derived from command ID prefixes, payload naming conventions or command targets.

### payload_belongs_to_subsystem

This relationship states that a payload belongs to an indexed subsystem.

It is derived from:

```text
payloads[].subsystem
```

Endpoints:

```text
from: payloads.<id>
to: subsystems.<id>
```

It is emitted only when `payloads[].subsystem` resolves to an indexed subsystem.

It is not derived from payload ID prefixes, subsystem naming conventions or command targets.

### payload_generates_event

This relationship states that a payload generates an event.

It is derived from:

```text
payloads[].events.generated
```

Endpoints:

```text
from: payloads.<id>
to: events.<id>
```

This is a direct payload contract reference.

It is not derived from event ID prefixes, event sources or payload naming conventions.

### payload_may_raise_fault

This relationship states that a payload may raise an indexed fault.

It is derived from:

```text
payloads[].faults.possible
```

Endpoints:

```text
from: payloads.<id>
to: faults.<id>
```

It is emitted only when a `payloads[].faults.possible` entry resolves to an indexed fault.

Conceptual record shape:

```json
{
  "relationship_id": "payloads:demo_iod_payload->payload_may_raise_fault:faults:payload.command_timeout_fault",
  "relationship_type": "payload_may_raise_fault",
  "from": {
    "domain": "payloads",
    "id": "demo_iod_payload"
  },
  "to": {
    "domain": "faults",
    "id": "payload.command_timeout_fault"
  },
  "derived_from": {
    "model_field": "payloads[].faults.possible"
  }
}
```

This is a direct payload contract reference.

It is not derived from payload ID prefixes, fault ID prefixes, event sources, fault sources, telemetry sources, recovery auto-commands or payload lifecycle states.

It does not imply runtime fault monitoring behavior, fault handling behavior or recovery execution behavior.

### payload_produces_telemetry

This relationship states that a payload produces a telemetry item.

It is derived from:

```text
payloads[].telemetry.produced
```

Endpoints:

```text
from: payloads.<id>
to: telemetry.<id>
```

This is a direct payload contract reference.

It is not derived from telemetry ID prefixes or payload naming conventions.

### recovery_intent_reacts_to_event

This relationship states that a recovery intent reacts to an indexed event.

It is derived from:

```text
commandability.recovery_intents[].event
```

Endpoints:

```text
from: recovery_intents.<id>
to: events.<id>
```

It is emitted only when `commandability.recovery_intents[].event` resolves to an indexed event.

This is a direct recovery intent contract reference.

It is not derived from recovery intent ID prefixes, event ID prefixes, expected events, expected effects, target modes, command lists or autonomous actions.

It does not execute recovery behavior, dispatch commands, transition modes, evaluate recovery policies, evaluate security policy behavior, schedule runtime behavior, expose ground behavior, expose Studio API behavior or expose plugin API behavior.

### recovery_intent_reacts_to_fault

This relationship states that a recovery intent reacts to an indexed fault.

It is derived from:

```text
commandability.recovery_intents[].fault
```

Endpoints:

```text
from: recovery_intents.<id>
to: faults.<id>
```

It is emitted only when `commandability.recovery_intents[].fault` resolves to an indexed fault.

Conceptual record shape:

```json
{
  "relationship_id": "recovery_intents:payload_battery_low_recovery->recovery_intent_reacts_to_fault:faults:eps.battery_low_fault",
  "relationship_type": "recovery_intent_reacts_to_fault",
  "from": {
    "domain": "recovery_intents",
    "id": "payload_battery_low_recovery"
  },
  "to": {
    "domain": "faults",
    "id": "eps.battery_low_fault"
  },
  "derived_from": {
    "model_field": "commandability.recovery_intents[].fault"
  }
}
```

This is a direct recovery intent contract reference.

It is not derived from recovery intent ID prefixes, fault ID prefixes, expected events, expected effects, target modes, command lists or autonomous actions.

It does not execute recovery behavior, dispatch commands, transition modes, evaluate recovery policies, evaluate security policy behavior, schedule runtime behavior, expose ground behavior, expose Studio API behavior or expose plugin API behavior.

### telemetry_sourced_from_subsystem

This relationship states that a telemetry item is sourced from an indexed subsystem.

It is derived from:

```text
telemetry[].source
```

Endpoints:

```text
from: telemetry.<id>
to: subsystems.<id>
```

It is emitted only when `telemetry[].source` resolves to an indexed subsystem.

It is not derived from telemetry ID prefixes, subsystem naming conventions, packets or payload telemetry declarations.

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

## Candidate future relationship families

No additional relationship families are currently listed as near-term candidates for this candidate surface.

Additional families may be considered only when they can be derived from explicit loaded Mission Model fields without weakening the current boundary.

No relationship family is accepted until documented in an implementation PR.

`data_product_produced_by_subsystem`, `payload_may_raise_fault`, `commandability_rule_constrains_command`, `autonomous_action_dispatches_command`, `recovery_intent_reacts_to_fault` and `recovery_intent_reacts_to_event` are no longer listed as future candidates because they are now admitted relationship families.

---

## Non-goals

The current candidate manifest does not introduce:

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

The Relationship Manifest Surface is a candidate Core-owned read-only inspection surface.

It currently admits `autonomous_action_dispatches_command`, `command_emits_event`, `command_targets_subsystem`, `commandability_rule_constrains_command`, `data_product_produced_by_payload`, `data_product_produced_by_subsystem`, `downlink_flow_includes_data_product`, `event_sourced_from_subsystem`, `fault_emits_event`, `fault_sourced_from_subsystem`, `packet_includes_telemetry`, `payload_accepts_command`, `payload_belongs_to_subsystem`, `payload_generates_event`, `payload_may_raise_fault`, `payload_produces_telemetry`, `recovery_intent_reacts_to_event`, `recovery_intent_reacts_to_fault` and `telemetry_sourced_from_subsystem` relationships.

Additional relationship families may be added only if Core can derive them deterministically from explicit Mission Model semantics.
