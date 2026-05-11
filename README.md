<div align="center">
  <img src="assets/brand/orbitfabric-logo-horizontal-light.png" alt="OrbitFabric" width="760">
</div>

<br>

<div align="center">

**Model-first Mission Data Fabric for small spacecraft**

Define telemetry, commands, events, faults, modes, packets, payload contracts, data products, contact/downlink assumptions, commandability/autonomy contracts, operational scenarios, runtime-facing contract bindings and ground-facing integration artifacts once.
Validate them, document them, simulate them and generate deterministic integration artifacts from the same source of truth.

</div>

---

## Overview

OrbitFabric is a **model-first Mission Data Fabric** for small spacecraft.

It lets teams define mission data contracts once, using a structured Mission Model, and then reuse that contract across validation, documentation, testing, simulation, runtime-facing bindings and ground-facing integration artifacts.

OrbitFabric is not a flight software framework, not a ground segment and not a spacecraft dynamics simulator.

It is the contract layer between:

```text
mission design
onboard software
simulation
testing
documentation
runtime-facing integration
ground integration
```

> Define once. Validate. Simulate. Test. Document. Integrate.

---

## Current Status

OrbitFabric is currently at `v0.8.0 - Ground Integration Artifacts`.

In v0.8.0, **Ground Integration Artifacts** means ground-facing Mission Data Contract exports.

OrbitFabric does not generate a ground segment, mission control system, telemetry archive, command uplink service, operator console, decoder runtime, database, Yamcs integration, OpenC3 integration or XTCE-compliant mission database.

It generates deterministic, inspectable, tool-neutral ground-facing artifacts derived from the validated Mission Model.

The current repository includes:

- the `v0.2.1 - Payload Contract Model` vertical slice;
- the `v0.2.3 - Mission Data Chain Roadmap Alignment` direction;
- the `v0.3.0 - Data Product and Storage Contracts` vertical slice;
- the `v0.4.0 - Contact Windows and Downlink Flow Contracts` vertical slice;
- the `v0.5.0 - Commandability and Autonomy Contracts` vertical slice;
- the `v0.6.0 - End-to-End Mission Data Flow Evidence` vertical slice;
- the `v0.7.0 - Generated Runtime Skeletons` vertical slice;
- the `v0.8.0 - Ground Integration Artifacts` vertical slice.

The current vertical slice is functional:

- Mission Model YAML loading;
- structural validation;
- semantic linting;
- generated Markdown documentation;
- scenario YAML loading and validation;
- deterministic scenario execution;
- JSON lint and simulation reports;
- RuntimeContract construction;
- `orbitfabric gen runtime` generation;
- C++17 runtime-facing contract bindings;
- host-build smoke validation for generated C++17 bindings;
- GroundContract construction;
- `orbitfabric gen ground` generation;
- generic ground contract manifest;
- JSON ground dictionaries;
- CSV ground dictionaries;
- human-reviewable ground Markdown artifacts;
- synthetic demo mission: `demo-3u`.

The repository also includes a growing set of example mission slices:

- `examples/demo-3u/` - synthetic clean-room demo mission;
- `examples/university-cubesat-minislice/` - generic university CubeSat minislice;
- `examples/oresat-inspired-minislice/` - public-material-derived low-power / beacon / constrained-downlink minislice;
- `examples/finch-inspired-minislice/` - public-material-derived imaging acquisition / ADCS readiness / compression / constrained-downlink minislice;
- `examples/spacelab-inspired-communications-minislice/` - public-material-derived TT&C / OBDH / beacon / telecommanded data-request / decoder-evidence minislice.

The `*-inspired-*` examples are conceptual public demos. They are not official models, not endorsed by the original project teams, and do not imply adoption of OrbitFabric by those teams.

Current verified baseline:

```text
ruff check .
-> passing

pytest
-> passing

mkdocs build --strict
-> passing

cmake -S generated/runtime/cpp17 -B generated/runtime/cpp17/build
cmake --build generated/runtime/cpp17/build
-> passing after orbitfabric gen runtime

orbitfabric gen ground examples/demo-3u/mission/
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
- contract-level Mission Data Flow Evidence;
- generated runtime-facing contract bindings;
- generated ground-facing integration artifacts.

The data-flow evidence chain connects:

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
        -> runtime-facing bindings
        -> ground-facing artifacts
```

The v0.8 ground-facing generation chain is:

```text
Mission Model
        -> validation and linting
        -> GroundContract
        -> generic ground-facing dictionaries
        -> JSON / CSV / Markdown artifacts
        -> downstream ground-system integration outside OrbitFabric
```

Payload, Data Product, Contact/Downlink, Commandability/Autonomy, Data-Flow Evidence, Runtime Contract Binding and Ground Integration artifacts are part of the Mission Data Contract architecture. They do not describe payload firmware, payload drivers, hardware buses, onboard services, physical payload simulation, real storage execution, real contact scheduling, real downlink runtime behavior, live uplink services, operator authentication, command queues, onboard schedulers, autonomy runtime, real FDIR behavior or live ground operations.

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
- a mission control system;
- an operator console;
- a telemetry archive;
- a command uplink service;
- a payload firmware framework;
- a payload driver framework;
- a payload physical simulator;
- a payload data processing pipeline;
- an onboard storage runtime;
- a downlink runtime;
- an orbit propagator;
- an RF/link budget simulator;
- a real contact scheduler;
- a command dispatch runtime;
- an onboard scheduler;
- a HAL or RTOS abstraction.

Generated Runtime Skeletons in v0.7.0 are runtime-facing contract bindings.

Ground Integration Artifacts in v0.8.0 are ground-facing contract exports.

Neither is flight software or ground software.

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
        -> Runtime-Facing Contract Bindings
        -> Ground-Facing Integration Artifacts
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
orbitfabric 0.8.0
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

---

## Generate Runtime Contract Bindings

Generate C++17 runtime-facing contract bindings:

```bash
orbitfabric gen runtime examples/demo-3u/mission/
```

Generated files:

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

Validate the generated C++17 contract surface with CMake:

```bash
cmake -S generated/runtime/cpp17 -B generated/runtime/cpp17/build
cmake --build generated/runtime/cpp17/build
```

This is host-build smoke validation only.

It does not produce flight software.

---

## Generate Ground Integration Artifacts

Generate the generic ground-facing mission data package:

```bash
orbitfabric gen ground examples/demo-3u/mission/
```

Generated files:

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

These files are ground-facing contract exports.

They are not a ground runtime, decoder, telemetry archive, database, operator console, Yamcs integration, OpenC3 integration or XTCE-compliant mission database.

---

## Run Scenario Simulation

Run the battery-low recovery scenario:

```bash
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml \
  --json generated/reports/battery_low_during_payload_report.json \
  --log generated/logs/battery_low_during_payload.log
```

Run the data-flow evidence scenario:

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
├── reports/
├── logs/
├── runtime/
│   └── cpp17/
└── ground/
    └── generic/
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
- `docs/reference/runtime-contract-bindings.md`
- `docs/reference/ground-integration-artifacts.md`
- `docs/releases/v0.8.0.md`
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

orbitfabric gen data-flow examples/demo-3u/mission/ \
  --output-file generated/docs/data_flow.md

orbitfabric gen runtime examples/demo-3u/mission/

cmake -S generated/runtime/cpp17 -B generated/runtime/cpp17/build
cmake --build generated/runtime/cpp17/build

orbitfabric gen ground examples/demo-3u/mission/

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
