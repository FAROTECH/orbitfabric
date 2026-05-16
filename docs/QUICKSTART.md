# Quickstart

This guide shows how to run the current OrbitFabric development preview locally.

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

The current vertical slice demonstrates:

```text
Mission Model YAML
  -> structural validation
  -> semantic lint
  -> generated Markdown docs
  -> mission inspection
  -> scenario validation
  -> deterministic scenario execution
  -> Payload Contract documentation
  -> Data Product Contract documentation
  -> Contact and Downlink Contract documentation
  -> Commandability and Autonomy Contract documentation
  -> Data Flow Evidence documentation
  -> RuntimeContract generation
  -> C++17 runtime-facing contract bindings
  -> C++17 host-build smoke validation
  -> GroundContract generation
  -> ground-facing JSON dictionaries
  -> ground-facing CSV dictionaries
  -> human-reviewable ground Markdown artifacts
  -> model_summary.json contract introspection report
  -> entity_index.json entity index report
  -> relationship_manifest.json candidate relationship report
  -> stability and compatibility classification references
  -> JSON lint reports
  -> JSON simulation reports with data-flow evidence
  -> simulation logs
```

OrbitFabric is not a flight software framework, not a ground segment and not a spacecraft dynamics simulator.

Generated runtime-facing contract bindings are not flight software.

Generated ground integration artifacts are not ground software.

Contract introspection, entity index and relationship manifest surfaces are not plugin APIs, graph engines or Studio-specific APIs.

Compatibility classification references are not runtime behavior, ground behavior, schema migration tooling, plugin execution or a v1.0 stability guarantee.

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

Expected version:

```text
orbitfabric 0.10.0
```

---

## 6. Run code quality checks

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

Generate the domain-level model summary:

```bash
orbitfabric export model-summary examples/demo-3u/mission/ \
  --json generated/reports/model_summary.json
```

Generate the entity-level index:

```bash
orbitfabric export entity-index examples/demo-3u/mission/ \
  --json generated/reports/entity_index.json
```

Generate the relationship-level manifest:

```bash
orbitfabric export relationship-manifest examples/demo-3u/mission/ \
  --json generated/reports/relationship_manifest.json
```

Generated output:

```text
generated/reports/model_summary.json
generated/reports/entity_index.json
generated/reports/relationship_manifest.json
```

`model_summary.json` answers:

```text
What contract domains are present in this mission?
```

`entity_index.json` answers:

```text
What contract entities are defined in this mission?
```

`relationship_manifest.json` answers:

```text
How are indexed mission contract entities related?
```

These surfaces are Core-owned, read-only and derived from the loaded Mission Model.

They do not expose plugin execution, graph engines, Studio-specific APIs, runtime behavior or ground behavior.

---

## 11. Review compatibility classification references

v0.10.0 adds compatibility classification references for the path toward v1.0.0.

Key references include:

```text
Stability and Compatibility Contract
Mission Model Stability Contract
CLI Contract v1 Preview
Generated Surfaces Stability
Lint Rule Code Stability
JSON Report Compatibility
Scenario Evidence Stability
Release Compatibility Policy
```

These references classify existing public and preview surfaces.

They do not introduce new Mission Model semantics, CLI behavior, JSON report fields, generated surfaces, lint diagnostics, scenario behavior, plugin execution, runtime behavior, ground behavior or a stable v1.0 compatibility guarantee.

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

After generating runtime bindings, run:

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

## 16. Run the battery-low demo scenario

```bash
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml
```

Expected result:

```text
Result: PASSED
```

Generate both JSON report and timeline log:

```bash
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml \
  --json generated/reports/battery_low_during_payload_report.json \
  --log generated/logs/battery_low_during_payload.log
```

---

## 17. Run the data-flow evidence scenario

```bash
orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml
```

Expected result:

```text
Result: PASSED
```

Generate both JSON report and timeline log:

```bash
orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml \
  --json generated/reports/payload_data_flow_evidence_report.json \
  --log generated/logs/payload_data_flow_evidence.log
```

The JSON report includes a `data_flow_evidence` section tracing the declared contract path:

```text
command -> data product -> storage intent -> downlink intent -> downlink flow -> contact window
```

---

## 18. What this proves

The current demo proves that OrbitFabric can:

- load a multi-file YAML Mission Model;
- load optional `payloads.yaml`, `data_products.yaml`, `contacts.yaml` and `commandability.yaml` domains;
- validate Mission Model structure;
- run semantic lint rules;
- generate Markdown documentation;
- inspect a Mission Model summary;
- export a model summary from the loaded Mission Model;
- export an entity index from the loaded Mission Model;
- export a relationship manifest from the loaded Mission Model;
- classify public, preview, candidate, generated and internal compatibility surfaces;
- validate scenarios without executing them;
- execute deterministic operational sequences;
- record contract-level data-flow evidence;
- assert command-to-data-product-to-contact evidence in a scenario;
- produce JSON reports and logs;
- build a RuntimeContract from the validated Mission Model;
- generate deterministic C++17 runtime-facing contract bindings;
- validate generated C++17 contract bindings with a host-build smoke target;
- build a GroundContract from the validated Mission Model;
- generate deterministic JSON, CSV and Markdown ground-facing contract artifacts;
- export deterministic Core-owned structured surfaces for downstream inspection tools.

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
- orbital, attitude, power or thermal dynamics;
- command dispatch runtime behavior;
- telemetry polling runtime behavior;
- HAL or RTOS integration;
- relationship graph behavior;
- dependency graph behavior;
- plugin API behavior;
- plugin execution behavior;
- v1.0 compatibility guarantee;
- qualification for operational spacecraft use.

Those are intentionally outside the current development preview scope.
