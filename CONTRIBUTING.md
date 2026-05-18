# Contributing to OrbitFabric

Thank you for your interest in OrbitFabric.

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

The project is currently in pre-1.0 development. Contributions should stay focused, small and aligned with the Mission Data Contract architecture.

---

## Current Project Focus

The current public baseline is `v0.12.0 - v1.0 Release Candidate Hardening`.

v0.12.0 hardens the release candidate path toward `v1.0.0 - Stable Mission Data Contract` without broadening OrbitFabric into flight software, ground software, visual modeling, plugin discovery, plugin loading or plugin execution.

v0.11.0 remains the completed extensibility boundary baseline. It documented how future extension-owned outputs may relate to Core-owned Mission Data Contract semantics without introducing plugin discovery, plugin loading, plugin execution or a plugin runtime.

The current development focus is to prepare `v1.0.0 - Stable Mission Data Contract` from the v0.12.0 hardening baseline.

The active v0.12.0 hardening references are:

```text
v1.0 Candidate Surface Inventory
Golden Output and Regression Confidence Policy
v1.0 Compatibility and Migration Notes
```

These references support review and release candidate hardening.

They are part of the v0.12.0 documentation baseline.

They do not make any surface stable v1.0 by themselves.

They do not introduce new Mission Model semantics, generated Core surfaces, JSON report fields, CLI behavior, golden files, snapshot tests, schema migration tooling, JSON Schema publication, plugin discovery, plugin loading, plugin execution, runtime behavior, ground behavior or Studio-specific APIs.

The current baseline proves this Mission Data Chain:

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
  -> Contract Introspection Surface
  -> Entity Index Surface
  -> Relationship Manifest Surface
  -> Stability and Compatibility Classification
  -> Extensibility Boundary Contract
  -> v1.0 Release Candidate Hardening References
```

Do not add large integrations before the contract model, Core-owned structured surfaces, compatibility boundaries, extensibility boundary and release candidate hardening references are coherent.

Out of scope for the current preview:

- flight runtime;
- hardware drivers;
- RTOS integration;
- real onboard storage runtime;
- real downlink runtime;
- real contact scheduling;
- command uplink runtime;
- flight autonomy runtime;
- operator console;
- command dispatch runtime;
- command queues;
- onboard scheduler;
- HAL;
- CCSDS/PUS/CFDP implementation;
- Yamcs/OpenC3 full integration;
- XTCE compliance;
- binary packet decoders;
- telemetry archive runtime;
- ground database implementation;
- Basilisk integration;
- cFS/F Prime bridge;
- web UI;
- relationship graph export;
- dependency graph export;
- schema migration tooling;
- JSON Schema publication;
- stable v1.0 compatibility guarantee;
- Mission Model security domain before v1.0.0;
- security YAML fields before v1.0.0;
- security enforcement semantics;
- plugin API;
- plugin discovery;
- plugin loading;
- plugin execution;
- metadata schema;
- metadata parser;
- metadata loader;
- metadata validator;
- real spacecraft data.

Runtime-facing contract bindings must remain generated, deterministic and disposable.

Ground-facing integration artifacts must remain generated, deterministic, tool-neutral and disposable.

Contract introspection reports must remain Core-owned, deterministic, read-only and disposable.

Entity index reports must remain Core-owned, deterministic, read-only and disposable.

Relationship manifest reports must remain Core-owned, deterministic, read-only, explicitly bounded and disposable.

Compatibility classification references must remain documentation contracts, not implementation behavior, schema migration tooling, plugin execution or a v1.0 stability guarantee.

The Extensibility Boundary Contract must remain a boundary contract, not metadata schema, plugin discovery, plugin loading, plugin execution or a plugin runtime.

v0.12.0 hardening references must remain review and governance documentation, not new runtime behavior, new generated surfaces or a stable v1.0 claim.

User implementation code and downstream integration code must live outside `generated/`.

Future plugin and extensibility work must not allow plugins to silently redefine Core Mission Data Contract semantics or bypass validation.

---

## Clean-Room Requirement

OrbitFabric is developed as a clean-room open-source project.

Do not contribute:

- proprietary mission data;
- private architecture details;
- private packet formats;
- real operational logs;
- real anomaly timelines;
- non-public payload details;
- real bus maps;
- real pinouts;
- employer-owned code;
- customer-owned code;
- NDA-protected material;
- export-controlled material.

All examples must be synthetic or based on public information.

By contributing to OrbitFabric, you confirm that your contribution is your original work or is based only on material you have the legal right to contribute, and that it does not contain confidential, proprietary, export-controlled or NDA-protected information.

See:

```text
docs/CLEAN_ROOM_POLICY.md
```

---

## Development Setup

Create a virtual environment:

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

Expected current version:

```text
orbitfabric 0.12.0
```

---

## Required Local Checks

Before opening a pull request or committing significant changes, run:

```bash
ruff check .
pytest
mkdocs build --strict
```

Then verify the demo vertical slice:

```bash
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

orbitfabric gen runtime examples/demo-3u/mission/

cmake -S generated/runtime/cpp17 -B generated/runtime/cpp17/build
cmake --build generated/runtime/cpp17/build

orbitfabric gen ground examples/demo-3u/mission/

orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml \
  --json generated/reports/battery_low_during_payload_report.json \
  --log generated/logs/battery_low_during_payload.log

orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml \
  --json generated/reports/payload_data_flow_evidence_report.json \
  --log generated/logs/payload_data_flow_evidence.log
```

Expected result:

```text
ruff check .                 -> All checks passed
pytest                       -> passing
mkdocs                       -> passing
lint                         -> Result: PASSED
export model-summary         -> Result: PASSED
export entity-index          -> Result: PASSED
export relationship-manifest -> Result: PASSED
gen docs                     -> Result: PASSED
gen data-flow                -> Result: PASSED
gen runtime                  -> Result: PASSED
cmake build                  -> passing
gen ground                   -> Result: PASSED
sim                          -> Result: PASSED
```

---

## Coding Style

OrbitFabric uses:

- Python 3.11+;
- Pydantic v2;
- Typer;
- PyYAML;
- pytest;
- ruff.

Rules:

- keep modules small;
- keep the Mission Model as the source of truth;
- do not parse YAML independently in generators, simulators, exporters or downstream tools;
- consume validated model objects and Core-owned structured surfaces;
- prefer explicit diagnostics;
- write tests for new lint rules, generators, exporters and simulator behavior;
- do not introduce heavy dependencies without a clear reason.

---

## Architecture Rules

The Model Layer is the lowest stable layer.

Allowed dependency direction:

```text
cli -> model
cli -> lint
cli -> gen
cli -> sim
cli -> export

lint -> model
gen -> model
gen -> RuntimeContract builder
gen -> GroundContract builder
export -> model
RuntimeContract builder -> model
GroundContract builder -> model
sim -> model
```

Forbidden patterns:

```text
model -> cli
model -> sim
model -> gen
model -> export
lint -> sim
gen -> sim
sim -> gen
RuntimeContract builder -> raw YAML files
GroundContract builder -> raw YAML files
profile-specific generator -> raw YAML files
exporter -> raw YAML files
extension output -> Core-owned semantics
plugin output -> Core-owned relationship manifest
```

Do not hardcode behavior for `demo-3u` inside the framework core.

Relationship manifest records must remain derived from explicit loaded Mission Model fields and must reference indexed entities rather than synthetic downstream nodes.

Compatibility classification references must not become a second source of Mission Data Contract semantics.

The Extensibility Boundary Contract must not become a plugin execution surface without a separate architectural review.

v0.12.0 hardening references must not become a new source of Mission Data Contract semantics.

---

## Commit Style

Use short imperative commit messages.

Good examples:

```text
Add contact downlink consistency rules
Generate ground dictionaries
Align public documentation with relationship manifest surface
Fix scenario command validation
```

Avoid vague messages:

```text
updates
stuff
fixes
misc
```

---

## Pull Request Expectations

A good pull request should include:

- a clear description of the change;
- the affected project area or milestone;
- explicit Mission Data Contract impact;
- an architectural boundary statement for non-trivial changes;
- tests when behavior changes;
- updated documentation when user-facing behavior changes;
- confirmation that local checks pass;
- no generated artifacts unless explicitly required.

Generated outputs under `generated/` are reproducible artifacts and should normally not be committed.

Use the repository pull request template and keep the `Architectural Boundary`, `Clean-Room Confirmation` and `Validation` sections meaningful.
