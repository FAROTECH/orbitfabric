# Runtime Contract Bindings

Status: Introduced in v0.7.0  
Scope: Generated Runtime-Facing Contract Bindings

---

## Purpose

Runtime Contract Bindings are generated software-facing artifacts derived from the validated OrbitFabric Mission Model.

They provide a deterministic boundary that implementation code can include, compile and implement against.

They do not implement onboard behavior.

The intended flow is:

```text
Mission Model
        -> validation and linting
        -> RuntimeContract
        -> generated C++17 contract bindings
        -> host-build smoke validation
        -> user implementation outside generated/
```

---

## Boundary

Runtime Contract Bindings are contract-facing artifacts.

They are intended to expose:

```text
stable identifiers
typed command argument structs
static metadata registries
abstract integration interfaces
host-build smoke files
```

They are not intended to expose:

```text
runtime loops
command queues
command dispatch implementation
scheduler behavior
HAL or driver abstractions
RTOS integration
binary serialization
CCSDS/PUS/CFDP behavior
flight software behavior
```

Generated files are disposable and reproducible.

User code must live outside `generated/`.

---

## Command

Runtime bindings are generated with:

```bash
orbitfabric gen runtime examples/demo-3u/mission/
```

By default, the generator writes to:

```text
generated/runtime/cpp17/
```

The currently supported generation profile is:

```text
cpp17
```

---

## Generated output

The C++17 profile generates:

```text
generated/runtime/cpp17/runtime_contract_manifest.json
generated/runtime/cpp17/include/orbitfabric/generated/mission_ids.hpp
generated/runtime/cpp17/include/orbitfabric/generated/mission_enums.hpp
generated/runtime/cpp17/include/orbitfabric/generated/mission_registries.hpp
generated/runtime/cpp17/include/orbitfabric/generated/command_args.hpp
generated/runtime/cpp17/include/orbitfabric/generated/adapter_interfaces.hpp
generated/runtime/cpp17/CMakeLists.txt
generated/runtime/cpp17/src/orbitfabric_runtime_contract_smoke.cpp
```

These files are generated artifacts.

They are not committed as source files in the repository.

---

## RuntimeContract manifest

The runtime contract manifest is a JSON representation of the software-facing contract surface.

It records:

```text
mission identity
generation profile
contract counts
modes
telemetry
commands
events
faults
packets
payloads
data products
storage policies
downlink policies
```

It also records that the generated output:

```text
contains_flight_runtime = false
generated_artifacts_are_disposable = true
```

---

## Identifier headers

`mission_ids.hpp` contains deterministic strongly typed identifiers such as:

```text
ModeId
TelemetryId
CommandId
EventId
FaultId
PacketId
PayloadId
DataProductId
StoragePolicyId
DownlinkPolicyId
```

Each enum reserves:

```cpp
Invalid = 0
```

Real identifiers are derived deterministically from the RuntimeContract.

---

## Runtime enums

`mission_enums.hpp` contains runtime-facing value enums derived from the contract surface.

For example:

```text
RuntimeValueType
```

This is metadata for generated contract bindings.

It is not a serializer, decoder or telemetry runtime.

---

## Static registries

`mission_registries.hpp` contains static descriptor arrays for contract metadata.

The generated registries include:

```text
TelemetryRegistry
CommandRegistry
EventRegistry
FaultRegistry
DataProductRegistry
```

These registries expose metadata such as model IDs, symbol names, value types, units, sources, severities, command targets and data product attributes.

They do not read sensors, execute commands, report events, manage faults or move data.

---

## Command argument structs

`command_args.hpp` contains one typed argument struct per command.

For example:

```cpp
struct PayloadStartAcquisitionArgs {
    std::uint16_t duration_s;
};
```

These structs provide a deterministic contract-facing shape for command arguments.

They do not parse packets, validate command authorization, enqueue commands or execute command behavior.

---

## Adapter interfaces

`adapter_interfaces.hpp` contains abstract interfaces that implementation code may implement outside `generated/`.

The generated interfaces include:

```text
ICommandHandler
ITelemetrySink
IEventReporter
IFaultReporter
```

For example:

```cpp
class ICommandHandler {
public:
    virtual ~ICommandHandler() = default;

    virtual CommandResult handle_payload_start_acquisition(
        const PayloadStartAcquisitionArgs& args
    ) = 0;
};
```

These are integration boundaries only.

They are not concrete handlers, dispatchers, queues, schedulers or runtime services.

---

## Host-build smoke validation

The C++17 profile also generates:

```text
CMakeLists.txt
src/orbitfabric_runtime_contract_smoke.cpp
```

This allows the generated contract bindings to be validated with a host-side C++17 build:

```bash
cmake -S generated/runtime/cpp17 -B generated/runtime/cpp17/build
cmake --build generated/runtime/cpp17/build
```

This confirms that the emitted contract-binding surface is syntactically valid and buildable as C++17.

It does not validate flight behavior.

---

## Non-goals

Runtime Contract Bindings intentionally do not implement:

```text
flight runtime
onboard application framework
command dispatch runtime
command queue
command validation runtime
telemetry polling runtime
event routing runtime
fault manager runtime
scheduler
HAL
drivers
RTOS abstraction
Linux daemon
binary serialization
CCSDS/PUS/CFDP mapping
storage runtime
downlink runtime
user-code merge
protected regions
```

These are outside the v0.7.0 boundary.

---

## Architectural meaning

Runtime Contract Bindings are the first software-facing output of OrbitFabric.

They make the Mission Model visible to implementation code without turning OrbitFabric into flight software.

The key architectural rule remains:

```text
generated code is disposable;
user code lives outside generated/;
integration happens through interfaces.
```
