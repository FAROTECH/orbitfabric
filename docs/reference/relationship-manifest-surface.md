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

At the current baseline, this surface exists only as a candidate skeleton.

It can be exported by the CLI, but it intentionally emits no relationship records yet.

Relationship types must be admitted one by one in later PRs, only when they can be derived deterministically from explicit loaded Mission Model fields.

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

`relationship_manifest.json` is currently a candidate relationship surface skeleton.

It answers no relationship question yet because no relationship types have been admitted.

`entity_index.json` contains nodes, not edges.

The current candidate relationship manifest contains an empty edge set.

---

## CLI export

The candidate skeleton can be exported with:

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

The command exports a candidate skeleton only.

It does not infer relationships.

It does not generate a graph.

It does not expose plugin behavior.

---

## Surface classification

The Relationship Manifest Surface candidate skeleton is:

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

## Current skeleton shape

The current candidate skeleton contains:

```json
{
  "manifest_version": "0.1-candidate",
  "kind": "orbitfabric.relationship_manifest",
  "status": "candidate",
  "counts": {
    "total_relationships": 0,
    "relationship_types": {}
  },
  "relationship_types": [],
  "relationships": []
}
```

This is an intentionally empty relationship surface.

The empty relationship set means:

```text
relationship export envelope exists
relationship semantics are not admitted yet
no relationship records are emitted yet
no graph is implied
```

---

## Boundary flags

The candidate skeleton declares boundary flags equivalent to:

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

They do not mean that relationship semantics are complete.

---

## Relationship records

A future relationship record must connect two indexed entities.

The conceptual shape is:

```json
{
  "relationship_id": "command:payload.capture_image->target:payload.camera",
  "relationship_type": "targets",
  "from": {
    "domain": "commands",
    "id": "payload.capture_image"
  },
  "to": {
    "domain": "payloads",
    "id": "payload.camera"
  },
  "derived_from": {
    "model_field": "commands[].target"
  }
}
```

This example is illustrative only.

It is not a committed schema.

The current candidate skeleton emits:

```json
[]
```

for `relationships`.

---

## Deterministic derivation rule

Every future relationship record must be derived from an explicit field already present in the loaded Mission Model.

Allowed derivation sources may include explicit fields such as:

```text
telemetry.source
command.target
command.emits
command.expected_effects
event.source
fault.source
fault.emits
fault.recovery.auto_commands
packet.telemetry
payload.subsystem
payload.telemetry.produced
payload.commands.accepted
payload.events.generated
payload.faults.possible
data_product.producer
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

This list is illustrative.

A future implementation must admit relationship types one by one.

Each admitted relationship type must be documented and tested.

---

## Forbidden derivation sources

A future relationship manifest must not derive relationship records from:

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

The relationship manifest must depend on the Entity Index Surface.

A relationship record must refer to entities already indexed by `entity_index.json`.

It must not create independent synthetic nodes.

The current skeleton records its dependency on the entity index through:

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

The first relationship implementation should prefer not emitting unsupported or unresolved relationships.

---

## Relationship manifest and plugins

A relationship manifest is not a plugin API.

Plugins must not silently inject relationship records into a Core-owned relationship manifest.

If future plugins are allowed to contribute diagnostics or reports, their outputs must be clearly separated from Core output.

A future plugin-contributed relationship-like artifact must be marked as plugin output, not Core relationship data.

---

## Relationship manifest and Studio

OrbitFabric Studio must not infer relationships before Core exposes them.

The intended downstream chain is:

```text
model_summary.json -> domain navigation
entity_index.json -> entity navigation
relationship_manifest.json -> relationship navigation
```

At the current baseline, Studio may inspect the candidate skeleton but must still treat relationship navigation as unavailable because the relationship set is empty and no relationship type has been admitted.

Studio must not use the existence of the candidate skeleton as permission to infer graph edges privately.

---

## Candidate minimal relationship families

A future first implementation may consider a small subset of explicit relationship families.

Candidate families include:

```text
command targets subsystem or payload
command emits event
fault emits event
packet includes telemetry item
payload produces telemetry
payload accepts command
payload generates event
payload may raise fault
data product produced by payload or subsystem
downlink flow includes data product
commandability rule constrains command
autonomous action dispatches command
recovery intent reacts to fault or event
```

These are candidates only.

No relationship family is accepted until documented in an implementation PR.

---

## Non-goals

The current candidate skeleton does not introduce:

```text
relationship records
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

A future implementation PR that admits actual relationship records must satisfy all of the following:

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

The current implementation exposes only the deterministic candidate envelope.

It may begin to carry relationship records in v0.9 only if Core can derive them deterministically from explicit Mission Model semantics.
