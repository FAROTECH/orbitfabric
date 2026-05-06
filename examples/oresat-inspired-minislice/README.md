# OreSat-inspired Minislice

This example is a small **OreSat-inspired public conceptual demo** for OrbitFabric.

It is derived from the generic:

```text
examples/university-cubesat-minislice/
```

and specializes that pattern toward a publicly documented university CubeSat ecosystem inspired by OreSat / Portland State Aerospace Society / Portland State University.

## Status and scope

This example is:

- public-material-derived;
- conceptual;
- intentionally small;
- intended for OrbitFabric validation, simulation and documentation generation;
- an external open-source example;
- not an official OreSat model.

This example is **not**:

- an official OreSat configuration;
- endorsed by OreSat, PSAS or Portland State University;
- a statement that OreSat uses OrbitFabric;
- a conversion of `oresat-configs` into OrbitFabric;
- a replacement for OreSat CANopen object dictionaries;
- a replacement for OreSat flight software, OLAF, Yamcs, ground tools or operational processes;
- a real mission operations model.

The correct description is:

```text
OreSat-inspired public demo
```

or:

```text
publicly derived conceptual example
```

Avoid describing it as:

```text
OreSat OrbitFabric model
official OreSat model
OreSat uses OrbitFabric
conversion of OreSat configs
replacement for OreSat configs / CANopen / OLAF / ground tools
```

## Why this example exists

OrbitFabric is a model-first mission data fabric for small spacecraft. It is not flight software, not an OBC firmware, not a dynamic simulator and not a ground segment.

This minislice demonstrates how OrbitFabric can describe a narrow but realistic mission-data contract:

```text
payload data generated
→ low-power condition constrains operations
→ beacon and critical telemetry are prioritized
→ contact capacity is limited
→ payload/science data remains partially pending
→ events, faults and scenario evidence explain the outcome
```

The point is not to reproduce OreSat. The point is to test OrbitFabric’s contract-layer approach against a recognizable open CubeSat-style architecture.

## Public inspiration

The example is inspired by public OreSat material, especially the kind of information exposed through:

- OreSat project website: https://www.oresat.org/
- OreSat0.5 public mission description: https://www.oresat.org/satellites/oresat0-5
- OreSat GitHub organization: https://github.com/oresat
- OreSat configs repository: https://github.com/oresat/oresat-configs
- OreSat0.5 beacon definition: https://oresat-configs.readthedocs.io/en/latest/oresat0_5/gen/beacon.html
- OreSat software and configuration repositories, used only as public context.

The example intentionally uses a reduced subset of concepts:

- C3-like command/control/data-handling context;
- EPS, battery and solar health;
- GPS state;
- ADCS manager/readiness context;
- star tracker status;
- CFC-style payload data;
- DxWiFi-style data context;
- low-rate constrained downlink;
- beacon and housekeeping priority.

It does not import or mechanically translate OreSat object dictionaries.

## Directory layout

```text
examples/oresat-inspired-minislice/
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
    └── low_power_cfc_data_pending.yaml
```

There is deliberately no `mission/downlink.yaml`.

In OrbitFabric v0.4.0, downlink flows are modeled inside:

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
scenarios/low_power_cfc_data_pending.yaml
```

Scenario id:

```text
low_power_cfc_data_pending
```

Conceptual sequence:

1. The spacecraft starts in `NOMINAL`.
2. A CFC-style payload capture is scheduled.
3. Payload data is generated.
4. Battery state of charge drops below the warning threshold.
5. A low-power warning is raised.
6. The spacecraft transitions to `LOW_POWER`.
7. A constrained contact window becomes available.
8. Downlink priority is set to `critical_first`.
9. Beacon and critical housekeeping are prioritized.
10. CFC/DxWiFi-style payload data is eligible but too large for the available contact.
11. The downlink is partial.
12. Payload data remains pending.
13. The scenario evidence explains why the payload backlog remains.

The expected end state is:

```text
scenario passed
payload data still pending
spacecraft back in LOW_POWER after contact
```

## Mode model

The demo uses a compact mode model:

```text
SAFE
STANDBY
NOMINAL
PAYLOAD_ACQUISITION
DOWNLINK
LOW_POWER
FAULT_RECOVERY
```

These modes are conceptual OrbitFabric mission-data states. They are not intended to represent an official OreSat mode table.

## Subsystems

The example models a small representative subsystem set:

```text
spacecraft_bus
c3
eps
battery
solar
gps
adcs
star_tracker
dxwifi
cfc_payload
comms
data_storage
ground_station_context
```

The mapping is intentionally compact:

| OrbitFabric subsystem | OreSat-inspired role |
|---|---|
| `c3` | command, control and data-handling context |
| `eps` | power system aggregation |
| `battery` | battery state, voltage and temperature |
| `solar` | solar input power context |
| `gps` | fix and time-sync state |
| `adcs` | ADCS manager/readiness context |
| `star_tracker` | attitude sensor context |
| `dxwifi` | high-volume data/radio-style context |
| `cfc_payload` | CFC-style payload data source |
| `comms` | beacon/contact/downlink context |
| `data_storage` | onboard stored-data/evidence context |
| `ground_station_context` | abstract ground-contact context |

This is not a complete OreSat subsystem model.

## Telemetry focus

The telemetry model keeps only representative fields needed by the scenario:

```text
eps.battery.state_of_charge
eps.battery.voltage
eps.battery.temperature
solar.input_power
c3.uptime
c3.storage_used
comms.link_status
gps.fix_status
gps.time_sync_status
adcs.manager_mode
adcs.attitude_ready
star_tracker.status
cfc.camera_status
cfc.camera_temperature
dxwifi.status
payload.data_generated_bytes
payload.data_pending_bytes
downlink.capacity_remaining_bytes
data_storage.used_bytes
```

The selected fields are deliberately small and contract-oriented. They are not intended to mirror the complete OreSat beacon or object dictionary.

## Commands

The command set is minimal:

```text
c3.request_health_telemetry
comms.request_payload_data
cfc.schedule_capture
comms.set_downlink_priority
comms.start_downlink
comms.end_downlink
c3.enter_safe_mode
c3.clear_fault
```

Commands are modeled as mission-data contracts: allowed modes, preconditions, emitted events and expected effects.

They are not flight-software commands.

## Events

Representative events include:

```text
comms.beacon_transmitted
cfc.data_generated
eps.low_power_warning_raised
comms.contact_window_started
comms.downlink_started
comms.downlink_partial
payload.data_pending
comms.downlink_capacity_insufficient
c3.mode_changed
adcs.mode_changed
gps.lock_acquired
gps.lock_lost
```

These events are used to explain the scenario outcome and generate evidence.

## Faults and warnings

The fault model includes warning/fault conditions such as:

```text
eps.low_battery_warning
eps.low_battery_critical
cfc.camera_temperature_high
cfc.data_backlog
comms.downlink_capacity_insufficient
gps.not_locked
adcs.not_ready
data_storage.high_usage
```

The primary warning exercised by the scenario is:

```text
eps.low_battery_warning
```

The primary downlink constraint is:

```text
comms.downlink_capacity_insufficient
```

## Payload and data products

The main payload contract is:

```text
cfc_payload
```

The payload lifecycle is:

```text
OFF
READY
CAPTURING
DATA_READY
DOWNLINK_PENDING
BACKLOG
FAULT
```

Representative data products are:

```text
health_beacon
critical_housekeeping_packet
cfc_image_capture
compressed_cfc_bundle
dxwifi_image_bundle
gps_state_sample
adcs_sensor_snapshot
downlink_summary_report
scenario_evidence_log
```

The scenario intentionally creates more eligible data volume than the declared contact capacity can downlink.

## Contact and downlink model

The contact model is synthetic:

```text
contact profile: oresat_inspired_ground_contact
link profile: low_rate_uhf_downlink
contact window: oresat_inspired_contact_001
downlink flow: oresat_inspired_priority_downlink
queue policy: critical_first
```

The contact window declares:

```text
assumed_capacity_bytes: 12000
```

The eligible data products exceed that capacity by design.

This causes the expected OrbitFabric lint warning:

```text
WARNING OF-DL-005 contacts.yaml oresat_inspired_priority_downlink estimated eligible data product volume may exceed declared contact capacity
```

This warning is intentional. It is the behavior the example is designed to demonstrate.

Do not “fix” this warning by increasing contact capacity unless the purpose of the example changes.

## Validation

From the repository root:

```bash
orbitfabric lint examples/oresat-inspired-minislice/mission
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
orbitfabric gen docs examples/oresat-inspired-minislice/mission
```

Expected result:

```text
Result: PASSED
```

Run the scenario:

```bash
orbitfabric sim examples/oresat-inspired-minislice/scenarios/low_power_cfc_data_pending.yaml
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

The model is demonstrating that OrbitFabric can make this contract-level mismatch explicit before and during scenario execution:

```text
critical data is prioritized
payload data is only partially downlinked
remaining payload data is retained as backlog
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

It also shows that the same conceptual pattern used by the generic university CubeSat minislice can be specialized toward a more concrete public CubeSat ecosystem without claiming official compatibility.

## What this example does not prove

This example does not prove:

- compatibility with OreSat flight software;
- compatibility with OreSat CANopen object dictionaries;
- compatibility with OreSat OLAF;
- compatibility with OreSat Yamcs or ground operations;
- correctness of OreSat operational data;
- correctness of real OreSat contact windows, rates, callsigns or frequencies;
- completeness of any OreSat mission model.

It is a conceptual OrbitFabric example only.

## Naming guidance

Use:

```text
OreSat-inspired public demo
publicly derived conceptual example
OreSat-inspired minislice
```

Do not use:

```text
OreSat OrbitFabric model
official OreSat model
OreSat uses OrbitFabric
OreSat conversion
OreSat replacement model
```

## Recommended use

Use this example when explaining OrbitFabric as a contract layer between:

```text
mission design
onboard software expectations
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

Do not use it as a source of truth for OreSat.

## License and attribution

This example is part of OrbitFabric.

OreSat, PSAS, Portland State University and related repository names are referenced only as public inspiration and attribution context.

No endorsement or collaboration is implied.
