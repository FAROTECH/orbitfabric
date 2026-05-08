<div align="center">
  <img src="assets/brand/orbitfabric-logo-horizontal-light.png" alt="OrbitFabric" width="760">
</div>

<br>

<div align="center">

**Model-first Mission Data Fabric for small spacecraft**

Define telemetry, commands, events, faults, modes, packets, payload contracts, data products, contact/downlink assumptions, commandability/autonomy contracts and operational scenarios once.
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

OrbitFabric is currently at `v0.6.0 — End-to-End Mission Data Flow Evidence`.

The current repository includes:

- the `v0.2.1 — Payload Contract Model` vertical slice;
- the `v0.2.3 — Mission Data Chain Roadmap Alignment` direction;
- the `v0.3.0 — Data Product and Storage Contracts` vertical slice;
- the `v0.4.0 — Contact Windows and Downlink Flow Contracts` vertical slice;
- the `v0.5.0 — Commandability and Autonomy Contracts` vertical slice;
- the `v0.6.0 — End-to-End Mission Data Flow Evidence` vertical slice.

The current vertical slice is functional:

- Mission Model YAML loading;
- optional `payloads.yaml` loading;
- optional `data_products.yaml` loading;
- optional `contacts.yaml` loading;
- optional `commandability.yaml` loading;
- structural validation;
- semantic linting;
- engineering lint rules;
- payload contract lint rules;
- data product contract lint rules;
- contact/downlink contract lint rules;
- commandability/autonomy contract lint rules;
- command-declared data product effect linting;
- scenario data-flow expectation reference validation;
- JSON lint report generation;
- generated Markdown documentation;
- generated payload contract documentation;
- generated data product contract documentation;
- generated contact/downlink contract documentation;
- generated commandability/autonomy contract documentation;
- generated data-flow evidence documentation;
- scenario YAML loading;
- scenario reference validation;
- deterministic scenario execution;
- minimal payload lifecycle simulation;
- contract-level data-flow evidence recording;
- simulation JSON report generation with `data_flow_evidence`;
- simulation plain-text log generation;
- synthetic demo mission: `demo-3u`.

The repository also includes a growing set of example mission slices:

- `examples/demo-3u/` — synthetic clean-room demo mission;
- `examples/university-cubesat-minislice/` — generic university CubeSat minislice;
- `examples/oresat-inspired-minislice/` — public-material-derived low-power / beacon / constrained-downlink minislice;
- `examples/finch-inspired-minislice/` — public-material-derived imaging acquisition / ADCS readiness / compression / constrained-downlink minislice;
- `examples/spacelab-inspired-communications-minislice/` — public-material-derived TT&C / OBDH / beacon / telecommanded data-request / decoder-evidence minislice.

The `*-inspired-*` examples are conceptual public demos. They are not official models, not endorsed by the original project teams, and do not imply adoption of OrbitFabric by those teams.

Current verified baseline:

```text
ruff check .
-> passing

pytest
-> passing

mkdocs build --strict
-> passing
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
- persistence and downlink policies;
- optional Payload / IOD Payload Contracts;
- optional Data Product and Storage Contracts;
- optional Contact Windows and Downlink Flow Contracts;
- optional Commandability and Autonomy Contracts;
- contract-level Mission Data Flow Evidence.

The v0.6 data-flow evidence chain connects:

```text
command expected effect
        -> data product
        -> storage intent
        -> downlink intent
        -> eligible downlink flow
        -> matching contact window
        -> scenario evidence
        -> generated documentation
        -> JSON report evidence
```

Payload, Data Product, Contact/Downlink, Commandability/Autonomy and Data-Flow Evidence Contracts are part of the Mission Data Contract. They do not describe payload firmware, payload drivers, hardware buses, onboard services, physical payload simulation, real storage execution, real contact scheduling, real downlink runtime behavior, live uplink services, operator authentication, command queues, onboard schedulers, autonomy runtime or real FDIR behavior.

---

## What OrbitFabric Is Not

OrbitFabric is not:

- a flight-ready onboard runtime;
- a replacement for cFS or F Prime;
- a replacement for Yamcs or OpenC3;
- a spacecraft physics simulator;
- a Basilisk alternative;
- a CCSDS/PUS/CFDP implementation;
- a hardware abstraction layer;
- a CubeSat tutorial;
- a ground segment;
- a payload firmware framework;
- a payload driver framework;
- a payload physical simulator;
- a payload data processing pipeline;
- an onboard storage runtime;
- a downlink runtime;
- an orbit propagator;
- an RF/link budget simulator;
- a real contact scheduler;
- a runtime skeleton generator in v0.6.

Those may become future integration targets or generated artifacts, but they are not part of the current development preview.

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
│   ├── policies.yaml
│   ├── payloads.yaml
│   ├── data_products.yaml
│   ├── contacts.yaml
│   └── commandability.yaml
└── scenarios/
    ├── battery_low_during_payload.yaml
    ├── nominal_payload_acquisition.yaml
    └── payload_data_flow_evidence.yaml
```

The demo includes:

```text
Payload Contract
        -> Data Product Contract
        -> Storage Intent
        -> Downlink Intent
        -> Contact Window Assumption
        -> Downlink Flow Contract
        -> Commandability and Autonomy Contract
        -> End-to-End Mission Data Flow Evidence
```

The dedicated v0.6 scenario demonstrates:

```text
payload.start_acquisition
        -> payload.acquisition_started
        -> payload lifecycle ACQUIRING
        -> payload.acquisition.active = true
        -> payload.radiation_histogram evidence recorded
        -> storage intent declared
        -> downlink intent declared
        -> science_next_available_contact eligible
        -> demo_contact_001 matched
        -> DATA_FLOW expectation met
        -> SCENARIO PASSED
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
orbitfabric 0.6.0
```

---

## Run Mission Lint

```bash
orbitfabric lint examples/demo-3u/mission/ \
  --json generated/reports/lint_report.json
```

Expected result:

```text
Result: PASSED
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
├── packets.md
├── payloads.md
├── data_products.md
├── contacts.md
├── commandability.md
└── data_flow.md
```

A dedicated data-flow generator is also available:

```bash
orbitfabric gen data-flow examples/demo-3u/mission/ \
  --output-file generated/docs/data_flow.md
```

Generated files are derived from the validated Mission Model. Do not edit them manually.

---

## Run Scenario Simulation

Run the battery-low recovery scenario:

```bash
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml \
  --json generated/reports/battery_low_during_payload_report.json \
  --log generated/logs/battery_low_during_payload.log
```

Run the v0.6 data-flow evidence scenario:

```bash
orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml \
  --json generated/reports/payload_data_flow_evidence_report.json \
  --log generated/logs/payload_data_flow_evidence.log
```

Expected result:

```text
Result: PASSED
```

---

## Run Tests

```bash
ruff check .
pytest
mkdocs build --strict
```

Current expected baseline:

```text
ruff check .           -> All checks passed
pytest                 -> passing
mkdocs build --strict  -> passing
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
│   ├── packets.md
│   ├── payloads.md
│   ├── data_products.md
│   ├── contacts.md
│   ├── commandability.md
│   └── data_flow.md
├── reports/
│   ├── lint_report.json
│   ├── battery_low_during_payload_report.json
│   └── payload_data_flow_evidence_report.json
└── logs/
    ├── battery_low_during_payload.log
    └── payload_data_flow_evidence.log
```

Generated artifacts are reproducible outputs. They are not the source of truth.

The source of truth remains:

```text
examples/demo-3u/mission/*.yaml
examples/demo-3u/scenarios/*.yaml
```

---

## Documentation

Published documentation is available at:

```text
https://farotech.github.io/orbitfabric/
```

Useful entry points:

- `docs/PROJECT_CHARTER.md`
- `docs/CLEAN_ROOM_POLICY.md`
- `docs/ARCHITECTURE.md`
- `docs/ROADMAP.md`
- `docs/DEVELOPMENT.md`
- `docs/QUICKSTART.md`
- `docs/DEMO_WALKTHROUGH.md`
- `docs/reference/mission-model-v0.1.md`
- `docs/reference/data-flow-evidence.md`
- `docs/reference/json-reports-v0.1.md`
- `docs/reference/lint-rules-v0.1.md`
- `docs/releases/v0.6.0.md`
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

Do not add proprietary mission data, private architectures, private protocols, real operational logs, non-public payload details, real bus maps, real pinouts, employer/customer-owned code or NDA-protected material.

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

orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml \
  --json generated/reports/payload_data_flow_evidence_report.json \
  --log generated/logs/payload_data_flow_evidence.log
```

---

## License

OrbitFabric is licensed under the Apache License 2.0.

See:

```text
LICENSE
```
