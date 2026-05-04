# OrbitFabric — Clean-Room Policy

Version: 0.3-draft
Status: Draft
Scope: Entire OrbitFabric project

---

## 1. Purpose

OrbitFabric must be developed as a clean-room open-source project.

The project must be based only on:

- original work created specifically for OrbitFabric;
- public knowledge;
- public standards;
- generic engineering concepts;
- synthetic examples;
- fictional missions;
- non-proprietary abstractions.

OrbitFabric must not include, encode, derive from or reveal any confidential, proprietary, employer-owned, customer-owned, export-controlled or NDA-protected information.

This policy applies to all project artifacts, including:

- source code;
- examples;
- documentation;
- YAML Mission Models;
- scenarios;
- diagrams;
- generated outputs;
- tests;
- comments;
- issue discussions;
- commit messages;
- pull requests;
- public demos;
- presentations;
- website content.

---

## 2. Core Principle

OrbitFabric must be useful because of its architecture, not because it reproduces private mission knowledge.

The project must never depend on proprietary mission details to appear credible.

The correct approach is:

> Use fictional missions, abstract subsystem models and public engineering concepts.

The forbidden approach is:

> Repackage real private systems, private protocols, private logs or private architecture details as open-source examples.

---

## 3. Prohibited Content

The following content is strictly prohibited.

### 3.1 Non-Public Mission Information

Do not include:

- real non-public mission names;
- real mission timelines;
- real launch information not already public;
- real LEOP/IOD procedures;
- real operational constraints;
- real ground contact plans;
- real mission events;
- real anomaly histories;
- real mission-specific decision logic;
- real customer or institutional mission requirements.

### 3.2 Proprietary Architecture Details

Do not include:

- private spacecraft architectures;
- private onboard software architectures;
- private redundancy schemes;
- private boot sequences;
- private task structures;
- private subsystem interaction diagrams;
- private data flow diagrams;
- private software layering choices if recognizably derived from a non-public project;
- private internal naming conventions;
- private interface control details.

### 3.3 Hardware-Specific Private Details

Do not include:

- real bus maps from private systems;
- real pinouts from private systems;
- real connector mappings;
- real chip-select assignments;
- real SPI/I2C/UART/CAN routing from private boards;
- real GPIO mappings;
- real board bring-up notes;
- real electrical constraints from private designs;
- real payload interface details;
- real subsystem interface quirks.

### 3.4 Proprietary Protocols and Packet Formats

Do not include:

- private packet formats;
- private telemetry frame formats;
- private command frame formats;
- private binary encodings;
- private CRC variants if mission-specific;
- private message IDs;
- private opcodes;
- private routing rules;
- private ground-to-spacecraft protocols;
- private diagnostic protocols;
- private payload protocols.

### 3.5 Proprietary Source Code

Do not include:

- employer-owned code;
- customer-owned code;
- vendor code under restrictive license;
- copied code from private repositories;
- modified private code;
- private scripts;
- private test fixtures;
- private CI configurations;
- private build systems;
- private embedded drivers;
- private mission applications;
- private simulator code.

No proprietary source file may be copied, adapted, translated or structurally mirrored into OrbitFabric.

### 3.6 Private Logs and Telemetry

Do not include:

- real flight logs;
- real ground logs;
- real subsystem logs;
- real debug logs;
- real telemetry dumps;
- real command histories;
- real anomaly traces;
- real payload data;
- real operational reports;
- real failure timelines;
- real test campaign outputs;
- real qualification logs.

Synthetic logs are allowed only if clearly fictional and not numerically or structurally traceable to private systems.

### 3.7 Private Failure Cases

Do not include recognizable real failure cases.

Forbidden examples:

- reproducing a real anomaly as an OrbitFabric scenario;
- changing names but keeping the real sequence of events;
- using real threshold values from a private mission;
- using real recovery actions from private procedures;
- encoding real operational lessons as specific demo logic.

Generic failure classes are allowed.

Example allowed:

```text
Battery voltage drops below a synthetic threshold while a demo payload is active.
```

Example prohibited:

```text
A private mission's actual battery degradation behavior, thresholds, timing and recovery sequence with names changed.
```

### 3.8 Confidential Documentation

Do not include content from:

- private ICDs;
- private design reviews;
- private requirements documents;
- private mission analysis documents;
- private AIT/AIV plans;
- private qualification procedures;
- private operations manuals;
- private customer presentations;
- private proposals;
- private technical reports;
- private internal spreadsheets;
- private email threads.

This includes paraphrased content if the structure or details remain recognizably derived from private documents.

---

## 4. Allowed Content

The following content is allowed.

### 4.1 Synthetic Missions

OrbitFabric may include fictional missions created specifically for the project.

Allowed examples:

- `demo-3u`;
- `training-1u`;
- `payload-demo`;
- `synthetic-eps-demo`;
- `generic-technology-demonstrator`.

Mission names must not resemble private mission names unless those names are already public and intentionally used only as public references.

### 4.2 Generic Subsystems

OrbitFabric may model generic spacecraft subsystems:

- OBC;
- EPS;
- ADCS;
- radio;
- payload;
- thermal;
- storage;
- software service;
- mock subsystem.

Subsystem behavior must remain abstract and synthetic.

### 4.3 Public Standards

OrbitFabric may reference public standards and public documentation.

Examples:

- CCSDS concepts;
- ECSS concepts;
- XTCE concepts;
- public CubeSat educational references;
- public NASA/ESA/open-source framework documentation;
- public Yamcs/OpenC3 documentation;
- public cFS/F Prime documentation;
- public Basilisk documentation.

When standards are used, OrbitFabric must avoid copying protected text and must cite public sources where appropriate in documentation.

### 4.4 Generic Engineering Concepts

OrbitFabric may use common engineering concepts:

- telemetry;
- commands;
- events;
- faults;
- modes;
- packets;
- state machines;
- debouncing;
- thresholds;
- watchdog-like concepts;
- scenario testing;
- linting;
- generated documentation;
- simulation mocks.

These concepts must be expressed generically.

### 4.5 Original Code

OrbitFabric code must be written from scratch for the project.

Allowed:

- original Python toolchain code;
- original schema/model classes;
- original lint rules;
- original simulator code;
- original documentation generators;
- original examples;
- original tests.

The implementation must not copy private code structures, comments, names or logic.

### 4.6 Public Open-Source Dependencies

OrbitFabric may depend on open-source packages with compatible licenses.

Allowed initial examples:

- Pydantic;
- Typer;
- PyYAML or ruamel.yaml;
- pytest;
- ruff;
- MkDocs Material.

Dependencies must be reviewed for license compatibility before release.

---

## 5. Synthetic Data Rules

Synthetic examples must be obviously fictional.

### 5.1 Thresholds

Synthetic thresholds must not reuse private mission thresholds.

Allowed:

```yaml
limits:
  warning_low: 6.8
  critical_low: 6.4
```

Only if these values are explicitly fictional and not copied from a real private mission.

### 5.2 Timing

Synthetic timing must not reproduce real operational timelines.

Allowed:

```yaml
- t: 30
  inject:
    telemetry: eps.battery.voltage
    value: 6.7
```

Only as fictional demonstration timing.

### 5.3 Packet Sizes

Synthetic packet sizes must be generic.

Allowed:

```yaml
max_payload_bytes: 512
```

Only as a demo-friendly value, not as a private radio, storage or protocol constraint.

### 5.4 Names

Use generic names.

Allowed:

```text
demo-3u
eps
payload
radio
obc
battery_low_during_payload
```

Avoid names that resemble private missions, private payloads, private boards, private internal tools or private customers.

---

## 6. Example Mission Rules

The canonical demo mission `demo-3u` must obey these rules:

- it is fictional;
- it is not based on any real private spacecraft;
- it uses generic subsystem names;
- it uses synthetic telemetry;
- it uses synthetic thresholds;
- it uses synthetic events;
- it uses synthetic faults;
- it uses synthetic recovery actions;
- it uses synthetic data products;
- it uses synthetic storage and downlink intent;
- it does not include real bus maps;
- it does not include real packet formats;
- it does not include real payload behavior;
- it does not include real operational procedures;
- it does not include private customer, employer or mission references.

The purpose of `demo-3u` is to demonstrate OrbitFabric concepts, not to approximate a real mission.

---

## 7. Public Source Usage

Public sources may be used to understand the landscape and terminology.

However:

- do not copy large passages;
- do not copy diagrams;
- do not copy examples unless license permits it;
- do not rebrand public examples as OrbitFabric examples;
- do not imply compatibility unless implemented;
- do not claim compliance unless verified;
- cite public sources where documentation makes factual claims.

OrbitFabric may say:

```text
Future versions may export artifacts useful for Yamcs/OpenC3/XTCE-like integration.
```

OrbitFabric must not say:

```text
OrbitFabric is Yamcs-compatible.
```

unless that compatibility exists and is tested.

---

## 8. Naming Policy

Names must be generic, invented or clearly public.

### 8.1 Allowed Naming Style

Allowed examples:

```text
demo-3u
mock-eps
mock-payload
battery_low_during_payload
payload.start_acquisition
eps.battery.voltage
```

### 8.2 Forbidden Naming Style

Do not use:

- private mission names;
- private subsystem names;
- private payload names;
- private customer names;
- private project acronyms;
- private board names;
- private internal tool names;
- private repository names;
- private branch names;
- private operation names;
- names that are lightly disguised versions of private names.

---

## 9. Scenario Policy

Scenarios must be synthetic.

Allowed scenario classes:

- battery degradation;
- command rejected due to mode;
- payload timeout;
- telemetry out of range;
- transition to degraded mode;
- transition to safe mode;
- missing event expectation;
- packet over-size lint example;
- invalid command argument lint example.

Forbidden scenario sources:

- real anomaly timelines;
- real customer operations;
- real flight events;
- real payload campaigns;
- real debug sessions;
- real launch/LEOP events;
- real qualification failures;
- real bus faults from private hardware.

A scenario must be reviewed if it feels like:

> This is basically something that happened on a real private project with names changed.

If that is true, remove or generalize it.

---

## 10. Code Policy

All OrbitFabric code must be original.

### 10.1 Forbidden Code Sources

Do not copy or adapt code from:

- employer repositories;
- customer repositories;
- private GitHub/GitLab/Bitbucket repositories;
- internal tools;
- proprietary firmware;
- proprietary simulators;
- private scripts;
- private notebooks;
- private test harnesses;
- private CI/CD pipelines.

### 10.2 Public Code

Public open-source code may be used only through dependencies or with proper license review.

Do not paste public code directly into OrbitFabric unless:

- the license permits it;
- attribution requirements are satisfied;
- the copied code is necessary;
- the decision is documented.

Default rule:

> Prefer dependencies over copied code. Prefer original code over both.

---

## 11. Documentation Policy

Documentation must not contain private knowledge disguised as generic explanation.

Forbidden documentation patterns:

- “in a real mission we used...”;
- “our actual architecture was...”;
- “the real packet looked like...”;
- “the customer required...”;
- “during the anomaly...”;
- “the launch provider procedure...”;
- “the real payload interface...”;
- “the board pinout was...”;
- “the actual data rate was...”.

Allowed documentation pattern:

```text
In a generic small spacecraft mission, an EPS voltage telemetry item may be monitored against warning and critical thresholds.
```

Documentation must stay public, generic and synthetic.

---

## 12. Diagrams Policy

Diagrams must be original and generic.

Do not reproduce:

- private block diagrams;
- private data flow diagrams;
- private software architecture diagrams;
- private electrical diagrams;
- private interface diagrams;
- private deployment diagrams;
- private sequence diagrams.

Allowed diagrams:

- generic OrbitFabric architecture;
- generic Mission Model flow;
- generic lint pipeline;
- generic scenario execution flow;
- generic model-to-docs generation flow;
- generic future integration view.

---

## 13. Review Checklist

Before adding any file, ask:

1. Is this original work created for OrbitFabric?
2. Is this based only on public or generic knowledge?
3. Could this reveal a private mission, employer, customer or payload detail?
4. Could someone familiar with a private project recognize it?
5. Are names generic and fictional?
6. Are thresholds and timings synthetic?
7. Are packet formats invented or public?
8. Are scenarios fictional?
9. Is any source code copied from a private repository?
10. Is any documentation paraphrased from a private document?

If any answer is uncertain, do not add the content until it is generalized or removed.

---

## 14. Contributor Rules

Contributors must not submit content they do not have the right to publish.

Contributors must not submit:

- employer-owned code;
- customer-owned code;
- NDA material;
- private mission data;
- proprietary packet formats;
- private operational procedures;
- private logs;
- export-controlled technical details;
- restricted vendor material;
- copied material with incompatible license.

A future `CONTRIBUTING.md` should include this clean-room requirement explicitly.

Suggested contribution statement:

```text
By contributing to OrbitFabric, you confirm that your contribution is your original work or is based only on material you have the legal right to contribute under the project license, and that it does not contain confidential, proprietary, export-controlled or NDA-protected information.
```

---

## 15. Handling Suspect Content

If content may violate this policy:

1. stop using it;
2. do not commit it;
3. remove it from working examples;
4. replace it with a synthetic generic version;
5. document the cleanup if needed;
6. review nearby content for similar contamination.

If suspect content has already been committed, remove it immediately and consider repository history cleanup if necessary.

Do not try to “fix” prohibited content by simply renaming variables or changing numeric values.

The structure and logic may still be contaminated.

---

## 16. AI-Assisted Development Rule

AI tools may be used to help design, write or review OrbitFabric content.

However, AI-generated output must still comply with this policy.

Do not provide AI tools with confidential or proprietary source material for the purpose of generating OrbitFabric content.

Do not ask AI tools to rewrite private documents into public OrbitFabric documentation.

Do not ask AI tools to convert private code into OrbitFabric code.

Do not ask AI tools to anonymize private logs or packet formats for inclusion in OrbitFabric.

Allowed AI-assisted tasks:

- drafting generic documentation;
- writing original code from public requirements;
- reviewing architecture for clarity;
- generating synthetic examples;
- checking consistency;
- improving wording;
- creating fictional scenarios.

The responsibility for clean-room compliance remains with the project maintainers and contributors.

---

## 17. Export Control and Dual-Use Caution

Space software can be dual-use.

OrbitFabric must remain a generic open-source framework for mission data modeling, validation, simulation and documentation.

Avoid adding content that could materially increase the operational capability of a restricted system or reveal sensitive implementation details.

Current development previews must stay far from:

- real mission operations procedures;
- real secure command handling;
- real encryption/authentication schemes;
- real military-specific communication workflows;
- real tactical data links;
- real restricted payload operation;
- real launch or deployment procedures;
- real spacecraft exploitation or attack scenarios.

Generic safety, validation and engineering discipline are allowed.

Sensitive operational specifics are not.

---

## 18. License Hygiene

OrbitFabric should use a clear open-source license.

Recommended initial license:

```text
Apache-2.0
```

Before adding third-party material, verify:

- license compatibility;
- attribution requirements;
- redistribution rights;
- modification rights;
- documentation requirements.

Do not add assets, diagrams, templates or code snippets with unclear licensing.

---

## 19. Clean-Room Examples

### 19.1 Allowed Example

```yaml
telemetry:
  - id: eps.battery.voltage
    name: Battery Voltage
    type: float32
    unit: V
    source: eps
    sampling: 1Hz
    criticality: high
    persistence: store_and_downlink
    downlink_priority: high
    limits:
      warning_low: 6.8
      critical_low: 6.4
```

Reason: generic, synthetic, not tied to a private system.

### 19.2 Prohibited Example

```yaml
telemetry:
  - id: private_payload.actual_sensor.raw_count
    source: private_payload
    packet_offset: 37
    conversion: copied_from_private_icd
```

Reason: private payload and private ICD-derived structure.

### 19.3 Allowed Scenario

```yaml
scenario:
  id: battery_low_during_payload

steps:
  - t: 30
    inject:
      telemetry: eps.battery.voltage
      value: 6.7
```

Reason: fictional and generic.

### 19.4 Prohibited Scenario

```yaml
scenario:
  id: renamed_real_anomaly
```

Reason: a real private anomaly cannot be reused with a different name.

---

## 20. Final Rule

When in doubt, do not include it.

Generalize, simplify or remove.

OrbitFabric must earn credibility through clean architecture, clear modeling and useful tooling, not through hidden private knowledge.

The project must remain safe to publish, safe to discuss and safe for external contributors to adopt.

