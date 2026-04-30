# Development Guide

This document explains how to work on OrbitFabric locally.

---

## Requirements

OrbitFabric currently targets:

```text
Python 3.11+
```

Development tools are installed through the project optional dependency group:

```text
.[dev]
```

---

## Setup

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Verify installation:

```bash
orbitfabric --version
orbitfabric --help
```

---

## Local Quality Checks

Run:

```bash
ruff check .
pytest
```

Expected current baseline:

```text
ruff check .  -> All checks passed
pytest        -> 34 passed
```

---

## Verify the v0.1 Vertical Slice

Run mission lint:

```bash
orbitfabric lint examples/demo-3u/mission/ \
  --json generated/reports/lint_report.json
```

Generate documentation:

```bash
orbitfabric gen docs examples/demo-3u/mission/
```

Run the scenario:

```bash
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml \
  --json generated/reports/battery_low_during_payload_report.json \
  --log generated/logs/battery_low_during_payload.log
```

Expected results:

```text
lint      -> Result: PASSED
gen docs  -> Result: PASSED
sim       -> Result: PASSED
```

---

## Generated Outputs

Generated outputs are written under:

```text
generated/
├── docs/
├── reports/
└── logs/
```

These files are reproducible outputs.

They are not the source of truth and should normally not be committed.

The source of truth is:

```text
examples/demo-3u/mission/*.yaml
examples/demo-3u/scenarios/*.yaml
```

---

## Documentation Site

Build the documentation site locally:

```bash
mkdocs build --strict
```

Preview locally:

```bash
mkdocs serve
```

---

## Recommended Development Order

For new behavior, follow this order:

```text
1. update or define the Mission Model semantics
2. add or update lint rules
3. add tests
4. update generated docs or reports if needed
5. update user-facing documentation
```

Do not add simulator behavior that is not represented in the Mission Model.

Do not add generated artifacts that bypass validation.

---

## Clean-Room Reminder

Do not use private mission data, proprietary code, private packet formats, real operational logs or NDA-protected material.

See:

```text
docs/CLEAN_ROOM_POLICY.md
```
