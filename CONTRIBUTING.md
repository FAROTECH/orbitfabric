# Contributing to OrbitFabric

Thank you for your interest in OrbitFabric.

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

The project is currently in pre-1.0 development. Contributions should stay focused, small and aligned with the Mission Data Contract architecture.

---

## Current Project Focus

The current public baseline is `v0.4.0 — Contact Windows and Downlink Flow Contracts`.

The next development focus is `v0.5 — Commandability and Autonomy Contracts`.

The current baseline proves this Mission Data Chain:

```text
Payload Contract
  -> Data Product Contract
  -> Storage Intent
  -> Downlink Intent
  -> Contact Window Assumption
  -> Downlink Flow Contract
```

Do not add large integrations before the contract model is coherent.

Out of scope for the current preview:

- flight runtime;
- hardware drivers;
- RTOS integration;
- real onboard storage runtime;
- real downlink runtime;
- real contact scheduling;
- command uplink runtime;
- flight autonomy runtime;
- operator console;
- CCSDS/PUS/CFDP implementation;
- Yamcs/OpenC3 full integration;
- Basilisk integration;
- cFS/F Prime bridge;
- web UI;
- database-backed telemetry archive;
- real spacecraft data.

---

## Clean-Room Requirement

OrbitFabric is developed as a clean-room open-source project.

Do not contribute:

- proprietary mission data;
- private architecture details;
- private packet formats;
- real operational logs;
- real anomaly timelines;
- non-public payload details;
- real bus maps;
- real pinouts;
- employer-owned code;
- customer-owned code;
- NDA-protected material;
- export-controlled material.

All examples must be synthetic or based on public information.

By contributing to OrbitFabric, you confirm that your contribution is your original work or is based only on material you have the legal right to contribute, and that it does not contain confidential, proprietary, export-controlled or NDA-protected information.

See:

```text
docs/CLEAN_ROOM_POLICY.md
```

---

## Development Setup

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Verify the CLI:

```bash
orbitfabric --version
orbitfabric --help
```

Expected current version:

```text
orbitfabric 0.4.0
```

---

## Required Local Checks

Before opening a pull request or committing significant changes, run:

```bash
ruff check .
pytest
mkdocs build --strict
```

Then verify the demo vertical slice:

```bash
orbitfabric lint examples/demo-3u/mission/   --json generated/reports/lint_report.json

orbitfabric gen docs examples/demo-3u/mission/

orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml   --json generated/reports/battery_low_during_payload_report.json   --log generated/logs/battery_low_during_payload.log
```

Expected result:

```text
ruff check .  -> All checks passed
pytest        -> passing
mkdocs        -> passing
lint          -> Result: PASSED
gen docs      -> Result: PASSED
sim           -> Result: PASSED
```

---

## Coding Style

OrbitFabric uses:

- Python 3.11+;
- Pydantic v2;
- Typer;
- PyYAML;
- pytest;
- ruff.

Rules:

- keep modules small;
- keep the Mission Model as the source of truth;
- do not parse YAML independently in generators or simulators;
- consume validated model objects;
- prefer explicit diagnostics;
- write tests for new lint rules, generators and simulator behavior;
- do not introduce heavy dependencies without a clear reason.

---

## Architecture Rules

The Model Layer is the lowest stable layer.

Allowed dependency direction:

```text
cli -> model
cli -> lint
cli -> gen
cli -> sim

lint -> model
gen -> model
sim -> model
```

Forbidden patterns:

```text
model -> cli
model -> sim
model -> gen
lint -> sim
gen -> sim
sim -> gen
```

Do not hardcode behavior for `demo-3u` inside the framework core.

---

## Commit Style

Use short imperative commit messages.

Good examples:

```text
Add contact downlink consistency rules
Generate contact downlink documentation
Align public documentation with v0.4
Fix scenario command validation
```

Avoid vague messages:

```text
updates
stuff
fixes
misc
```

---

## Pull Request Expectations

A good pull request should include:

- a clear description of the change;
- tests when behavior changes;
- updated documentation when user-facing behavior changes;
- confirmation that local checks pass;
- no generated artifacts unless explicitly required.

Generated outputs under `generated/` are reproducible artifacts and should normally not be committed.
