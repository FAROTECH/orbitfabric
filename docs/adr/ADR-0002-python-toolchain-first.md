# ADR-0002 — Python Toolchain First

Status: Accepted  
Date: 2026-04-29  
Scope: OrbitFabric MVP v0.1  

---

## Context

OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

The project needs an initial implementation stack for:

- loading Mission Model files;
- validating model structure;
- performing semantic linting;
- generating documentation;
- executing operational scenarios;
- producing readable logs;
- producing JSON reports;
- supporting a clean command-line interface.

A future version may generate onboard runtime artifacts, likely in C++17 or another embedded-suitable language.

However, v0.1 is not a flight runtime milestone.

The goal of v0.1 is to prove the Mission Data Contract concept end-to-end.

This requires fast iteration, strong readability, low implementation friction and good support for YAML, validation, CLI tooling, tests and documentation generation.

---

## Decision

OrbitFabric v0.1 shall use Python as the primary implementation language for the toolchain.

The initial Python toolchain shall cover:

- `orbitfabric lint`;
- `orbitfabric gen docs`;
- `orbitfabric sim`;
- Mission Model loading;
- structural validation;
- semantic linting;
- scenario execution;
- report generation;
- Markdown documentation generation.

The recommended baseline is:

- Python 3.11 or newer;
- Pydantic v2 for typed model validation;
- Typer for the command-line interface;
- PyYAML or ruamel.yaml for YAML loading;
- pytest for tests;
- ruff for linting and formatting;
- MkDocs Material for project documentation;
- GitHub Actions for CI.

C++ runtime generation is explicitly deferred.

Python is the toolchain language for v0.1, not the final onboard runtime language.

---

## Rationale

Python is the correct choice for v0.1 because OrbitFabric currently needs model clarity more than embedded performance.

The highest-risk parts of the project are:

- Mission Model design;
- semantic validation;
- lint rule quality;
- scenario semantics;
- documentation generation;
- developer experience.

Python supports rapid development of these parts with minimal ceremony.

It also makes the project accessible to the initial target audience:

- university teams;
- CubeSat labs;
- embedded engineers;
- power makers;
- small technical teams;
- early open-source contributors.

Starting with C++ would prematurely optimize for a runtime that does not yet have a stable model to consume.

Starting with Rust, Go or TypeScript would be possible, but would add unnecessary strategic friction for v0.1.

---

## Consequences

### Positive Consequences

The project can iterate quickly on the Mission Model.

The lint engine can be implemented and evolved without excessive boilerplate.

The scenario runner can remain simple, readable and deterministic.

The CLI can be made usable early.

Tests can be written quickly.

Documentation generation can be implemented with straightforward templates.

Contributors can understand and modify the project without first learning an embedded runtime architecture.

### Negative Consequences

Python is not suitable as a flight-critical onboard runtime language for typical embedded spacecraft targets.

Performance and memory determinism are not representative of a future onboard runtime.

Care must be taken not to let Python-specific assumptions leak into the Mission Model.

A future generated runtime will require separate design and validation.

### Neutral Consequences

Python may remain the long-term language for OrbitFabric tooling even after C++ generation is introduced.

The project may eventually contain both:

- Python toolchain;
- generated C++ runtime skeletons.

This is acceptable because they serve different roles.

---

## Alternatives Considered

### Alternative 1 — C++ First

Start OrbitFabric directly in C++17.

Rejected for v0.1.

C++ will likely be relevant for future onboard runtime generation, but it is the wrong starting point for model exploration, linting, documentation generation and scenario prototyping.

Using C++ too early would slow down iteration and bias the model toward implementation details.

### Alternative 2 — Rust First

Start with Rust for strong typing, safety and modern tooling.

Rejected for v0.1.

Rust is technically attractive, but it raises the contribution barrier for the initial target audience and is not necessary to prove the Mission Data Contract concept.

### Alternative 3 — TypeScript First

Start with TypeScript for schema-oriented tooling and web-friendly integration.

Rejected for v0.1.

TypeScript could be useful for future web tooling, but OrbitFabric v0.1 is primarily a CLI, linting, simulation and documentation toolchain. Python is more natural for this phase.

### Alternative 4 — Go First

Start with Go for simple binaries and good CLI distribution.

Rejected for v0.1.

Go would provide good tooling and distribution, but Python provides better immediate flexibility for model iteration, validation and scientific/engineering scripting workflows.

### Alternative 5 — Mixed Python/C++ from the Start

Build the toolchain in Python and immediately generate or compile C++ runtime code.

Rejected for v0.1.

This would introduce a second axis of complexity before the Mission Model is stable.

---

## Implementation Guidance for v0.1

The Python package shall be structured as a standard `src` layout project:

```text
orbitfabric/
├── pyproject.toml
├── src/
│   └── orbitfabric/
│       ├── __init__.py
│       ├── cli.py
│       ├── model/
│       ├── lint/
│       ├── sim/
│       ├── gen/
│       └── utils/
└── tests/
```

The CLI shall expose at least:

```bash
orbitfabric lint examples/demo-3u/mission/
orbitfabric gen docs examples/demo-3u/mission/
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml
```

The Python implementation shall avoid unnecessary heavy dependencies.

The model layer must remain independent from CLI presentation details.

The lint engine must remain independent from the simulator.

The documentation generator must consume the validated Mission Model rather than re-parsing YAML independently.

The scenario runner must consume the same Mission Model objects used by the lint engine.

---

## Dependency Policy

For v0.1, dependencies must be limited and justified.

Allowed initial dependencies:

- `pydantic`;
- `typer`;
- `pyyaml` or `ruamel.yaml`;
- `pytest` for tests;
- `ruff` for development;
- `mkdocs-material` for documentation.

Avoid in v0.1:

- large simulation frameworks;
- binary protocol frameworks;
- database dependencies;
- web frameworks;
- message brokers;
- heavy async frameworks;
- hardware libraries;
- CCSDS/PUS-specific packages;
- ground-system SDKs.

The rule is strict:

> A dependency is allowed only if it directly supports the Mission Model, linting, scenario execution, documentation generation or CLI usability.

---

## Boundary with Future Runtime

The Python toolchain must not define hidden runtime semantics that cannot later be represented in generated C++ or another onboard-oriented language.

All mission behavior relevant to commands, telemetry, modes, events, faults and scenarios must remain explicit in the Mission Model.

The simulator may implement execution mechanics, but it must not become the source of mission truth.

Future C++ generation shall be treated as a downstream artifact derived from the Mission Model.

---

## Architectural Rule

Python is the implementation language for OrbitFabric v0.1 tooling.

Python is not the architectural identity of OrbitFabric.

The architectural identity remains the Mission Data Contract.

Any Python code that introduces behavior not represented in the Mission Model must be treated as suspicious and either:

- moved into the model;
- documented as simulator-only behavior;
- removed.

---

## Decision Summary

OrbitFabric v0.1 shall be implemented as a Python-first toolchain.

This choice optimizes for model design, semantic linting, scenario execution, documentation generation and fast iteration.

C++ runtime generation remains a future downstream capability and must not drive the in