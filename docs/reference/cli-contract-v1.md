# CLI Contract v1

Status: Active v1 CLI contract with v1.1 candidate additions  
Scope: CLI compatibility classification for documented workflows  
Applies to: OrbitFabric CLI from `v1.0.0 - Stable Mission Data Contract` onward, including `v1.1.0 - Candidate Integration Surface Consolidation`

This page classifies the current OrbitFabric CLI surface after v1.1.0.

It is a documentation contract. It does not introduce new behavior, new Mission Model semantics, plugin execution, runtime behavior, ground behavior or Studio-specific APIs.

---

## 1. Purpose

The OrbitFabric CLI is a public user-facing workflow surface.

From v1.0.0 onward, documented command names, command groups, required arguments, documented options and documented machine-readable outputs for selected workflows are compatibility-sensitive.

v1.1.0 adds documented candidate integration-surface exports. Those commands are Core-owned, but their emitted surfaces remain candidate until a later stability decision promotes them.

This page identifies the current CLI surface and separates:

- command names;
- command groups;
- required arguments;
- documented options;
- human-oriented output;
- machine-readable output paths and report families;
- stable v1.0.0 surfaces;
- candidate v1.1.0 surfaces;
- unsupported compatibility assumptions.

---

## 2. Stability classification

Current CLI classification:

| CLI area | Classification | Notes |
|---|---|---|
| top-level command name `orbitfabric` | Stable contract | User-facing entry point. |
| top-level command groups | Stable contract | `gen`, `validate`, `inspect`, `export`. |
| top-level commands | Stable contract | `lint`, `sim`. |
| documented options | Stable contract | Option names are compatibility-sensitive after v1.0.0. |
| command required arguments | Stable contract | Required positional arguments are compatibility-sensitive. |
| CLI textual output | Human-oriented public preview | Useful for users. Not a machine contract. |
| JSON outputs produced via `--json` | Stable or candidate where documented | Classification depends on the report family. |
| v1.0.0 structured exports | Stable Core-owned surface | `model_summary.json`, `entity_index.json`, `relationship_manifest.json`. |
| v1.1.0 structured exports | Candidate Core-owned surface | `dashboard_summary.json`, `scenario_run_index.json`, `coverage_summary.json`. |
| generated artifact paths | Public preview or stable depending on surface | Paths are compatibility-sensitive when documented. |
| internal Python implementation | Internal implementation detail | Not a CLI contract. |

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

## 4. Output path rule

Mission-based commands resolve omitted generated artifact paths under the mission workspace.

For this mission directory:

```text
examples/demo-3u/mission/
```

omitted generated outputs resolve under:

```text
examples/demo-3u/generated/
```

Examples:

```bash
orbitfabric gen docs examples/demo-3u/mission/
orbitfabric gen runtime examples/demo-3u/mission/
orbitfabric gen ground examples/demo-3u/mission/
orbitfabric export dashboard-summary examples/demo-3u/mission/
orbitfabric export coverage-summary examples/demo-3u/mission/
```

Default outputs include:

```text
examples/demo-3u/generated/docs/
examples/demo-3u/generated/runtime/cpp17/
examples/demo-3u/generated/ground/generic/
examples/demo-3u/generated/reports/dashboard_summary.json
examples/demo-3u/generated/reports/coverage_summary.json
```

Explicit user-provided paths are preserved exactly as provided.

---

## 5. Lint command

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

## 6. Simulation command

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

The JSON simulation report is a machine-readable stable report family with additive v1.1.0 structured expectation accounting.

The plain-text log is human-reviewable evidence and should not be treated as a machine contract.

---

## 7. Generation command group

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

Generated artifacts are disposable outputs unless explicitly classified otherwise. They must not become the source of truth.

---

## 8. Documentation generation

Current command:

```bash
orbitfabric gen docs <mission_dir>
```

Current documented option:

```text
--output-dir <path>
```

Default output directory for omitted output paths:

```text
<mission_workspace>/generated/docs
```

For `examples/demo-3u/mission/`, this resolves to:

```text
examples/demo-3u/generated/docs
```

Compatibility-sensitive behavior:

- generates Markdown documentation from the Mission Model;
- aborts when lint errors exist;
- writes human-reviewable generated documentation.

Generated Markdown documentation is not the Mission Data Contract source of truth.

---

## 9. Data-flow documentation generation

Current command:

```bash
orbitfabric gen data-flow <mission_dir>
```

Current documented option:

```text
--output-file <path>
```

Default output file for omitted output paths:

```text
<mission_workspace>/generated/docs/data_flow.md
```

For `examples/demo-3u/mission/`, this resolves to:

```text
examples/demo-3u/generated/docs/data_flow.md
```

Compatibility-sensitive behavior:

- generates Markdown data-flow documentation from the Mission Model;
- aborts when lint errors exist;
- writes a human-reviewable data-flow documentation artifact.

---

## 10. Runtime-facing generation

Current command:

```bash
orbitfabric gen runtime <mission_dir>
```

Current documented options:

```text
--output-dir <path>
--profile <profile>
```

Default output directory for omitted output paths:

```text
<mission_workspace>/generated/runtime
```

For `examples/demo-3u/mission/`, this resolves to:

```text
examples/demo-3u/generated/runtime
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

## 11. Ground-facing generation

Current command:

```bash
orbitfabric gen ground <mission_dir>
```

Current documented options:

```text
--output-dir <path>
--profile <profile>
```

Default output directory for omitted output paths:

```text
<mission_workspace>/generated/ground
```

For `examples/demo-3u/mission/`, this resolves to:

```text
examples/demo-3u/generated/ground
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

## 12. Export command group

Current command group:

```bash
orbitfabric export ...
```

Stable v1.0.0 export commands:

```text
orbitfabric export model-summary
orbitfabric export entity-index
orbitfabric export relationship-manifest
```

Candidate v1.1.0 export commands:

```text
orbitfabric export dashboard-summary
orbitfabric export scenario-run-index
orbitfabric export coverage-summary
```

These commands export Core-owned read-only machine-readable inspection surfaces.

They are the supported downstream inspection boundary.

Downstream tools must consume these surfaces instead of reconstructing Mission Data Contract semantics from raw YAML, generated artifacts, textual CLI output or UI state.

---

## 13. Model summary export

Current command:

```bash
orbitfabric export model-summary <mission_dir>
```

Current documented option:

```text
--json <path>
```

Default output file for omitted output paths:

```text
<mission_workspace>/generated/reports/model_summary.json
```

Compatibility-sensitive behavior:

- exports the Core-owned model summary surface;
- answers what contract domains are present;
- writes a machine-readable JSON report.

Classification:

```text
v1.0.0 stable Core-owned surface
```

---

## 14. Entity index export

Current command:

```bash
orbitfabric export entity-index <mission_dir>
```

Current documented option:

```text
--json <path>
```

Default output file for omitted output paths:

```text
<mission_workspace>/generated/reports/entity_index.json
```

Compatibility-sensitive behavior:

- exports the Core-owned entity index surface;
- answers what contract entities are defined;
- writes a machine-readable JSON report.

Classification:

```text
v1.0.0 stable Core-owned surface
```

---

## 15. Relationship manifest export

Current command:

```bash
orbitfabric export relationship-manifest <mission_dir>
```

Current documented option:

```text
--json <path>
```

Default output file for omitted output paths:

```text
<mission_workspace>/generated/reports/relationship_manifest.json
```

Compatibility-sensitive behavior:

- exports the stable Core-owned relationship manifest surface for admitted families;
- answers how indexed mission contract entities are related;
- writes a machine-readable JSON report.

Classification:

```text
v1.0.0 stable Core-owned surface
```

This command does not expose a relationship graph, dependency graph, plugin API, runtime routing table, ground routing table or Studio-specific API.

---

## 16. Dashboard summary export

Current command:

```bash
orbitfabric export dashboard-summary <mission_dir>
```

Current documented option:

```text
--json <path>
```

Default output file for omitted output paths:

```text
<mission_workspace>/generated/reports/dashboard_summary.json
```

Compatibility-sensitive behavior:

- exports a dashboard-ready aggregation of existing Core facts;
- derives from validated Mission Model and Core-owned structured outputs;
- writes a machine-readable JSON report.

Classification:

```text
v1.1.0 candidate Core-owned integration surface
```

This command does not make OrbitFabric Core a dashboard backend or Studio API.

---

## 17. Scenario run index export

Current command:

```bash
orbitfabric export scenario-run-index
```

Current documented options:

```text
--simulation-reports <path>
--json <path>
```

Compatibility-sensitive behavior:

- indexes Core simulation JSON report runs;
- writes a machine-readable JSON index;
- does not execute scenarios;
- does not compute runtime health or mission readiness.

Classification:

```text
v1.1.0 candidate Core-owned integration surface
```

---

## 18. Coverage summary export

Current command:

```bash
orbitfabric export coverage-summary <mission_dir>
```

Current documented options:

```text
--scenario-index <path>
--json <path>
```

Default output file for omitted output paths:

```text
<mission_workspace>/generated/reports/coverage_summary.json
```

Compatibility-sensitive behavior:

- exports limited coverage derived from Core structured outputs;
- consumes Mission Model facts and scenario evidence summaries;
- writes a machine-readable JSON report.

Classification:

```text
v1.1.0 candidate Core-owned integration surface
```

This command does not introduce mission health scoring, model completeness scoring, flight readiness scoring or formal verification.

---

## 19. Inspect command group

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

## 20. Validate command group

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

## 21. Machine-readable versus human-oriented output

Only explicitly documented JSON reports and Core-owned structured surfaces should be treated as machine-readable stable or candidate outputs according to their classification.

Human-oriented terminal output is useful for users, demonstrations and diagnostics, but it is not a machine compatibility contract.

Scripts and downstream tools should prefer:

```text
--json outputs
model_summary.json
entity_index.json
relationship_manifest.json
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
generated manifests
```

over parsing terminal text.

---

## 22. Compatibility-sensitive CLI changes

The following changes are compatibility-sensitive after v1.0.0:

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

Candidate v1.1.0 surfaces may still evolve, but changes must not be silent because downstream tools are expected to consume them as Core-owned structured surfaces.

---

## 23. Current CLI non-goals

The CLI contract does not introduce or promise:

```text
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
OpenOBSW/OpenSVF-specific generation
```

---

## 24. Final statement

v1.1.0 is the current project release.

v1.0.0 remains the stable Mission Data Contract baseline.

The CLI is stable enough for users and CI workflows to rely on documented command names, command groups, required arguments, documented options and machine-readable outputs according to their explicit stability classification, without freezing human-oriented terminal prose.
