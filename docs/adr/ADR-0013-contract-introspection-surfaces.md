# ADR-0013 - Contract Introspection Surfaces

Status: Proposed  
Date: 2026-05-14

---

## Context

OrbitFabric Core is the authoritative implementation of the Mission Data Contract.

The Core owns:

```text
Mission Model loading
structural validation
semantic linting
scenario evidence
generated documentation
runtime-facing contract bindings
ground-facing integration artifacts
contract meaning
```

Downstream tools, including visual workbenches, should not reconstruct Mission Model semantics by independently parsing YAML files, generated artifacts or human-oriented command output.

The repository already exposes several machine-readable outputs:

```text
lint JSON reports
simulation JSON reports
runtime contract manifest
ground contract manifest
ground JSON dictionaries
```

These outputs are useful, but they are vertical surfaces. They do not answer the more basic downstream questions:

```text
What contract domains are present in this mission?
What contract entities are defined in this mission?
What relationships are explicit in the Mission Data Contract?
```

Before plugin extensibility is introduced, the Core must expose stable read-only contract surfaces that tools and plugins can consume without bypassing the Core.

---

## Decision

OrbitFabric will introduce Core-owned, read-only contract introspection surfaces before the Plugin and Extensibility Layer.

The roadmap sequence is:

```text
v0.8.1 - Contract Introspection Surface
v0.8.2 - Entity Index Surface
v0.9   - Plugin and Extensibility Layer
```

v0.8.1 will focus on a model summary surface that answers:

```text
What contract domains are present in this mission?
```

v0.8.2 will focus on an entity index surface that answers:

```text
What contract entities are defined in this mission?
```

v0.9 may introduce relationship manifests and plugin-safe extension boundaries only after the model summary and entity index surfaces are defined.

---

## Boundary

Contract introspection surfaces are not:

```text
plugins
Studio-specific APIs
YAML source maps
relationship graphs
generated artifact explorers
runtime behavior
ground behavior
new Mission Model semantics
```

They are Core-derived reports.

They must be deterministic, machine-readable and derived from the loaded Mission Model and canonical Core knowledge.

They must not depend on downstream tool assumptions.

---

## Consequences

Downstream tools should consume Core-generated structured surfaces instead of inferring semantics from files.

The Core must distinguish clearly between:

```text
source Mission Model files
Core-derived reports
generated artifacts
runtime-facing bindings
ground-facing exports
future plugin extension points
```

The v0.8.1 model summary should not expose entity lists or relationships.

The v0.8.2 entity index should not expose relationship graphs.

The v0.9 relationship manifest should be introduced only if relationships can be derived without fragile heuristics.

---

## Non-goals

This ADR does not introduce:

```text
model_summary.json implementation
entity_index.json implementation
relationship_manifest.json implementation
source line or column tracking
plugin API
plugin discovery
custom lint rule plugins
custom generator plugins
Studio UI behavior
```

Those belong to later implementation PRs.

---

## Final position

OrbitFabric Core remains authoritative.

The Mission Model remains the source of truth.

Generated artifacts are disposable.

Downstream tools consume Core surfaces.

They do not infer contract semantics privately.
