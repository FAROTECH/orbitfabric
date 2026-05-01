# Versioning Model

This page explains how OrbitFabric uses version numbers.

OrbitFabric currently distinguishes between:

- the OrbitFabric tool/package version;
- the Mission Model version declared by a mission;
- the version field written into generated JSON reports.

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
orbitfabric 0.3.0
```

This version answers the question:

```text
Which version of the OrbitFabric tool generated, validated or executed this artifact?
```

Generated JSON reports use this version in their top-level `version` field.

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
  "version": "0.3.0",
  "mission": "demo-3u",
  "model_version": "0.1.0"
}
```

The top-level `version` identifies the OrbitFabric tool that produced the report.

The `model_version` identifies the Mission Model version declared by the mission.

---

## Why the versions differ

During development previews, OrbitFabric may evolve faster than the Mission Model contract.

For example:

```text
OrbitFabric tool/package version: 0.3.0
Mission Model version:           0.1.0
```

This is valid.

It means:

- the tool has gained new capabilities such as Payload Contracts and Data Product Contracts;
- the demo mission still declares the v0.1 Mission Model contract;
- generated artifacts record both pieces of information.

---

## Current v0.3 rule

For the current development preview:

| Version field | Meaning |
|---|---|
| `orbitfabric --version` | OrbitFabric CLI/package version. |
| JSON report top-level `version` | OrbitFabric tool version that produced the report. |
| `spacecraft.model_version` | Mission Model contract version declared by the mission. |
| JSON report `model_version` | Mission Model version copied from mission YAML. |

---

## What not to assume

Do not assume that:

- the OrbitFabric package version and Mission Model version are always identical;
- a Mission Model version bump always requires a Python package major/minor bump;
- a Python package patch/dev version always changes the Mission Model contract;
- generated artifacts are valid without checking both tool version and mission model version.

---

## Future direction

Future versions may introduce a more explicit schema versioning mechanism.

Possible future additions include:

- a dedicated Mission Model schema version field;
- schema migration helpers;
- compatibility checks between tool version and Mission Model version;
- JSON Schema export for Mission Model validation.

These are not part of the current v0.3.0 development preview.
