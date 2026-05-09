# ADR-0011 — Generated Runtime Skeleton Boundary

Status: Accepted for v0.7.0  
Date: 2026-05-09

---

## Context

OrbitFabric is a model-first Mission Data Contract framework for small spacecraft.

The v0.6.0 baseline introduced End-to-End Mission Data Flow Evidence.

The Mission Data Chain connects:

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

The v0.7.0 milestone introduces the first explicit bridge between the Mission Data Contract and software-facing implementation artifacts.

That bridge is valuable, but it is architecturally sensitive.

OrbitFabric must not become flight software, an onboard runtime, a scheduler, a HAL, a transport layer, a command stack, a storage runtime, a downlink runtime or a ground segment.

The source of truth must remain the Mission Model.

Generated runtime skeletons are therefore defined as runtime-facing contract bindings, not runtime behavior.

---

## Decision

OrbitFabric v0.7.0 introduces Generated Runtime Skeletons as deterministic, host-buildable, inspectable and regenerable software-facing artifacts derived from the validated Mission Model.

The generated artifacts expose contract-aligned identifiers, descriptors, typed command argument structures, static registries and narrow adapter interfaces.

They do not implement onboard behavior.

The architectural interpretation is:

```text
Mission Model
        -> validated MissionModel
        -> RuntimeContract intermediate model
        -> generated runtime-facing contract bindings
        -> host-buildable evidence
```

The forbidden interpretation is:

```text
Mission Model
        -> generated flight software
        -> generated onboard runtime
        -> generated scheduler / HAL / transport / storage / downlink behavior
```

The preferred internal term is:

```text
Runtime-facing contract bindings
```

The public milestone name remains:

```text
Generated Runtime Skeletons
```

---

## Core Principle

OrbitFabric v0.7 does not generate onboard behavior.

It generates the contract-aligned software boundary that onboard behavior can implement.

This principle is mandatory.

Every v0.7 feature must be evaluated against it.

---

## RuntimeContract Intermediate Model

v0.7.0 introduces a RuntimeContract intermediate model.

The generator must not read raw YAML in scattered places.

The required dependency direction is:

```text
CLI
        -> Mission Model loading and validation
        -> RuntimeContract builder
        -> profile-specific generator
        -> generated files
```

The disallowed dependency direction is:

```text
profile-specific generator
        -> raw YAML files
        -> simulator internals
        -> documentation generator internals
```

The RuntimeContract is intentionally smaller than the full Mission Model.

It contains only the contract surface that is meaningful for software-facing generated artifacts.

RuntimeContract domains include:

```text
mission identity
modes
telemetry items
commands
command arguments
events
faults
packets
payloads
data products
storage policy identifiers
downlink policy identifiers
generation metadata
```

Each exported element carries a deterministic software symbol, a stable generated numeric identifier and a reference to the Mission Model source identity.

---

## Initial Generation Profile

The first supported generation profile is:

```text
cpp17
```

The generated output root is:

```text
generated/runtime/cpp17/
```

The current v0.7.0 output is:

```text
generated/runtime/cpp17/
├── runtime_contract_manifest.json
├── CMakeLists.txt
├── include/
│   └── orbitfabric/
│       └── generated/
│           ├── mission_ids.hpp
│           ├── mission_enums.hpp
│           ├── mission_registries.hpp
│           ├── command_args.hpp
│           └── adapter_interfaces.hpp
└── src/
    └── orbitfabric_runtime_contract_smoke.cpp
```

Generated C++17 code is simple, static, readable and dependency-light.

---

## Generated Artifact Semantics

Generated artifacts are reproducible outputs.

They are not the source of truth.

The source of truth remains:

```text
mission/*.yaml
```

Generated artifacts are disposable.

They may be overwritten on every generation.

Users must not place handwritten implementation code inside generated files.

OrbitFabric does not rely on protected regions in v0.7.0.

User implementation must live outside the generated tree and integrate through generated identifiers, descriptors, typed structures and interfaces.

---

## v0.7.0 Scope

The v0.7.0 core scope includes:

```text
RuntimeContract intermediate model
deterministic naming rules
deterministic generated numeric identifiers
orbitfabric gen runtime command
cpp17 generation profile
generated IDs and enums
generated descriptors
generated static registries
generated command argument structs
generated narrow adapter interfaces
generation manifest
generated host-buildable CMake smoke target
tests for determinism, output structure and naming
documentation of scope, boundary and non-goals
```

The implementation remains narrow.

The goal is to prove a stable contract-binding architecture, not to maximize the amount of generated code.

---

## Deferred v0.7.x Candidates

The following may be considered after the v0.7.0 core is stable:

```text
minimal typed command dispatch helper
richer command handler interface
mode transition descriptor table
JSON export of RuntimeContract
C profile
Python host-test profile
example user implementation outside generated/
CI-level host build matrix
```

These are not required for the first v0.7.0 release.

---

## Non-Goals

v0.7.0 must not introduce:

```text
flight-ready onboard runtime
scheduler
RTOS abstraction
HAL
drivers
SPI / I2C / UART transport
radio transport
CCSDS / PUS / CFDP implementation
binary command parser
command authentication
command authorization
command queue
telemetry polling runtime
telemetry publish/subscribe runtime
mode manager runtime
fault manager runtime
FDIR implementation
watchdog integration
storage runtime
downlink runtime
ground station runtime
Yamcs runtime integration
OpenC3 runtime integration
Linux daemon template
bare-metal application template
threading model
protected regions
user-code merge inside generated files
private mission code
```

These are not missing features of v0.7.0.

They are intentionally outside the milestone boundary.

---

## Command Skeleton Boundary

Command-related generation may include typed command argument structures and narrow interfaces.

It may expose a software-facing call boundary such as:

```text
CommandId + typed args -> user-provided handler boundary
```

It must not implement command reception, packet parsing, authentication, authorization, queuing, scheduling, timeout handling, retry handling or real acknowledgement behavior.

A command dispatch helper may be introduced only if it remains a deterministic host-buildable contract helper and does not become a runtime command stack.

---

## Telemetry Skeleton Boundary

Telemetry-related generation may include telemetry identifiers, descriptors and static registries.

It may describe:

```text
telemetry identity
type
unit
subsystem
mode or context metadata when available
```

It must not read sensors, poll drivers, schedule sampling, buffer telemetry, publish telemetry over a bus, packetize telemetry or downlink telemetry.

---

## Data Product Skeleton Boundary

Data product generation is part of the v0.7 value proposition because it connects earlier OrbitFabric milestones to software-facing artifacts.

Generated data product descriptors may expose:

```text
data product identity
source payload or subsystem
storage policy identifier
downlink policy identifier
criticality or priority metadata when available
```

They must not implement storage, compression, retention, routing, contact scheduling or downlink execution.

---

## Event, Fault and Mode Boundary

Event, fault and mode generation may include identifiers, descriptors and static metadata.

It must not implement:

```text
event emission runtime
fault detection runtime
fault recovery runtime
mode transition execution
safe-mode logic
FDIR behavior
```

Mode transition descriptor tables may be considered only as contract metadata if the Mission Model provides enough declared information.

A generated mode manager is outside v0.7.0 scope.

---

## Adapter Interface Boundary

Adapter interfaces may be generated only when they remain contract-oriented.

Acceptable interface direction:

```text
ICommandHandler
ITelemetryProvider or ITelemetrySink
IDataProductSink
IEventReporter
IFaultReporter
```

Disallowed interface direction:

```text
ISpiDriver
IUartDriver
IStorageDriver
IRadioTransport
IScheduler
IWatchdog
IRtosTask
```

OrbitFabric may define what contract events cross the boundary.

It must not define how the spacecraft platform implements transport, scheduling, storage, drivers or watchdog behavior.

---

## Determinism Rules

Generated outputs must be deterministic.

Repeated generation from the same validated Mission Model and the same generator version must produce equivalent file contents.

The implementation should avoid generation timestamps in file contents unless explicitly disabled by default or captured only in non-deterministic optional metadata.

Ordering must be stable and testable.

Generated numeric identifiers must be deterministic.

The initial strategy reserves `Invalid = 0` and assigns deterministic identifiers per domain.

Generated numeric identifiers are skeleton identifiers unless the Mission Model later introduces explicit normative IDs.

They must not be presented as flight protocol IDs by default.

---

## Testing Direction

v0.7.0 includes tests for:

```text
RuntimeContract construction
deterministic naming rules
deterministic numeric ID assignment
CLI runtime generation
expected output tree structure
generated file content smoke checks
regeneration stability
```

The required local release checks remain:

```bash
ruff check .
pytest
mkdocs build --strict
```

The runtime generation flow additionally supports:

```bash
orbitfabric lint examples/demo-3u/mission/
orbitfabric gen runtime examples/demo-3u/mission/ --profile cpp17
cmake -S generated/runtime/cpp17 -B generated/runtime/cpp17/build
cmake --build generated/runtime/cpp17/build
```

The release candidate must still be host-built before tagging v0.7.0.

---

## Branch and Release Process

v0.7.0 was developed through a milestone integration branch.

The process was:

```text
main
  ↑ final release PR only
release/v0.7.0-runtime-skeletons
  ↑ feature PRs
feature/v0.7-runtime-boundary-adr
feature/v0.7-runtime-contract-model
feature/v0.7-runtime-cli-minimal
feature/v0.7-cpp17-ids-enums
feature/v0.7-runtime-registries
feature/v0.7-command-args
feature/v0.7-adapter-interfaces
feature/v0.7-host-build-smoke
feature/v0.7-runtime-docs
feature/v0.7-release-alignment
```

Feature branches converged into the release branch first.

The release branch should merge into main only when the v0.7.0 core is stable.

The `v0.7.0` tag must be created only after the final release PR reaches main.

---

## Consequences

This decision creates a controlled bridge from Mission Data Contracts to software-facing artifacts.

It makes OrbitFabric more useful to embedded, onboard, simulator and ground-integration developers without turning OrbitFabric into a flight software framework.

It enables future generation profiles without coupling them directly to raw YAML or internal simulator behavior.

It also creates a clear review boundary for v0.7 work:

```text
Does this generated artifact expose contract-aligned software boundary?
Or does it implement runtime behavior?
```

Only the first category belongs in v0.7.0.

---

## Acceptance Criteria for This Decision

This ADR is satisfied when:

- generated runtime skeletons are defined as runtime-facing contract bindings;
- the non-flight-software boundary is explicit;
- RuntimeContract is selected as the mandatory intermediate model;
- generated artifacts are defined as deterministic, inspectable and disposable;
- user implementation is required to live outside generated files;
- protected regions are excluded from v0.7.0;
- the initial `cpp17` profile is defined as host-buildable;
- v0.7.0 core scope is documented;
- v0.7.x candidates are separated from v0.7.0 core;
- non-goals are explicit;
- testing expectations are documented;
- the milestone branch strategy is documented.

---

## Final Position

Generated Runtime Skeletons are valuable only if they preserve OrbitFabric's identity.

The v0.7.0 milestone generates the software boundary derived from the Mission Model.

It does not generate the spacecraft runtime that lives behind that boundary.
