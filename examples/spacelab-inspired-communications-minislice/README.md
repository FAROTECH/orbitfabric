# SpaceLab-inspired Communications Minislice

This example is a small **SpaceLab-inspired public communications demo** for OrbitFabric.

It is derived from the generic and specialized minislice pattern used by:

```text
examples/university-cubesat-minislice/
examples/oresat-inspired-minislice/
examples/finch-inspired-minislice/
```

The example is inspired by publicly available SpaceLab UFSC / FloripaSat / GOLDS-UFSC material, especially public descriptions of OBDH, TT&C, beacon, telecommanded data request and decoder workflows.

## Status and scope

This example is:

- public-material-derived;
- conceptual;
- intentionally small;
- communications / TT&C / OBDH oriented;
- intended for OrbitFabric validation, simulation and documentation generation;
- an external open-source example;
- not an official SpaceLab, FloripaSat or GOLDS-UFSC model.

This example is **not**:

- an official FloripaSat model;
- endorsed by SpaceLab UFSC, UFSC, FloripaSat or GOLDS-UFSC;
- a statement that SpaceLab UFSC uses OrbitFabric;
- a collaboration announcement;
- a conversion of FloripaSat architecture, firmware, packet formats or operational plans into OrbitFabric;
- a replacement for SpaceLab decoder, transmitter, TT&C, OBDH, firmware or ground station software;
- a real mission operations model.

The correct description is:

```text
SpaceLab-inspired public communications demo
```

or:

```text
publicly derived conceptual communications example
```

or:

```text
SpaceLab UFSC / FloripaSat-inspired TT&C minislice
```

Avoid describing it as:

```text
official FloripaSat model
SpaceLab OrbitFabric model
SpaceLab uses OrbitFabric
conversion of the FloripaSat architecture into OrbitFabric
replacement for SpaceLab decoder / transmitter / TT&C / OBDH / ground software
```

## Why this example exists

OrbitFabric is a model-first mission data fabric for small spacecraft. It is not flight software, not an OBC firmware, not a dynamic simulator and not a ground segment.

This minislice demonstrates a narrow communications-oriented mission-data contract:

```text
periodic beacon available
-> ground contact starts
-> TT&C receives an abstract data-request telecommand
-> TT&C forwards the request to OBDH
-> OBDH selects stored telemetry/data frames
-> OBDH packages frames for downlink
-> beacon and critical housekeeping are prioritized first
-> requested frames are partially downlinked
-> remaining requested frames stay pending onboard
-> decoder evidence records received frames and partial completion
```

The point is not to reproduce SpaceLab or FloripaSat. The point is to test OrbitFabric's contract-layer approach against a recognizable public CubeSat communications pattern.

## Public inspiration

The example is inspired by public SpaceLab / FloripaSat material, especially:

- SpaceLab UFSC website: https://spacelab.ufsc.br/
- FloripaSat-1 website: https://floripasat.ufsc.br/
- FloripaSat-2 mission page: https://spacelab.ufsc.br/en/floripasat2/
- GOLDS-UFSC / FloripaSat-2 documentation repository: https://github.com/spacelab-ufsc/floripasat2-doc
- SpaceLab Decoder documentation: https://spacelab-ufsc.github.io/spacelab-decoder/
- SpaceLab Transmitter telecommands documentation: https://spacelab-ufsc.github.io/spacelab-transmitter/telecommands.html

The example intentionally uses only a reduced subset of public concepts:

- OBDH-style data handling and stored frame selection;
- TT&C-style beacon and telecommand reception;
- periodic beacon context;
- abstract requested telemetry/data frames;
- constrained downlink flow;
- decoder-side received-frame evidence.

It does not import or mechanically translate real packet formats, keys, callsigns, frequencies, TLEs, operational schedules, decoder configuration files or ground station procedures.

## Directory layout

```text
examples/spacelab-inspired-communications-minislice/
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
│   ├── policies.yaml
│   ├── payloads.yaml
│   ├── data_products.yaml
│   └── contacts.yaml
└── scenarios
    └── ttc_data_request_constrained_downlink.yaml
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
scenarios/ttc_data_request_constrained_downlink.yaml
```

Scenario id:

```text
ttc_data_request_constrained_downlink
```

Conceptual sequence:

1. The spacecraft starts in `NOMINAL`.
2. A periodic beacon product is available.
3. A synthetic ground contact starts.
4. TT&C receives an abstract data-request telecommand.
5. OBDH accepts the request.
6. OBDH selects stored telemetry/data frames.
7. OBDH packages the selected frames for downlink.
8. Downlink priority is set to `critical_first`.
9. TT&C/comms start downlink.
10. Beacon and critical housekeeping are prioritized first.
11. Requested telemetry/data frames are only partially downlinked.
12. Remaining requested frames remain pending onboard.
13. Decoder evidence records received frames and partial completion.
14. The contact ends.
15. The scenario passes with partial completion explicitly recorded.

The expected end state is:

```text
scenario passed
requested frames still pending
spacecraft back in NOMINAL after contact
```

## Mode model

The demo uses a compact communications-oriented mode model:

```text
SAFE
STANDBY
NOMINAL
CONTACT
DATA_REQUEST_HANDLING
DOWNLINK
HIBERNATION
FAULT_RECOVERY
```

These modes are conceptual OrbitFabric mission-data states. They are not intended to represent an official SpaceLab, FloripaSat or GOLDS-UFSC mode table.

## Subsystems

The example models a small representative subsystem set:

```text
spacecraft_bus
obdh
ttc
beacon_context
data_storage
comms
rf
transceiver
ground_station_context
decoder_context
eps
thermal
```

The mapping is intentionally compact:

| OrbitFabric subsystem | SpaceLab-inspired role |
|---|---|
| `obdh` | command/data-handling, stored frame selection and packaging context |
| `ttc` | telecommand reception, beacon and downlink context |
| `beacon_context` | periodic beacon availability and transmission evidence |
| `data_storage` | retained telemetry/data frame and evidence storage context |
| `comms` | contact-window and downlink-flow coordination context |
| `rf` | abstract RF downlink state with no operational parameters |
| `transceiver` | receive/transmit/standby state context |
| `ground_station_context` | synthetic contact assumption context |
| `decoder_context` | ground-side received-frame evidence context |
| `eps` | battery state context |
| `thermal` | board-temperature context |

This is not a complete SpaceLab subsystem model.

## Telemetry focus

The telemetry model keeps only representative fields needed by the scenario:

```text
obdh.uptime
obdh.storage_used_bytes
data_storage.used_bytes
ttc.link_status
ttc.beacon_status
ttc.command_rx_status
ttc.downlink_status
comms.contact_status
rf.downlink_status
transceiver.status
downlink.capacity_remaining_bytes
requested_data.frames_selected
requested_data.frames_pending
decoder.frames_received
decoder.partial_completion_status
eps.battery.state_of_charge
thermal.board_temperature
```

The selected fields are deliberately small and contract-oriented. They are not intended to mirror complete FloripaSat, GOLDS-UFSC or SpaceLab Decoder telemetry definitions.

## Commands

The command set is minimal:

```text
obdh.request_health_telemetry
ttc.receive_data_request
obdh.select_requested_data
obdh.package_downlink_frames
comms.set_downlink_priority
comms.start_downlink
comms.end_downlink
obdh.enter_safe_mode
obdh.clear_fault
```

Commands are modeled as mission-data contracts: allowed modes, expected effects and emitted events.

They are not flight-software commands and do not encode real telecommand packets.

## Events

Representative events include:

```text
ttc.beacon_transmitted
comms.contact_window_started
ttc.telecommand_received
obdh.data_request_accepted
obdh.data_frames_selected
obdh.downlink_frames_packaged
comms.downlink_started
comms.downlink_partial
requested_data.frames_pending
decoder.frames_received
decoder.partial_reception_recorded
comms.contact_window_ended
```

These events are used to explain the scenario outcome and generate evidence.

## Faults and warnings

The fault model includes warning/fault conditions such as:

```text
ttc.command_authentication_failed
comms.downlink_capacity_insufficient
requested_data.backlog
data_storage.high_usage
eps.low_battery_warning
thermal.board_temperature_high
```

The main scenario does not center on authentication. Authentication failure is included only as a simple optional branch concept.

The primary downlink constraint is:

```text
comms.downlink_capacity_insufficient
```

## Payload and data products

This example is communications-oriented and does not model a mission-specific payload.

The payload contract file is intentionally empty:

```yaml
payloads: []
```

Representative data products are:

```text
periodic_beacon_packet
critical_housekeeping_packet
requested_telemetry_frame_batch
requested_data_frame_batch
downlink_summary_report
decoder_reception_log
scenario_evidence_log
```

The scenario intentionally creates more eligible data volume than the declared contact capacity can downlink.

## Contact and downlink model

The contact model is synthetic:

```text
contact profile: spacelab_inspired_ground_contact
link profile: constrained_ttc_downlink
contact window: spacelab_inspired_contact_001
downlink flow: spacelab_inspired_priority_downlink
queue policy: critical_first
```

The contact window declares:

```text
assumed_capacity_bytes: 12000
```

The eligible data products exceed that capacity by design.

This should cause the expected OrbitFabric lint warning:

```text
WARNING OF-DL-005 contacts.yaml spacelab_inspired_priority_downlink estimated eligible data product volume may exceed declared contact capacity
```

This warning is intentional. It is the behavior the example is designed to demonstrate.

Do not fix this warning by increasing contact capacity unless the purpose of the example changes.

## Validation

From the repository root:

```bash
orbitfabric lint examples/spacelab-inspired-communications-minislice/mission
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
orbitfabric gen docs examples/spacelab-inspired-communications-minislice/mission
```

Expected result:

```text
Result: PASSED
```

Run the scenario:

```bash
orbitfabric sim examples/spacelab-inspired-communications-minislice/scenarios/ttc_data_request_constrained_downlink.yaml
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
beacon and critical housekeeping are prioritized
requested telemetry/data frames are only partially downlinked
remaining requested frames are retained onboard
scenario evidence and decoder context record the reason
```

This is the core behavior of the minislice.

## What this example proves

This example proves that OrbitFabric can describe and validate a mission-data slice involving:

- spacecraft modes;
- subsystem telemetry;
- commands;
- events;
- faults/warnings;
- data products;
- packets;
- contact windows;
- downlink flows;
- decoder evidence context;
- scenario evidence.

It also shows that the same controlled-specialization pattern used by the university, OreSat-inspired and FINCH-inspired minislices can be applied to a communications-oriented public CubeSat architecture without claiming official compatibility.

## What this example does not prove

This example does not prove:

- compatibility with SpaceLab OBDH or TT&C firmware;
- compatibility with FloripaSat or GOLDS-UFSC packet formats;
- compatibility with SpaceLab Decoder or SpaceLab Transmitter;
- correctness of real SpaceLab operational data;
- correctness of real contact windows, rates, callsigns, keys, frequencies or ground station procedures;
- completeness of any SpaceLab, FloripaSat or GOLDS-UFSC mission model.

It is a conceptual OrbitFabric example only.

## Naming guidance

Use:

```text
SpaceLab-inspired public communications demo
publicly derived conceptual communications example
SpaceLab UFSC / FloripaSat-inspired TT&C minislice
```

Do not use:

```text
SpaceLab OrbitFabric model
official FloripaSat model
SpaceLab uses OrbitFabric
FloripaSat conversion
SpaceLab replacement model
```

## Recommended use

Use this example when explaining OrbitFabric as a contract layer between:

```text
mission design
onboard software expectations
TT&C / OBDH data flow
telemetry
commands
events
faults
data products
contact windows
downlink behavior
decoder evidence
generated documentation
```

Do not use it as a source of truth for SpaceLab, FloripaSat or GOLDS-UFSC.

## License and attribution

This example is part of OrbitFabric.

SpaceLab UFSC, FloripaSat, GOLDS-UFSC and related repository names are referenced only as public inspiration and attribution context.

No endorsement or collaboration is implied.
