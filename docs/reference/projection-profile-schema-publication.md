# Projection Profile Integration Schema Publication

Status: Candidate supporting contract, design-frozen and reference-proven  
Applies to: Projection Profile Contract `0.1-candidate`  
Design issue: #231

## 1. Purpose

The generic Projection Profile envelope intentionally leaves ecosystem-specific semantics inside:

```text
settings
bindings[].config
```

This document defines how an Integration Package publishes the machine-readable schema required to validate and assist editing of those fields without moving target-specific semantics into OrbitFabric Core or OrbitFabric Studio.

The goal is one schema authority reusable by:

```text
adapter validation
CI validation
Studio-assisted editing
human-facing schema documentation
```

The publication model is design-frozen and has been exercised by the OpenOBSW/OpenSVF reference Integration Package. It remains part of the `0.1-candidate` extension-contract family.

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

The generic contract introduces no YAML-specific custom validation semantics.

## 3. Schema ownership

The schema is integration-owned.

```text
OrbitFabric governance
    defines the generic Projection Profile envelope

Integration Package
    publishes the detailed schema for integration.id + schema_version

Studio / CLI / CI
    consume that package-published schema
```

Core must not embed target-specific Profile keys in Mission Data Contract schemas.

Studio must not maintain a second hard-coded copy of target-specific Profile rules.

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

The selected Integration Package must resolve exactly one compatible Profile schema for the requested pair.

Adapter/package version is separate provenance and is not a substitute for schema compatibility.

## 5. Package publication

The Integration Package Manifest publishes supported Profile schemas statically through `profile_schemas[]`.

Representative record:

```json
{
  "schema_version": "0.1-candidate",
  "format": "json-schema-2020-12",
  "path": "schemas/profile-0.1.schema.json",
  "sha256": "..."
}
```

Rules:

```text
schema_version values are unique within the package
format = json-schema-2020-12 for v0
path is relative to the package manifest directory
sha256 fingerprints the exact primary schema bytes
```

Lookup remains anchored to:

```text
Profile integration.id
+
Profile integration.schema_version
+
selected Integration Package
```

A Profile does not carry a remote schema URL as its compatibility authority.

## 6. Offline resolution

Profile validation must not require network access.

All schema resources required for validation must be available inside the trusted package root or another explicitly package-owned local resource set.

The v0 contract performs no remote `$ref` retrieval.

Reasons include:

```text
offline engineering workflows
reproducible CI
no mutable remote dependency
no URL becoming semantic identity
no Studio network requirement
```

Schema resolution rejects escape attempts such as:

```text
absolute path substitution
.. traversal
symlink/equivalent resolution outside the trusted package root
```

The declared SHA-256 of the primary schema resource is validated before the schema is accepted as the package-published resource.

## 7. Full-document schema scope

The preferred v0 publication is a schema for the complete Projection Profile document, not isolated schemas for only `settings` or one binding `config` object.

This allows one structural validation operation to enforce:

```text
generic envelope shape
integration.id const value
supported integration.schema_version value
settings structure
binding config structure
integration-specific conditional rules expressible in JSON Schema
```

An integration-owned schema may reuse a generic envelope schema where useful, but it must not fork or redefine generic Profile semantics.

## 8. Recommended schema metadata

A published schema should provide at least:

```text
$schema
$id
title
description
type
```

`$id` should remain stable for the schema family/version and must not depend on a local filesystem path.

A public URI may be documented for identification or publication purposes, but it is not the runtime compatibility key and does not create a network dependency.

Compatibility remains:

```text
integration.id + integration.schema_version
```

## 9. Shared structural validation

Ordinary JSON Schema validation does not require starting the adapter process.

A generic consumer may:

```text
read integration_package.json
resolve the matching profile_schemas[] record
validate the schema digest and local containment
load the Profile YAML into a JSON-compatible data model
validate the complete Profile document
```

The same package-published schema should be used by CLI, CI and Studio.

This avoids a Studio-specific or CI-specific fork of target rules.

## 10. Validation layering

Validation remains layered:

```text
1. YAML parse / JSON-compatible data model
2. generic Projection Profile envelope validation
3. integration-specific JSON Schema validation
4. Core source-reference resolution against the Core Integration Input Set / Entity Index
5. projection-specific semantic validation by the adapter
```

JSON Schema is not expected to encode every target rule.

Adapter-owned semantic validation still covers concepts such as:

```text
numeric allocation collisions
source-domain compatibility with target mappings
cross-binding allocation rules
external-tool compatibility
whether a target encoding faithfully represents Core semantics
```

Schema validation and projection validation must remain distinguishable in diagnostics.

## 11. Diagnostic ownership

Schema-validation findings are integration/Profile diagnostics, not Core lint findings.

A schema diagnostic should identify conceptually:

```text
owner = integration
phase = profile_schema
integration.id
integration.schema_version
instance path
message
```

Projection semantic diagnostics use a separate phase such as:

```text
phase = projection_validation
```

Studio may aggregate them visually but must preserve their producer and authority.

## 12. Studio consumption rule

Studio uses the package-published schema for target-specific Profile editor assistance.

Conceptually:

```text
Profile file
    -> generic envelope parsing
    -> integration.id + schema_version
    -> selected Integration Package
    -> package-published JSON Schema
    -> form/editor hints + structural validation
```

Studio may add presentation metadata, but it must not alter validation semantics.

If Studio cannot obtain a compatible trusted schema, it may display the Profile as text/read-only metadata but must not claim target-specific validation or semantic editing support.

## 13. Schema evolution

`integration.schema_version` is the compatibility identifier for target-specific Profile configuration.

A schema change is compatibility-sensitive when it:

```text
removes an accepted authored field
renames an accepted authored field
changes a field's target meaning
changes requiredness incompatibly
narrows accepted values incompatibly
changes how existing Profile config is interpreted
```

Additive optional target-specific fields may remain within a compatible schema version only when that schema version explicitly permits compatible additive evolution.

When compatibility cannot be preserved, the integration publishes a new `integration.schema_version`.

No automatic Profile migration mechanism is defined in v0.

## 14. Adapter/package compatibility

An Integration Package declares exactly which integration schema versions it supports.

Conceptually:

```text
adapter version A
    supports schema versions X, Y

adapter version B
    supports schema versions Y, Z
```

A Profile is rejected for projection when its declared schema version is unsupported.

The adapter must not silently reinterpret the Profile using a different schema version.

## 15. Provenance into Integration Result

The Integration Result records the relevant resolved provenance, including:

```text
integration.id
integration.schema_version
adapter identity/version
exact consumed Profile SHA-256
```

The package manifest separately provides the selected schema identity and exact schema digest.

A Result or higher-level evidence bundle may preserve the schema digest as additional provenance when proving the exact validation/projection schema bytes matters.

The Profile itself does not need to embed that execution provenance.

## 16. Reference proof

The OpenOBSW/OpenSVF reference Integration Package exercises this boundary with:

```text
a package-local Draft 2020-12 Profile schema
explicit schema_version
exact schema SHA-256
local/offline resolution
one schema authority shared by adapter validation and Studio/CI consumers
```

This proves the generic publication shape without making OpenOBSW/OpenSVF/PUS/SRDB/YAMCS fields generic OrbitFabric semantics.

## 17. Non-goals

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

## 18. Final position

The v0 schema-publication boundary is:

```text
Projection Profile remains YAML and version-control friendly.

Its loaded data model is JSON-compatible.

Integration-specific Profile semantics are published as JSON Schema Draft 2020-12.

The schema is distributed with the Integration Package and is fully usable offline.

Profile compatibility is keyed by integration.id + integration.schema_version, not by a remote URL or adapter package version alone.

Studio, CLI and CI consume the same package-owned schema rather than duplicating target-specific rules.

Projection-specific semantic checks remain adapter-owned beyond JSON Schema validation.
```

The supporting contract remains `0.1-candidate`, design-frozen and reference-proven.
