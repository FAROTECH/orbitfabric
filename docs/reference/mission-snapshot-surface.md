# Mission Snapshot Surface

Status: Candidate integration surface for full loaded-model inspection  
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
  "model": {
    "spacecraft": {},
    "subsystems": [],
    "modes": [],
    "mode_transitions": [],
    "telemetry": [],
    "commands": [],
    "events": [],
    "faults": [],
    "packets": [],
    "policies": {},
    "payloads": [],
    "data_products": [],
    "contacts": {},
    "commandability": {}
  }
}
```

`model` is produced from the loaded Pydantic `MissionModel` with JSON serialization and field aliases enabled. A downstream consumer must not interpret array order as additional mission semantics unless a domain contract explicitly defines ordering.

---

## Structural load failure

A structural Mission Model failure still produces the machine-readable surface.

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

The CLI exits non-zero for `result == "failed"`, but the JSON report is still written.

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

If Core cannot construct the Mission Model, the snapshot does not expose a partial semantic model.

```text
result = failed
mission = null
model = null
```

Diagnostics explain the load failure.

Downstream applications must not assemble a replacement partial mission from raw files.

---

## Loadability and lint are different questions

Mission Snapshot answers whether Core can construct the Mission Model.

Semantic lint is a separate Core operation.

Therefore:

```text
Mission Snapshot result = loaded
```

can coexist with lint findings, including lint errors.

A downstream application may make the loaded model inspectable while surfacing lint findings separately.

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

Unknown additive fields should be tolerated by compatible consumers. Missing fields required by the documented surface must not be silently synthesized.

---

## Relationship to existing inspection surfaces

The snapshot complements, rather than replaces, existing focused inspection surfaces:

```text
mission_snapshot.json        -> What complete loaded contract does Core know?
model_summary.json           -> Which model domains/counts are present?
entity_index.json            -> Which indexed contract entities are defined?
relationship_manifest.json   -> Which admitted explicit relationships connect them?
```

The focused surfaces remain useful because they provide stable normalized inventories and relationship records without requiring every downstream consumer to derive those indexes independently.

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
- a Studio bundle containing every Core report.

Its role is deliberately narrow:

> expose the complete loaded Mission Data Contract in a deterministic, structured, downstream-readable form.
