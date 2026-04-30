<div align="center">
  <img src="assets/brand/orbitfabric-logo-horizontal-light.png" alt="OrbitFabric" width="760">
</div>

<br>

<div align="center">

**Model-first Mission Data Fabric for small spacecraft**

Define telemetry, commands, events, faults, modes, packets and operational scenarios once.  
Validate them, document them, and execute deterministic mission scenarios from the same source of truth.

</div>

---

## Overview

OrbitFabric is a **model-first Mission Data Fabric** for small spacecraft.

It lets teams define mission data contracts once, using a structured Mission Model, and then reuse that contract across validation, documentation, testing, simulation and future onboard/ground integration artifacts.

OrbitFabric is not a flight software framework, not a ground segment, and not a spacecraft dynamics simulator.

It is the contract layer between:

```text
mission design
onboard software
simulation
testing
documentation
ground integration
```

> Define once. Validate. Simulate. Test. Document. Integrate.

---

## Current Status

OrbitFabric is in early **v0.1-dev** development.

The current vertical slice is functional:

- Mission Model YAML loading;
- structural validation;
- semantic linting;
- engineering lint rules;
- JSON lint report generation;
- generated Markdown documentation;
- scenario YAML loading;
- scenario reference validation;
- deterministic scenario execution;
- simulation JSON report generation;
- simulation plain-text log generation;
- synthetic demo mission: `demo-3u`.

Current verified baseline:

```text
ruff check .  -> passing
pytest        -> 34 tests passing
```

---

## What OrbitFabric Is

OrbitFabric is a Mission Data Contract framework.

It models:

- telemetry;
- commands;
- events;
- faults;
- operational modes;
- packets;
- scenarios;
- persistence and downlink policies.

From that model, OrbitFabric currently provides:

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

---

## What OrbitFabric Is Not

OrbitFabric v0.1 is not:

- a flight-ready onboard runtime;
- a replacement for cFS or F Prime;
- a replacement for Yamcs or OpenC3;
- a spacecraft physics simulator;
- a Basilisk alternative;
- a CCSDS/PUS/CFDP implementation;
- a hardware abstraction layer;
- a CubeSat tutorial;
- a ground segment.

Those may become future integration targets or generated artifacts, but they are not the core of v0.1.

---

## Demo Mission: `demo-3u`

The repository includes a synthetic clean-room demo mission:

```text
examples/demo-3u/
├── mission/
│   ├── spacecraft.yaml
│   ├── subsystems.yaml
│   ├── modes.yaml
│   ├── telemetry.yaml
│   ├── commands.yaml
│   ├── events.yaml
│   ├── faults.yaml
│   ├── packets.yaml
│   └── policies.yaml
└── scenarios/
    └── battery_low_during_payload.yaml
```

The demo contains:

- OBC mock;
- EPS mock;
- Payload mock;
- Radio mock;
- modes: `BOOT`, `NOMINAL`, `PAYLOAD_ACTIVE`, `DEGRADED`, `SAFE`, `MAINTENANCE`;
- one executable scenario: `battery_low_during_payload`.

The scenario demonstrates:

```text
payload.start_acquisition
→ payload.acquisition_started
→ NOMINAL -> PAYLOAD_ACTIVE
→ battery voltage degradation
→ eps.battery_low
→ PAYLOAD_ACTIVE -> DEGRADED
→ payload.stop_acquisition AUTO_DISPATCHED
→ payload.acquisition_stopped
→ payload.acquisition.active = false
→ SCENARIO PASSED
```

---

## Installation for Local Development

Create and activate a Python virtual environment:

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

Expected:

```text
orbitfabric 0.1.0
```

---

## Run Mission Lint

Run semantic mission linting:

```bash
orbitfabric lint examples/demo-3u/mission/
```

Generate a machine-readable lint report:

```bash
orbitfabric lint examples/demo-3u/mission/ \
  --json generated/reports/lint_report.json
```

Expected result:

```text
Result: PASSED
```

Generated artifact:

```text
generated/reports/lint_report.json
```

---

## Generate Mission Documentation

Generate Markdown documentation from the Mission Model:

```bash
orbitfabric gen docs examples/demo-3u/mission/
```

Generated files:

```text
generated/docs/
├── telemetry.md
├── commands.md
├── events.md
├── faults.md
├── modes.md
└── packets.md
```

These files are generated from the validated Mission Model. Do not edit them manually.

---

## Run Scenario Simulation

Run the demo scenario:

```bash
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml
```

Generate both a JSON report and a plain-text timeline log:

```bash
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml \
  --json generated/reports/battery_low_during_payload_report.json \
  --log generated/logs/battery_low_during_payload.log
```

Expected result:

```text
Result: PASSED
```

Example timeline excerpt:

```text
[00:00] MODE=NOMINAL
[00:05] COMMAND payload.start_acquisition -> ACCEPTED
[00:05] EVENT payload.acquisition_started severity=INFO
[00:05] MODE TRANSITION NOMINAL -> PAYLOAD_ACTIVE reason=payload.acquisition_started
[00:30] INJECT eps.battery.voltage=6.7
[00:31] INJECT eps.battery.voltage=6.7
[00:32] INJECT eps.battery.voltage=6.7
[00:32] EVENT eps.battery_low severity=WARNING
[00:32] MODE TRANSITION PAYLOAD_ACTIVE -> DEGRADED reason=eps.battery_low_fault
[00:32] COMMAND payload.stop_acquisition -> AUTO_DISPATCHED
[00:32] EVENT payload.acquisition_stopped severity=INFO
[00:40] SCENARIO PASSED
```

Generated artifacts:

```text
generated/reports/battery_low_during_payload_report.json
generated/logs/battery_low_during_payload.log
```

---

## Run Tests

```bash
ruff check .
pytest
```

Current expected baseline:

```text
ruff check .  -> All checks passed
pytest        -> 34 passed
```

---

## Generated Artifacts

The current vertical slice can produce:

```text
generated/
├── docs/
│   ├── telemetry.md
│   ├── commands.md
│   ├── events.md
│   ├── faults.md
│   ├── modes.md
│   └── packets.md
├── reports/
│   ├── lint_report.json
│   └── battery_low_during_payload_report.json
└── logs/
    └── battery_low_during_payload.log
```

Generated artifacts are reproducible outputs. They are not the source of truth.

The source of truth remains:

```text
examples/demo-3u/mission/*.yaml
examples/demo-3u/scenarios/*.yaml
```

---

## Repository Layout

```text
orbitfabric/
├── assets/
│   └── brand/
│       ├── orbitfabric-icon.png
│       ├── orbitfabric-logo-horizontal-light.png
│       ├── orbitfabric-logo-horizontal-dark.png
│       └── orbitfabric-social-preview.png
├── docs/
├── examples/
│   └── demo-3u/
├── src/
│   └── orbitfabric/
├── tests/
└── generated/
```

---

## Documentation

Project documentation lives under:

```text
docs/
```

Useful entry points:

- `docs/PROJECT_CHARTER.md`
- `docs/CLEAN_ROOM_POLICY.md`
- `docs/ARCHITECTURE.md`
- `docs/ROADMAP.md`
- `docs/DEVELOPMENT.md`
- `docs/reference/mission-model-v0.1.md`
- `docs/adr/`

Build the documentation site locally:

```bash
mkdocs build --strict
```

Preview locally:

```bash
mkdocs serve
```

---

## Clean-Room Policy

OrbitFabric is developed as a clean-room open-source project.

Do not add:

- proprietary mission data;
- private architectures;
- private protocols;
- real operational logs;
- non-public payload details;
- real bus maps;
- real pinouts;
- employer/customer-owned code;
- NDA-protected material.

All examples must be synthetic or based on public information.

See:

```text
docs/CLEAN_ROOM_POLICY.md
```

---

## Contributing

Contributions should stay aligned with the Mission Data Contract architecture.

Before contributing, read:

```text
CONTRIBUTING.md
```

Required local checks:

```bash
ruff check .
pytest
mkdocs build --strict
```

Also verify the demo vertical slice:

```bash
orbitfabric lint examples/demo-3u/mission/ \
  --json generated/reports/lint_report.json

orbitfabric gen docs examples/demo-3u/mission/

orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml \
  --json generated/reports/battery_low_during_payload_report.json \
  --log generated/logs/battery_low_during_payload.log
```

---

## License

OrbitFabric is licensed under the Apache License 2.0.

See:

```text
LICENSE
```
