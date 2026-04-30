# Contributing to OrbitFabric

Thank you for your interest in OrbitFabric.

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

The project is currently in early v0.1-dev development. Contributions should stay focused, small and aligned with the Mission Data Contract architecture.

---

## Current Project Focus

The current priority is to stabilize the v0.1 vertical slice:

```text
Mission Model YAML
  -> structural validation
  -> semantic lint
  -> JSON lint report
  -> generated Markdown docs
  -> scenario loading
  -> deterministic scenario execution
  -> simulation JSON report
  -> simulation log file
```

Do not add large integrations before the core is stable.

Out of scope for v0.1:

- flight runtime;
- hardware drivers;
- RTOS integration;
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

---

## Required Local Checks

Before opening a pull request or committing significant changes, run:

```bash
ruff check .
pytest
```

Then verify the demo vertical slice:

```bash
orbitfabric lint examples/demo-3u/mission/ \
  --json generated/reports/lint_report.json

orbitfabric gen docs examples/demo-3u/mission/

orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml \
  --json generated/reports/battery_low_during_payload_report.json \
  --log generated/logs/battery_low_during_payload.log
```

Expected result:

```text
ruff check .  -> All checks passed
pytest        -> passing
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
Add scenario JSON report generation
Add engineering lint rules
Document v0.1 vertical slice
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

---

## License

By contributing, you agree that your contributions will be licensed under the project license:

```text
Apache-2.0
```
