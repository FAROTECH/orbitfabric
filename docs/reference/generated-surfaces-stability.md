# Generated Surfaces Stability

Status: Active v1.x classification through v1.2.0  
Scope: generated and exported surface compatibility  
Applies to: OrbitFabric generated and exported surfaces from v1.0.0 onward

The Mission Model remains the semantic source of truth. Generated and exported surfaces are derived outputs with explicit maturity classifications.

## 1. Stable Core-owned machine-readable surfaces

The stable Core-owned surface set now includes:

```text
lint JSON report
simulation JSON report
model_summary.json
entity_index.json
relationship_manifest.json for admitted families
mission_snapshot.json
Core Integration Input Set
```

The original v1 inspection chain remains:

```text
model_summary.json          What contract domains are present?
entity_index.json           What contract entities are defined?
relationship_manifest.json  Which explicit admitted relationships connect them?
```

v1.2 adds:

```text
mission_snapshot.json       What complete Mission Model did Core actually load?
Core Integration Input Set  What coherent Core-owned input can an external integration consume?
```

These surfaces are read-only and derived. They do not become editable sources of mission truth.

## 2. Relationship Manifest additive families

The original v1 admitted relationship families remain stable.

v1.2 adds seven additive stable-compatible FDIR families. They are derived deterministically from explicit loaded Mission Model fields and do not redefine original relationship meaning.

Consumers must not treat the relationship-type set as permanently closed unless they intentionally pin to a specific release contract.

## 3. Candidate Core-owned inspection surfaces

The following v1.1 surfaces remain candidate after v1.2:

```text
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
simulation JSON structured expectation accounting
```

They are Core-owned, read-only outputs, but they are not part of the stable Core compatibility class.

They do not make Core a dashboard backend, coverage engine, Studio API or formal verification tool.

## 4. Generated runtime-facing artifacts

Generated runtime-facing outputs include:

```text
runtime_contract_manifest.json
C++17 identifiers and metadata registries
command argument structures
abstract adapter interfaces
host-build smoke files
```

They remain public-preview generated artifacts unless explicitly promoted later.

They are not flight software and do not promise a flight ABI, scheduler, driver layer, command dispatcher or telemetry runtime.

## 5. Generated ground-facing artifacts

Generated ground outputs include:

```text
ground_contract_manifest.json
JSON dictionaries
CSV dictionaries
human-reviewable Markdown artifacts
```

They remain public-preview generated artifacts unless explicitly promoted later.

They are not a telemetry archive, database, operator console, command uplink service or live ground segment.

## 6. Generated documentation and logs

Generated mission Markdown, data-flow Markdown and plain-text simulation logs are reproducible human-reviewable artifacts.

They are not machine compatibility contracts unless a later explicit decision says otherwise.

## 7. Current classification table

| Surface | Classification | Source | Notes |
|---|---|---|---|
| lint JSON report | Stable | Mission Model and lint rules | Core validation result. |
| simulation JSON report | Stable | Mission Model and scenario YAML | Host-side scenario evidence. |
| `model_summary.json` | Stable | Mission Model | Domain-level inspection. |
| `entity_index.json` | Stable | Mission Model | Entity-level inspection. |
| `relationship_manifest.json` original families | Stable | Mission Model | Original admitted explicit relationships. |
| Relationship Manifest v1.2 FDIR families | Additive stable-compatible | Mission Model | Additional explicit relationships. |
| `mission_snapshot.json` | Stable from v1.2 | Mission Model | Complete loaded-model inspection. |
| Core Integration Input Set | Stable from v1.2 | One Core load/lint operation | Coherent external integration input boundary. |
| `dashboard_summary.json` | Candidate | Core facts | Dashboard-ready aggregation. |
| `scenario_run_index.json` | Candidate | Simulation JSON reports | Run index. |
| `coverage_summary.json` | Candidate | Core structured outputs | Limited coverage. |
| simulation JSON `expectations` | Candidate additive extension | Scenario execution | Structured expectation accounting. |
| generated runtime artifacts | Public preview | Mission Model | Contract-facing artifacts, not flight software. |
| generated ground artifacts | Public preview | Mission Model | Integration artifacts, not ground runtime. |
| generated Markdown | Human-oriented derived output | Mission Model | Documentation, not machine contract. |
| plain-text simulation logs | Human-oriented derived output | Scenario execution | Reviewable log, not machine contract. |

## 8. Core Integration Input Set

The stable v1.2 Integration Input Set is a coherent multi-file surface containing:

```text
integration_input_manifest.json
mission_snapshot.json
entity_index.json
relationship_manifest.json
lint_report.json
model_summary.json
```

Its stability covers documented role classification, availability states, surface identity/version/digests, load and lint state separation, RFC 8785/JCS set fingerprinting, manifest-last coherence and no raw-YAML semantic fallback.

The existing `input_set_version = 0.1-candidate` identifier is retained as a wire identifier and does not weaken the v1.2 stability classification.

## 9. Compatibility-sensitive changes

For stable surfaces, compatibility-sensitive changes include:

- renaming a documented file or `kind` identity;
- removing or renaming documented stable fields;
- changing documented field meaning;
- changing stable result tokens;
- changing stable default output paths;
- changing stable relationship meaning;
- changing Integration Input Set required-role or coherence rules;
- weakening explicit boundary flags;
- changing whether an artifact is treated as source or derived output.

Such changes must be explicit, reviewed and documented.

Candidate and public-preview outputs may evolve more freely, but their changes must still be documented when downstream tools are expected to consume them.

## 10. Downstream consumer rule

Downstream tools must consume the strongest appropriate documented Core-owned surface.

They must not reconstruct Mission Data Contract meaning from:

```text
raw YAML independently when a Core integration boundary is required
generated Markdown
generated runtime code
generated ground dictionaries
terminal text
plain-text logs
file naming conventions
timestamps
UI state
```

Core loads and interprets the Mission Model. Derived consumers use explicit Core-owned facts.

## 11. Non-goals

This classification does not introduce:

```text
new Mission Model semantics
relationship inference
graph execution
plugin execution
runtime behavior
ground behavior
schema migration tooling
Studio-specific semantic authority
```

## 12. Final statement

v1.2.0 extends the stable generated/exported Core boundary with Mission Snapshot and the coherent Integration Input Set while preserving the original v1 surfaces and leaving the v1.1 inspection additions candidate.

Generated runtime, ground and human-readable artifacts remain derived and disposable unless explicitly promoted by a later reviewed compatibility decision.
