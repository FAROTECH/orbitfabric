# ADR-0014 - v0.9 Plugin and Relationship Surface Boundaries

Status: Accepted  
Date: 2026-05-15

---

## Context

OrbitFabric Core is currently at the `v0.8.2 - Entity Index Surface` baseline.

The Core already exposes two Core-owned read-only structured surfaces:

```text
model_summary.json
entity_index.json
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

The entity index deliberately provides nodes, not edges.

It does not expose relationship records, dependency graphs, source locations, YAML AST data, plugin APIs or Studio-specific APIs.

The next roadmap milestone is:

```text
v0.9 - Plugin and Extensibility Layer
```

At the same time, downstream tools such as OrbitFabric Studio require a future Core-owned relationship surface before they can safely implement relationship or graph navigation.

Studio must not infer relationships from raw YAML, naming conventions, source files, generated documentation, CLI output, React state or private assumptions.

Therefore v0.9 needs a boundary decision before implementation starts.

---

## Decision

v0.9 starts with boundary definition before code.

The first v0.9 work must classify Core surfaces and define the relationship between:

```text
public Core-owned surfaces
internal Core implementation details
candidate relationship surfaces
future plugin extension points
downstream consumers
```

The first v0.9 implementation step must not add runtime behavior, ground behavior, relationship export code or plugin execution.

The correct initial v0.9 posture is:

```text
plugin boundary + relationship manifest planning only
```

This keeps plugin extensibility and relationship semantics separate.

Plugins may become a controlled extension mechanism later in v0.9.

A relationship manifest may become a Core-owned surface later in v0.9 only if relationship records can be derived deterministically from explicit Mission Model fields already loaded by Core.

---

## Surface Classification

### Public Core-owned surfaces

Current public Core-owned structured surfaces include:

```text
model_summary.json
entity_index.json
```

They are:

```text
Core-derived
read-only
machine-readable
derived from the loaded Mission Model
safe for downstream consumption
not source of truth
```

The source of truth remains the Mission Model.

### Internal Core implementation details

The following are internal unless explicitly promoted to documented public surfaces:

```text
Python module layout
Pydantic model internals
helper functions
private builder functions
internal lint implementation details
internal generator implementation details
intermediate Python object identities
```

Downstream tools and plugins must not depend on these details as stable public API.

### Candidate Core-owned surfaces

The following are candidate surfaces, not current stable surfaces:

```text
relationship_manifest.json
plugin metadata manifest
plugin capability manifest
plugin-generated report manifest
```

Candidate surfaces require documentation, boundary flags and tests before they can be treated as implementation contracts.

### Experimental Core-owned surfaces

A future `relationship_manifest.json` must initially be experimental unless and until its semantics stabilize.

Experimental means:

```text
versioned
read-only
Core-derived
partial when necessary
not a v1.0 compatibility promise
safe to inspect
not safe to treat as a complete graph of the mission
```

### Forbidden surfaces for v0.9 boundary work

The following must not be introduced by the boundary PR:

```text
relationship graph
dependency graph
YAML AST export
source line tracking
source column tracking
Studio-specific API
runtime behavior surface
ground behavior surface
plugin execution surface
arbitrary plugin loader
remote plugin registry
plugin marketplace
```

---

## Relationship Manifest Boundary

A future `relationship_manifest.json` may be introduced only as a Core-owned derived surface.

It must reference entities already exposed by `entity_index.json`.

It must not create synthetic nodes that are absent from the entity index.

It must not create relationship records from:

```text
naming conventions
string similarity
source file names
YAML file ordering
generated documentation
human-oriented CLI output
Studio assumptions
React state
raw YAML scanning without loaded Mission Model semantics
```

Every relationship record must be derived from explicit fields in the loaded Mission Model.

Examples of explicit model fields that may support future relationship records include:

```text
telemetry.source
command.target
command.emits
fault.source
fault.emits
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
autonomous_action.dispatches.command
autonomous_action.dispatches.source
recovery_intent.fault
recovery_intent.event
recovery_intent.target_mode
recovery_intent.commands
```

This list is illustrative, not an implementation commitment.

Each future relationship type must be admitted explicitly, documented and tested.

No edge may be added merely because two IDs look related.

---

## Relationship Manifest Is Not a Graph

A relationship manifest is a list of Core-owned relationship records.

It is not automatically a graph engine.

It is not automatically a dependency graph.

It is not a visualization format.

It is not a Studio API.

A downstream tool may render a graph from a relationship manifest, but the engineering meaning of every edge must come from Core.

---

## Plugin Boundary

Plugins must extend OrbitFabric without silently redefining Core semantics.

A plugin must not bypass:

```text
Mission Model loading
structural validation
semantic linting
Core-owned structured surfaces
source of truth rules
```

A plugin must not reinterpret raw YAML privately when Core already owns the loaded Mission Model semantics.

A plugin must not override Core validation results silently.

A plugin must not mutate the Mission Model behind Core.

A plugin must not present plugin output as Core output.

A future plugin mechanism must distinguish:

```text
Core output
plugin output
plugin diagnostics
plugin-generated artifacts
plugin metadata
plugin compatibility status
```

Plugin execution requires an explicit trust and security design before arbitrary or untrusted plugin code is supported.

---

## Downstream Boundary

Downstream tools must consume Core-owned surfaces.

They must not infer contract semantics from:

```text
raw YAML
generated Markdown
generated runtime files
generated ground files
stdout or stderr text
file names
ID naming conventions
UI state
```

For downstream tools, the current safe chain is:

```text
Core model_summary.json -> domain navigation
Core entity_index.json  -> entity navigation
future Core relationship_manifest.json -> relationship navigation
```

Studio v0.4 relationship or graph navigation must remain blocked until the Core exposes a relationship surface.

---

## Non-goals

This ADR does not introduce:

```text
relationship_manifest.json implementation
relationship manifest CLI command
relationship graph
relationship exporter
relationship tests
plugin API implementation
plugin discovery
plugin loader
custom lint plugin support
custom generator plugin support
plugin metadata schema
runtime behavior
ground behavior
Studio-specific API
YAML AST export
source line or column tracking
```

Those require later PRs after this boundary is accepted.

---

## Consequences

The v0.9 milestone begins conservatively.

The first v0.9 PR is documentation and boundary work only.

The relationship manifest remains a candidate surface until it has a reference document, boundary flags, exporter tests and CLI tests.

Plugin extensibility remains a future controlled mechanism, not an immediate permission to execute arbitrary code.

Downstream relationship visualization remains gated by Core-owned relationship records.

This preserves the central OrbitFabric rule:

```text
Mission Model is the source of truth.
Core owns contract semantics.
Downstream tools consume, not infer.
Plugins extend, not redefine.
```

---

## Future PR Sequence

The expected v0.9 sequence is:

```text
PR 0 - boundary ADR and surface classification
PR 1 - relationship manifest reference skeleton, if approved
PR 2 - relationship export module skeleton, if approved
PR 3 - relationship manifest CLI, if approved
PR 4 - minimal explicit relationship types, if approved
PR N - plugin metadata and controlled extension points, if approved
```

Each step must remain independently reviewable.

No later step is implied by this ADR without a separate review.

---

## Acceptance Criteria

This ADR is satisfied when the project makes the following explicit:

```text
entity_index.json contains nodes, not edges
relationship_manifest.json is candidate and experimental until implemented and tested
relationship records must be Core-derived from explicit Mission Model fields
plugins must not redefine or bypass Core semantics
Studio must not infer relationships before Core exposes them
the first v0.9 work is boundary work, not implementation
```

---

## Final Position

OrbitFabric v0.9 must protect the Mission Data Contract before it extends it.

Boundary comes before plugin execution.

Relationship semantics come before relationship visualization.

Core remains authoritative.

Studio remains downstream.
