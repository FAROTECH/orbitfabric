# Versioning Model

This page explains how OrbitFabric uses version numbers.

OrbitFabric currently distinguishes between:

- the OrbitFabric tool/package version;
- the Mission Model version declared by a mission;
- the version field written into generated JSON reports;
- the generated runtime contract manifest context;
- the generated ground contract manifest context.

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
orbitfabric 0.8.0
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

Current example:

```json
{
  "tool": "orbitfabric-lint",
  "version": "0.8.0",
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

## Why the versions differ

During development previews, OrbitFabric may evolve faster than the Mission Model contract.

For example:

```text
OrbitFabric tool/package version: 0.8.0
Mission Model version:           0.1.0
```

This is valid.

It means:

- the tool has gained new capabilities such as Payload Contracts, Data Product Contracts, Contact/Downlink Contracts, Commandability/Autonomy Contracts, Data Flow Evidence, Runtime Contract Bindings and Ground Integration Artifacts;
- the demo mission still declares the v0.1 Mission Model contract;
- generated artifacts record the relevant tool and model context.

---

## Current v0.8 rule

For the current development preview:

| Version field | Meaning |
|---|---|
| `orbitfabric --version` | OrbitFabric CLI/package version. |
| JSON report top-level `version` | OrbitFabric tool version that produced the report. |
| `spacecraft.model_version` | Mission Model contract version declared by the mission. |
| JSON report `model_version` | Mission Model version copied from mission YAML. |
| Runtime manifest `generation.profile` | Runtime generation profile, currently `cpp17`. |
| Runtime manifest `contains_flight_runtime` | Explicit boundary flag, currently `false`. |
| Ground manifest `generation.profile` | Ground generation profile, currently `generic`. |
| Ground manifest `contains_ground_runtime` | Explicit boundary flag, currently `false`. |
| Ground manifest `claims_*` compatibility fields | Explicit tool-specific claim flags, currently `false`. |

---

## What not to assume

Do not assume that:

- the OrbitFabric package version and Mission Model version are always identical;
- a Mission Model version bump always requires a Python package major/minor bump;
- a Python package patch/dev version always changes the Mission Model contract;
- generated artifacts are valid without checking both tool version and mission model version;
- generated runtime-facing bindings are flight protocol IDs or flight software ABI guarantees;
- generated ground-facing artifacts imply ground runtime behavior or tool-specific compatibility.

---

## Future direction

Future versions may introduce a more explicit schema versioning mechanism.

Possible future additions include:

- a dedicated Mission Model schema version field;
- a dedicated RuntimeContract schema version;
- a dedicated GroundContract schema version;
- schema migration helpers;
- compatibility checks between tool version and Mission Model version;
- JSON Schema export for Mission Model validation;
- compatibility checks for generated artifact profiles.

These are not part of the current v0.8.0 development preview.
