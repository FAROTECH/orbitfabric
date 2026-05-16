# CLI Contract v1 Preview

Status: Development preview  
Scope: v0.10.0 CLI compatibility classification  
Applies to: OrbitFabric CLI before v1.0.0

This page classifies the current OrbitFabric CLI surface on the path toward v1.0.0.

It is a documentation contract. It does not introduce new commands, new options, new behavior, new Mission Model semantics, new reports, plugin execution, runtime behavior, ground behavior or Studio-specific APIs.

---

## 1. Purpose

The OrbitFabric CLI is a public user-facing workflow surface.

Before v1.0.0, the CLI is still a development-preview interface. However, command names, command groups, required arguments and documented machine-readable outputs are compatibility-sensitive.

This page identifies the current CLI surface and separates:

- command names;
- command groups;
- required arguments;
- documented options;
- human-oriented output;
- machine-readable output paths and report families;
- unsupported compatibility assumptions.

---

## 2. Stability classification

Current CLI classification:

| CLI area | Classification | Notes |
|---|---|---|
| top-level command name `orbitfabric` | Public preview | User-facing entry point. |
| top-level command groups | Public preview | `gen`, `validate`, `inspect`, `export`. |
| top-level commands | Public preview | `lint`, `sim`. |
| documented options | Public preview | Option names are compatibility-sensitive before v1.0.0. |
| command required arguments | Public preview | Required positional arguments are compatibility-sensitive. |
| CLI textual output | Human-oriented public preview | Useful for users. Not a machine contract. |
| JSON outputs produced via `--json` | Public preview report surface | Machine-readable report families are documented separately. |
| generated artifact paths | Public preview, generated artifact surface | Paths are compatibility-sensitive when documented. |
| internal Python implementation | Internal implementation detail | Not a CLI contract. |

No current CLI surface is classified as a stable v1.0 contract yet.

---

## 3. Top-level CLI surface

Current top-level invocation:

```bash
orbitfabric --help
orbitfabric --version
```

Current top-level commands and groups:

```text
orbitfabric lint
orbitfabric sim
orbitfabric gen ...
orbitfabric validate ...
orbitfabric inspect ...
orbitfabric export ...
```

`orbitfabric --version` reports the OrbitFabric tool/package version.

The OrbitFabric tool/package version is not the same thing as the Mission Model version declared by a mission.

---

## 4. Lint command

Current command:

```bash
orbitfabric lint <mission_dir>
```

Current documented options:

```text
--json <path>
--warnings-as-errors
```

Compatibility-sensitive behavior:

- the command validates and semantically lints a Mission Model directory;
- the required argument is a readable mission directory;
- `--json` writes a machine-readable lint report;
- `--warnings-as-errors` makes warning-level findings fail the command.

Human-oriented terminal text is not a machine contract.

The lint JSON report structure is documented separately in `JSON Reports v0.1`.

---

## 5. Simulation command

Current command:

```bash
orbitfabric sim <scenario_file>
```

Current documented options:

```text
--json <path>
--log <path>
```

Compatibility-sensitive behavior:

- the command executes a scenario YAML file against its referenced Mission Model;
- the required argument is a readable scenario file;
- `--json` writes a machine-readable simulation report;
- `--log` writes a plain-text simulation timeline log.

The JSON simulation report is a machine-readable public preview surface.

The plain-text log is human-reviewable evidence and should not be treated as a machine contract.

---

## 6. Generation command group

Current command group:

```bash
orbitfabric gen ...
```

Current generation commands:

```text
orbitfabric gen docs
orbitfabric gen data-flow
orbitfabric gen runtime
orbitfabric gen ground
```

These commands generate artifacts derived from the validated Mission Model.

Generated artifacts are disposable outputs. They must not become the source of truth.

---

## 7. Documentation generation

Current command:

```bash
orbitfabric gen docs <mission_dir>
```

Current documented option:

```text
--output-dir <path>
```

Default output directory:

```text
generated/docs
```

Compatibility-sensitive behavior:

- generates Markdown documentation from the Mission Model;
- aborts when lint errors exist;
- writes human-reviewable generated documentation.

Generated Markdown documentation is not the Mission Data Contract source of truth.

---

## 8. Data-flow documentation generation

Current command:

```bash
orbitfabric gen data-flow <mission_dir>
```

Current documented option:

```text
--output-file <path>
```

Default output file:

```text
generated/docs/data_flow.md
```

Compatibility-sensitive behavior:

- generates Markdown data-flow documentation from the Mission Model;
- aborts when lint errors exist;
- writes a human-reviewable data-flow documentation artifact.

---

## 9. Runtime-facing generation

Current command:

```bash
orbitfabric gen runtime <mission_dir>
```

Current documented options:

```text
--output-dir <path>
--profile <profile>
```

Current default output directory:

```text
generated/runtime
```

Current supported profile:

```text
cpp17
```

Compatibility-sensitive behavior:

- generates runtime-facing contract artifacts from the Mission Model;
- aborts when lint errors exist;
- rejects unsupported runtime generation profiles;
- writes a runtime contract manifest and generated C++17 binding artifacts.

This command does not generate flight software, scheduler behavior, command dispatch runtime, telemetry polling runtime, drivers, RTOS integration or protected user-code regions.

---

## 10. Ground-facing generation

Current command:

```bash
orbitfabric gen ground <mission_dir>
```

Current documented options:

```text
--output-dir <path>
--profile <profile>
```

Current default output directory:

```text
generated/ground
```

Current supported profile:

```text
generic
```

Compatibility-sensitive behavior:

- generates ground-facing contract artifacts from the Mission Model;
- aborts when lint errors exist;
- rejects unsupported ground generation profiles;
- writes a ground contract manifest, JSON dictionaries, CSV dictionaries and human-reviewable Markdown artifacts.

This command does not generate a live ground segment, database, command uplink service, operator console, telemetry archive, transport layer or station automation.

---

## 11. Export command group

Current command group:

```bash
orbitfabric export ...
```

Current export commands:

```text
orbitfabric export model-summary
orbitfabric export entity-index
orbitfabric export relationship-manifest
```

These commands export Core-owned read-only machine-readable inspection surfaces.

They are the supported downstream inspection boundary.

Downstream tools must consume these surfaces instead of reconstructing Mission Data Contract semantics from raw YAML, generated artifacts, textual CLI output or UI state.

---

## 12. Model summary export

Current command:

```bash
orbitfabric export model-summary <mission_dir>
```

Current documented option:

```text
--json <path>
```

Default output file:

```text
generated/reports/model_summary.json
```

Compatibility-sensitive behavior:

- exports the Core-owned model summary surface;
- answers what contract domains are present;
- writes a machine-readable JSON report.

---

## 13. Entity index export

Current command:

```bash
orbitfabric export entity-index <mission_dir>
```

Current documented option:

```text
--json <path>
```

Default output file:

```text
generated/reports/entity_index.json
```

Compatibility-sensitive behavior:

- exports the Core-owned entity index surface;
- answers what contract entities are defined;
- writes a machine-readable JSON report.

---

## 14. Relationship manifest export

Current command:

```bash
orbitfabric export relationship-manifest <mission_dir>
```

Current documented option:

```text
--json <path>
```

Default output file:

```text
generated/reports/relationship_manifest.json
```

Compatibility-sensitive behavior:

- exports the candidate Core-owned relationship manifest surface;
- answers how indexed mission contract entities are related;
- writes a machine-readable JSON report;
- reports candidate status.

This command does not expose a relationship graph, dependency graph, plugin API, runtime routing table, ground routing table or Studio-specific API.

---

## 15. Inspect command group

Current command group:

```bash
orbitfabric inspect ...
```

Current inspect command:

```text
orbitfabric inspect mission
```

Current command:

```bash
orbitfabric inspect mission <mission_dir>
```

Compatibility-sensitive behavior:

- loads and inspects a Mission Model directory;
- prints a human-oriented loaded model summary;
- does not lint, generate artifacts or export machine-readable reports.

The terminal output is human-oriented and must not be treated as a machine contract.

---

## 16. Validate command group

Current command group:

```bash
orbitfabric validate ...
```

Current validate command:

```text
orbitfabric validate scenario
```

Current command:

```bash
orbitfabric validate scenario <scenario_file>
```

Compatibility-sensitive behavior:

- validates a scenario YAML file without executing it;
- loads the referenced Mission Model;
- reports human-oriented scenario summary information.

This command does not execute scenario behavior, generate evidence reports or mutate Mission Model data.

---

## 17. Machine-readable versus human-oriented output

Only explicitly documented JSON reports and Core-owned structured surfaces should be treated as machine-readable public preview outputs.

Human-oriented terminal output is useful for users, demonstrations and diagnostics, but it is not a machine compatibility contract.

Scripts and downstream tools should prefer:

```text
--json outputs
model_summary.json
entity_index.json
relationship_manifest.json
generated manifests
```

over parsing terminal text.

---

## 18. Compatibility-sensitive CLI changes

The following changes are compatibility-sensitive before v1.0.0:

- renaming a documented command;
- removing a documented command;
- moving a documented command to another group;
- renaming a documented option;
- removing a documented option;
- changing a required positional argument;
- changing the default output path of a documented generated artifact;
- changing supported profile names;
- changing documented command failure behavior;
- changing the machine-readable report family produced by a command.

Compatibility-sensitive does not mean forbidden.

It means the change must be explicit, reviewed and documented.

---

## 19. Current CLI non-goals

The CLI contract does not introduce or promise:

```text
stable v1.0 compatibility
shell completion compatibility
terminal text parsing compatibility
plugin command discovery
plugin command execution
remote execution
background jobs
watch mode
live mission operations
flight runtime behavior
ground runtime behavior
operator console behavior
Studio-specific API behavior
```

---

## 20. v1.0 direction

Before v1.0.0, OrbitFabric should decide which CLI commands and options become stable.

Likely stable candidates include:

```text
orbitfabric lint
orbitfabric sim
orbitfabric gen docs
orbitfabric gen runtime
orbitfabric gen ground
orbitfabric export model-summary
orbitfabric export entity-index
orbitfabric export relationship-manifest
orbitfabric --version
```

The final v1.0 CLI contract should remain narrow.

OrbitFabric CLI stability should protect Mission Data Contract workflows, not turn OrbitFabric into a flight software runtime, ground segment, simulator platform, visual modeling tool or plugin execution environment.
