# Demo Walkthrough

This page explains the current OrbitFabric demo mission:

```text
examples/demo-3u/
```

The demo is synthetic and clean-room. It is not based on a real spacecraft, private mission, proprietary bus map, private payload or operational log.

---

## 1. Demo purpose

The `demo-3u` mission demonstrates the OrbitFabric vertical slice:

```text
Define once. Validate. Simulate. Test. Document. Integrate.
```

The goal is not to model a real CubeSat.

The goal is to show how a Mission Data Contract can define mission data and operational behavior once, then reuse it across linting, documentation and deterministic scenario execution.

---

## 2. Demo structure

The demo lives under:

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
│   └── data_products.yaml
└── scenarios/
    └── battery_low_during_payload.yaml
```

The `mission/` directory contains the Mission Model.

The `scenarios/` directory contains executable operational scenarios.

---

## 3. Mission Model files

### `spacecraft.yaml`

Defines the synthetic spacecraft identity and Mission Model version.

### `subsystems.yaml`

Defines the demo subsystems:

```text
obc
eps
payload
radio
```

These are generic synthetic subsystem abstractions.

### `modes.yaml`

Defines the operational modes:

```text
BOOT
NOMINAL
PAYLOAD_ACTIVE
DEGRADED
SAFE
MAINTENANCE
```

It also defines allowed mode transitions.

### `telemetry.yaml`

Defines telemetry items such as:

```text
obc.mode
eps.battery.voltage
eps.battery.current
payload.acquisition.active
radio.downlink.available
```

Telemetry items include source subsystem, type, unit, sampling, criticality, persistence and downlink priority.

### `commands.yaml`

Defines commands such as:

```text
payload.start_acquisition
payload.stop_acquisition
eps.get_status
radio.downlink_housekeeping
```

Commands define target subsystem, arguments, allowed modes, ACK policy, timeout, risk, emitted events and expected effects.

### `events.yaml`

Defines events emitted by commands and faults.

### `faults.yaml`

Defines synthetic fault logic.

The key fault in the demo is:

```text
eps.battery_low_fault
```

It monitors:

```text
eps.battery.voltage
```

and triggers a recovery action when voltage remains below a synthetic warning threshold.

### `packets.yaml`

Defines synthetic packet groupings for generated documentation and future integration artifacts.

### `policies.yaml`

Defines allowed policy values used by the model.

### `payloads.yaml`

Defines the synthetic IOD payload contract:

```text
demo_iod_payload
```

The contract describes payload lifecycle, telemetry references, accepted commands and generated events without introducing payload firmware, drivers or physical simulation.

### `data_products.yaml`

Defines one synthetic data product:

```text
payload.radiation_histogram
```

It is produced by `demo_iod_payload` and declares:

```text
type: histogram
estimated size: 4096 bytes
priority: high
storage class: science
retention: 7d
overflow policy: drop_oldest
downlink policy: next_available_contact
```

This is contract intent only. It does not implement storage or downlink execution.

---

## 4. Scenario: battery low during payload operation

The executable scenario is:

```text
examples/demo-3u/scenarios/battery_low_during_payload.yaml
```

It starts in:

```text
NOMINAL
```

with initial telemetry:

```text
obc.mode = NOMINAL
eps.battery.voltage = 7.4
eps.battery.current = 0.4
payload.acquisition.active = false
radio.downlink.available = true
```

---

## 5. Scenario timeline

The scenario demonstrates this operational sequence:

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

The data product contract is not executed by this scenario yet.

It documents the expected mission-data object produced by the payload and prepares the model for future contact/downlink contracts.

---

## 6. Run the scenario

```bash
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml
```

Expected result:

```text
Result: PASSED
```

---

## 7. Generate scenario outputs

```bash
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml \
  --json generated/reports/battery_low_during_payload_report.json \
  --log generated/logs/battery_low_during_payload.log
```

Generated files:

```text
generated/reports/battery_low_during_payload_report.json
generated/logs/battery_low_during_payload.log
```

---

## 8. Generate mission documentation

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
└── data_products.md
```

The generated data product documentation exposes storage and downlink intent as contract data, not runtime behavior.

---

## 9. What the simulator checks

During execution, OrbitFabric checks that:

- commands exist in the Mission Model;
- commands are allowed in the current mode;
- expected command effects are applied;
- payload lifecycle preconditions are respected;
- payload lifecycle expected effects are applied;
- events are emitted;
- telemetry injections update simulation state;
- fault conditions are evaluated;
- mode transitions occur;
- auto-dispatched recovery commands are recorded;
- scenario expectations pass.

---

## 10. Expected final state

At the end of the scenario:

```text
mode = DEGRADED
payload lifecycle = READY
payload.acquisition.active = false
scenario_status = PASSED
```

The important behavior is the contract-level recovery path:

```text
EPS warning fault
  -> transition to DEGRADED
  -> auto-dispatch payload.stop_acquisition
  -> payload acquisition inactive
  -> payload lifecycle READY
```

---

## 11. Clean-room boundary

This demo is deliberately synthetic.

It must not include:

- real mission names;
- private subsystem architectures;
- private bus maps;
- private payload protocols;
- real thresholds from private missions;
- real operational procedures;
- real telemetry logs;
- real anomaly sequences;
- real payload data;
- real storage or downlink policies.

The demo exists to prove OrbitFabric's architecture, not to approximate a real spacecraft.
