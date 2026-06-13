# Quickstart

This guide shows how to run OrbitFabric locally from the current repository baseline.

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

The current public release is:

```text
v1.1.0 - Candidate Integration Surface Consolidation
```

The stable Mission Data Contract baseline remains:

```text
v1.0.0 - Stable Mission Data Contract
```

v1.1.0 consolidates post-v1 Core-owned candidate integration surfaces while preserving the deliberately narrow v1.0.0 stable surface around the Mission Model, validation, linting, scenario evidence, machine-readable JSON reports, Core-owned structured surfaces, release compatibility governance and the extensibility boundary.

OrbitFabric is not a flight software framework, not a ground segment and not a spacecraft dynamics simulator.

Generated runtime-facing contract bindings are not flight software.

Generated ground integration artifacts are not ground software.

Core-owned structured surfaces are not plugin APIs, graph engines or Studio-specific APIs.

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
```

Expected current package version:

```text
orbitfabric 1.1.0
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

## 10. Export v1.0 stable Core-owned structured surfaces

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
relationship_manifest.json  -> How are indexed contract entities related?
```

They are Core-owned, read-only and derived from the validated Mission Model.

They do not expose plugin execution, graph engines, Studio-specific APIs, runtime behavior or ground behavior.

---

## 11. Export v1.1 candidate Core-owned integration surfaces

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

These v1.1.0 surfaces are Core-owned candidate integration surfaces. They are not promoted to the original v1.0.0 stable compatibility class.

---

## 12. Review v1.0 and v1.1 references

Key references include:

```text
Stability and Compatibility Contract
Mission Model Stability Contract
CLI Contract v1 Preview
Generated Surfaces Stability
Extensibility Boundary Contract
v1.0 Stable Surface Decision
v1.0 Demo Evidence Chain
Golden Output and Regression Confidence Policy
v1.0 Compatibility and Migration Notes
Post-v1 Candidate Integration Surfaces
Dashboard Summary Surface
Scenario Run Index Surface
Coverage Summary Surface
Lint Rule Code Stability
JSON Report Compatibility
Scenario Evidence Stability
Release Compatibility Policy
```

These references classify stable and candidate surfaces, define the extensibility boundary, record the v1.0 stable posture and explain what is stable, candidate, preview, disposable, internal or out of scope.

They do not introduce new Mission Model semantics, runtime behavior, ground behavior, plugin discovery, plugin loading, plugin execution or tool-specific integrations.

---

## 13. Generate mission documentation

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

## 14. Generate runtime-facing contract bindings

```bash
orbitfabric gen runtime examples/demo-3u/mission/
```

The generated C++17 files are runtime-facing contract bindings.

They expose IDs, metadata, command argument structs, abstract adapter interfaces and a host-build smoke target.

They do not implement onboard behavior.

---

## 15. Validate the generated C++17 host-build smoke target

```bash
cmake -S examples/demo-3u/generated/runtime/cpp17 -B examples/demo-3u/generated/runtime/cpp17/build
cmake --build examples/demo-3u/generated/runtime/cpp17/build
```

Expected result:

```text
build passed
```

This confirms that the generated contract-binding surface is syntactically valid and buildable as C++17 on the host.

It does not validate flight behavior.

---

## 16. Generate ground integration artifacts

```bash
orbitfabric gen ground examples/demo-3u/mission/
```

The generated ground files are ground-facing contract exports.

They are intended for engineering review, scripts and downstream integration work.

They do not implement a live ground segment, decoder, telemetry archive, database, operator console or command uplink service.

---

## 17. Run demo scenarios

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

The v1.1.0 simulation JSON structured expectation accounting is additive. The legacy top-level `failed_expectations` compatibility list remains available.

---

## 18. What this proves

The current demo proves that OrbitFabric can:

- load a multi-file YAML Mission Model;
- validate Mission Model structure;
- run semantic lint rules;
- generate documentation;
- inspect a Mission Model summary;
- export v1.0 stable Core-owned structured surfaces;
- export v1.1 candidate Core-owned integration surfaces;
- validate scenarios without executing them;
- execute deterministic host-side scenario evidence;
- record contract-level data-flow evidence;
- generate runtime-facing contract bindings;
- validate generated C++17 bindings with a host-build smoke target;
- generate ground-facing contract artifacts;
- protect selected Core-owned structured surface fields with golden signatures.

---

## 19. What this does not prove

The current demo does not prove:

- flight readiness;
- real-time behavior;
- hardware integration;
- real onboard storage execution;
- real downlink execution;
- real contact scheduling;
- orbit propagation;
- RF link budget simulation;
- CCSDS, PUS or CFDP compliance;
- compatibility with cFS, F Prime, Yamcs or OpenC3;
- XTCE compliance;
- binary decoder behavior;
- command uplink behavior;
- telemetry archive behavior;
- database behavior;
- operator console behavior;
- command dispatch runtime behavior;
- telemetry polling runtime behavior;
- HAL or RTOS integration;
- relationship graph behavior;
- dependency graph behavior;
- plugin API behavior;
- plugin discovery behavior;
- plugin loading behavior;
- plugin execution behavior;
- qualification for operational spacecraft use.

Those are intentionally outside the current scope.
