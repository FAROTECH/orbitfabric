# Contract Introspection Surface

OrbitFabric v0.8.1 introduced the first Core-owned contract introspection surface.

The initial surface is:

```text
model_summary.json
```

It answers one deliberately narrow question:

```text
What contract domains are present in this mission?
```

OrbitFabric v0.8.2 adds a related but separate entity-level surface:

```text
entity_index.json
```

It answers:

```text
What contract entities are defined in this mission?
```

---

## Purpose

The Contract Introspection Surface gives downstream tools a stable, machine-readable way to inspect the loaded Mission Model at domain level.

Downstream tools should not reconstruct Mission Model semantics by independently parsing:

```text
raw YAML files
generated documentation
generated runtime artifacts
generated ground artifacts
human-oriented CLI output
```

The Core loads and validates the Mission Model.

The Core owns the meaning of Mission Model domains.

The Core exports the introspection surface.

---

## CLI

Generate a model summary report with:

```bash
orbitfabric export model-summary examples/demo-3u/mission/ \
  --json generated/reports/model_summary.json
```

Default output:

```text
generated/reports/model_summary.json
```

---

## Output kind

The generated JSON report uses:

```json
{
  "kind": "orbitfabric.model_summary",
  "summary_version": "0.1"
}
```

---

## Top-level structure

The report contains:

```text
summary_version
kind
orbitfabric_version
mission
source
boundaries
counts
domains
```

### mission

The `mission` section includes:

```text
id
name
model_version
```

### source

The `source` section includes:

```text
mission_dir
```

This path identifies the Mission Model directory used to produce the report.

### boundaries

The `boundaries` section explicitly declares what this report is and is not.

Current boundary flags include:

```text
source_of_truth: mission_model
core_derived_report: true
contains_entity_index: false
contains_relationship_manifest: false
contains_plugin_api: false
contains_runtime_behavior: false
contains_ground_behavior: false
```

### counts

The `counts` section contains domain-level counts derived from the loaded Mission Model.

### domains

The `domains` section contains one record per contract domain.

Each domain record includes:

```text
id
display_name
source_file
required
present
count
count_provenance
```

---

## Domain scope

The v0.8.1 model summary includes Core-owned contract domains such as:

```text
spacecraft
subsystems
modes
mode_transitions
telemetry
commands
events
faults
packets
policies
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

The exact content is derived from the loaded Mission Model and the canonical Mission Model file registry.

---

## Boundary

The Contract Introspection Surface is not:

```text
a generated runtime binding
a generated ground artifact
an entity index
a relationship graph
a source map
a YAML AST export
a plugin API
a Studio-specific API
```

It does not expose entity-level records.

It does not expose relationship records.

It does not expose line or column locations.

It does not introduce new Mission Model semantics.

---

## Relationship to the Entity Index Surface

`model_summary.json` and `entity_index.json` are separate Core-owned surfaces.

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

The entity index is documented separately in:

```text
Reference -> Entity Index Surface
```

Neither surface is a relationship graph.

Neither surface is a plugin API.

Neither surface is a Studio-specific API.

---

## Relationship to v0.9

The planned sequence is:

```text
v0.8.1 - Contract Introspection Surface
v0.8.2 - Entity Index Surface
v0.9   - Plugin and Extensibility Layer
```

v0.9 should introduce controlled extension points only after Core-owned introspection and entity surfaces exist.

---

## Final position

`model_summary.json` is a Core-derived report.

It is deterministic, inspectable and machine-readable.

It exists so downstream tools consume OrbitFabric Core surfaces instead of inferring contract semantics privately.
