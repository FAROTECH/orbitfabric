# Versioning Model

This page explains how OrbitFabric uses version numbers.

OrbitFabric currently distinguishes between:

- the OrbitFabric tool/package version;
- the Mission Model version declared by a mission;
- the version field written into generated JSON reports;
- the generated runtime contract manifest context;
- the generated ground contract manifest context;
- the generated contract introspection report context;
- the generated entity index report context;
- the generated relationship manifest report context.

These versions are related, but they are not the same thing.

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
orbitfabric 0.9.0
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
  "version": "0.9.0",
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

It is not a separate schema version promise for v1.0 compatibility.

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

It is not a ground segment schema, mission database compatibility promise or v1.0 compatibility guarantee.

---

## Contract introspection report context

v0.8.1 introduced the first Core-owned Contract Introspection Surface.

The generated model summary report is written to:

```text
generated/reports/model_summary.json
```

It records the domain-level contract summary derived from the loaded Mission Model.

It includes:

```text
summary_version
kind = orbitfabric.model_summary
OrbitFabric tool version
mission identity
source mission directory
boundary flags
domain counts
domain records
```

The model summary report is generated from the current OrbitFabric tool and the declared Mission Model.

It is not an entity index, relationship manifest, plugin API or Studio-specific API.

---

## Entity index report context

v0.8.2 introduced the first Core-owned Entity Index Surface.

The generated entity index report is written to:

```text
generated/reports/entity_index.json
```

It records the entity-level contract index derived from the loaded Mission Model.

It includes:

```text
index_version
kind = orbitfabric.entity_index
OrbitFabric tool version
mission identity
source mission directory
boundary flags
domain summaries
entity records
```

The entity index report is generated from the current OrbitFabric tool and the declared Mission Model.

It is not a relationship manifest, dependency graph, plugin API or Studio-specific API.

---

## Relationship manifest report context

v0.9.0 introduced the first Core-owned Relationship Manifest Surface.

The generated relationship manifest report is written to:

```text
generated/reports/relationship_manifest.json
```

It records relationship-level contract records derived from explicit loaded Mission Model fields.

It includes:

```text
manifest_version
kind = orbitfabric.relationship_manifest
OrbitFabric tool version
mission identity
source mission directory
boundary flags
relationship type records
relationship type counts
relationship records
```

The relationship manifest report is generated from the current OrbitFabric tool and the declared Mission Model.

It is not a relationship graph, dependency graph, plugin API, Studio-specific API, runtime routing table or ground routing table.

---

## Why the versions differ

During development previews, OrbitFabric may evolve faster than the Mission Model contract.

For example:

```text
OrbitFabric tool/package version: 0.9.0
Mission Model version:           0.1.0
```

This is valid.

It means:

- the tool has gained new capabilities such as Payload Contracts, Data Product Contracts, Contact/Downlink Contracts, Commandability/Autonomy Contracts, Data Flow Evidence, Runtime Contract Bindings, Ground Integration Artifacts, Contract Introspection Surfaces, Entity Index Surfaces and Relationship Manifest Surfaces;
- the demo mission still declares the v0.1 Mission Model contract;
- generated artifacts record the relevant tool and model context.

---

## Current v0.9.0 rule

For the current development preview:

| Version field | Meaning |
|---|---|
| `orbitfabric --version` | OrbitFabric CLI/package version. |
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

---

## What not to assume

Do not assume that:

- the OrbitFabric package version and Mission Model version are always identical;
- a Mission Model version bump always requires a Python package major/minor bump;
- a Python package patch/dev version always changes the Mission Model contract;
- generated artifacts are valid without checking both tool version and mission model version;
- generated runtime-facing bindings are flight protocol IDs or flight software ABI guarantees;
- generated ground-facing artifacts imply ground runtime behavior or tool-specific compatibility;
- model summary reports imply entity-level indexing, relationship graphs or plugin APIs;
- entity index reports imply relationship graphs, dependency graphs or plugin APIs;
- relationship manifest reports imply graph engines, runtime behavior, ground behavior, plugin APIs or Studio-specific APIs.

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
- compatibility checks for generated artifact profiles.

These are not part of the current v0.9.0 development preview.