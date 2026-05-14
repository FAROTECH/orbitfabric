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
  -> JSON lint reports
  -> JSON simulation reports with data-flow evidence
  -> simulation logs
```

OrbitFabric is not a flight software framework, not a ground segment and not a spacecraft dynamics simulator.

Generated runtime-facing contract bindings are not flight software.

Generated ground integration artifacts are not ground software.

Contract introspection surfaces are not plugin APIs, relationship graphs or Studio-specific APIs.

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

Expected version for the current development preview:

```text
orbitfabric 0.8.1
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

## 10. Export the model summary

```bash
orbitfabric export model-summary examples/demo-3u/mission/ \
  --json generated/reports/model_summary.json
```

Generated output:

```text
generated/reports/model_summary.json
```

This report is the first Core-owned Contract Introspection Surface.

It answers:

```text
What contract domains are present in this mission?
```

It does not expose entity records, relationship graphs, plugin APIs or Studio-specific APIs.

---

## 11. Generate mission documentation

```bash
orbitfabric gen docs examples/demo-3u/mission/
```

Generated output:

```text
generated/docs/
├── telemetry.md
├── commands.md
├── events.md
├── faults.md
├── modes.md
├── packets.md
├── payloads.md
├── data_products.md
├── contacts.md
├── commandability.md
└── data_flow.md
```

Generate only the data-flow evidence reference:

```bash
orbitfabric gen data-flow examples/demo-3u/mission/ \
  --output-file generated/docs/data_flow.md
```

Generated mission documentation is derived from the validated Mission Model.

Do not edit generated files manually.

---

## 12. Generate runtime-facing contract bindings

```bash
orbitfabric gen runtime examples/demo-3u/mission/
```

Generated output:

```text
generated/runtime/cpp17/
├── runtime_contract_manifest.json
├── CMakeLists.txt
├── include/orbitfabric/generated/
│   ├── mission_ids.hpp
│   ├── mission_enums.hpp
│   ├── mission_registries.hpp
│   ├── command_args.hpp
│   └── adapter_interfaces.hpp
└── src/
    └── orbitfabric_runtime_contract_smoke.cpp
```

The generated C++17 files are runtime-facing contract bindings.

They expose IDs, metadata, command argument structs, abstract adapter interfaces and a host-build smoke target.

They do not implement onboard behavior.

---

## 13. Validate the generated C++17 host-build smoke target

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

## 14. Generate ground integration artifacts

```bash
orbitfabric gen ground examples/demo-3u/mission/
```

Generated output:

```text
generated/ground/generic/
├── ground_contract_manifest.json
├── README.md
├── dictionaries/
│   ├── telemetry_dictionary.json
│   ├── command_dictionary.json
│   ├── event_dictionary.json
│   ├── fault_dictionary.json
│   ├── data_product_dictionary.json
│   └── packet_dictionary.json
├── csv/
│   ├── telemetry_dictionary.csv
│   ├── command_dictionary.csv
│   ├── event_dictionary.csv
│   ├── fault_dictionary.csv
│   ├── data_product_dictionary.csv
│   └── packet_dictionary.csv
└── ground_dictionaries.md
```

The generated ground files are ground-facing contract exports.

They are intended for engineering review, scripts and downstream integration work.

They do not implement a live ground segment, decoder, telemetry archive, database, operator console or command uplink service.

---

## 15. Run the battery-low demo scenario

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

## 16. Run the data-flow evidence scenario

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

## 17. What this proves

The current demo proves that OrbitFabric can:

- load a multi-file YAML Mission Model;
- load optional `payloads.yaml`, `data_products.yaml`, `contacts.yaml` and `commandability.yaml` domains;
- validate Mission Model structure;
- run semantic lint rules;
- generate Markdown documentation;
- inspect a Mission Model summary;
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
- export a deterministic Core-owned model summary report for downstream inspection tools.

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
- orbital, attitude, power or thermal dynamics;
- command dispatch runtime behavior;
- telemetry polling runtime behavior;
- HAL or RTOS integration;
- entity indexing;
- relationship graph export;
- plugin API behavior;
- qualification for operational spacecraft use.

Those are intentionally outside the current development preview scope.
