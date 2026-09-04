# CLI Contract v1

Status: Active v1 CLI contract through v1.3.0  
Scope: CLI compatibility classification for documented workflows  
Applies to: OrbitFabric CLI from v1.0.0 onward

This page classifies the current OrbitFabric CLI surface.

It documents compatibility. It does not introduce new behavior, Mission Model semantics, provider-specific acquisition, flight runtime behavior, ground behavior or Studio-specific APIs.

## 1. Purpose

The OrbitFabric CLI is a public user-facing workflow surface.

From v1.0.0 onward, documented command names, command groups, required arguments, documented options and selected machine-readable outputs are compatibility-sensitive according to their documented maturity class.

The current Core version is:

```text
v1.3.0 - Adapter Management Foundation
```

The CLI contains a mixed maturity surface. Stable workflows and candidate inspection, integration and Adapter Management families are classified explicitly rather than treated as one undifferentiated API.

## 2. Top-level CLI surface

Current top-level invocation:

```bash
orbitfabric --help
orbitfabric --version
```

Stable v1 command groups and commands include:

```text
orbitfabric lint
orbitfabric sim
orbitfabric gen ...
orbitfabric validate ...
orbitfabric inspect ...
orbitfabric export ...
```

v1.3.0 also exposes the candidate Adapter Management command group:

```text
orbitfabric adapter ...
```

`orbitfabric --version` reports the OrbitFabric package version. It is not the same as a mission's `model_version`, a JSON surface format version, an Adapter Release version or an Adapter Catalog format version.

## 3. Stability classification

| CLI area | Classification | Notes |
|---|---|---|
| `orbitfabric` entry point | Stable | Public CLI entry point. |
| `lint`, `sim`, `gen`, `validate`, `inspect`, `export` | Stable | Documented v1 command surface. |
| required positional arguments | Stable where documented for stable workflows | Compatibility-sensitive. |
| documented options | Stable where documented for stable workflows | Compatibility-sensitive. |
| human-oriented terminal text | Human-oriented | Not a machine contract. |
| v1.0 structured exports | Stable | Model Summary, Entity Index, Relationship Manifest. |
| v1.2 Mission Snapshot export | Stable | Complete loaded Mission Model inspection boundary. |
| v1.2 Integration Input Set export | Stable | Coherent Core input boundary for external integrations. |
| v1.1 dashboard, scenario-index and coverage exports | Candidate | Core-owned inspection surfaces. |
| `orbitfabric adapter ...` | Candidate | v1.3 provider-neutral Adapter Management lifecycle surface. |
| `orbitfabric adapter lock ...` | Candidate | v1.3 exact desired-state workflow. |
| `orbitfabric adapter catalog ...` | Candidate | v1.3 local provider-neutral Catalog inspection/selection. |
| internal Python APIs | Internal unless separately documented | Not automatically a public CLI contract. |

A candidate command may evolve under explicit review. Shipping in Core `1.3.0` does not promote it to the stable Mission Data Contract CLI surface.

## 4. Output path rule

Mission-based commands resolve omitted generated artifact paths under the mission workspace where documented.

For:

```text
examples/demo-3u/mission/
```

representative defaults resolve under:

```text
examples/demo-3u/generated/
```

Explicit user-provided output paths remain explicit.

Adapter Manager state uses its separately documented state model and must not be inferred from mission-workspace generated-output rules.

## 5. Lint

```bash
orbitfabric lint <mission_dir>
```

Documented options:

```text
--json <path>
--warnings-as-errors
```

The command performs structural validation and semantic linting. `--json` writes the machine-readable lint report. `--warnings-as-errors` changes the command success policy for warning-level findings.

Core owns lint diagnostic meaning. Terminal wording is not a machine contract.

## 6. Scenario validation and execution

Validate without executing:

```bash
orbitfabric validate scenario <scenario_file>
```

Execute deterministic host-side evidence:

```bash
orbitfabric sim <scenario_file>
```

Simulation options:

```text
--json <path>
--log <path>
```

The simulation JSON report is machine-readable evidence. The plain-text log is human-reviewable output and must not be treated as a stable parsing contract.

## 7. Generation commands

### Mission documentation

```bash
orbitfabric gen docs <mission_dir> [--output-dir <path>]
```

Default output:

```text
<mission_workspace>/generated/docs
```

### Data-flow documentation

```bash
orbitfabric gen data-flow <mission_dir> [--output-file <path>]
```

Default output:

```text
<mission_workspace>/generated/docs/data_flow.md
```

### Runtime-facing contract bindings

```bash
orbitfabric gen runtime <mission_dir> [--output-dir <path>] [--profile <profile>]
```

Current profile:

```text
cpp17
```

This command generates contract bindings and a host-build smoke target. It does not generate flight software, scheduling, command dispatch, telemetry polling, drivers or RTOS integration.

### Ground-facing contract artifacts

```bash
orbitfabric gen ground <mission_dir> [--output-dir <path>] [--profile <profile>]
```

Current profile:

```text
generic
```

This command generates ground-facing contract artifacts. It does not generate a live ground segment, telemetry archive, database, operator console or command uplink service.

Generated runtime and ground artifacts remain public-preview/disposable outputs unless explicitly classified otherwise.

## 8. Export command group

Current exports are classified by surface maturity.

### Stable v1.0 exports

```text
orbitfabric export model-summary
orbitfabric export entity-index
orbitfabric export relationship-manifest
```

### Stable v1.2 exports

```text
orbitfabric export mission-snapshot
orbitfabric export integration-input-set
```

### Candidate v1.1 inspection exports

```text
orbitfabric export dashboard-summary
orbitfabric export scenario-run-index
orbitfabric export coverage-summary
```

Downstream tooling should consume documented machine-readable outputs instead of parsing terminal text, generated Markdown or raw YAML independently.

## 9. Model Summary

```bash
orbitfabric export model-summary <mission_dir> [--json <path>]
```

Default output:

```text
<mission_workspace>/generated/reports/model_summary.json
```

Purpose:

```text
What contract domains are present?
```

Classification: stable Core-owned surface.

## 10. Entity Index

```bash
orbitfabric export entity-index <mission_dir> [--json <path>]
```

Default output:

```text
<mission_workspace>/generated/reports/entity_index.json
```

Purpose:

```text
What contract entities are defined?
```

Classification: stable Core-owned surface.

## 11. Relationship Manifest

```bash
orbitfabric export relationship-manifest <mission_dir> [--json <path>]
```

Default output:

```text
<mission_workspace>/generated/reports/relationship_manifest.json
```

Purpose:

```text
Which admitted explicit relationships connect indexed mission entities?
```

The original v1 relationship families are stable. The seven FDIR families admitted in v1.2 are additive stable-compatible families. Unknown additive types must not receive guessed semantics.

The command does not expose a graph engine, dependency graph, runtime routing table, ground routing table or plugin API.

## 12. Mission Snapshot

```bash
orbitfabric export mission-snapshot <mission_dir> [--json <path>]
```

Default output:

```text
<mission_workspace>/generated/reports/mission_snapshot.json
```

Purpose:

```text
What complete Mission Model did OrbitFabric Core actually load?
```

Classification: stable Core-owned integration and inspection surface from v1.2.0.

The existing format identifier remains:

```text
snapshot_version = 0.1-candidate
```

That token is a wire-format identifier, not the release maturity class.

Structural load failure is represented explicitly. Core must not expose a fabricated partial semantic Mission Model after structural failure.

## 13. Core Integration Input Set

```bash
orbitfabric export integration-input-set <mission_dir> [--output-dir <dir>]
```

Default output directory:

```text
<mission_workspace>/generated/reports/integration_input
```

The command writes a coherent multi-file set rather than one `--json` output:

```text
integration_input_manifest.json
mission_snapshot.json
entity_index.json
relationship_manifest.json
lint_report.json
model_summary.json
```

Classification: stable Core-to-external-integration input workflow from v1.2.0.

The command preserves:

```text
one logical Core load/lint operation
required and companion role classification
explicit availability and failure state
per-surface kind and format version
per-surface SHA-256
RFC 8785/JCS input_set_sha256
manifest-last coherence
Core diagnostic ownership
no raw-YAML semantic fallback
```

The existing identifier remains:

```text
input_set_version = 0.1-candidate
```

Stability classification and format-version text are intentionally separate.

## 14. Dashboard Summary

```bash
orbitfabric export dashboard-summary <mission_dir> [--json <path>]
```

Purpose: dashboard-ready aggregation of existing Core facts.

Classification: candidate Core-owned inspection surface introduced in v1.1.0.

It does not make Core a dashboard backend or Studio API.

## 15. Scenario Run Index

```bash
orbitfabric export scenario-run-index \
  --simulation-reports <path> \
  [--json <path>]
```

Purpose: index Core simulation JSON report runs.

Classification: candidate Core-owned inspection surface introduced in v1.1.0.

It does not execute scenarios or compute mission readiness.

## 16. Coverage Summary

```bash
orbitfabric export coverage-summary <mission_dir> \
  [--entity-index <path>] \
  [--relationship-manifest <path>] \
  [--scenario-run-index <path>] \
  [--json <path>]
```

Purpose: limited coverage derived from Core-owned structured outputs.

Classification: candidate Core-owned inspection surface introduced in v1.1.0.

It does not provide mission health scoring, model completeness scoring, flight readiness scoring or formal verification.

## 17. Inspect Mission

```bash
orbitfabric inspect mission <mission_dir>
```

The command loads and displays a human-oriented mission summary.

It does not lint, generate artifacts or provide a machine-readable compatibility surface.

## 18. Adapter Management command group

v1.3.0 adds the candidate provider-neutral Adapter Management command family:

```bash
orbitfabric adapter --help
```

Candidate lifecycle commands include:

```text
orbitfabric adapter install
orbitfabric adapter list
orbitfabric adapter inspect
orbitfabric adapter verify
orbitfabric adapter execute
orbitfabric adapter remove
```

These commands operate on exact adapter releases and Core-owned Installed Adapter State. The first installation backend is `python-wheel-managed-env`.

`execute` launches the installed external adapter entrypoint according to the documented adapter execution contract. It does not import the adapter implementation into the Core process and does not imply flight or ground runtime execution.

Human-oriented adapter CLI prose is not a machine contract unless a separate structured output is explicitly documented.

## 19. Adapter Project Lock commands

Candidate Project Lock commands include:

```text
orbitfabric adapter lock validate <lock.json>
orbitfabric adapter lock check <lock.json>
orbitfabric adapter lock install <lock.json> ...
```

Adapter Project Lock is project-scoped exact desired state. Installed Adapter State is separate user-scoped actual state.

Lock identity includes exact Source Coordinate, release version, Release Descriptor digest, artifact id/digest and installation backend id. It must not depend on machine-local instance ids, install paths, executable paths or mutable provider locators.

`lock install` is the explicit-source lane. It consumes already-available exact Release Descriptor/artifact bytes and does not discover or contact a remote provider.

An already satisfied exact entry produces an idempotent `MATCH -> NOOP` lifecycle result.

## 20. Adapter Catalog commands

Candidate local Catalog commands include:

```text
orbitfabric adapter catalog validate <catalog.json>
orbitfabric adapter catalog list <catalog.json>
orbitfabric adapter catalog select <catalog.json> <SOURCE_COORDINATE> --version <EXACT_VERSION>
```

Core Catalog selection is exact and provider-neutral.

The CLI does not:

```text
fetch a default remote Catalog
contact GitHub or another provider
dispatch provider implementations
select latest/stable channels
solve version ranges
perform automatic upgrades
```

Provider-specific acquisition remains in external Release Source products.

There is intentionally no Core one-command install-from-Catalog/provider-dispatch workflow in v1.3.0.

## 21. Machine-readable output rule

Machine consumers should prefer documented structured surfaces such as:

```text
lint JSON report
simulation JSON report
model_summary.json
entity_index.json
relationship_manifest.json
mission_snapshot.json
integration_input_manifest.json
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
Adapter Project Lock
Adapter Release Descriptor
Adapter Catalog
generated manifests where their own references permit it
```

Classification still matters. A candidate surface does not become stable because a script consumes it.

Consumers must not parse human terminal wording when a structured surface exists.

## 22. Compatibility-sensitive CLI changes

After v1.0.0, the following are compatibility-sensitive where documented as stable:

- renaming or removing a command;
- moving a command to a different group;
- renaming or removing a documented option;
- changing a required positional argument;
- changing a documented default output path;
- changing a supported profile name;
- changing documented failure behavior;
- changing the machine-readable report family produced by a command;
- changing stable Integration Input Set role or coherence semantics.

Compatibility-sensitive does not mean forbidden. It means the change must be explicit, reviewed and documented.

Candidate CLI and report families may evolve, but changes must not be silent. In particular, changes to Adapter Manager, Project Lock or Catalog CLI identity/failure behavior require explicit candidate-surface review because external tooling may already consume them.

## 23. Current non-goals

The CLI contract does not introduce or promise:

```text
terminal text parsing compatibility
in-process plugin command discovery/loading/execution
provider-specific acquisition inside Core
provider registration/dispatch
remote Catalog default/fetch policy
latest/stable/range version solving
automatic adapter upgrades
remote execution
background jobs
watch mode
live mission operations
flight runtime behavior
ground runtime behavior
operator console behavior
Studio-specific API behavior
downstream-specific Core generation
```

## 24. Final statement

v1.3.0 is the current Core release baseline.

The CLI provides stable user and CI workflows for the documented v1 Mission Data Contract operations, including the v1.2 Mission Snapshot and coherent Integration Input Set exports.

Candidate v1.1 inspection exports remain candidate. v1.3 adds a separate candidate Adapter Management command family with provider-neutral exact identity and lifecycle boundaries. Human-oriented terminal prose remains outside the machine compatibility contract.
