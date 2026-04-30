# OrbitFabric — Architecture

Version: 0.1-draft  
Status: Draft  
Scope: MVP v0.1 architecture  

---

## 1. Architectural Intent

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

The architecture is centered on one primary artifact:

> the Mission Model.

The Mission Model defines telemetry, commands, events, faults, modes, packets, policies and scenarios once, in a structured Mission Data Contract.

All other OrbitFabric capabilities consume, validate, execute or derive artifacts from that model.

OrbitFabric is not designed as a flight software framework, a ground segment or a spacecraft dynamics simulator.

Its architectural role is:

> define and enforce the contract between mission data, onboard behavior, simulation, tests, documentation and ground integration.

---

## 2. Architectural Principles

### 2.1 Mission Model First

The Mission Model is the source of truth.

Runtime behavior, simulation behavior, generated documentation and future integration artifacts must derive from the model.

No important mission behavior should live only in Python code, documentation or simulator internals.

### 2.2 Contract Before Runtime

OrbitFabric v0.1 does not implement a flight runtime.

It implements a host-side toolchain that proves the Mission Data Contract concept.

The future runtime path must be generated from the model, not hand-designed independently from it.

### 2.3 Lint as Engineering Judgment

`orbitfabric lint` is a core architectural component.

It must detect mission consistency issues, not merely invalid YAML.

### 2.4 Scenario-First Operational Testing

Scenarios are structured artifacts.

They describe operational sequences and expected outcomes.

The simulator executes scenarios to validate model behavior.

### 2.5 Ground by Construction

OrbitFabric should produce artifacts useful for ground integration.

It must not become a ground segment.

### 2.6 Clean Core, Extensible Edges

The core must remain small.

Future integrations should be plugins, generators or adapters, not hardcoded assumptions in the core.

### 2.7 Clean-Room Development

All examples, scenarios and code must be original, synthetic or based on public knowledge.

No proprietary mission information belongs in the architecture.

---

## 3. High-Level System View

```text
OrbitFabric
├── Mission Model
│   ├── spacecraft
│   ├── subsystems
│   ├── modes
│   ├── telemetry
│   ├── commands
│   ├── events
│   ├── faults
│   ├── packets
│   ├── policies
│   └── scenarios
│
├── Toolchain
│   ├── orbitfabric lint
│   ├── orbitfabric gen docs
│   └── orbitfabric sim
│
├── Model Layer
│   ├── YAML loader
│   ├── typed model objects
│   ├── indexes
│   ├── reference resolver
│   └── diagnostics
│
├── Lint Layer
│   ├── structural validation
│   ├── semantic rules
│   ├── findings
│   ├── rule registry
│   └── JSON reports
│
├── Simulation Layer
│   ├── scenario runner
│   ├── simulation clock
│   ├── telemetry registry
│   ├── command router
│   ├── event bus
│   ├── mode manager
│   ├── fault monitor
│   └── mock subsystems
│
├── Generation Layer
│   ├── Markdown documentation
│   ├── model summaries
│   ├── lint reports
│   └── scenario reports
│
└── Future Extension Layer
    ├── C++ runtime skeletons
    ├── Yamcs export
    ├── OpenC3 export
    ├── XTCE export
    ├── plugin lint rules
    └── custom generators
```

---

## 4. MVP v0.1 Boundary

OrbitFabric v0.1 includes:

```text
Mission Model YAML
Model loader
Typed validation
Semantic lint
Scenario runner
Host-side simulation
Generated Markdown docs
Readable logs
JSON reports
Synthetic demo mission
```

OrbitFabric v0.1 excludes:

```text
Flight runtime
Embedded deployment
C++ runtime generation
RTOS integration
Linux onboard service
Hardware drivers
CCSDS/PUS/CFDP implementation
Yamcs/OpenC3 integration
Basilisk bridge
cFS/F Prime bridge
Formal verification
Security model
```

The v0.1 boundary is strict.

Anything requiring real hardware, real-time execution, spacecraft protocol compliance or external framework compatibility is out of scope.

---

## 5. Main Data Flow

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
      └──────────────► Scenario Runner ─────────► Simulation Log + Scenario Report
```

The model is loaded once and consumed by multiple downstream layers.

No generator or simulator should independently reinterpret raw YAML.

---

## 6. Command-Line Architecture

The v0.1 CLI exposes three primary commands:

```bash
orbitfabric lint examples/demo-3u/mission/
orbitfabric gen docs examples/demo-3u/mission/
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml
```

Conceptual CLI structure:

```text
orbitfabric
├── lint <mission-dir>
├── gen
│   └── docs <mission-dir>
└── sim <scenario-file>
```

Future commands may include:

```text
orbitfabric init
orbitfabric gen cpp
orbitfabric gen yamcs
orbitfabric gen openc3
orbitfabric validate scenario
orbitfabric inspect mission
```

These are not v0.1 requirements.

---

## 7. Model Layer

### 7.1 Responsibility

The Model Layer loads and represents the Mission Model.

It is responsible for:

- reading YAML files;
- validating top-level domain keys;
- building typed model objects;
- indexing objects by ID;
- detecting duplicates;
- resolving references;
- exposing diagnostics;
- providing a stable object model to lint, simulation and generation layers.

### 7.2 Non-Responsibility

The Model Layer must not:

- execute scenarios;
- generate documentation;
- decide operational behavior;
- implement lint rule policy beyond structural validation;
- contain mission-specific behavior;
- contain demo-specific shortcuts.

### 7.3 Conceptual Modules

```text
src/orbitfabric/model/
├── loader.py
├── mission.py
├── spacecraft.py
├── subsystems.py
├── modes.py
├── telemetry.py
├── commands.py
├── events.py
├── faults.py
├── packets.py
├── policies.py
├── scenarios.py
└── references.py
```

### 7.4 Internal Object Shape

The validated Mission Model should conceptually expose:

```text
MissionModel
├── spacecraft
├── subsystems_by_id
├── modes_by_id
├── mode_transitions
├── telemetry_by_id
├── commands_by_id
├── events_by_id
├── faults_by_id
├── packets_by_id
└── policies
```

All downstream layers consume this object.

---

## 8. Lint Layer

### 8.1 Responsibility

The Lint Layer performs mission consistency analysis.

It is responsible for:

- rule execution;
- semantic validation;
- finding generation;
- severity assignment;
- diagnostic formatting;
- JSON lint report generation;
- CI-friendly pass/fail decision.

### 8.2 Rule Families

Initial rule families:

```text
OF-SYN-*   syntax and file parsing
OF-STR-*   structural validation
OF-ID-*    identifier and uniqueness rules
OF-REF-*   cross-reference rules
OF-TLM-*   telemetry rules
OF-CMD-*   command rules
OF-EVT-*   event rules
OF-FLT-*   fault rules
OF-MODE-*  mode and transition rules
OF-PKT-*   packet rules
OF-SCN-*   scenario rules
OF-POL-*   policy rules
```

### 8.3 Conceptual Modules

```text
src/orbitfabric/lint/
├── engine.py
├── finding.py
├── rule.py
├── registry.py
├── rules_identifiers.py
├── rules_references.py
├── rules_telemetry.py
├── rules_commands.py
├── rules_events.py
├── rules_faults.py
├── rules_modes.py
├── rules_packets.py
└── rules_scenarios.py
```

### 8.4 Finding Shape

A lint finding should contain:

```text
severity
code
message
file
domain
object_id
suggestion
```

Example:

```text
ERROR OF-REF-005 faults.yaml eps.battery_low_fault references unknown telemetry eps.battery.vbat
```

### 8.5 Pass/Fail Policy

Default v0.1 behavior:

```text
ERROR   -> lint fails
WARNING -> lint passes with warnings
INFO    -> lint passes
```

Downstream generation and simulation should stop by default when lint errors exist.

---

## 9. Simulation Layer

### 9.1 Responsibility

The Simulation Layer executes operational scenarios against a validated Mission Model.

It is responsible for:

- initializing simulation state;
- executing timeline steps;
- dispatching commands;
- injecting telemetry;
- evaluating faults;
- emitting events;
- applying simple recovery actions;
- checking expectations;
- producing logs;
- producing scenario reports.

### 9.2 Non-Responsibility

The Simulation Layer does not model:

- orbital dynamics;
- attitude dynamics;
- power system physics;
- thermal behavior;
- RF link budget;
- real-time scheduling;
- hardware communication;
- embedded resource constraints;
- flight qualification semantics.

It is an operational consistency simulator, not a spacecraft physics simulator.

### 9.3 Conceptual Modules

```text
src/orbitfabric/sim/
├── runner.py
├── clock.py
├── state.py
├── telemetry_registry.py
├── command_router.py
├── event_bus.py
├── mode_manager.py
├── fault_monitor.py
├── report.py
└── mocks/
    ├── eps.py
    ├── payload.py
    └── radio.py
```

### 9.4 Simulation Runtime Components

#### ScenarioRunner

Coordinates scenario execution.

Consumes:

- Mission Model;
- Scenario Model;
- simulation components.

Produces:

- scenario log;
- scenario report;
- pass/fail result.

#### SimulationClock

Provides deterministic scenario time.

v0.1 uses discrete timeline steps, not wall-clock execution.

#### TelemetryRegistry

Stores current telemetry values and quality states.

Supports telemetry injection from scenario steps.

#### CommandRouter

Evaluates command dispatch requests.

Checks:

- command exists;
- command is allowed in current mode;
- arguments are within declared constraints;
- command risk is compatible with mode policy where applicable.

#### EventBus

Records emitted events.

Supports scenario expectations such as:

```yaml
expect_event: eps.battery_low
```

#### ModeManager

Tracks current operational mode.

Applies mode transitions triggered by commands or faults.

#### FaultMonitor

Evaluates fault conditions against telemetry and event history.

Applies simple recovery actions:

- emit events;
- transition mode;
- auto-dispatch commands.

#### Mock Subsystems

Mock subsystems implement synthetic behavior for `demo-3u`.

They must stay generic and clean-room.

---

## 10. Scenario Execution Flow

Canonical flow:

```text
load mission
run lint
load scenario
validate scenario references
initialize simulation state
sort timeline steps
for each step:
    advance simulation time
    execute command/injection/expectation
    evaluate faults
    emit events
    apply recovery
    check expectations
write log
write report
return pass/fail
```

Example timeline:

```text
[00:00] MODE=NOMINAL
[00:05] COMMAND payload.start_acquisition -> ACCEPTED
[00:06] EVENT payload.acquisition_started
[00:30] INJECT eps.battery.voltage=6.7
[00:33] EVENT eps.battery_low severity=WARNING
[00:35] MODE TRANSITION PAYLOAD_ACTIVE -> DEGRADED
[00:36] COMMAND payload.stop_acquisition -> AUTO_DISPATCHED
[00:37] EVENT payload.acquisition_stopped
[00:40] SCENARIO PASSED
```

---

## 11. Generation Layer

### 11.1 Responsibility

The Generation Layer derives human-readable and machine-readable artifacts from the Mission Model.

v0.1 focuses on Markdown documentation and JSON reports.

### 11.2 v0.1 Generated Artifacts

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

### 11.3 Conceptual Modules

```text
src/orbitfabric/gen/
├── docs.py
├── markdown.py
├── json_reports.py
└── templates/
```

### 11.4 Generator Rule

Generators must consume the validated Mission Model.

They must not parse YAML independently.

This prevents divergence between lint, simulation and documentation.

---

## 12. Demo Mission Architecture

The canonical v0.1 demo is `demo-3u`.

Purpose:

> demonstrate the full Mission Data Contract flow with the smallest coherent synthetic spacecraft mission.

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
│   └── policies.yaml
└── scenarios/
    └── battery_low_during_payload.yaml
```

The demo contains:

```text
OBC
EPS mock
Payload mock
Radio mock
BOOT
NOMINAL
PAYLOAD_ACTIVE
DEGRADED
SAFE
MAINTENANCE
battery voltage telemetry
payload acquisition telemetry
payload start/stop commands
EPS status command
battery warning fault
battery critical fault
battery degradation scenario
```

The demo must stay synthetic.

It must not approximate a private mission.

---

## 13. Repository Architecture

Recommended repository layout:

```text
orbitfabric/
├── README.md
├── LICENSE
├── pyproject.toml
├── mkdocs.yml
├── .gitignore
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── docs.yml
│
├── docs/
│   ├── PROJECT_CHARTER.md
│   ├── CLEAN_ROOM_POLICY.md
│   ├── ARCHITECTURE.md
│   ├── ROADMAP.md
│   ├── reference/
│   │   └── mission-model-v0.1.md
│   └── adr/
│       ├── ADR-0001-mission-model-first.md
│       ├── ADR-0002-python-toolchain-first.md
│       ├── ADR-0003-yaml-multifile-mission-model.md
│       ├── ADR-0004-no-flight-runtime-in-v0.1.md
│       └── ADR-0005-lint-as-core-feature.md
│
├── examples/
│   └── demo-3u/
│       ├── mission/
│       └── scenarios/
│
├── src/
│   └── orbitfabric/
│       ├── __init__.py
│       ├── cli.py
│       ├── model/
│       ├── lint/
│       ├── sim/
│       ├── gen/
│       └── utils/
│
├── tests/
│   ├── test_model_loader.py
│   ├── test_lint_rules.py
│   ├── test_scenario_runner.py
│   └── fixtures/
│
└── generated/
    └── .gitkeep
```

---

## 14. Dependency Architecture

v0.1 should use a small dependency set.

Recommended:

```text
Python 3.11+
Pydantic v2
Typer
PyYAML or ruamel.yaml
pytest
ruff
MkDocs Material
```

Dependency rule:

> A dependency is allowed only if it directly supports model loading, validation, linting, simulation, documentation generation, testing or CLI usability.

Avoid:

```text
web frameworks
databases
message brokers
heavy simulation frameworks
hardware libraries
CCSDS/PUS libraries
ground system SDKs
async frameworks unless necessary
```

---

## 15. Layer Dependency Rules

Allowed dependencies:

```text
cli -> model
cli -> lint
cli -> sim
cli -> gen

lint -> model
sim -> model
sim -> lint diagnostics only where needed
gen -> model
gen -> lint report data where needed
```

Forbidden dependencies:

```text
model -> cli
model -> sim
model -> gen
model -> lint policy
lint -> sim
sim -> gen
gen -> sim
```

The Model Layer must remain the lowest stable layer.

---

## 16. Error and Diagnostics Architecture

OrbitFabric diagnostics should be consistent across loader, lint and simulation.

Diagnostic fields:

```text
severity
code
message
file
domain
object_id
suggestion
```

Severity:

```text
ERROR
WARNING
INFO
```

All user-facing diagnostics must be actionable.

Bad:

```text
Invalid command.
```

Good:

```text
ERROR OF-CMD-007 commands.yaml payload.start_acquisition is allowed in SAFE mode but risk is medium. Remove SAFE from allowed_modes or add explicit justification.
```

---

## 17. Reports Architecture

v0.1 reports should be JSON.

### 17.1 Lint Report

```json
{
  "tool": "orbitfabric-lint",
  "version": "0.1.0",
  "mission": "demo-3u",
  "model_version": "0.1.0",
  "result": "passed_with_warnings",
  "summary": {
    "errors": 0,
    "warnings": 1,
    "info": 0
  },
  "findings": []
}
```

### 17.2 Scenario Report

```json
{
  "tool": "orbitfabric-sim",
  "version": "0.1.0",
  "scenario": "battery_low_during_payload",
  "mission": "demo-3u",
  "result": "passed",
  "events": [],
  "commands": [],
  "mode_transitions": [],
  "failed_expectations": []
}
```

Reports must be stable enough for tests and CI.

---

## 18. Testing Architecture

v0.1 test strategy:

```text
model loader tests
schema validation tests
identifier tests
cross-reference lint tests
telemetry lint tests
command lint tests
fault lint tests
packet lint tests
scenario validation tests
scenario execution tests
documentation generator smoke tests
CLI smoke tests
```

Test fixture structure:

```text
tests/fixtures/
├── valid_mission/
├── invalid_missing_reference/
├── invalid_duplicate_ids/
├── invalid_safe_mode_command/
└── scenarios/
```

The first CI should run:

```bash
pytest
ruff check
orbitfabric lint examples/demo-3u/mission/
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml
```

---

## 19. Documentation Architecture

OrbitFabric documentation has two classes.

### 19.1 Hand-Written Project Documentation

Examples:

```text
docs/PROJECT_CHARTER.md
docs/CLEAN_ROOM_POLICY.md
docs/ARCHITECTURE.md
docs/ROADMAP.md
docs/reference/mission-model-v0.1.md
docs/adr/*.md
```

These explain the framework.

### 19.2 Generated Mission Documentation

Examples:

```text
generated/docs/telemetry.md
generated/docs/commands.md
generated/docs/events.md
generated/docs/faults.md
generated/docs/modes.md
generated/docs/packets.md
```

These document a specific mission model.

Generated docs must not be manually edited.

---

## 20. Future Extension Architecture

Future extensions should be added as generators, plugins or adapters.

Possible future layers:

```text
C++ Generator
Yamcs Export Generator
OpenC3 Export Generator
XTCE Export Generator
Custom Lint Rule Plugins
Custom Mission Model Extensions
Runtime Adapter SDK
Basilisk Bridge
cFS/F Prime Integration Bridges
```

These must remain downstream of the Mission Model.

They must not redefine the mission contract.

---

## 21. Anti-Patterns

The following patterns are architecturally wrong.

### 21.1 Runtime-First Drift

Adding runtime behavior that is not represented in the Mission Model.

### 21.2 Demo-Driven Special Cases

Hardcoding behavior for `demo-3u` in the framework core.

### 21.3 Hidden Mission Logic

Putting command rules, mode rules or fault recovery only in Python.

### 21.4 Premature Standard Compliance

Adding CCSDS/PUS/XTCE/Yamcs/OpenC3 complexity before the model is stable.

### 21.5 Ground Segment Creep

Turning OrbitFabric into a mission control tool.

### 21.6 Flight Framework Creep

Turning OrbitFabric into an incomplete cFS/F Prime alternative.

### 21.7 Simulation Creep

Turning OrbitFabric into a spacecraft dynamics simulator.

### 21.8 Proprietary Example Contamination

Using real private mission details as examples.

---

## 22. v0.1 Acceptance Architecture

OrbitFabric v0.1 is architecturally acceptable when this flow works end-to-end:

```bash
orbitfabric lint examples/demo-3u/mission/ \
  --json generated/reports/lint_report.json

orbitfabric gen docs examples/demo-3u/mission/

orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml \
  --json generated/reports/battery_low_during_payload_report.json \
  --log generated/logs/battery_low_during_payload.log
```

And produces:

```text
valid lint output
Markdown mission documentation
scenario execution log
scenario JSON report
```

The result must demonstrate:

```text
model loading
semantic linting
command validation
event emission
fault detection
mode transition
auto-dispatched recovery command
scenario pass/fail result
generated documentation
```

No more is required for v0.1.

---

## 23. Final Architectural Statement

OrbitFabric is architecturally centered on the Mission Model.

The Mission Model is the contract.

The lint engine validates the contract.

The simulator executes scenarios against the contract.

The documentation generator explains the contract.

Future runtime and ground integrations consume the contract.

Nothing should bypass the contract.

