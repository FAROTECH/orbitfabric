# ADR-0003 — YAML Multi-File Mission Model

Status: Accepted  
Date: 2026-04-29  
Scope: OrbitFabric MVP v0.1  

---

## Context

OrbitFabric is based on a Mission Data Contract.

This contract must describe telemetry, commands, events, faults, modes, packets, policies and operational scenarios in a structured and machine-readable way.

The Mission Model could be represented in different ways:

- one large YAML file;
- multiple YAML files in a mission directory;
- JSON files;
- TOML files;
- a custom DSL;
- Python code;
- a database;
- generated configuration from another modeling tool.

For OrbitFabric v0.1, the model must satisfy several requirements:

- be readable by humans;
- be writable without specialized tooling;
- be versionable in Git;
- be easy to review in pull requests;
- support clear separation of concerns;
- remain accessible to students, makers and small technical teams;
- avoid premature dependence on complex modeling tools;
- allow future schema validation and semantic linting;
- allow future generation of documentation, runtime skeletons and ground artifacts.

A single monolithic file would be easy to start with, but it would become harder to maintain as the model grows.

OrbitFabric must look small in v0.1, but it must not be structurally naive.

---

## Decision

OrbitFabric v0.1 shall use a YAML multi-file Mission Model.

A mission shall be represented as a directory containing domain-specific YAML files.

The initial canonical layout is:

```text
mission/
├── spacecraft.yaml
├── subsystems.yaml
├── modes.yaml
├── telemetry.yaml
├── commands.yaml
├── events.yaml
├── faults.yaml
├── packets.yaml
└── policies.yaml
```

Operational scenarios shall be stored separately from the mission definition:

```text
scenarios/
└── battery_low_during_payload.yaml
```

The Mission Model directory is the canonical input for:

```bash
orbitfabric lint mission/
orbitfabric gen docs mission/
```

Scenario files are the canonical input for:

```bash
orbitfabric sim scenarios/<scenario>.yaml
```

The scenario runner must resolve the referenced Mission Model explicitly or through a documented project layout convention.

---

## Rationale

YAML is readable and familiar to the target audience.

A multi-file structure makes the Mission Model easier to maintain, review and extend.

Separating telemetry, commands, events, faults, modes and packets prevents the model from becoming a large unstructured configuration file.

This also supports future ownership boundaries. For example:

- subsystem engineers may edit telemetry;
- operations engineers may edit modes and scenarios;
- ground engineers may consume packets and events;
- software engineers may consume commands and runtime interfaces.

The multi-file model also improves lint diagnostics because errors can be reported against specific domains and files.

Example:

```text
ERROR OF-CMD-003 commands.yaml: payload.start_acquisition emits unknown event payload.started
ERROR OF-FLT-001 faults.yaml: eps.battery_low_fault references unknown telemetry eps.battery.vbat
```

This is more usable than reporting errors from a single large document.

---

## Consequences

### Positive Consequences

The Mission Model remains modular from the beginning.

Each domain has a clear place:

- spacecraft identity in `spacecraft.yaml`;
- subsystem inventory in `subsystems.yaml`;
- modes and transitions in `modes.yaml`;
- telemetry definitions in `telemetry.yaml`;
- command definitions in `commands.yaml`;
- event definitions in `events.yaml`;
- fault definitions in `faults.yaml`;
- packet definitions in `packets.yaml`;
- policy vocabularies in `policies.yaml`.

Git diffs are cleaner.

Review is easier.

Generated documentation can preserve the same domain separation.

Future plugin generators can consume only the model domains they need.

### Negative Consequences

Loading the model is slightly more complex than parsing one file.

Cross-file references must be resolved explicitly.

The toolchain must detect missing files, duplicate identifiers and inconsistent references across files.

Users must learn the expected directory layout.

### Neutral Consequences

OrbitFabric may later support a single-file model for very small examples or tutorials.

OrbitFabric may later support import/include mechanisms.

OrbitFabric may later support schema exports to JSON Schema or other formats.

These are compatibility features, not v0.1 requirements.

---

## Alternatives Considered

### Alternative 1 — Single YAML File

Use one `mission.yaml` file containing everything.

Rejected as the default.

This would be simpler for the first parser, but it would scale poorly and encourage poor model organization.

A single-file format may be supported later as an optional compact format, but it must not be the canonical v0.1 structure.

### Alternative 2 — JSON Files

Use JSON instead of YAML.

Rejected for authoring.

JSON is machine-friendly but less pleasant for humans to write and review. It does not support comments in the standard format and tends to be verbose for configuration-like data.

JSON may still be used for generated exports and reports.

### Alternative 3 — TOML Files

Use TOML for the Mission Model.

Rejected for v0.1.

TOML is readable for configuration, but the nested structures required for telemetry, commands, faults and scenarios are better represented in YAML.

### Alternative 4 — Custom DSL

Create an OrbitFabric-specific modeling language.

Rejected.

A custom DSL would increase implementation effort, documentation burden and adoption friction. It is unjustified before proving the Mission Data Contract concept.

### Alternative 5 — Python-as-Configuration

Define missions directly in Python objects.

Rejected.

This would make the model executable code rather than a portable mission contract. It would also make it harder to consume from other languages and tools.

### Alternative 6 — Database-Backed Model

Store the Mission Model in a relational or document database.

Rejected.

This adds unnecessary operational complexity and makes the project less transparent, less portable and harder to version in Git.

---

## Canonical v0.1 Layout

The canonical demo mission layout shall be:

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

Each file shall contain exactly one top-level domain key.

Examples:

```yaml
# telemetry.yaml
telemetry:
  - id: eps.battery.voltage
    name: Battery Voltage
    type: float32
    unit: V
```

```yaml
# commands.yaml
commands:
  - id: payload.start_acquisition
    target: payload
    description: Start payload acquisition
```

```yaml
# faults.yaml
faults:
  - id: eps.battery_low_fault
    source: eps
    severity: warning
```

This rule keeps parsing and validation predictable.

---

## File Responsibilities

### `spacecraft.yaml`

Defines mission identity and high-level spacecraft metadata.

Responsible for:

- spacecraft ID;
- name;
- class;
- form factor;
- mission type;
- model version.

### `subsystems.yaml`

Defines the known subsystem inventory.

Responsible for:

- subsystem IDs;
- subsystem names;
- subsystem type;
- subsystem criticality.

### `modes.yaml`

Defines operational modes and allowed mode transitions.

Responsible for:

- mode names;
- mode descriptions;
- initial mode;
- transition graph.

### `telemetry.yaml`

Defines telemetry items.

Responsible for:

- telemetry IDs;
- names;
- types;
- units;
- sources;
- sampling policy;
- criticality;
- persistence policy;
- downlink priority;
- limits;
- quality requirements.

### `commands.yaml`

Defines telecommands.

Responsible for:

- command IDs;
- command targets;
- arguments;
- allowed modes;
- preconditions;
- timeout;
- acknowledgment requirement;
- risk level;
- emitted events;
- expected effects.

### `events.yaml`

Defines operational events.

Responsible for:

- event IDs;
- sources;
- severity;
- descriptions;
- persistence policy;
- downlink priority.

### `faults.yaml`

Defines fault detection and basic recovery policy.

Responsible for:

- fault IDs;
- source;
- severity;
- condition;
- emitted events;
- recovery actions.

### `packets.yaml`

Defines packet groupings.

Responsible for:

- packet IDs;
- packet names;
- packet type;
- maximum payload size;
- period;
- included telemetry.

### `policies.yaml`

Defines controlled vocabularies and reusable policy values.

Responsible for:

- allowed persistence values;
- allowed downlink priority values;
- allowed risk values;
- future mission-wide constraints.

---

## Cross-File Reference Rules

The loader and lint engine shall validate cross-file references.

Required checks include:

- telemetry source must reference an existing subsystem;
- command target must reference an existing subsystem;
- event source must reference an existing subsystem;
- fault source must reference an existing subsystem;
- fault condition telemetry must reference an existing telemetry item;
- command emitted events must reference existing events;
- fault emitted events must reference existing events;
- command allowed modes must reference existing modes;
- recovery mode transitions must reference existing modes;
- packet telemetry entries must reference existing telemetry items;
- scenario commands must reference existing commands;
- scenario expected events must reference existing events;
- scenario expected modes must reference existing modes.

These are semantic requirements, not optional warnings.

Unknown references must produce errors.

---

## Versioning

The Mission Model shall include a model version.

For v0.1, the version may be declared in `spacecraft.yaml`:

```yaml
spacecraft:
  id: demo-3u
  name: Demo 3U Spacecraft
  model_version: 0.1.0
```

Future versions may introduce a dedicated manifest file such as:

```text
mission.yaml
```

or:

```text
orbitfabric.yaml
```

However, a separate manifest is not required for v0.1.

---

## Loader Behavior

The v0.1 model loader shall:

1. accept a mission directory path;
2. detect expected YAML files;
3. parse each file;
4. validate each file has the expected top-level key;
5. build typed model objects;
6. build identifier indexes;
7. resolve cross-file references;
8. return a complete Mission Model object;
9. expose diagnostics with file/domain context.

Missing optional files may become allowed in future versions, but for the canonical `demo-3u` all v0.1 model files should be present.

---

## Architectural Rule

A mission definition must remain data, not code.

The model must be readable, reviewable and portable.

YAML files define the contract.

Python code loads, validates, simulates and generates artifacts from the contract, but Python code must not become the contract itself.

---

## Decision Summary

OrbitFabric v0.1 shall use a YAML multi-file Mission Model as its canonical mission representation.

This provides the right balance of readability, modularity, Git-friendliness, validation potential and future extensibility.

The canonical mission directory is the source of truth for linting, documentation generation, simulation and future downstream artifacts.

