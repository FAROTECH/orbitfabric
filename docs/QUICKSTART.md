# Quickstart

This guide shows how to run OrbitFabric locally from the current repository baseline.

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

The current released baseline is:

```text
v0.12.0 - v1.0 Release Candidate Hardening
```

The immediate target is:

```text
v1.0.0 - Stable Mission Data Contract
```

After v0.12.0, the repository contains the v1.0 candidate alignment material needed before final release preparation:

```text
v1.0 Stable Surface Decision
v1.0 golden signatures for selected Core-owned structured surfaces
v1.0 Demo Evidence Chain
v1.0 Compatibility and Migration Notes aligned to the current candidate posture
```

This does not mean v1.0.0 has already been released.

It does not introduce new Mission Model semantics, YAML fields, CLI behavior, JSON report fields, generated Core surfaces, runtime behavior, ground behavior, schema migration tooling, JSON Schema publication, plugin discovery, plugin loading, plugin execution or tool-specific integrations.

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
orbitfabric 0.12.0
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
  --json generated/reports/lint_report.json
```

---

## 10. Export Core-owned structured surfaces

```bash
orbitfabric export model-summary examples/demo-3u/mission/ \
  --json generated/reports/model_summary.json

orbitfabric export entity-index examples/demo-3u/mission/ \
  --json generated/reports/entity_index.json

orbitfabric export relationship-manifest examples/demo-3u/mission/ \
  --json generated/reports/relationship_manifest.json
```

Generated output:

```text
generated/reports/model_summary.json
generated/reports/entity_index.json
generated/reports/relationship_manifest.json
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

## 11. Review v1.0 candidate references

Key references include:

```text
Stability and Compatibility Contract
Mission Model Stability Contract
CLI Contract v1 Preview
Generated Surfaces Stability
Extensibility Boundary Contract
v1.0 Candidate Surface Inventory
v1.0 Stable Surface Decision
v1.0 Demo Evidence Chain
Golden Output and Regression Confidence Policy
v1.0 Compatibility and Migration Notes
Lint Rule Code Stability
JSON Report Compatibility
Scenario Evidence Stability
Release Compatibility Policy
```

These references classify existing surfaces, define the extensibility boundary, record the current v1.0 candidate posture and explain what is selected, preview, disposable, internal or out of scope.

They do not introduce new Mission Model semantics, CLI behavior beyond version reporting, JSON report fields, generated surfaces, lint diagnostics, scenario behavior, migration tooling, runtime behavior, ground behavior, plugin discovery, plugin loading, plugin execution or tool-specific integrations.

---

## 12. Generate mission documentation

```bash
orbitfabric gen docs examples/demo-3u/mission/
```

Generate only the data-flow evidence reference:

```bash
orbitfabric gen data-flow examples/demo-3u/mission/ \
  --output-file generated/docs/data_flow.md
```

Generated mission documentation is derived from the validated Mission Model.

Do not edit generated files manually.

---

## 13. Generate runtime-facing contract bindings

```bash
orbitfabric gen runtime examples/demo-3u/mission/
```

The generated C++17 files are runtime-facing contract bindings.

They expose IDs, metadata, command argument structs, abstract adapter interfaces and a host-build smoke target.

They do not implement onboard behavior.

---

## 14. Validate the generated C++17 host-build smoke target

```bash
cmake -S generated/runtime/cpp17 -B generated/runtime/cpp17/build
cmake --build generated/runtime/cpp17/build
```

Expected result:

```text
build passed
```

This confirms that the generated contract-binding surface is syntactically valid and buildable as C++17 on the host.

It does not validate flight behavior.

---

## 15. Generate ground integration artifacts

```bash
orbitfabric gen ground examples/demo-3u/mission/
```

The generated ground files are ground-facing contract exports.

They are intended for engineering review, scripts and downstream integration work.

They do not implement a live ground segment, decoder, telemetry archive, database, operator console or command uplink service.

---

## 16. Run demo scenarios

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
  --json generated/reports/battery_low_during_payload_report.json \
  --log generated/logs/battery_low_during_payload.log

orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml \
  --json generated/reports/payload_data_flow_evidence_report.json \
  --log generated/logs/payload_data_flow_evidence.log
```

The data-flow evidence report traces the declared contract path:

```text
command -> data product -> storage intent -> downlink intent -> downlink flow -> contact window
```

---

## 17. What this proves

The current demo proves that OrbitFabric can:

- load a multi-file YAML Mission Model;
- validate Mission Model structure;
- run semantic lint rules;
- generate documentation;
- inspect a Mission Model summary;
- export Core-owned structured surfaces;
- validate scenarios without executing them;
- execute deterministic host-side scenario evidence;
- record contract-level data-flow evidence;
- generate runtime-facing contract bindings;
- validate generated C++17 bindings with a host-build smoke target;
- generate ground-facing contract artifacts;
- protect selected Core-owned structured surface fields with golden signatures.

---

## 18. What this does not prove

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
- released v1.0.0 compatibility;
- qualification for operational spacecraft use.

Those are intentionally outside the current scope.
