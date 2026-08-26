# Projection Profile Integration Schema Publication

Status: Architecture candidate — Phase B.2 supporting contract  
Applies to: Projection Profile Contract `0.1-candidate`  
Design issue: #231

---

## 1. Purpose

The generic Projection Profile envelope intentionally leaves ecosystem-specific semantics inside:

```text
settings
bindings[].config
```

This document defines how an Integration Adapter/package exposes the machine-readable schema required to validate and edit those fields without moving target-specific semantics into OrbitFabric Core or OrbitFabric Studio.

The goal is one schema authority usable by:

```text
adapter CLI validation
CI validation
Studio visual editing
human-facing documentation generation
```

---

## 2. Schema dialect

The v0 integration-specific Profile schema uses:

```text
JSON Schema Draft 2020-12
```

The root schema declares:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema"
}
```

Projection Profile YAML is validated against the JSON-compatible instance data obtained after YAML parsing.

No YAML-specific custom validation semantics are introduced by the generic contract.

---

## 3. Schema ownership

The schema is **integration-owned**.

```text
OrbitFabric Core governance
    defines the generic Profile envelope

Integration Adapter/package
    publishes the detailed schema for its integration.id + schema_version

Studio / CLI / CI
    consume that schema
```

Core must not embed target-specific Profile keys in its own Mission Data Contract schemas.

Studio must not maintain a second hard-coded copy of target-specific Profile rules.

---

## 4. Schema identity

A schema publication is identified by the same compatibility pair authored in the Profile:

```text
integration.id
integration.schema_version
```

Example:

```yaml
integration:
  id: orbitfabric-openobsw-opensvf
  schema_version: 0.1-candidate
```

The adapter package must resolve exactly one Profile schema for each supported pair.

The adapter software/package version is not a substitute for schema compatibility.

---

## 5. No remote schema URL in the Profile

The v0 Profile envelope does not contain a schema URL.

It must not require network access to validate an authored Profile.

Resolution is:

```text
Profile integration.id + schema_version
        ↓
installed Integration Adapter/package
        ↓
locally published schema
```

Reasons:

```text
offline engineering workflows
reproducible CI
no mutable remote dependency
no URL becoming semantic identity
no Studio network requirement
```

An integration package may document a canonical public schema location, but the runtime validation contract uses the locally installed schema corresponding to the declared identity/version.

---

## 6. Published schema scope

The preferred v0 publication is a schema for the **complete Profile document**, not isolated schemas for only `settings` and `config`.

This allows one validation operation to enforce:

```text
generic envelope shape
integration.id const value
supported integration.schema_version value
settings structure
binding config structure
integration-specific conditional rules expressible in JSON Schema
```

The integration-owned full-document schema may reference a generic OrbitFabric Profile-envelope schema where useful, but semantic ownership remains unchanged:

```text
generic envelope constraints -> OrbitFabric governance
integration-specific constraints -> integration package
```

An implementation must not fork/change generic envelope meaning through its integration schema.

---

## 7. Required schema metadata

The published schema should provide at least:

```text
$schema
$id
title
description
type
```

Its `$id` must be stable for the schema family/version and must not depend on a local filesystem path.

A recommended conceptual form is:

```text
https://orbitfabric.dev/schemas/integrations/<integration-id>/projection-profile/<schema-version>
```

The exact public URI namespace is a publication/detail decision and is not used as the Profile's compatibility key.

The compatibility key remains:

```text
integration.id + integration.schema_version
```

---

## 8. Offline resolution and bundled references

All schema references required for validation must be satisfiable from the installed integration package without network access.

An integration may use JSON Schema `$ref`, but referenced schemas must be bundled or otherwise locally resolvable by the adapter/schema provider.

A remote-only `$ref` is not sufficient for the v0 contract.

This requirement applies equally to:

```text
CLI validation
CI validation
Studio editing
```

---

## 9. Schema provider capability

An Integration Adapter/package that supports Projection Profiles exposes a conceptual capability:

```text
profile_schema
```

with an operation equivalent to:

```text
get_profile_schema(integration_id, schema_version)
    -> JSON Schema document
```

This is an architectural capability, not a Python function signature.

The concrete transport may later be:

```text
adapter CLI command
adapter manifest resource
library API
Studio integration-provider call
```

The generic contract must not require a particular programming language or in-process Core API.

---

## 10. Studio consumption rule

Studio uses the adapter-provided schema for target-specific editor behavior.

Conceptually:

```text
Profile file
    ↓ generic envelope parsing
integration.id + schema_version
    ↓
Integration provider
    ↓
JSON Schema
    ↓
Studio form/editor hints + validation
```

Studio may add presentation metadata locally, but it must not change validation semantics.

If Studio cannot obtain a compatible schema, it may still show the Profile as text/read-only metadata, but must not claim target-specific validation or offer semantic target-specific editing controls.

---

## 11. Validation layering

Validation remains layered:

```text
1. YAML parse / JSON-compatible data model
2. generic Projection Profile envelope validation
3. integration-specific JSON Schema validation
4. Core source-reference resolution against Entity Index
5. projection-specific semantic validation by adapter
```

JSON Schema is not expected to perform all projection semantics.

Examples that remain adapter semantic validation include:

```text
numeric allocation collision across resolved bindings
source-domain compatibility with a target mapping
cross-binding allocation rules
external-tool compatibility rules
whether a target encoding faithfully represents Core semantics
```

Schema validation and projection validation must remain distinguishable in diagnostics.

---

## 12. Diagnostic ownership

Schema-validation findings are integration/Profile diagnostics, not Core lint findings.

A diagnostic should identify at least conceptually:

```text
owner = integration
phase = profile_schema
integration.id
integration.schema_version
instance path
message
```

Adapter semantic projection diagnostics use a different phase such as:

```text
phase = projection_validation
```

Studio may aggregate these visually but must preserve their authority/source.

---

## 13. Schema evolution

`integration.schema_version` is the compatibility identifier for integration-specific Profile configuration.

A schema change is compatibility-sensitive when it:

```text
removes an accepted authored field
renames an accepted authored field
changes a field's target meaning
changes requiredness incompatibly
narrows accepted values incompatibly
changes how existing Profile config is interpreted
```

Additive optional target-specific fields may remain within a compatible schema version only when the integration package explicitly documents that consumers of that version are required to tolerate them.

When compatibility cannot be preserved, the integration must publish a new `integration.schema_version`.

No automatic Profile migration mechanism is defined in v0.

---

## 14. Schema and adapter package compatibility

An adapter declares which integration schema versions it supports.

Conceptually:

```text
adapter version A
    supports schema versions X, Y

adapter version B
    supports schema versions Y, Z
```

A Profile is rejected for projection when its declared schema version is unsupported.

The adapter must not silently reinterpret the Profile using a different schema version.

---

## 15. Provenance into Integration Result

The later Integration Result should record:

```text
integration.id
integration.schema_version
adapter identity/version
exact consumed Profile SHA-256
schema identity/version
optionally exact schema content SHA-256
```

Recording the schema digest is useful when reproducibility requires proving the exact validation/projection schema bytes used.

The Profile itself does not need to embed this provenance.

---

## 16. Non-goals

This supporting contract does not define:

```text
Core Mission Model JSON Schema publication
remote schema registry service
Profile migration tooling
Profile inheritance/composition
Studio widget/layout schema
adapter RPC protocol
plugin loading inside Core
OpenOBSW/OpenSVF-specific Profile fields
```

---

## 17. Final position

The v0 schema-publication boundary is:

```text
Projection Profile stays YAML and version-control friendly.

Its loaded data model is JSON-compatible.

Integration-specific Profile semantics are published as JSON Schema Draft 2020-12.

The schema is distributed with the Integration Adapter/package and is fully usable offline.

Profile compatibility is keyed by integration.id + integration.schema_version, not by a remote URL or adapter package version alone.

Studio, CLI and CI consume the same adapter-owned schema rather than duplicating target-specific rules.

Projection-specific semantic checks remain adapter-owned beyond JSON Schema validation.
```
