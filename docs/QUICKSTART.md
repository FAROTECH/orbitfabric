# Quickstart

This guide shows how to run the current OrbitFabric development preview locally.

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

The current vertical slice demonstrates:

```text
Mission Model YAML
  -> structural validation
  -> semantic lint
  -> generated Markdown docs
  -> scenario loading
  -> deterministic scenario execution
  -> JSON reports
  -> simulation log
```

OrbitFabric is not a flight software framework, not a ground segment and not a spacecraft dynamics simulator.

---

## 1. Requirements

OrbitFabric currently requires:

```text
Python 3.11 or newer
Git
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
orbitfabric 0.1.0.dev0
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

## 7. Run Mission Model lint

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

Generated output:

```text
generated/reports/lint_report.json
```

---

## 8. Generate mission documentation

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
└── packets.md
```

Generated mission documentation is derived from the validated Mission Model.

Do not edit generated files manually.

---

## 9. Run the demo scenario

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

Generated outputs:

```text
generated/reports/battery_low_during_payload_report.json
generated/logs/battery_low_during_payload.log
```

---

## 10. What this proves

The current demo proves that OrbitFabric can:

- load a multi-file YAML Mission Model;
- validate its structure;
- run semantic lint rules;
- generate Markdown documentation;
- load a scenario;
- execute a deterministic operational sequence;
- emit events;
- apply a fault-triggered mode transition;
- auto-dispatch a recovery command;
- produce JSON reports and logs.

---

## 11. What this does not prove

The current demo does not prove:

- flight readiness;
- real-time behavior;
- hardware integration;
- CCSDS, PUS or CFDP compliance;
- compatibility with cFS, F Prime, Yamcs or OpenC3;
- orbital, attitude, power or thermal dynamics;
- qualification for operational spacecraft use.

Those are intentionally outside the current v0.1.0 development preview scope.
