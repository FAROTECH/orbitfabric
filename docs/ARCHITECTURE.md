# OrbitFabric - Architecture

Version: 0.9.0 development baseline  
Status: Development preview  
Scope: Mission Data Contract architecture through Relationship Manifest Surface

---

## 1. Architectural Intent

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

Its architecture is centered on one primary artifact:

> the Mission Data Contract.

The Mission Data Contract is expressed as a structured Mission Model.

It defines mission data, operational behavior, payload contracts, data products, storage intent, contact/downlink assumptions, commandability/autonomy assumptions, data-flow evidence, runtime-facing contract bindings, ground-facing integration artifacts, Core-owned introspection surfaces, entity index surfaces, relationship manifest surfaces, documentation and scenario evidence from one source of truth.

OrbitFabric is not designed as:

```text
flight software framework
ground segment
mission control system
operator console
telemetry archive
spacecraft dynamics simulator
payload runtime framework
CCSDS/PUS/CFDP implementation
hardware abstraction layer
visual modeling tool
Studio-specific backend API
plugin execution platform
```

Its architectural role is:

> define, validate, simulate, document, introspect, index, relate and generate contract-facing artifacts between mission design, onboard software, tests, documentation, simulation, runtime-facing bindings, ground-facing integration and downstream inspection tools.

The current architectural development baseline is `v0.9.0 - Relationship Manifest Surface and Extensibility Boundary`.

The package and CLI version remain `0.8.2` until the final v0.9.0 release preparation PR.

v0.8.1 introduced the first Core-owned read-only model summary surface derived from the loaded Mission Model.

v0.8.2 introduced the first Core-owned read-only entity index surface derived from the loaded Mission Model.

v0.9.0 introduces the first Core-owned read-only relationship manifest surface derived from explicit loaded Mission Model fields.

---

## 2. Architectural Principles

### 2.1 Mission Model First

The Mission Model is the source of truth.

Runtime-facing bindings, ground-facing artifacts, contract introspection reports, entity index reports, relationship manifest reports, simulation behavior and generated documentation must derive from the model.

No important mission behavior should live only in Python code, documentation, generated files, simulator internals, plugin outputs or downstream tools.

### 2.2 Contract Before Runtime

OrbitFabric does not implement a flight runtime or a ground runtime.

It implements a host-side toolchain that proves and hardens the Mission Data Contract.

v0.7.0 introduced generated runtime-facing contract bindings, not onboard behavior.

v0.8.0 introduced generated ground-facing contract exports, not ground behavior.

v0.8.1 introduced a Core-owned model summary report, not relationship graphs or plugins.

v0.8.2 introduced a Core-owned entity index report, not relationship graphs or plugins.

v0.9.0 introduces a Core-owned relationship manifest report, not graph execution, plugin execution or Studio-specific behavior.

### 2.3 Chain Before Generated Artifacts

OrbitFabric models the Mission Data Chain before generating downstream artifacts.

The current chain is:

```text
Payload behavior
        -> Data Product Contract
        -> Storage Intent
        -> Downlink Intent
        -> Contact Windows and Downlink Flow Contracts
        -> Commandability and Autonomy Contracts
        -> End-to-End Mission Data Flow Evidence
        -> Runtime-Facing Contract Bindings
        -> Ground-Facing Integration Artifacts
        -> Contract Introspection Surface
        -> Entity Index Surface
        -> Relationship Manifest Surface
```

### 2.4 Generated Bindings, Exports and Reports Are Not Behavior

Generated Runtime Skeletons are contract bindings.

Generated Ground Integration Artifacts are contract exports.

Generated Contract Introspection reports are Core-owned read-only summaries.

Generated Entity Index reports are Core-owned read-only entity indexes.

Generated Relationship Manifest reports are Core-owned read-only relationship records.

They may expose identifiers, descriptors, typed command argument structures, static registries, abstract interfaces, manifests, dictionaries, review documents, domain-level model summaries, entity-level records and relationship records.

They must not implement command dispatch, queues, scheduling, HAL, drivers, RTOS integration, telemetry polling, fault management, storage runtime, downlink runtime, decoder runtime, database behavior, operator workflows, live ground operations, relationship graph behavior or plugin execution.

### 2.5 Lint as Engineering Judgment

`orbitfabric lint` is a core architectural component.

It must detect mission consistency issues, not merely invalid YAML.

A concept that can become operationally ambiguous should have a lint rule before downstream runtime-facing, ground-facing, introspection, entity-index or relationship artifacts depend on it.

### 2.6 Docs from Model

Documentation generated by OrbitFabric must derive from the validated Mission Model.

Generated mission documentation is not the source of truth.

The model is the source of truth.

### 2.7 Scenario-First Operational Testing

Scenarios are structured artifacts.

They describe operational sequences and expected outcomes.

The simulator executes scenarios to validate contract-level behavior.

The simulator is deterministic and host-side.

It is not a real-time onboard runtime.

### 2.8 Downstream Tools Consume, Not Infer

Downstream tools should consume Core-generated structured surfaces.

They must not reconstruct Mission Model semantics from raw YAML, generated files or human-oriented CLI output.

v0.8.1 establishes this principle with `model_summary.json`.

v0.8.2 extends it with `entity_index.json`.

v0.9.0 extends it with `relationship_manifest.json`.

---

## 3. High-Level System View

```text
OrbitFabric
├── Mission Data Contract
│   ├── spacecraft
│   ├── subsystems
│   ├── modes
│   ├── telemetry
│   ├── commands
│   ├── events
│   ├── faults
│   ├── packets
│   ├── policies
│   ├── payload contracts
│   ├── data product contracts
│   ├── contact/downlink contracts
│   ├── commandability/autonomy contracts
│   ├── data-flow evidence contracts
│   ├── runtime-facing contract binding inputs
│   ├── ground-facing contract export inputs
│   ├── contract introspection inputs
│   ├── entity index inputs
│   ├── relationship manifest inputs
│   └── scenarios
│
├── Toolchain
│   ├── orbitfabric inspect mission
│   ├── orbitfabric validate scenario
│   ├── orbitfabric lint
│   ├── orbitfabric gen docs
│   ├── orbitfabric gen data-flow
│   ├── orbitfabric gen runtime
│   ├── orbitfabric gen ground
│   ├── orbitfabric export model-summary
│   ├── orbitfabric export entity-index
│   ├── orbitfabric export relationship-manifest
│   └── orbitfabric sim
│
├── Model Layer
├── Lint Layer
├── Simulation Layer
├── RuntimeContract Layer
├── GroundContract Layer
├── Export Layer
├── Generation Layer
└── Future Extension Layer
```

---

## 4. Current Capability Boundary - v0.9.0 Development Baseline

OrbitFabric currently includes:

```text
Mission Model YAML
canonical multi-file mission directory
optional payloads.yaml domain
optional data_products.yaml domain
optional contacts.yaml domain
optional commandability.yaml domain
Pydantic typed validation
structural validation
semantic lint
scenario loading and reference validation
host-side deterministic scenario execution
contract-level data-flow evidence recording
generated Markdown docs
JSON lint reports
JSON scenario reports with data_flow_evidence
RuntimeContract intermediate model
orbitfabric gen runtime command
C++17 runtime-facing contract bindings
C++17 host-build smoke CMake target
GroundContract intermediate model
orbitfabric gen ground command
generic ground contract manifest
JSON ground dictionaries
CSV ground dictionaries
human-reviewable ground Markdown artifacts
orbitfabric export model-summary command
model_summary.json contract introspection report
orbitfabric export entity-index command
entity_index.json entity index report
orbitfabric export relationship-manifest command
relationship_manifest.json candidate relationship report
synthetic demo mission
```

OrbitFabric currently excludes:

```text
flight runtime
embedded deployment
RTOS integration
Linux onboard service
hardware drivers
real onboard storage runtime
real downlink execution
downlink runtime
ground segment
mission control system
operator console
telemetry archive
telemetry database
command uplink service
telecommand transport
network/session/routing behavior
binary packet decoder
binary telecommand encoder
Yamcs integration
OpenC3 integration
XTCE compliance
CCSDS/PUS/CFDP implementation
security enforcement
real command authentication
real command authorization
live uplink services
flight autonomy runtime
real FDIR or safing logic
relationship graph
dependency graph
plugin API
plugin discovery
plugin loader
plugin execution
Studio-specific API
```

These are intentional architectural boundaries.

---

## 5. Canonical Data Flow

The canonical OrbitFabric flow is:

```text
Mission YAML files
      │
      ▼
Model Loader
      │
      ▼
Typed Mission Model
      │
      ├──────────────► Lint Engine ─────────────► Lint Report
      │
      ├──────────────► Documentation Generator ─► Markdown Docs
      │
      ├──────────────► Scenario Runner ─────────► Simulation Log + Scenario Report
      │
      ├──────────────► RuntimeContract Builder ─► Runtime-Facing Contract Bindings
      │
      ├──────────────► GroundContract Builder ──► Ground-Facing Integration Artifacts
      │
      └──────────────► Export Layer ────────────► Core-Owned Structured Surfaces
```

The model is loaded once and consumed by multiple downstream layers.

No generator, simulator, exporter, plugin or downstream tool should independently reinterpret raw YAML.

---

## 6. Mission Data Chain View

The current Mission Data Chain view is:

```text
Subsystems and payloads
      │
      ▼
Telemetry, commands, events, faults and modes
      │
      ▼
Payload Contracts
      │
      ▼
Data Product Contracts
      │
      ▼
Storage Intent and Downlink Intent
      │
      ▼
Contact Windows and Downlink Flow Contracts
      │
      ▼
Commandability and Autonomy Contracts
      │
      ▼
End-to-End Mission Data Flow Evidence
      │
      ▼
Runtime-Facing Contract Bindings
      │
      ▼
Ground-Facing Integration Artifacts
      │
      ▼
Contract Introspection Surface
      │
      ▼
Entity Index Surface
      │
      ▼
Relationship Manifest Surface
```

This is the architectural reason OrbitFabric did not jump directly from payload contracts to plugins.

Plugins and downstream tools are useful only after the mission data chain and Core-owned structured surfaces are explicit enough to consume safely.

---

## 7. Command-Line Architecture

The current CLI exposes these primary commands:

```bash
orbitfabric --version
orbitfabric lint examples/demo-3u/mission/
orbitfabric gen docs examples/demo-3u/mission/
orbitfabric gen data-flow examples/demo-3u/mission/
orbitfabric gen runtime examples/demo-3u/mission/
orbitfabric gen ground examples/demo-3u/mission/
orbitfabric export model-summary examples/demo-3u/mission/ --json generated/reports/model_summary.json
orbitfabric export entity-index examples/demo-3u/mission/ --json generated/reports/entity_index.json
orbitfabric export relationship-manifest examples/demo-3u/mission/ --json generated/reports/relationship_manifest.json
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml
orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml
orbitfabric inspect mission examples/demo-3u/mission/
orbitfabric validate scenario examples/demo-3u/scenarios/payload_data_flow_evidence.yaml
```

Conceptual CLI structure:

```text
orbitfabric
├── lint <mission-dir>
├── gen
│   ├── docs <mission-dir>
│   ├── data-flow <mission-dir>
│   ├── runtime <mission-dir>
│   └── ground <mission-dir>
├── export
│   ├── model-summary <mission-dir>
│   ├── entity-index <mission-dir>
│   └── relationship-manifest <mission-dir>
├── sim <scenario-file>
├── inspect
│   └── mission <mission-dir>
└── validate
    └── scenario <scenario-file>
```

Future commands may include tool-specific exporters and plugin-related commands only after their semantics, trust model and boundaries are implemented and tested explicitly.

---

## 8. RuntimeContract Architecture

RuntimeContract is the intermediate model for runtime-facing generation.

The required dependency direction is:

```text
Mission Model
        -> validation and linting
        -> RuntimeContract builder
        -> profile-specific generator
        -> generated runtime-facing files
```

RuntimeContract contains the software-facing subset of the Mission Data Contract.

It is not flight software and it is not the source of truth.

---

## 9. GroundContract Architecture

GroundContract is the intermediate model for ground-facing generation.

The required dependency direction is:

```text
Mission Model
        -> validation and linting
        -> GroundContract builder
        -> generic ground exporter
        -> generated ground-facing package
```

The disallowed direction is:

```text
ground exporter
        -> raw YAML files
        -> simulator internals
        -> runtime generator internals
        -> generated runtime files
```

GroundContract contains the ground-facing subset of the Mission Data Contract.

It is not a mission database runtime.

It is not a ground segment configuration format.

It is not the source of truth.

---

## 10. Export Layer Architecture

v0.8.1 introduced the first export layer surface:

```text
model_summary.json
```

v0.8.2 introduced the second export layer surface:

```text
entity_index.json
```

v0.9.0 introduces the third export layer surface:

```text
relationship_manifest.json
```

The required dependency direction is:

```text
Mission Model
        -> canonical loader
        -> validated MissionModel
        -> export layer
        -> model_summary.json
        -> entity_index.json
        -> relationship_manifest.json
```

The disallowed direction is:

```text
export layer
        -> raw YAML files
        -> generated docs
        -> generated runtime files
        -> generated ground files
        -> human-oriented CLI output
        -> downstream UI state
        -> plugin assumptions
```

The model summary report contains domain-level information only.

The entity index report contains entity-level records only.

The relationship manifest report contains admitted Core-owned relationship records only.

None of these surfaces contains source locations, YAML AST data, plugin definitions, Studio-specific formatting, runtime behavior or ground behavior.

---

## 11. Relationship Manifest Architecture

The Relationship Manifest Surface is a Core-owned read-only candidate report.

It references entities already exposed by the Entity Index Surface.

It does not create independent synthetic downstream nodes.

Every emitted relationship record must be derived from explicit loaded Mission Model fields.

It must not derive records from:

```text
naming conventions
string similarity
ID prefixes
source file names
YAML file ordering
generated Markdown
generated runtime files
generated ground files
human-oriented CLI output
Studio UI state
React component state
private downstream assumptions
```

For `examples/demo-3u/mission`, the current manifest emits 46 relationship records across 17 emitted relationship families.

The candidate surface currently admits 19 relationship families documented in `docs/reference/relationship-manifest-surface.md`.

The relationship manifest is not:

```text
a graph engine
a dependency graph
a visualization format
a Studio API
a layout format
a runtime routing table
a ground routing table
a scheduler input
a command dispatcher input
a plugin API
```

A downstream tool may render a graph from relationship records, but the engineering meaning of every edge must still come from Core.

---

## 12. Ground-Facing Generation Layer

The generic ground profile generates:

```text
generated/ground/generic/
├── ground_contract_manifest.json
├── README.md
├── dictionaries/*.json
├── csv/*.csv
└── ground_dictionaries.md
```

These artifacts expose telemetry, command, event, fault, data product and packet contract metadata.

They do not expose binary packet decoders, ground runtime, telemetry archive, database implementation, operator console, command uplink service, Yamcs compatibility, OpenC3 compatibility, XTCE compliance, CCSDS/PUS/CFDP behavior or security enforcement.

Generated ground artifacts are disposable.

Downstream ground integration code must live outside generated OrbitFabric output unless explicitly generated by a future tool-specific profile.

---

## 13. Runtime-Facing Generation Layer

The C++17 runtime profile generates:

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

These artifacts expose stable generated identifiers, typed command argument structs, static metadata registries, abstract adapter interfaces and host-build smoke validation.

They do not implement flight behavior.

Generated runtime-facing artifacts are disposable.

User implementation code must live outside `generated/`.

---

## 14. Host-Build, Ground Export and Structured Surface Validation

Runtime-facing bindings can be validated with:

```bash
orbitfabric gen runtime examples/demo-3u/mission/
cmake -S generated/runtime/cpp17 -B generated/runtime/cpp17/build
cmake --build generated/runtime/cpp17/build
```

Ground-facing artifacts can be validated with:

```bash
orbitfabric gen ground examples/demo-3u/mission/
```

The model summary surface can be validated with:

```bash
orbitfabric export model-summary examples/demo-3u/mission/ \
  --json generated/reports/model_summary.json
```

The entity index surface can be validated with:

```bash
orbitfabric export entity-index examples/demo-3u/mission/ \
  --json generated/reports/entity_index.json
```

The relationship manifest surface can be validated with:

```bash
orbitfabric export relationship-manifest examples/demo-3u/mission/ \
  --json generated/reports/relationship_manifest.json
```

These commands confirm that the generated contract surfaces are syntactically valid and reproducible on the host.

They do not validate flight behavior, live ground behavior, relationship graph behavior or plugin behavior.

---

## 15. Documentation Generation Layer

The Generation Layer derives human-readable and machine-readable artifacts from the Mission Model.

Current generated mission documentation includes:

```text
generated/docs/telemetry.md
generated/docs/commands.md
generated/docs/events.md
generated/docs/faults.md
generated/docs/modes.md
generated/docs/packets.md
generated/docs/payloads.md
generated/docs/data_products.md
generated/docs/contacts.md
generated/docs/commandability.md
generated/docs/data_flow.md
```

Ground-facing review artifacts are generated under:

```text
generated/ground/generic/
```

Core-owned structured reports are generated under:

```text
generated/reports/
```

Generated documentation and reports are not the source of truth.

---

## 16. Demo Mission Architecture

The canonical demo is `demo-3u`.

Canonical structure:

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

The demo must stay synthetic and clean-room.

---

## 17. Reports and Generated Artifact Architecture

Reports are JSON where machine-readable output is required.

Generated artifact manifests are also JSON where deterministic downstream inspection is required.

Current generated JSON families include:

```text
lint reports
simulation reports
runtime contract manifest
ground contract manifest
ground dictionaries
model summary report
entity index report
relationship manifest report
```

Reports and manifests must remain stable enough for tests and CI, but they are still development-preview artifacts before v1.0.

---

## 18. Layer Dependency Rules

Allowed dependencies:

```text
cli -> model
cli -> lint
cli -> sim
cli -> gen
cli -> export
cli -> reports

lint -> model
sim -> model
sim -> reports
gen -> model
gen -> RuntimeContract builder
gen -> GroundContract builder
export -> model
RuntimeContract builder -> model
GroundContract builder -> model
reports -> lint report data
reports -> simulation report data
```

Forbidden dependencies:

```text
model -> cli
model -> sim
model -> gen
model -> export
model -> lint policy
lint -> sim
sim -> gen
gen -> sim
RuntimeContract builder -> raw YAML files
GroundContract builder -> raw YAML files
profile-specific generator -> raw YAML files
exporter -> raw YAML files
relationship exporter -> raw YAML files
relationship exporter -> generated Markdown
relationship exporter -> downstream UI state
plugin output -> Core-owned relationship manifest
```

The Model Layer must remain the lowest stable layer.

---

## 19. Testing Architecture

Current test strategy covers:

```text
model loader tests
structural validation tests
duplicate identifier tests
cross-reference lint tests
engineering lint rules
payload contract lint rules
data product contract lint rules
contact/downlink contract lint rules
commandability/autonomy lint rules
command data-product effect lint rules
scenario validation tests
scenario data-flow expectation tests
scenario execution tests
data-flow evidence JSON report tests
documentation generator tests
RuntimeContract builder tests
C++17 runtime generator tests
GroundContract builder tests
ground manifest tests
ground JSON export tests
ground CSV export tests
ground Markdown export tests
model summary export tests
entity index export tests
relationship manifest export tests
relationship manifest CLI tests
CLI smoke tests
```

CI runs:

```text
ruff check .
pytest
orbitfabric lint examples/demo-3u/mission/
orbitfabric gen docs examples/demo-3u/mission/
orbitfabric gen data-flow examples/demo-3u/mission/
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml
orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml
mkdocs build --strict
```

Release validation additionally includes:

```bash
orbitfabric export model-summary examples/demo-3u/mission/ \
  --json generated/reports/model_summary.json
orbitfabric export entity-index examples/demo-3u/mission/ \
  --json generated/reports/entity_index.json
orbitfabric export relationship-manifest examples/demo-3u/mission/ \
  --json generated/reports/relationship_manifest.json
orbitfabric gen runtime examples/demo-3u/mission/
cmake -S generated/runtime/cpp17 -B generated/runtime/cpp17/build
cmake --build generated/runtime/cpp17/build
orbitfabric gen ground examples/demo-3u/mission/
```

---

## 20. Future Extension Architecture

Future extensions should be added as generators, plugins or adapters.

Possible future layers:

```text
Custom Ground Exporters
Custom Lint Rule Plugins
Custom Mission Model Extensions
Runtime Adapter SDK
Plugin Metadata Manifests
Yamcs Export Generator
OpenC3 Export Generator
XTCE Export Generator
Basilisk Bridge
cFS/F Prime Integration Bridges
```

These must remain downstream of the Mission Model and Core-owned structured surfaces.

They must not redefine the mission contract.

Plugin execution requires explicit trust and security design before arbitrary or untrusted plugin code is supported.

---

## 21. Anti-Patterns

The following patterns are architecturally wrong:

```text
runtime-first drift
ground-first drift
demo-driven special cases
hidden mission logic
premature standard compliance
ground segment creep
flight framework creep
simulation creep
storage runtime creep
downlink runtime creep
plugin-before-core-surface creep
relationship-graph-before-relationship-semantics creep
proprietary example contamination
```

---

## 22. v0.9.0 Development Acceptance Architecture

OrbitFabric v0.9.0 is architecturally acceptable when this flow works end-to-end:

```bash
ruff check .
pytest
mkdocs build --strict

orbitfabric lint examples/demo-3u/mission/ \
  --json generated/reports/lint_report.json

orbitfabric export model-summary examples/demo-3u/mission/ \
  --json generated/reports/model_summary.json

orbitfabric export entity-index examples/demo-3u/mission/ \
  --json generated/reports/entity_index.json

orbitfabric export relationship-manifest examples/demo-3u/mission/ \
  --json generated/reports/relationship_manifest.json

orbitfabric gen docs examples/demo-3u/mission/

orbitfabric gen data-flow examples/demo-3u/mission/ \
  --output-file generated/docs/data_flow.md

orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml \
  --json generated/reports/battery_low_during_payload_report.json \
  --log generated/logs/battery_low_during_payload.log

orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml \
  --json generated/reports/payload_data_flow_evidence_report.json \
  --log generated/logs/payload_data_flow_evidence.log

orbitfabric gen runtime examples/demo-3u/mission/

cmake -S generated/runtime/cpp17 -B generated/runtime/cpp17/build
cmake --build generated/runtime/cpp17/build

orbitfabric gen ground examples/demo-3u/mission/
```

And produces:

```text
valid lint output
model_summary.json
entity_index.json
relationship_manifest.json
Markdown mission documentation
scenario execution logs
scenario JSON reports
data_flow_evidence JSON records
RuntimeContract manifest
C++17 runtime-facing contract headers
host-build smoke validation
GroundContract manifest
JSON ground dictionaries
CSV ground dictionaries
human-reviewable ground Markdown artifacts
```

No flight runtime, live ground segment, orbital propagation, RF simulation, storage/downlink runtime, live uplink, decoder runtime, telemetry archive, operator console, autonomy runtime, relationship graph or plugin API is required for v0.9.0.

---

## 23. Next Architectural Step After v0.9.0

The next architectural step after v0.9.0 may return to the wider plugin and extensibility roadmap.

That work should begin with metadata, capability boundaries and trust model decisions, not arbitrary plugin execution.

---

## 24. Final Architectural Statement

OrbitFabric is architecturally centered on the Mission Data Contract.

The Mission Model expresses the contract.

The lint engine validates the contract.

The simulator executes deterministic scenarios against the contract.

The documentation generator explains the contract.

The v0.6 data-flow evidence layer proves the first end-to-end Mission Data Chain at contract level.

The v0.7 runtime-facing binding layer exposes that contract to implementation code without generating flight behavior.

The v0.8.0 ground-facing artifact layer exposes that contract to ground integration work without generating ground behavior.

The v0.8.1 contract introspection surface exposes a Core-owned model summary for downstream tools without introducing relationship graphs or plugins.

The v0.8.2 entity index surface exposes Core-owned entity records for downstream tools without introducing relationship graphs or plugins.

The v0.9.0 relationship manifest surface exposes Core-owned relationship records for downstream tools without introducing graph behavior, plugin execution or Studio-specific APIs.

Future plugins must consume the contract.

Nothing should bypass the contract.

That narrowness is intentional.

It is the architecture.
