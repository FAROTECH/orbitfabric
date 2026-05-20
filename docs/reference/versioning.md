# Versioning Model

This page explains how OrbitFabric uses version numbers after `v1.0.0 - Stable Mission Data Contract`.

OrbitFabric distinguishes between:

- the OrbitFabric tool/package version;
- the Mission Model version declared by a mission;
- the version fields written into generated JSON reports;
- the generated runtime contract manifest context;
- the generated ground contract manifest context;
- the Core-owned structured surface format versions;
- the extensibility boundary documentation context;
- the v1.0 stable Mission Data Contract governance context.

These versions and contexts are related, but they are not the same thing.

---

## OrbitFabric tool/package version

The OrbitFabric tool/package version identifies the version of the Python package and CLI.

It is defined in:

```text
pyproject.toml
src/orbitfabric/__init__.py
```

It is shown by:

```bash
orbitfabric --version
```

Current example:

```text
orbitfabric 1.0.0
```

This version answers the question:

```text
Which version of the OrbitFabric tool generated, validated or executed this artifact?
```

Generated JSON reports and generated manifests record this tool context where applicable.

---

## Mission Model version

The Mission Model version is declared inside the mission YAML.

For the current multi-file Mission Model, it is stored in:

```text
spacecraft.yaml
```

Current demo example:

```yaml
spacecraft:
  id: demo-3u
  name: Demo 3U Spacecraft
  model_version: 0.1.0
```

This version answers the question:

```text
Which Mission Model contract version does this mission declare?
```

It is part of the mission data contract.

It is not the same as the OrbitFabric Python package version.

---

## Generated JSON report version

Generated JSON reports include the OrbitFabric tool/package version.

Current lint report example:

```json
{
  "tool": "orbitfabric-lint",
  "version": "1.0.0",
  "mission": "demo-3u",
  "model_version": "0.1.0"
}
```

The top-level `version` identifies the OrbitFabric tool that produced the report.

The `model_version` identifies the Mission Model version declared by the mission.

---

## Runtime contract manifest context

v0.7.0 introduced runtime-facing contract bindings.

The generated runtime manifest is written to:

```text
generated/runtime/cpp17/runtime_contract_manifest.json
```

It records the software-facing contract surface generated from the Mission Model.

It also records generation metadata such as:

```text
generation profile
contains_flight_runtime = false
generated_artifacts_are_disposable = true
```

The runtime manifest is generated from the current OrbitFabric tool and the declared Mission Model.

It remains a public preview generated manifest in v1.0.0.

It is not a separate stable schema version promise and is not flight runtime behavior.

---

## Ground contract manifest context

v0.8.0 introduced ground-facing contract exports.

The generated ground manifest is written to:

```text
generated/ground/generic/ground_contract_manifest.json
```

It records the generated ground-facing package, artifact paths and architectural boundary flags.

It also records generation metadata such as:

```text
generation profile
generated_artifacts_are_disposable = true
contains_ground_runtime = false
contains_operator_console = false
contains_transport = false
contains_database = false
claims_yamcs_compatibility = false
claims_openc3_compatibility = false
claims_xtce_compliance = false
```

The ground manifest is generated from the current OrbitFabric tool and the declared Mission Model.

It remains a public preview generated manifest in v1.0.0.

It is not a ground segment schema, mission database compatibility promise or tool-specific integration guarantee.

---

## Core-owned structured surface context

v1.0.0 stabilizes these Core-owned structured surfaces:

```text
model_summary.json
entity_index.json
relationship_manifest.json for admitted families
```

Their format version fields remain distinct from the OrbitFabric tool/package version:

| Surface | Format version field | Current value |
|---|---|---|
| `model_summary.json` | `summary_version` | `0.1` |
| `entity_index.json` | `index_version` | `0.1` |
| `relationship_manifest.json` | `manifest_version` | `0.1-candidate` |

These values identify the report format version for each surface.

They do not replace the OrbitFabric package version.

They do not replace the Mission Model version declared by the mission.

---

## Stability and compatibility context

v1.0.0 establishes the first stable narrow Mission Data Contract surface.

The stable surface includes:

```text
Mission Model documented contract semantics
Core structural validation
Core semantic lint diagnostic policy
scenario YAML evidence inputs
lint JSON report
simulation JSON report
model_summary.json
entity_index.json
relationship_manifest.json for admitted families
CLI command interface for documented workflows
release compatibility policy
extensibility boundary contract
```

The stability and compatibility references classify stable, preview, disposable, internal and out-of-scope surfaces.

They do not introduce schema migration tooling, JSON Schema publication, plugin execution, runtime behavior, ground behavior or tool-specific integrations.

---

## Extensibility boundary context

The Extensibility Boundary Contract is a stable v1.0 governance surface.

It records expectations such as:

```text
Core remains semantic owner
Mission Model remains source of truth
extensions consume Core-owned surfaces
extension-owned outputs remain distinguishable from Core-owned outputs
semantic override remains forbidden
execution remains out of scope
```

This boundary does not introduce a metadata schema, JSON shape, metadata manifest format, parser, loader, validator, registry, CLI command, plugin discovery, plugin loading or plugin execution.

---

## Why the versions differ

OrbitFabric tool/package version and Mission Model version intentionally differ.

For example:

```text
OrbitFabric tool/package version: 1.0.0
Mission Model version:           0.1.0
```

This is valid.

It means:

- the tool has reached the v1.0.0 stable Mission Data Contract release;
- the demo mission still declares the v0.1 Mission Model contract;
- generated artifacts record the relevant tool and model context;
- generated surface format versions remain independent from the tool/package version.

---

## Current v1.0.0 rule

For the current stable release:

| Version field | Meaning |
|---|---|
| `orbitfabric --version` | OrbitFabric CLI/package version, currently `1.0.0`. |
| JSON report top-level `version` | OrbitFabric tool version that produced the report, where used. |
| `spacecraft.model_version` | Mission Model contract version declared by the mission. |
| JSON report `model_version` | Mission Model version copied from mission YAML, where used. |
| Runtime manifest `generation.profile` | Runtime generation profile, currently `cpp17`. |
| Runtime manifest `contains_flight_runtime` | Explicit boundary flag, currently `false`. |
| Ground manifest `generation.profile` | Ground generation profile, currently `generic`. |
| Ground manifest `contains_ground_runtime` | Explicit boundary flag, currently `false`. |
| Ground manifest `claims_*` compatibility fields | Explicit tool-specific claim flags, currently `false`. |
| Model summary `summary_version` | Contract introspection report format version, currently `0.1`. |
| Model summary `kind` | Contract introspection report kind, currently `orbitfabric.model_summary`. |
| Entity index `index_version` | Entity index report format version, currently `0.1`. |
| Entity index `kind` | Entity index report kind, currently `orbitfabric.entity_index`. |
| Relationship manifest `manifest_version` | Relationship manifest report format version, currently `0.1-candidate`. |
| Relationship manifest `kind` | Relationship manifest report kind, currently `orbitfabric.relationship_manifest`. |
| Extensibility Boundary Contract | Stable documentation boundary for future extension-owned outputs, not an execution version. |
| v1.0 governance references | Stable documentation and review context for compatibility, migration notes and future evolution. |

---

## What not to assume

Do not assume that:

- the OrbitFabric package version and Mission Model version are always identical;
- a Mission Model version bump always requires a Python package major/minor bump;
- a Python package patch version always changes the Mission Model contract;
- generated artifacts are valid without checking both tool version and mission model version;
- generated runtime-facing bindings are flight protocol IDs or flight software ABI guarantees;
- generated ground-facing artifacts imply ground runtime behavior or tool-specific compatibility;
- model summary reports imply entity-level indexing, relationship graphs or plugin APIs;
- entity index reports imply relationship graphs, dependency graphs or plugin APIs;
- relationship manifest reports imply graph engines, runtime behavior, ground behavior, plugin APIs or Studio-specific APIs;
- stability and compatibility references imply schema migration tooling, JSON Schema publication or plugin execution;
- Extensibility Boundary Contract implies metadata schema, plugin discovery, plugin loading, plugin execution or a plugin runtime.

---

## Future direction

Future versions may introduce a more explicit schema versioning mechanism.

Possible future additions include:

- a dedicated Mission Model schema version field;
- a dedicated RuntimeContract schema version;
- a dedicated GroundContract schema version;
- a dedicated Entity Index schema version;
- a dedicated Relationship Manifest schema version;
- schema migration helpers;
- compatibility checks between tool version and Mission Model version;
- JSON Schema export for Mission Model validation;
- compatibility checks for generated artifact profiles;
- a separately reviewed metadata format for future extension-owned outputs.

These are not part of the v1.0.0 stable release boundary.
