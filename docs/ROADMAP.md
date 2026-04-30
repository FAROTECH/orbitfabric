# OrbitFabric — Roadmap

Version: 0.1.0.dev0  
Status: Development preview  
Scope: v0.1 to v0.5 planning   

---

## 1. Roadmap Principle

OrbitFabric must grow through coherent vertical slices, not through feature accumulation.

The project must not try to become, at the same time:

- a flight software framework;
- a ground segment;
- a spacecraft simulator;
- a packet standard implementation;
- a formal verification tool;
- a hardware abstraction layer;
- a CubeSat tutorial.

The correct growth path is:

```text
Mission Model
  -> lint
  -> scenario simulation
  -> generated documentation
  -> runtime skeletons
  -> ground integration artifacts
  -> plugins and extensibility
```

Every milestone must reinforce the core identity:

> OrbitFabric is a Mission Data Contract framework.

---

## 2. Version Strategy

OrbitFabric versions before v1.0 are allowed to evolve the model quickly.

The priority before v1.0 is:

1. clarity;
2. usefulness;
3. consistency;
4. testability;
5. extensibility;
6. compatibility.

Backward compatibility matters, but it must not prevent correction of weak early model choices.

The model should become more stable from v0.3 onward.

---

## 3. Roadmap Overview

```text
v0.1  Mission Contract MVP
v0.2  Model Hardening
v0.3  Generated Runtime Skeletons
v0.4  Ground Integration Artifacts
v0.5  Plugin and Extensibility Layer
v1.0  Stable Mission Data Contract
```

The immediate target is v0.1 only.

Everything after v0.1 is directional and must remain subordinate to what is learned from the first working vertical slice.

---

# 4. v0.1 — Mission Contract MVP

## 4.1 Objective

Demonstrate the complete OrbitFabric philosophy with one small, coherent, synthetic mission.

v0.1 must prove that a user can:

1. define a mission once;
2. lint it semantically;
3. generate documentation;
4. execute an operational scenario;
5. receive readable logs and JSON reports.

The v0.1 goal is not breadth.

The v0.1 goal is coherence.

---

## 4.2 Required Capabilities

v0.1 includes the following implemented capabilities:

```text
Mission Model YAML
Model loader
Typed validation
Structural validation
Semantic linting
Engineering lint rules
JSON lint report generation
Generated Markdown docs
Scenario model loading
Scenario reference validation
Host-side deterministic scenario execution
Simulation JSON report generation
Simulation plain-text log generation
Synthetic demo mission demo-3u
```

---

## 4.3 Required CLI Commands

v0.1 currently supports:

```bash
orbitfabric lint examples/demo-3u/mission/

orbitfabric lint examples/demo-3u/mission/ \
  --json generated/reports/lint_report.json

orbitfabric gen docs examples/demo-3u/mission/

orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml

orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml \
  --json generated/reports/battery_low_during_payload_report.json \
  --log generated/logs/battery_low_during_payload.log
```

`inspect` is not required for v0.1.

---

## 4.4 Required Repository Artifacts

```text
README.md
LICENSE
pyproject.toml
mkdocs.yml
.github/workflows/ci.yml

docs/PROJECT_CHARTER.md
docs/CLEAN_ROOM_POLICY.md
docs/ARCHITECTURE.md
docs/ROADMAP.md
docs/reference/mission-model-v0.1.md
docs/adr/ADR-0001-mission-model-first.md
docs/adr/ADR-0002-python-toolchain-first.md
docs/adr/ADR-0003-yaml-multifile-mission-model.md
docs/adr/ADR-0004-no-flight-runtime-in-v0.1.md
docs/adr/ADR-0005-lint-as-core-feature.md

examples/demo-3u/mission/*.yaml
examples/demo-3u/scenarios/battery_low_during_payload.yaml

src/orbitfabric/...
tests/...
```

---

## 4.5 Required Demo Mission

The canonical demo mission is:

```text
demo-3u
```

It must include:

```text
subsystems:
  obc
  eps
  payload
  radio

modes:
  BOOT
  NOMINAL
  PAYLOAD_ACTIVE
  DEGRADED
  SAFE
  MAINTENANCE

scenario:
  battery_low_during_payload
```

The scenario narrative:

```text
payload starts acquisition
battery voltage drops below warning threshold
fault monitor detects battery warning
warning event is emitted
mode transitions to DEGRADED
payload stop command is auto-dispatched
scenario passes
```

---

## 4.6 Required Generated Artifacts

v0.1 now generates:

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

Generated docs must be derived from the validated Mission Model.

Generated docs must not be manually edited.

---

## 4.7 v0.1 Lint Rule Minimum

The first lint implementation must include at least:

```text
OF-ID-001 duplicate IDs are not allowed within a domain
OF-ID-002 IDs must follow canonical format
OF-REF-001 telemetry source must reference an existing subsystem
OF-REF-002 command target must reference an existing subsystem
OF-REF-003 event source must reference an existing subsystem
OF-REF-004 fault source must reference an existing subsystem
OF-REF-005 fault condition telemetry must reference known telemetry
OF-REF-006 command emitted events must reference existing events
OF-REF-007 fault emitted events must reference existing events
OF-REF-008 command allowed modes must reference existing modes
OF-REF-009 recovery mode transitions must reference existing modes
OF-REF-010 packet telemetry entries must reference existing telemetry
OF-TLM-001 high-criticality telemetry must define operational limits
OF-CMD-005 command should define timeout_ms
OF-CMD-007 risky commands must not be allowed in SAFE mode unless justified
OF-EVT-002 event should define downlink priority
OF-FLT-003 fault must emit at least one event
OF-MODE-001 exactly one initial mode must be defined
OF-PKT-002 packet must not be empty
OF-SCN-005 scenario timeline must be monotonic
```

The complete rule catalog may be documented in v0.1, but the implementation can start with this minimum set.

---

## 4.8 v0.1 Tests

Minimum tests:

```text
load valid demo mission
fail on missing YAML file
fail on invalid top-level key
fail on duplicate telemetry ID
fail on unknown telemetry source
fail on command emitted unknown event
fail on fault references unknown telemetry
fail on command allowed in unknown mode
fail on packet references unknown telemetry
warn on high-criticality telemetry without limits
warn on command without timeout
run battery_low_during_payload scenario successfully
generate Markdown docs without crashing
produce lint JSON report
produce scenario JSON report
```

---

## 4.9 v0.1 Done Criteria

v0.1 is functionally close when:

```text
README explains the project clearly                       done
clean-room policy exists                                  done
architecture exists                                       done
roadmap exists                                            done
mission model reference exists                            done
ADRs 0001-0005 exist                                      done
demo-3u mission exists                                    done
lint command works                                        done
lint JSON report works                                    done
gen docs command works                                    done
sim command executes the demo scenario                    done
sim JSON report works                                     done
sim log output works                                      done
pytest passes                                             done
ruff passes                                               done
no private mission data is present                        required ongoing
```

---

## 4.10 Explicit v0.1 Non-Goals

v0.1 must not include:

```text
C++ runtime generation
flight runtime
hardware drivers
RTOS integration
Linux onboard service
CCSDS implementation
PUS implementation
CFDP implementation
Yamcs export
OpenC3 export
XTCE export
Basilisk bridge
cFS bridge
F Prime bridge
web UI
database
message broker
real spacecraft data
```

These are not delayed bugs.

They are intentionally out of scope.

---

# 5. v0.2 — Model Hardening

## 5.1 Objective

Make the Mission Model more robust after the first working vertical slice.

v0.2 should improve correctness, diagnostics, test coverage and user experience without expanding into runtime or ground integration too early.

---

## 5.2 Candidate Features

```text
mission manifest file
schema versioning improvements
better unknown-field handling
better diagnostics with file/line context if practical
scenario validation command
more complete command preconditions
more robust expected_effects model
better packet size estimation
rule documentation pages
lint severity profiles
warnings-as-errors flag
improved generated docs
more invalid mission fixtures
more scenario examples
```

---

## 5.3 Possible New CLI Commands

```bash
orbitfabric validate scenario examples/demo-3u/scenarios/battery_low_during_payload.yaml
orbitfabric inspect examples/demo-3u/mission/
orbitfabric lint examples/demo-3u/mission/ --warnings-as-errors
```

---

## 5.4 v0.2 Non-Goals

Still out of scope:

```text
flight runtime
hardware support
CCSDS/PUS/CFDP
Yamcs/OpenC3 export
Basilisk integration
```

v0.2 should harden the contract before adding external integrations.

---

# 6. v0.3 — Generated Runtime Skeletons

## 6.1 Objective

Start deriving onboard-oriented artifacts from the Mission Model.

This is not flight software.

This is generated skeleton code that demonstrates how the Mission Data Contract can support future onboard runtime integration.

---

## 6.2 Candidate Features

```text
C++17 generated headers
generated telemetry IDs
generated command IDs
generated event IDs
generated mode IDs
generated packet IDs
generated command argument structs
generated adapter interfaces
generated command dispatch skeleton
generated telemetry registry skeleton
host-buildable CMake example
```

---

## 6.3 Required Boundary

v0.3 generated code must be described as:

```text
runtime skeleton
host-buildable example
integration starting point
```

It must not be described as:

```text
flight-ready runtime
qualified software
complete OBC framework
replacement for cFS/F Prime
```

---

## 6.4 Candidate CLI Commands

```bash
orbitfabric gen cpp examples/demo-3u/mission/
```

Possible output:

```text
generated/cpp/
├── include/
│   └── orbitfabric_demo3u/
│       ├── telemetry_ids.hpp
│       ├── command_ids.hpp
│       ├── event_ids.hpp
│       ├── mode_ids.hpp
│       └── adapters.hpp
├── src/
│   └── command_dispatch.cpp
└── CMakeLists.txt
```

---

## 6.5 v0.3 Non-Goals

Still out of scope:

```text
real hardware support
RTOS-specific runtime
Linux service integration
flight qualification
complete scheduler
complete storage subsystem
complete radio stack
```

---

# 7. v0.4 — Ground Integration Artifacts

## 7.1 Objective

Generate useful artifacts for ground integration without becoming a ground segment.

OrbitFabric should help external tools consume the Mission Data Contract.

---

## 7.2 Candidate Features

```text
JSON mission database export
packet dictionary export
simple decoder skeletons
telemetry dictionary export
command dictionary export
Yamcs-like export prototype
OpenC3-like export prototype
XTCE exploration/prototype
WebSocket or UDP debug bridge prototype
```

---

## 7.3 Candidate CLI Commands

```bash
orbitfabric gen mission-db examples/demo-3u/mission/
orbitfabric gen decoder examples/demo-3u/mission/
orbitfabric gen yamcs examples/demo-3u/mission/
orbitfabric gen openc3 examples/demo-3u/mission/
```

The exact commands must be decided only after v0.1 and v0.2 clarify the internal model.

---

## 7.4 Required Boundary

OrbitFabric may export to ground tools.

OrbitFabric must not become a ground tool.

No v0.4 feature should implement:

```text
complete mission control UI
operator console
database-backed telemetry archive
real command uplink service
user management
security system
live spacecraft operations stack
```

---

# 8. v0.5 — Plugin and Extensibility Layer

## 8.1 Objective

Turn OrbitFabric from a useful tool into a framework.

v0.5 should introduce controlled extension points.

---

## 8.2 Candidate Features

```text
custom lint rule plugins
custom generator plugins
mission model extension mechanism
adapter SDK
plugin discovery
plugin metadata
example plugin
contribution guide
rule documentation generator
semantic versioning policy
```

---

## 8.3 Candidate Plugin Types

```text
lint-rule plugin
documentation generator plugin
runtime generator plugin
ground export plugin
model extension plugin
scenario step plugin
```

---

## 8.4 Required Boundary

Plugins must extend OrbitFabric without breaking the core contract.

A plugin may consume or extend the Mission Model.

A plugin must not silently redefine core semantics.

---

# 9. v1.0 — Stable Mission Data Contract

## 9.1 Objective

v1.0 should be the first version where the Mission Data Contract is considered stable enough for external users to build around.

---

## 9.2 Possible v1.0 Requirements

```text
stable Mission Model schema
stable CLI commands
stable lint rule code policy
stable generated documentation format
stable JSON report format
stable plugin API if introduced
migration guide from earlier model versions
complete demo mission
multiple example missions
published documentation site
CI-tested release artifacts
clear contribution process
```

---

## 9.3 v1.0 Should Not Require

```text
flight qualification
complete CCSDS/PUS stack
complete Yamcs/OpenC3 compatibility
complete cFS/F Prime bridge
real spacecraft deployment
```

v1.0 should mean stable Mission Data Contract framework, not complete space software ecosystem.

---

## 10. Backlog Parking Lot

These ideas are valid but must not distract from v0.1.

```text
XTCE export
CCSDS packet generator
PUS service mapping
CFDP metadata
Yamcs integration
OpenC3 integration
Basilisk bridge
Space ROS bridge
F Prime topology generator
cFS table/app generator
web dashboard
visual mission model editor
Obsidian/MkDocs publishing workflow
SARIF lint export
VS Code extension
JSON Schema publication
schema migration tool
simulation time acceleration
fault tree visualization
mode transition graph rendering
requirements traceability
coverage metrics for scenarios
packet budget analyzer
downlink window planner
power budget toy model
ADCS abstract mode examples
thermal abstract mode examples
security policy model
command authorization model
```

Parking lot items are not rejected.

They are explicitly deferred.

---

## 11. Priority Rules

When deciding what to implement next, use these rules.

### Rule 1 — Protect v0.1

If a feature does not help complete v0.1, defer it.

### Rule 2 — Model Before Generator

If the model cannot express a concept cleanly, do not generate code for it.

### Rule 3 — Lint Before Runtime

If a behavior can be inconsistent, create a lint rule before creating downstream generators.

### Rule 4 — Docs from Model

If information exists in the model, generated docs should expose it.

### Rule 5 — No Hidden Semantics

If behavior matters, it must not live only in Python code.

### Rule 6 — No Private Examples

If an example resembles a private mission, remove or generalize it.

### Rule 7 — Small Working Slice Beats Broad Incomplete Scope

A working `demo-3u` vertical slice is more valuable than ten half-implemented integrations.

---

## 12. Immediate Work Plan After This Roadmap

After the foundation documents are complete, the next work package is:

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

Then:

```text
src/orbitfabric/model/
src/orbitfabric/lint/
src/orbitfabric/sim/
src/orbitfabric/gen/
src/orbitfabric/cli.py
```

The first implementation should follow this order:

```text
1. repository skeleton
2. demo-3u YAML files
3. model loader
4. lint engine minimum rules
5. CLI lint command
6. scenario loader
7. simulator minimum runtime
8. CLI sim command
9. docs generator
10. CLI gen docs command
11. tests and CI
```

Do not implement the simulator before the demo model exists.

Do not implement generators before the loader is stable.

Do not implement C++ before v0.1 is complete.

---

## 13. Final Roadmap Statement

OrbitFabric must first become excellent at one thing:

> defining, validating, simulating and documenting a Mission Data Contract for a small spacecraft.

Only after that should it grow into runtime generation, ground integration and plugin extensibility.

The v0.1 milestone is deliberately narrow.

That narrowness is a strength, not a limitation.

