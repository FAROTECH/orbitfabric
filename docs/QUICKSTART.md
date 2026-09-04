# Quickstart

This guide shows how to run OrbitFabric locally from the current repository baseline.

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

The current public release is:

```text
v1.3.0 - Adapter Management Foundation
```

The stable Mission Data Contract commitment originated with:

```text
v1.0.0 - Stable Mission Data Contract
```

v1.2.0 extended that stable boundary additively with the Mission Snapshot and coherent Core Integration Input Set, without changing Mission Model semantics. v1.3.0 preserves those stable semantics and adds candidate operation-input and provider-neutral Adapter Management capabilities.

The v1.1.0 dashboard, scenario-run, coverage and structured-expectation surfaces remain candidate unless separately promoted. The v1.3 Adapter Management contracts and CLI surfaces also remain candidate unless separately promoted.

OrbitFabric is not a flight software framework, not a ground segment and not a spacecraft dynamics simulator.

Generated runtime-facing contract bindings are not flight software.

Generated ground integration artifacts are not ground software.

Core-owned structured surfaces are not graph engines or Studio-specific APIs. Adapter Manager does not turn Core into an in-process plugin host or a provider-specific package manager.

---

## 1. Requirements

OrbitFabric currently requires:

```text
Python 3.11 or newer
Git
```

The generated C++17 host-build smoke validation additionally requires:

```text
CMake
A C++17-capable compiler
```

The CI validates Python 3.11 and Python 3.12.

---

## 2. Clone the repository

```bash
git clone https://github.com/FAROTECH/orbitfabric.git
cd orbitfabric
```

---

## 3. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

---

## 4. Install OrbitFabric for local development

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

---

## 5. Verify the CLI

```bash
orbitfabric --version
orbitfabric --help
orbitfabric adapter --help
```

Expected current package version:

```text
orbitfabric 1.3.0
```

---

## 6. Run core checks

```bash
ruff check .
pytest
mkdocs build --strict
```

All checks should pass.

---

## 7. Inspect the demo Mission Model

```bash
orbitfabric inspect mission examples/demo-3u/mission/
```

Expected result:

```text
Result: PASSED
```

---

## 8. Validate demo scenarios without executing them

```bash
orbitfabric validate scenario examples/demo-3u/scenarios/battery_low_during_payload.yaml
orbitfabric validate scenario examples/demo-3u/scenarios/payload_data_flow_evidence.yaml
```

Expected result:

```text
Result: PASSED
```

---

## 9. Run Mission Model lint

```bash
orbitfabric lint examples/demo-3u/mission/
```

Expected result:

```text
Result: PASSED
```

Generate a JSON lint report:

```bash
orbitfabric lint examples/demo-3u/mission/ \
  --json examples/demo-3u/generated/reports/lint_report.json
```

The explicit path is preserved exactly as provided.

---

## 10. Export the stable Mission Snapshot

Export the complete loaded Mission Model through the stable Mission Snapshot surface introduced in v1.2:

```bash
orbitfabric export mission-snapshot examples/demo-3u/mission/ \
  --json examples/demo-3u/generated/reports/mission_snapshot.json
```

Generated output:

```text
examples/demo-3u/generated/reports/mission_snapshot.json
```

The Mission Snapshot answers:

```text
What complete Mission Model did Core actually load?
```

It is Core-owned, read-only and versioned. It does not replace the Mission Model as source of truth, expose a YAML AST, provide source editing semantics, expose a partial semantic model after structural load failure or define a Studio-specific API.

Its existing `snapshot_version = 0.1-candidate` format identifier is intentionally retained; v1.2 stability classification and format-version text are separate compatibility concepts.

---

## 11. Export stable Core-owned structured surfaces

```bash
orbitfabric export model-summary examples/demo-3u/mission/ \
  --json examples/demo-3u/generated/reports/model_summary.json

orbitfabric export entity-index examples/demo-3u/mission/ \
  --json examples/demo-3u/generated/reports/entity_index.json

orbitfabric export relationship-manifest examples/demo-3u/mission/ \
  --json examples/demo-3u/generated/reports/relationship_manifest.json
```

Generated output:

```text
examples/demo-3u/generated/reports/model_summary.json
examples/demo-3u/generated/reports/entity_index.json
examples/demo-3u/generated/reports/relationship_manifest.json
```

These surfaces answer:

```text
model_summary.json          -> What contract domains are present?
entity_index.json           -> What contract entities are defined?
relationship_manifest.json  -> Which admitted explicit relationships connect them?
```

The seven FDIR-oriented relationship families admitted in v1.2 are additive stable-compatible families derived from explicit Mission Model fields. Compatible consumers must not guess semantics for unknown additive relationship types.

---

## 12. Export the stable coherent Core Integration Input Set

For external ecosystem integration, use the single coherent export operation:

```bash
orbitfabric export integration-input-set examples/demo-3u/mission/ \
  --output-dir examples/demo-3u/generated/reports/integration_input
```

The output directory contains:

```text
integration_input_manifest.json
mission_snapshot.json
entity_index.json
relationship_manifest.json
lint_report.json
model_summary.json
```

Core performs one logical load/lint operation, writes exact surface digests, computes the RFC 8785/JCS-based `input_set_sha256` and publishes the manifest last.

A directory without a valid Integration Input Manifest is not a coherent Integration Input Set.

External adapters must reject incompatible required surfaces and must not fall back to reparsing Mission Model YAML.

The existing `input_set_version = 0.1-candidate` identifier is retained for compatibility with the reference-proven producer/consumer chain.

---

## 13. Export v1.1 candidate Core-owned inspection surfaces

```bash
orbitfabric export dashboard-summary examples/demo-3u/mission/

orbitfabric export scenario-run-index \
  --simulation-reports examples/demo-3u/generated/reports \
  --json examples/demo-3u/generated/reports/scenario_run_index.json

orbitfabric export coverage-summary examples/demo-3u/mission/
```

With omitted output paths, mission-based commands write under the mission workspace:

```text
examples/demo-3u/generated/reports/dashboard_summary.json
examples/demo-3u/generated/reports/coverage_summary.json
```

`scenario_run_index.json` is emitted to the explicit `--json` path shown above.

These v1.1.0 surfaces remain Core-owned candidate inspection surfaces after v1.3.0.

---

## 14. Inspect the candidate Adapter Management CLI

v1.3.0 adds a provider-neutral candidate Adapter Management surface to Core.

Start by inspecting the available commands:

```bash
orbitfabric adapter --help
orbitfabric adapter lock --help
orbitfabric adapter catalog --help
```

The Core-owned Catalog commands operate on a local Catalog file:

```text
orbitfabric adapter catalog validate <catalog.json>
orbitfabric adapter catalog list <catalog.json>
orbitfabric adapter catalog select <catalog.json> <SOURCE_COORDINATE> --version <EXACT_VERSION>
```

Core does not fetch a remote Catalog or dispatch provider implementations. Provider-specific acquisition is handled by separate Release Source products, which hand a verified `ResolvedAdapterRelease` into the Core lifecycle.

The exact desired/actual state split is:

```text
Adapter Project Lock     project-scoped exact desired state
Installed Adapter State user-scoped actual state
```

See the Adapter Manager, Adapter Project Lock, explicit-source install-from-lock and Adapter Catalog reference pages before using these candidate surfaces in production workflows.

---

## 15. Review stable and candidate references

Key references include:

```text
Stability and Compatibility Contract
Mission Model Stability Contract
Release Compatibility Policy
v1.0 Stable Surface Decision
v1.0 Demo Evidence Chain
Golden Output and Regression Confidence Policy
v1.0 Compatibility and Migration Notes
v1.2 Integration Input Stability Decision
Post-v1 Integration Surface Classification
Mission Snapshot Surface
Core Integration Input Contract
Relationship Manifest Surface
Projection Profile Contract
Integration Result Contract
Integration Package and Adapter Execution Contract
Integration Operation-Input Contract v1
Adapter Manager M0
Adapter Project Lock M1
Explicit-Source Install from Adapter Project Lock
Adapter Catalog CLI
Dashboard Summary Surface
Scenario Run Index Surface
Coverage Summary Surface
```

These references separate stable Core-owned contracts from candidate Core inspection, integration-extension and Adapter Management surfaces.

They do not introduce flight runtime behavior, ground runtime behavior, provider-specific acquisition inside Core or in-process third-party adapter loading.

---

## 16. Generate mission documentation

```bash
orbitfabric gen docs examples/demo-3u/mission/
```

Generate only the data-flow evidence reference:

```bash
orbitfabric gen data-flow examples/demo-3u/mission/ \
  --output-file examples/demo-3u/generated/docs/data_flow.md
```

Generated mission documentation is derived from the validated Mission Model.

Do not edit generated files manually.

---

## 17. Generate runtime-facing contract bindings

```bash
orbitfabric gen runtime examples/demo-3u/mission/
```

The generated C++17 files are runtime-facing contract bindings. They expose IDs, metadata, command argument structs, abstract adapter interfaces and a host-build smoke target.

They do not implement onboard behavior.

---

## 18. Validate the generated C++17 host-build smoke target

```bash
cmake -S examples/demo-3u/generated/runtime/cpp17 -B examples/demo-3u/generated/runtime/cpp17/build
cmake --build examples/demo-3u/generated/runtime/cpp17/build
```

Expected result:

```text
build passed
```

This confirms that the generated contract-binding surface is syntactically valid and buildable as C++17 on the host. It does not validate flight behavior.

---

## 19. Generate ground integration artifacts

```bash
orbitfabric gen ground examples/demo-3u/mission/
```

The generated ground files are ground-facing contract exports. They are intended for engineering review, scripts and downstream integration work.

They do not implement a live ground segment, decoder, telemetry archive, database, operator console or command uplink service.

---

## 20. Run demo scenarios

```bash
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml
orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml
```

Expected result:

```text
Result: PASSED
```

Generate JSON reports and timeline logs:

```bash
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml \
  --json examples/demo-3u/generated/reports/battery_low_during_payload_report.json \
  --log examples/demo-3u/generated/logs/battery_low_during_payload.log

orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml \
  --json examples/demo-3u/generated/reports/payload_data_flow_evidence_report.json \
  --log examples/demo-3u/generated/logs/payload_data_flow_evidence.log
```

The data-flow evidence report traces the declared contract path:

```text
command -> data product -> storage intent -> downlink intent -> downlink flow -> contact window
```

The v1.1.0 simulation JSON structured expectation accounting remains additive and candidate. The legacy top-level `failed_expectations` compatibility list remains available.

---

## 21. What this proves

The current repository baseline proves that OrbitFabric Core can:

- load a multi-file YAML Mission Model;
- validate Mission Model structure;
- run semantic lint rules;
- generate documentation;
- export stable Mission Snapshot, Model Summary, Entity Index and Relationship Manifest surfaces;
- emit additive stable-compatible FDIR relationship families;
- export one coherent stable Core Integration Input Set;
- export candidate dashboard/scenario-run/coverage inspection surfaces;
- validate scenarios without executing them;
- execute deterministic host-side scenario evidence;
- record contract-level data-flow evidence;
- generate runtime-facing contract bindings;
- validate generated C++17 bindings with a host-build smoke target;
- generate ground-facing contract artifacts;
- validate candidate operation-input integration contracts;
- manage exact adapter desired/actual state through candidate provider-neutral Adapter Management contracts;
- protect selected Core-owned structured surface fields with golden signatures.

The broader Integration Framework is reference-proven through external adapter repositories and an independent Studio consumer, while target-specific contracts remain extension-owned. Provider-specific Catalog acquisition proofs also live outside Core.

---

## 22. What this does not prove

The built-in demo does not itself prove:

- flight readiness;
- real-time behavior;
- hardware integration;
- real onboard storage or downlink execution;
- real contact scheduling;
- orbit propagation;
- RF link budget simulation;
- CCSDS, PUS or CFDP compliance;
- compatibility with any particular downstream framework solely from this Core demo;
- XTCE compliance;
- binary decoder or encoder behavior;
- command uplink behavior;
- telemetry archive/database/operator-console behavior;
- HAL or RTOS integration;
- relationship or dependency graph behavior;
- Core in-process third-party adapter discovery/loading/execution;
- provider-neutral provider dispatch, version-range solving or automatic adapter upgrades;
- qualification for operational spacecraft use.

Downstream-specific compatibility is demonstrated and maintained in the corresponding external adapter/integration repositories, not inferred from this Core demo.
