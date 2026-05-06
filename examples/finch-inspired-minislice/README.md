# FINCH-inspired Minislice

This example is a small **FINCH-inspired public conceptual demo** for OrbitFabric.

It is derived from the generic:

```text
examples/university-cubesat-minislice/
```

and follows the controlled-specialization pattern used by:

```text
examples/oresat-inspired-minislice/
```

The example is inspired by publicly available UTAT Space Systems / FINCH material.

## Status and scope

This example is:

- public-material-derived;
- conceptual;
- intentionally small;
- imaging-payload / acquisition / constrained-downlink oriented;
- intended for OrbitFabric validation, simulation and documentation generation;
- an external open-source example;
- not an official FINCH model.

This example is **not**:

- an official FINCH configuration;
- endorsed by UTAT Space Systems, the University of Toronto Aerospace Team, or the University of Toronto;
- a statement that UTAT uses OrbitFabric;
- a collaboration announcement;
- a conversion of FINCH architecture diagrams, firmware, payload design, science-processing pipelines or operational plans into OrbitFabric;
- a replacement for FINCH firmware, system architecture diagrams, data-processing tools, systems-engineering tools or mission-operations workflows;
- a real mission operations model.

The correct description is:

```text
FINCH-inspired public demo
```

or:

```text
publicly derived conceptual example
```

or:

```text
FINCH-inspired imaging/downlink minislice
```

Avoid describing it as:

```text
official FINCH model
FINCH OrbitFabric model
UTAT uses OrbitFabric
conversion of FINCH architecture
replacement for FINCH firmware / diagrams / data-processing tools
```

## Why this example exists

OrbitFabric is a model-first mission data fabric for small spacecraft. It is not flight software, not an OBC firmware, not a dynamic simulator and not a ground segment.

This minislice demonstrates a narrow mission-data contract:

```text
acquisition parameters loaded
-> OBC schedules imaging and enters ACQUISITION_PREP
-> ADCS readiness and camera readiness are checked
-> OBC verifies acquisition conditions
-> IMAGE_ACQUISITION generates hyperspectral image data
-> compressed image data is retained onboard
-> contact capacity prioritizes critical summaries first
-> compressed image data remains partially pending
-> events, faults and scenario evidence explain the outcome
```

The point is not to reproduce FINCH. The point is to test OrbitFabric's contract-layer approach against a recognizable public university CubeSat imaging-payload pattern.

## Public inspiration

The example is inspired by public UTAT Space Systems / FINCH material, especially:

- UTAT Space Systems website: https://www.utat.ca/space-systems
- UTAT Space Systems Cube Satellite Development page: https://www.utat.ca/space-systems-cube-satellite-development
- FINCH SmallSat 2022 public paper: https://digitalcommons.usu.edu/smallsat/2022/all2022/88/
- FINCH EYE SmallSat 2025 public paper: https://digitalcommons.usu.edu/smallsat/2025/all2025/64/

The example intentionally uses only a reduced subset of public concepts:

- FINCH-style university CubeSat context;
- hyperspectral / SWIR imaging mission context;
- acquisition preparation and readiness gating;
- ADCS readiness before imaging;
- camera readiness and payload health context;
- compressed image data as a representative downlink product;
- constrained contact capacity;
- evidence explaining partial downlink completion.

It does not import, copy or mechanically translate real FINCH architecture diagrams, firmware behavior, packet formats, payload implementation details, science-processing algorithms, operational schedules, ground procedures or mission operations data.

## Directory layout

```text
examples/finch-inspired-minislice/
├── README.md
├── mission
│   ├── spacecraft.yaml
│   ├── subsystems.yaml
│   ├── modes.yaml
│   ├── telemetry.yaml
│   ├── commands.yaml
│   ├── events.yaml
│   ├── faults.yaml
│   ├── packets.yaml
│   ├── payloads.yaml
│   ├── policies.yaml
│   ├── data_products.yaml
│   └── contacts.yaml
└── scenarios
    └── image_acquisition_downlink_constraint.yaml
```

There is deliberately no `mission/downlink.yaml`.

In OrbitFabric v0.4.0-style examples, downlink flows are modeled inside:

```text
mission/contacts.yaml
```

through:

```yaml
contacts:
  contact_profiles:
  link_profiles:
  contact_windows:
  downlink_flows:
```

## Main scenario

The main scenario is:

```text
scenarios/image_acquisition_downlink_constraint.yaml
```

Scenario id:

```text
image_acquisition_downlink_constraint
```

Conceptual sequence:

1. The spacecraft starts in `NOMINAL`.
2. Acquisition parameters are loaded during a contact-oriented operation.
3. The OBC schedules an image acquisition and enters `ACQUISITION_PREP`.
4. ADCS is marked ready for acquisition pointing.
5. The payload camera is prepared and marked ready.
6. The OBC emits `obc.acquisition_conditions_met`.
7. The spacecraft enters `IMAGE_ACQUISITION` and the hyperspectral image acquisition completes.
8. The spacecraft enters `DATA_COMPRESSION` and creates a downlink-eligible bundle.
9. A constrained contact starts.
10. Critical housekeeping, acquisition summary and evidence products are prioritized.
11. The compressed hyperspectral bundle is only partially downlinked.
12. Remaining compressed image data remains pending onboard.

The expected end state is:

```text
scenario passed
compressed image data still pending
spacecraft back in NOMINAL after contact
```

## Mode model

The demo uses a compact imaging-oriented mode model:

```text
SAFE
STANDBY
NOMINAL
ACQUISITION_PREP
IMAGE_ACQUISITION
DATA_COMPRESSION
DOWNLINK
FAULT_RECOVERY
```

These modes are conceptual OrbitFabric mission-data states. They are not intended to represent an official FINCH mode table.

## Subsystems

The example models a small representative subsystem set:

```text
spacecraft_bus
obc
eps
adcs
star_tracker
sun_sensors
gnss
hyperspectral_payload
thermal
rf
transceiver
comms
data_storage
ground_station_context
```

The mapping is intentionally compact:

| OrbitFabric subsystem | FINCH-inspired role |
|---|---|
| `obc` | command, data-handling and acquisition coordination context |
| `eps` | battery state context |
| `adcs` | acquisition-pointing readiness context |
| `star_tracker` | attitude sensor context |
| `sun_sensors` | coarse attitude/sun-sensing readiness context |
| `gnss` | fix/state context |
| `hyperspectral_payload` | imaging payload lifecycle and data-product source |
| `thermal` | payload temperature context |
| `rf` | abstract RF downlink state with no operational parameters |
| `transceiver` | receive/transmit/standby state context |
| `comms` | contact-window and downlink-flow coordination context |
| `data_storage` | onboard stored-data/evidence context |
| `ground_station_context` | synthetic contact assumption context |

This is not a complete FINCH subsystem model.

## Telemetry focus

The telemetry model keeps only representative fields needed by the scenario:

```text
obc.uptime
data_storage.used_bytes
comms.link_status
rf.downlink_status
transceiver.status
downlink.capacity_remaining_bytes
adcs.attitude_ready
adcs.pointing_status
star_tracker.status
sun_sensors.status
gnss.fix_status
payload.camera_status
payload.camera_temperature
thermal.payload_temperature
payload.acquisition_status
payload.compression_status
payload.data_generated_bytes
payload.data_pending_bytes
eps.battery.state_of_charge
```

The selected fields are deliberately small and contract-oriented. They are not intended to mirror complete FINCH telemetry definitions, science products or internal software interfaces.

## Commands

The command set is minimal:

```text
payload.load_acquisition_params
payload.schedule_image_acquisition
adcs.request_pointing_ready
payload.prepare_camera
obc.verify_acquisition_conditions
payload.start_image_acquisition
payload.compress_image_data
obc.request_health_telemetry
comms.set_downlink_priority
comms.start_downlink
comms.end_downlink
obc.enter_safe_mode
obc.clear_fault
```

Commands are modeled as mission-data contracts: allowed modes, preconditions, emitted events and expected effects.

They are not flight-software commands and do not encode real telecommand packets.

## Events

Representative events include:

```text
payload.acquisition_params_loaded
payload.acquisition_scheduled
adcs.ready_for_acquisition
payload.camera_ready
obc.acquisition_conditions_met
payload.image_acquisition_started
payload.image_acquisition_completed
payload.image_compressed
obc.health_telemetry_requested
comms.downlink_priority_set
comms.contact_window_started
comms.downlink_started
comms.downlink_partial
comms.downlink_capacity_insufficient
payload.image_data_pending
comms.contact_window_ended
```

These events are used to explain the scenario outcome and generate evidence.

## Faults and warnings

The fault model includes warning/fault conditions such as:

```text
adcs.not_ready
payload.camera_not_ready
payload.temperature_high
payload.compression_failed
comms.downlink_capacity_insufficient
data_storage.high_usage
eps.low_battery_warning
```

The primary downlink constraint is:

```text
comms.downlink_capacity_insufficient
```

## Payload and data products

The main payload contract is:

```text
hyperspectral_payload
```

The payload lifecycle is:

```text
OFF
READY
PARAMS_LOADED
SCHEDULED
CAMERA_READY
CONDITIONS_VERIFIED
ACQUIRING
DATA_READY
COMPRESSED_READY
DOWNLINK_PENDING
BACKLOG
FAULT
```

Representative data products are:

```text
critical_housekeeping_packet
acquisition_summary_report
adcs_readiness_snapshot
payload_health_snapshot
raw_hyperspectral_image
compressed_hyperspectral_bundle
downlink_summary_report
scenario_evidence_log
```

Downstream processing placeholders are modeled only as conceptual candidates when present. They are not onboard products and do not represent real FINCH processing algorithms.

The scenario intentionally creates more eligible data volume than the declared contact capacity can downlink.

## Contact and downlink model

The contact model is synthetic:

```text
contact profile: finch_inspired_ground_contact
link profile: constrained_payload_downlink
contact window: finch_inspired_contact_001
downlink flow: finch_inspired_priority_downlink
queue policy: critical_first
```

The contact window declares:

```text
assumed_capacity_bytes: 16000
```

The eligible data products exceed that capacity by design.

This should cause the expected OrbitFabric lint warning:

```text
WARNING OF-DL-005 contacts.yaml finch_inspired_priority_downlink estimated eligible data product volume may exceed declared contact capacity
```

This warning is intentional. It is the behavior the example is designed to demonstrate.

Do not fix this warning by increasing contact capacity unless the purpose of the example changes.

All numeric values, thresholds, contact capacities, timings, target identifiers and scenario sequences are synthetic demonstration values.

## Validation

From the repository root:

```bash
orbitfabric lint examples/finch-inspired-minislice/mission
```

Expected result:

```text
Result: PASSED WITH WARNINGS
```

Expected warning:

```text
OF-DL-005 estimated eligible data product volume may exceed declared contact capacity
```

This warning is part of the scenario design.

Generate documentation:

```bash
orbitfabric gen docs examples/finch-inspired-minislice/mission
```

Expected result:

```text
Result: PASSED
```

Run the scenario:

```bash
orbitfabric sim examples/finch-inspired-minislice/scenarios/image_acquisition_downlink_constraint.yaml
```

Expected result:

```text
Result: PASSED
```

## Interpretation of the expected warning

The warning means:

```text
eligible downlink volume > declared contact capacity
```

In this example, that is intentional.

The model is demonstrating that OrbitFabric can make this contract-level mismatch explicit:

```text
critical health and acquisition-summary products are prioritized
compressed image data is only partially downlinked
remaining compressed image data is retained onboard
scenario evidence records the reason
```

This is the core behavior of the minislice.

## What this example proves

This example proves that OrbitFabric can describe and validate a mission-data slice involving:

- spacecraft modes;
- subsystem telemetry;
- commands;
- events;
- faults/warnings;
- payload lifecycle;
- data products;
- packets;
- contact windows;
- downlink flows;
- scenario evidence.

It also shows that the same controlled-specialization pattern used by the university and OreSat-inspired minislices can be applied to a public university imaging CubeSat concept without claiming official compatibility.

## What this example does not prove

This example does not prove:

- compatibility with FINCH firmware;
- compatibility with FINCH payload design or optical implementation;
- compatibility with FINCH science-processing or data-processing pipelines;
- correctness of real FINCH operational data;
- correctness of real contact windows, rates, callsigns, frequencies or ground station procedures;
- completeness of any FINCH mission model.

It is a conceptual OrbitFabric example only.

## Naming guidance

Use:

```text
FINCH-inspired public demo
publicly derived conceptual example
FINCH-inspired imaging/downlink minislice
```

Do not use:

```text
FINCH OrbitFabric model
official FINCH model
UTAT uses OrbitFabric
FINCH conversion
FINCH replacement model
```

## Recommended use

Use this example when explaining OrbitFabric as a contract layer between:

```text
mission design
onboard software expectations
imaging-payload readiness
telemetry
commands
events
faults
payload contracts
data products
contact windows
downlink behavior
scenario evidence
generated documentation
```

Do not use it as a source of truth for FINCH, UTAT Space Systems or the University of Toronto Aerospace Team.

## License and attribution

This example is part of OrbitFabric.

FINCH, UTAT Space Systems, the University of Toronto Aerospace Team and the University of Toronto are referenced only as public inspiration and attribution context.

No endorsement or collaboration is implied.
