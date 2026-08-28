# Mission Snapshot Surface

Status: **Stable Core-owned integration/inspection surface from v1.2.0**  
Surface version: `0.1-candidate`  
Default path: `generated/reports/mission_snapshot.json`

---

## Purpose

The Mission Snapshot Surface is an OrbitFabric Core-owned, machine-readable, read-only inspection surface.

It answers:

```text
What complete Mission Model did OrbitFabric Core actually load?
```

The Mission Model remains the source of truth.

The snapshot does not create a new model, a Studio-specific API or a second semantic authority. It serializes the complete loaded `MissionModel` inside a versioned envelope suitable for downstream consumers.

The primary downstream requirement is that a consumer can inspect the complete contract without reparsing OrbitFabric YAML or reconstructing domain semantics from generated documentation.

---

## Stability classification

From OrbitFabric v1.2.0, the documented Snapshot envelope, result/failure semantics, boundary flags and complete-loaded-model role are stable compatibility commitments.

The surface format identifier deliberately remains:

```text
snapshot_version = 0.1-candidate
```

OrbitFabric treats stability classification and surface format-version text as separate concepts. Retaining the already reference-proven identifier avoids an artificial compatibility break.

The stable commitment does **not** freeze the complete `model` payload byte-for-byte. `model` is a faithful JSON serialization of the loaded Mission Model and follows the Mission Model's own compatibility rules. Compatible consumers must tolerate additive Mission Model fields where those rules permit additive evolution.

A selected v1.2 golden signature protects contract-significant Snapshot fields and representative serialization invariants without freezing the whole generated report.

---

## CLI export

```bash
orbitfabric export mission-snapshot examples/demo-3u/mission
```

The default output path is:

```text
generated/reports/mission_snapshot.json
```

A custom output file can be selected with:

```bash
orbitfabric export mission-snapshot examples/demo-3u/mission \
  --json /tmp/mission_snapshot.json
```

Downstream applications are encouraged to pass an explicit output path when they do not want to modify the mission workspace.

---

## Loaded result

When Core successfully constructs the Mission Model, the envelope has this conceptual shape:

```json
{
  "kind": "orbitfabric.mission_snapshot",
  "snapshot_version": "0.1-candidate",
  "orbitfabric_version": "1.x",
  "result": "loaded",
  "mission": {
    "id": "demo-3u",
    "name": "Demo 3U Spacecraft",
    "model_version": "0.1.0"
  },
  "source": {
    "mission_dir": "/absolute/path/to/mission"
  },
  "boundaries": {
    "source_of_truth": "mission_model",
    "core_derived_report": true,
    "read_only": true,
    "contains_full_loaded_model": true,
    "contains_structured_diagnostics": true,
    "contains_yaml_ast": false,
    "contains_source_locations": false,
    "contains_plugin_api": false,
    "contains_studio_api": false,
    "contains_runtime_behavior": false,
    "contains_ground_behavior": false
  },
  "diagnostics": [],
  "model": {}
}
```

`model` is produced from the loaded Pydantic `MissionModel` with JSON serialization and field aliases enabled. A downstream consumer must not interpret array order as additional mission semantics unless a domain contract explicitly defines ordering.

---

## Structural load failure

A structural Mission Model failure still produces the machine-readable surface when technically possible.

Conceptually:

```json
{
  "kind": "orbitfabric.mission_snapshot",
  "snapshot_version": "0.1-candidate",
  "orbitfabric_version": "1.x",
  "result": "failed",
  "mission": null,
  "source": {
    "mission_dir": "/absolute/path/to/mission"
  },
  "diagnostics": [
    {
      "severity": "ERROR",
      "code": "OF-SYN-002",
      "file": "telemetry.yaml",
      "domain": "telemetry",
      "object_id": null,
      "message": "...",
      "suggestion": "..."
    }
  ],
  "model": null
}
```

The CLI exits non-zero for `result == "failed"`, but the JSON report is still written when possible.

This distinction is intentional:

```text
process exit status
        !=
structured surface availability
        !=
semantic result encoded by the surface
```

Consumers must inspect the envelope rather than assuming that a non-zero exit means no machine-readable result exists.

---

## No partial Mission Model

If Core cannot construct the Mission Model, the snapshot does not expose a partial semantic model:

```text
result = failed
mission = null
model = null
```

Diagnostics explain the load failure. Downstream applications must not assemble a replacement partial mission from raw files.

---

## Loadability and lint are different questions

Mission Snapshot answers whether Core can construct the Mission Model. Semantic lint is a separate Core operation.

Therefore:

```text
Mission Snapshot result = loaded
```

can coexist with lint findings, including lint errors.

The coherent Core Integration Input Set carries the separate lint result/report required by production integration consumers.

---

## Boundary contract

The snapshot:

- is Core-owned;
- is read-only;
- contains the complete loaded Mission Model;
- contains structured load diagnostics;
- preserves Mission Model field aliases;
- does not contain a YAML AST;
- does not expose source line/column locations;
- does not expose plugin execution;
- does not expose runtime behavior;
- does not expose ground runtime behavior;
- is not a Studio-specific API.

---

## Compatibility

Consumers must check at least:

```text
kind == orbitfabric.mission_snapshot
snapshot_version == a supported format identifier
```

`orbitfabric_version` is useful for support and diagnostics but is not a substitute for surface-format compatibility.

Unknown additive envelope or Mission Model fields must be tolerated where the documented underlying contracts permit additive evolution. Missing fields required by the supported Snapshot contract must not be silently synthesized.

---

## Relationship to existing inspection surfaces

The snapshot complements, rather than replaces, existing focused inspection surfaces:

```text
mission_snapshot.json        -> complete loaded contract
model_summary.json           -> domain/count introspection
entity_index.json            -> canonical indexed entities
relationship_manifest.json   -> admitted explicit relationships
```

The focused surfaces remain normative companions because downstream consumers must not independently re-derive Core-owned indexes or admitted relationships from the full Snapshot.

---

## Relationship to the Core Integration Input Set

From v1.2.0, Mission Snapshot is a required surface in the stable coherent Core Integration Input Set.

A projection-capable set requires compatible:

```text
mission_snapshot
entity_index
relationship_manifest
lint_report
```

with `model_summary` as the canonical companion surface.

---

## Non-goals

The Mission Snapshot Surface does not provide:

- a dependency graph;
- inferred relationships;
- a UI navigation model;
- health/readiness/completeness scoring;
- scenario execution state;
- telemetry history;
- source editing;
- plugin execution;
- runtime or ground behavior.

Its role is deliberately narrow:

> expose the complete loaded Mission Data Contract in a deterministic, structured, downstream-readable form.
