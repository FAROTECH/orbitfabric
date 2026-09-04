# Contributing to OrbitFabric

Thank you for your interest in OrbitFabric.

OrbitFabric is a model-first Mission Data Fabric for small spacecraft. Contributions are welcome when they strengthen the Mission Data Contract while preserving the project's architectural boundaries, compatibility discipline and clean-room requirements.

## Current project baseline

Current Core version:

```text
v1.3.0 - Adapter Management Foundation
```

The stable Mission Data Contract commitment started with v1.0.0. v1.2.0 extended that stable boundary additively with:

```text
mission_snapshot.json
Core Integration Input Set
seven additive stable-compatible FDIR relationship families
```

v1.3.0 preserves those stable semantics and adds candidate operation-input and provider-neutral Adapter Management product surfaces.

The following Core-owned inspection surfaces remain candidate:

```text
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
simulation JSON structured expectation accounting
```

The following integration contracts remain candidate:

```text
Projection Profile
Integration Result
Integration Package / Adapter Execution
operation-input v1 contract lane
```

The v1.3 Adapter Management foundation also remains candidate:

```text
Adapter Manager lifecycle
Adapter Release Descriptor 0.1-candidate
Adapter Project Lock 0.1-candidate
explicit-source install-from-lock
source-neutral ResolvedAdapterRelease attachment
Adapter Catalog 0.1-candidate
Adapter Catalog CLI
```

Do not treat candidate or generated surfaces as stable merely because they exist in a `1.x` Core release.

## Architectural rules

The Mission Model is the semantic source of truth.

Core owns Mission Data Contract interpretation. Generated artifacts, integration outputs and downstream visualizations must remain derived from explicit Core-owned semantics.

Contributions must preserve these rules:

1. Do not create a second Mission Model interpretation in a generator, exporter, adapter or downstream tool.
2. Do not parse raw Mission Model YAML independently when a validated Core-owned boundary exists for the required semantics.
3. Keep Core diagnostics distinct from integration diagnostics and external runtime or verification evidence.
4. Derive Core relationships only from explicit loaded Mission Model fields.
5. Do not infer relationship semantics from identifier names, string similarity, file placement, ordering or scenario co-occurrence.
6. Keep target-specific Projection Profile semantics outside Core.
7. Keep ecosystem-specific adapter implementation code outside the Core process. Adapter Manager may execute an installed external adapter only through the documented execution contract and environment-local entrypoint.
8. Keep provider-specific Release Source acquisition outside Core. GitHub, registries and future providers must hand verified exact material into Core through `ResolvedAdapterRelease`.
9. Do not introduce a universal provider registration/dispatch protocol from one provider implementation.
10. Keep runtime-facing and ground-facing generated artifacts reproducible and disposable unless an explicit compatibility decision promotes a surface.
11. Treat changes to stable public surfaces as compatibility-sensitive engineering changes.
12. Treat changes to candidate public machine-readable or CLI surfaces as explicit compatibility review items even when breaking preview evolution is allowed.

The generic integration ownership model is:

```text
OrbitFabric Core
  Mission Data Contract semantics
  coherent Core Integration Input Set

Projection Profile
  authored target-specific intent

External Integration Package / Adapter
  target validation, projection and generation

Integration Result
  mappings, artifacts, diagnostics, coverage and provenance

Studio and other downstream tools
  consume and present explicit records
```

The Adapter Management ownership model is:

```text
OrbitFabric Core
  exact Source Coordinate semantics
  Adapter Release Descriptor conformance
  Adapter Project Lock desired state
  Installed Adapter State
  installation / verification / execution / removal lifecycle
  provider-neutral Catalog model and exact selection

Provider-specific Release Source
  provider lookup/authentication/acquisition
  exact descriptor/artifact materialization
  ResolvedAdapterRelease handoff
```

Core must not learn OpenOBSW, OpenSVF, YAMCS, PUS, cFS, F Prime, GitHub or other ecosystem/provider-specific semantics simply to support an integration or release source.

## Clean-room requirement

OrbitFabric is developed as a clean-room open-source project.

Do not contribute:

- proprietary mission data;
- private spacecraft architecture details;
- private packet or protocol definitions;
- real operational logs or anomaly timelines;
- private bus maps, pinouts or hardware mappings;
- employer-owned or customer-owned code;
- NDA-protected material;
- export-controlled material;
- credentials, tokens or private infrastructure details.

All examples must be synthetic or based only on material that can legally be used and redistributed.

By contributing to OrbitFabric, you confirm that the contribution is your original work or material you have the legal right to contribute.

See [Clean-Room Policy](docs/CLEAN_ROOM_POLICY.md).

## Development setup

OrbitFabric requires Python 3.11 or newer.

Create a virtual environment and install the development dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Verify the CLI:

```bash
orbitfabric --version
orbitfabric --help
orbitfabric adapter --help
```

Expected version for the v1.3 baseline:

```text
orbitfabric 1.3.0
```

The generated C++17 host-build smoke target additionally requires CMake and a C++17-capable compiler.

## Required local checks

Before opening a pull request or committing a significant change, run:

```bash
ruff check .
pytest
mkdocs build --strict
```

The project CI validates Python 3.11 and Python 3.12.

For changes affecting the main Mission Data Contract workflow, also exercise the demo as appropriate:

```bash
orbitfabric lint examples/demo-3u/mission/

orbitfabric export mission-snapshot examples/demo-3u/mission/ \
  --json examples/demo-3u/generated/reports/mission_snapshot.json

orbitfabric export model-summary examples/demo-3u/mission/ \
  --json examples/demo-3u/generated/reports/model_summary.json

orbitfabric export entity-index examples/demo-3u/mission/ \
  --json examples/demo-3u/generated/reports/entity_index.json

orbitfabric export relationship-manifest examples/demo-3u/mission/ \
  --json examples/demo-3u/generated/reports/relationship_manifest.json

orbitfabric export integration-input-set examples/demo-3u/mission/ \
  --output-dir examples/demo-3u/generated/reports/integration_input

orbitfabric gen docs examples/demo-3u/mission/
orbitfabric gen data-flow examples/demo-3u/mission/
orbitfabric gen runtime examples/demo-3u/mission/
orbitfabric gen ground examples/demo-3u/mission/

orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml
orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml
```

When runtime bindings are affected, validate the generated host-build smoke target:

```bash
cmake -S examples/demo-3u/generated/runtime/cpp17 -B examples/demo-3u/generated/runtime/cpp17/build
cmake --build examples/demo-3u/generated/runtime/cpp17/build
```

When Adapter Management behavior is affected, at minimum run the relevant adapter-manager, Project Lock, release-source-attachment and Catalog tests. If the change affects a cross-repository boundary, include or update external acceptance evidence instead of relying only on synthetic Core fixtures.

## Coding style

OrbitFabric uses Python 3.11+, Pydantic v2, Typer, PyYAML, pytest and Ruff.

Prefer:

- small focused modules;
- explicit types and diagnostics;
- deterministic behavior;
- additive compatibility-safe evolution;
- tests that protect contract meaning rather than incidental formatting;
- clear ownership boundaries between Core and extensions/providers;
- documented failure behavior;
- explicit machine-readable surfaces for downstream consumers;
- fail-closed exact identity checks for Adapter Management.

Avoid:

- heavy dependencies without a clear architectural reason;
- hidden semantics in naming conventions;
- downstream reconstruction of Core semantics;
- provider-specific dependencies in Core;
- behavior hardcoded for `demo-3u`;
- user implementation code inside generated files;
- generated files committed without a deliberate reason.

## Dependency direction

The Model Layer remains the lowest semantic layer.

Representative allowed directions are:

```text
cli -> model
cli -> lint
cli -> gen
cli -> sim
cli -> export
cli -> adapter_manager

lint -> model
gen -> model
export -> model
sim -> model
RuntimeContract builder -> model
GroundContract builder -> model
adapter_manager -> Core integration/conformance contracts
```

Forbidden examples include:

```text
model -> cli
model -> sim
model -> gen
model -> export
RuntimeContract builder -> raw YAML parsing
GroundContract builder -> raw YAML parsing
external adapter -> raw YAML semantic fallback
extension output -> Core-owned semantic override
provider-specific Release Source -> Project Lock identity rewrite
adapter_manager -> GitHub-specific acquisition
plugin output -> Core-owned relationship manifest mutation
```

## Compatibility review

From v1.0.0 onward, changes to stable public surfaces are compatibility-sensitive.

A pull request must explicitly identify compatibility impact when it changes any documented stable element such as:

```text
Mission Model files or fields
field meanings or controlled values
identifier or reference rules
CLI commands or documented options
JSON report fields or result tokens
Core-owned surface kinds or version fields
lint diagnostic codes or severities
scenario expectation semantics
generated default paths
stable relationship families
Core Integration Input Set behavior
```

Candidate public surfaces also require explicit review, including:

```text
Integration Package Manifest / Result candidate contracts
Adapter Release Descriptor
Adapter Project Lock
Adapter Catalog
Adapter Manager CLI behavior
provider-neutral Release Source handoff semantics
```

Prefer additive changes where possible. A stable change that is not backward compatible requires explicit architectural justification, release notes and migration guidance.

Candidate surfaces may evolve, but their changes must still be explicit because downstream tools may already consume them.

See [Release Compatibility Policy](docs/reference/release-compatibility-policy.md).

## Generated outputs

Generated files are reproducible outputs and should normally not be committed.

For the demo mission they live under:

```text
examples/demo-3u/generated/
```

User implementation code, integration implementation code and handwritten mission logic must live outside generated output directories.

Selective golden signatures are an exception. They are committed only when they intentionally protect contract-significant fields of a stable surface.

## Commit style

Use short imperative commit messages.

Good examples:

```text
Add contact downlink consistency rules
Generate ground dictionaries
Clarify integration input compatibility
Fix scenario command validation
```

Avoid vague messages such as `updates`, `stuff`, `fixes` or `misc`.

## Pull request expectations

A good pull request should include:

- a clear description of the change;
- the affected project area or milestone;
- explicit Mission Data Contract impact;
- explicit compatibility impact for stable and candidate public surfaces;
- an architectural boundary statement for non-trivial changes;
- tests when behavior changes;
- cross-repository evidence when an external boundary changes;
- documentation when user-facing behavior changes;
- confirmation that required checks pass;
- clean-room confirmation;
- no unrelated generated artifacts.

Do not combine a compatibility-sensitive contract change with unrelated cleanup if the combination makes review harder.

## Documentation

Documentation changes are engineering changes when they define public behavior, stability, ownership or compatibility.

Keep these documents aligned when the relevant boundary changes:

```text
README.md
docs/PROJECT_CHARTER.md
docs/ARCHITECTURE.md
docs/ROADMAP.md
docs/QUICKSTART.md
docs/DEVELOPMENT.md
docs/reference/*
docs/releases/*
CHANGELOG.md
```

Historical release notes and ADRs should remain historically accurate. Current reference documents must describe the current supported baseline. Do not mechanically replace historical version references during release preparation.

## Community and security

Please also read:

- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security Policy](SECURITY.md)

Do not report security vulnerabilities or protected mission information in a public issue.
