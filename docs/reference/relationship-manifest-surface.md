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

At the current baseline, this surface emits eleven deliberately narrow relationship families:

```text
command_emits_event
command_targets_subsystem
data_product_produced_by_payload
event_sourced_from_subsystem
fault_emits_event
packet_includes_telemetry
payload_accepts_command
payload_belongs_to_subsystem
payload_generates_event
payload_produces_telemetry
telemetry_sourced_from_subsystem
```

These relationships are derived only from explicit loaded Mission Model fields:

```text
commands[].emits
commands[].target
data_products[].producer
events[].source
faults[].emits
packets[].telemetry
payloads[].commands.accepted
payloads[].subsystem
payloads[].events.generated
payloads[].telemetry.produced
telemetry[].source
```

No other relationship type is admitted yet.

---

## Current status

OrbitFabric Core exposes:

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

`relationship_manifest.json` is currently a candidate relationship surface.

It emits command-to-event emission records, command-to-subsystem target records, data-product-to-payload producer records, event-to-subsystem source records, fault-to-event emission records, packet-to-telemetry inclusion records, payload-to-command acceptance records, payload-to-subsystem membership records, payload-to-event generation records, payload-to-telemetry production records and telemetry-to-subsystem source records.

`entity_index.json` contains nodes, not edges.

The relationship manifest contains Core-owned edge records derived from explicit Mission Model references.

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

## Surface classification

The Relationship Manifest Surface candidate is:

```text
Core-derived
read-only
machine-readable
deterministic
versioned as 0.1-candidate
explicitly bounded
safe for downstream inspection
not the source of truth
```

The Mission Model remains the source of truth.

The relationship manifest is a derived inspection artifact.

---

## Current shape

The current candidate manifest contains:

```json
{
  "manifest_version": "0.1-candidate",
  "kind": "orbitfabric.relationship_manifest",
  "status": "candidate",
  "counts": {
    "total_relationships": 35,
    "relationship_types": {
      "command_emits_event": 4,
      "command_targets_subsystem": 4,
      "data_product_produced_by_payload": 1,
      "event_sourced_from_subsystem": 8,
      "fault_emits_event": 2,
      "packet_includes_telemetry": 5,
      "payload_accepts_command": 2,
      "payload_belongs_to_subsystem": 1,
      "payload_generates_event": 2,
      "payload_produces_telemetry": 1,
      "telemetry_sourced_from_subsystem": 5
    }
  },
  "relationship_types": [
    {
      "relationship_type": "command_emits_event",
      "display_name": "Command emits event",
      "from_domain": "commands",
      "to_domain": "events",
      "derived_from": {
        "model_field": "commands[].emits"
      },
      "relationship_count": 4
    },
    {
      "relationship_type": "command_targets_subsystem",
      "display_name": "Command targets subsystem",
      "from_domain": "commands",
      "to_domain": "subsystems",
      "derived_from": {
        "model_field": "commands[].target"
      },
      "relationship_count": 4
    },
    {
      "relationship_type": "data_product_produced_by_payload",
      "display_name": "Data product produced by payload",
      "from_domain": "data_products",
      "to_domain": "payloads",
      "derived_from": {
        "model_field": "data_products[].producer"
      },
      "relationship_count": 1
    },
    {
      "relationship_type": "event_sourced_from_subsystem",
      "display_name": "Event sourced from subsystem",
      "from_domain": "events",
      "to_domain": "subsystems",
      "derived_from": {
        "model_field": "events[].source"
      },
      "relationship_count": 8
    },
    {
      "relationship_type": "fault_emits_event",
      "display_name": "Fault emits event",
      "from_domain": "faults",
      "to_domain": "events",
      "derived_from": {
        "model_field": "faults[].emits"
      },
      "relationship_count": 2
    },
    {
      "relationship_type": "packet_includes_telemetry",
      "display_name": "Packet includes telemetry",
      "from_domain": "packets",
      "to_domain": "telemetry",
      "derived_from": {
        "model_field": "packets[].telemetry"
      },
      "relationship_count": 5
    },
    {
      "relationship_type": "payload_accepts_command",
      "display_name": "Payload accepts command",
      "from_domain": "payloads",
      "to_domain": "commands",
      "derived_from": {
        "model_field": "payloads[].commands.accepted"
      },
      "relationship_count": 2
    },
    {
      "relationship_type": "payload_belongs_to_subsystem",
      "display_name": "Payload belongs to subsystem",
      "from_domain": "payloads",
      "to_domain": "subsystems",
      "derived_from": {
        "model_field": "payloads[].subsystem"
      },
      "relationship_count": 1
    },
    {
      "relationship_type": "payload_generates_event",
      "display_name": "Payload generates event",
      "from_domain": "payloads",
      "to_domain": "events",
      "derived_from": {
        "model_field": "payloads[].events.generated"
      },
      "relationship_count": 2
    },
    {
      "relationship_type": "payload_produces_telemetry",
      "display_name": "Payload produces telemetry",
      "from_domain": "payloads",
      "to_domain": "telemetry",
      "derived_from": {
        "model_field": "payloads[].telemetry.produced"
      },
      "relationship_count": 1
    },
    {
      "relationship_type": "telemetry_sourced_from_subsystem",
      "display_name": "Telemetry sourced from subsystem",
      "from_domain": "telemetry",
      "to_domain": "subsystems",
      "derived_from": {
        "model_field": "telemetry[].source"
      },
      "relationship_count": 5
    }
  ],
  "relationships": []
}
```

The example count above reflects the demo mission.

The `relationships` list is populated deterministically from the loaded Mission Model.

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

## Admitted relationship types

### command_emits_event

This relationship states that a command emits an event.

It is derived from:

```text
commands[].emits
```

Relationship endpoints are:

```text
from: commands.<id>
to: events.<id>
```

Conceptual record shape:

```json
{
  "relationship_id": "commands:payload.start_acquisition->command_emits_event:events:payload.acquisition_started",
  "relationship_type": "command_emits_event",
  "from": {
    "domain": "commands",
    "id": "payload.start_acquisition"
  },
  "to": {
    "domain": "events",
    "id": "payload.acquisition_started"
  },
  "derived_from": {
    "model_field": "commands[].emits"
  }
}
```

This is a direct command contract reference.

It is not derived from command ID prefixes, event ID prefixes, command targets or expected effects.

### command_targets_subsystem

This relationship states that a command targets an indexed subsystem.

It is derived from:

```text
commands[].target
```

Relationship endpoints are:

```text
from: commands.<id>
to: subsystems.<id>
```

Conceptual record shape:

```json
{
  "relationship_id": "commands:eps.get_status->command_targets_subsystem:subsystems:eps",
  "relationship_type": "command_targets_subsystem",
  "from": {
    "domain": "commands",
    "id": "eps.get_status"
  },
  "to": {
    "domain": "subsystems",
    "id": "eps"
  },
  "derived_from": {
    "model_field": "commands[].target"
  }
}
```

This is a direct command contract reference.

It is emitted only when `commands[].target` resolves to an indexed subsystem.

It is not derived from command ID prefixes, subsystem naming conventions or payload contract references.

### data_product_produced_by_payload

This relationship states that a data product is produced by an indexed payload.

It is derived from:

```text
data_products[].producer
```

Relationship endpoints are:

```text
from: data_products.<id>
to: payloads.<id>
```

Conceptual record shape:

```json
{
  "relationship_id": "data_products:payload.radiation_histogram->data_product_produced_by_payload:payloads:demo_iod_payload",
  "relationship_type": "data_product_produced_by_payload",
  "from": {
    "domain": "data_products",
    "id": "payload.radiation_histogram"
  },
  "to": {
    "domain": "payloads",
    "id": "demo_iod_payload"
  },
  "derived_from": {
    "model_field": "data_products[].producer"
  }
}
```

This is a direct data product contract reference.

It is emitted only when `data_products[].producer_type` is `payload` and `data_products[].producer` resolves to an indexed payload.

It is not derived from data product ID prefixes, payload naming conventions, storage policy or downlink policy.

### event_sourced_from_subsystem

This relationship states that an event is sourced from an indexed subsystem.

It is derived from:

```text
events[].source
```

Relationship endpoints are:

```text
from: events.<id>
to: subsystems.<id>
```

Conceptual record shape:

```json
{
  "relationship_id": "events:eps.battery_low->event_sourced_from_subsystem:subsystems:eps",
  "relationship_type": "event_sourced_from_subsystem",
  "from": {
    "domain": "events",
    "id": "eps.battery_low"
  },
  "to": {
    "domain": "subsystems",
    "id": "eps"
  },
  "derived_from": {
    "model_field": "events[].source"
  }
}
```

This is a direct event contract reference.

It is emitted only when `events[].source` resolves to an indexed subsystem.

It is not derived from event ID prefixes, subsystem naming conventions, command emissions, fault emissions or payload event declarations.

### fault_emits_event

This relationship states that a fault emits an event.

It is derived from:

```text
faults[].emits
```

Relationship endpoints are:

```text
from: faults.<id>
to: events.<id>
```

Conceptual record shape:

```json
{
  "relationship_id": "faults:eps.battery_low_fault->fault_emits_event:events:eps.battery_low",
  "relationship_type": "fault_emits_event",
  "from": {
    "domain": "faults",
    "id": "eps.battery_low_fault"
  },
  "to": {
    "domain": "events",
    "id": "eps.battery_low"
  },
  "derived_from": {
    "model_field": "faults[].emits"
  }
}
```

This is a direct fault contract reference.

It is not derived from fault ID prefixes, event ID prefixes, fault conditions, source fields or recovery actions.

### packet_includes_telemetry

This relationship states that a packet includes a telemetry item.

It is derived from:

```text
packets[].telemetry
```

Relationship endpoints are:

```text
from: packets.<id>
to: telemetry.<id>
```

Conceptual record shape:

```json
{
  "relationship_id": "packets:hk_fast->packet_includes_telemetry:telemetry:obc.mode",
  "relationship_type": "packet_includes_telemetry",
  "from": {
    "domain": "packets",
    "id": "hk_fast"
  },
  "to": {
    "domain": "telemetry",
    "id": "obc.mode"
  },
  "derived_from": {
    "model_field": "packets[].telemetry"
  }
}
```

This is a direct model reference.

It is not derived from naming conventions.

### payload_accepts_command

This relationship states that a payload accepts a command.

It is derived from:

```text
payloads[].commands.accepted
```

Relationship endpoints are:

```text
from: payloads.<id>
to: commands.<id>
```

Conceptual record shape:

```json
{
  "relationship_id": "payloads:demo_iod_payload->payload_accepts_command:commands:payload.start_acquisition",
  "relationship_type": "payload_accepts_command",
  "from": {
    "domain": "payloads",
    "id": "demo_iod_payload"
  },
  "to": {
    "domain": "commands",
    "id": "payload.start_acquisition"
  },
  "derived_from": {
    "model_field": "payloads[].commands.accepted"
  }
}
```

This is a direct payload contract reference.

It is not derived from command ID prefixes, payload naming conventions or command targets.

### payload_belongs_to_subsystem

This relationship states that a payload belongs to an indexed subsystem.

It is derived from:

```text
payloads[].subsystem
```

Relationship endpoints are:

```text
from: payloads.<id>
to: subsystems.<id>
```

Conceptual record shape:

```json
{
  "relationship_id": "payloads:demo_iod_payload->payload_belongs_to_subsystem:subsystems:payload",
  "relationship_type": "payload_belongs_to_subsystem",
  "from": {
    "domain": "payloads",
    "id": "demo_iod_payload"
  },
  "to": {
    "domain": "subsystems",
    "id": "payload"
  },
  "derived_from": {
    "model_field": "payloads[].subsystem"
  }
}
```

This is a direct payload contract reference.

It is emitted only when `payloads[].subsystem` resolves to an indexed subsystem.

It is not derived from payload ID prefixes, subsystem naming conventions or command targets.

### payload_generates_event

This relationship states that a payload generates an event.

It is derived from:

```text
payloads[].events.generated
```

Relationship endpoints are:

```text
from: payloads.<id>
to: events.<id>
```

Conceptual record shape:

```json
{
  "relationship_id": "payloads:demo_iod_payload->payload_generates_event:events:payload.acquisition_started",
  "relationship_type": "payload_generates_event",
  "from": {
    "domain": "payloads",
    "id": "demo_iod_payload"
  },
  "to": {
    "domain": "events",
    "id": "payload.acquisition_started"
  },
  "derived_from": {
    "model_field": "payloads[].events.generated"
  }
}
```

This is a direct payload contract reference.

It is not derived from event ID prefixes, event sources or payload naming conventions.

### payload_produces_telemetry

This relationship states that a payload produces a telemetry item.

It is derived from:

```text
payloads[].telemetry.produced
```

Relationship endpoints are:

```text
from: payloads.<id>
to: telemetry.<id>
```

Conceptual record shape:

```json
{
  "relationship_id": "payloads:demo_iod_payload->payload_produces_telemetry:telemetry:payload.acquisition.active",
  "relationship_type": "payload_produces_telemetry",
  "from": {
    "domain": "payloads",
    "id": "demo_iod_payload"
  },
  "to": {
    "domain": "telemetry",
    "id": "payload.acquisition.active"
  },
  "derived_from": {
    "model_field": "payloads[].telemetry.produced"
  }
}
```

This is a direct payload contract reference.

It is not derived from telemetry ID prefixes or payload naming conventions.

### telemetry_sourced_from_subsystem

This relationship states that a telemetry item is sourced from an indexed subsystem.

It is derived from:

```text
telemetry[].source
```

Relationship endpoints are:

```text
from: telemetry.<id>
to: subsystems.<id>
```

Conceptual record shape:

```json
{
  "relationship_id": "telemetry:eps.battery.voltage->telemetry_sourced_from_subsystem:subsystems:eps",
  "relationship_type": "telemetry_sourced_from_subsystem",
  "from": {
    "domain": "telemetry",
    "id": "eps.battery.voltage"
  },
  "to": {
    "domain": "subsystems",
    "id": "eps"
  },
  "derived_from": {
    "model_field": "telemetry[].source"
  }
}
```

This is a direct telemetry contract reference.

It is emitted only when `telemetry[].source` resolves to an indexed subsystem.

It is not derived from telemetry ID prefixes, subsystem naming conventions, packets or payload telemetry declarations.

---

## Deterministic derivation rule

Every relationship record must be derived from an explicit field already present in the loaded Mission Model.

Currently admitted derivation sources:

```text
commands[].emits
commands[].target
data_products[].producer
events[].source
faults[].emits
packets[].telemetry
payloads[].commands.accepted
payloads[].subsystem
payloads[].events.generated
payloads[].telemetry.produced
telemetry[].source
```

Candidate future derivation sources may include explicit fields such as:

```text
command.expected_effects
fault.source
fault.recovery.auto_commands
payload.faults.possible
data_product.payload
contact_window.contact_profile
contact_window.link_profile
downlink_flow.contact_profile
downlink_flow.link_profile
downlink_flow.eligible_data_products
commandability_rule.command
commandability_rule.sources
commandability_rule.expected_events
commandability_rule.expected_effects
autonomous_action.trigger.event
autonomous_action.trigger.fault
autonomous_action.trigger.telemetry
autonomous_action.trigger.mode
autonomous_action.dispatches.command
autonomous_action.dispatches.source
recovery_intent.fault
recovery_intent.event
recovery_intent.target_mode
recovery_intent.commands
recovery_intent.expected_events
recovery_intent.expected_effects
```

Candidate fields are illustrative only.

Each new relationship type must be admitted one by one.

Each admitted relationship type must be documented and tested.

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

## Relationship manifest and entity index

The relationship manifest depends on the Entity Index Surface.

A relationship record must refer to entities already indexed by `entity_index.json`.

It must not create independent synthetic nodes.

The current manifest records its dependency on the entity index through:

```json
{
  "entity_index_kind": "orbitfabric.entity_index",
  "entity_index_version": "0.1"
}
```

If Core cannot resolve one endpoint to an indexed entity, the relationship type must either:

```text
not be emitted
be emitted only under an explicitly documented unresolved endpoint policy
or remain unsupported
```

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

A future implementation may consider additional explicit relationship families.

Candidate families include:

```text
payload may raise fault
data product produced by subsystem
downlink flow includes data product
commandability rule constrains command
autonomous action dispatches command
recovery intent reacts to fault or event
```

These are candidates only.

No relationship family is accepted until documented in an implementation PR.

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

It currently emits `command_emits_event`, `command_targets_subsystem`, `data_product_produced_by_payload`, `event_sourced_from_subsystem`, `fault_emits_event`, `packet_includes_telemetry`, `payload_accepts_command`, `payload_belongs_to_subsystem`, `payload_generates_event`, `payload_produces_telemetry` and `telemetry_sourced_from_subsystem` relationships.

Additional relationship families may be added only if Core can derive them deterministically from explicit Mission Model semantics.
