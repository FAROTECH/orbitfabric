# Post-v1 Candidate Integration Surfaces

Status: Active v1.1.0 reference  
Scope: candidate Core-owned integration surfaces after `v1.0.0 - Stable Mission Data Contract`  
Applies to: OrbitFabric Core `v1.1.0 - Candidate Integration Surface Consolidation` and later, until any future promotion decision

This page is the public index for candidate Core-owned integration surfaces introduced after the v1.0.0 stable Mission Data Contract release and consolidated in v1.1.0.

It exists to keep the boundary explicit:

```text
Core is the contract authority.
Downstream tools are read-only consumers.
Candidate surfaces are not automatically stable surfaces.
```

---

## 1. Current stable v1.0.0 Core-owned structured surfaces

The original v1.0.0 stable Core-owned structured surface chain remains:

```text
model_summary.json
entity_index.json
relationship_manifest.json
```

Those surfaces are derived from the validated Mission Model and protected by selected golden signatures.

The Mission Model remains the source of truth.

---

## 2. Current v1.1.0 candidate Core-owned integration surfaces

The candidate post-v1 surfaces consolidated in v1.1.0 are:

```text
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
simulation JSON structured expectation accounting
```

They are Core-owned because Core defines their fields, computes their values and declares their boundary flags.

They are candidate because they were introduced after v1.0.0 and have not yet been promoted to a stronger compatibility class.

---

## 3. Surface inventory

| Surface | Status | Purpose | Source of truth |
|---|---|---|---|
| `dashboard_summary.json` | Candidate | Dashboard-ready aggregation of existing Core facts | Mission Model and Core structured surfaces |
| `scenario_run_index.json` | Candidate | Index simulation JSON report runs | Simulation JSON reports |
| `coverage_summary.json` | Candidate | Limited coverage metrics from Core structured outputs | Entity index, relationship manifest, scenario run index and referenced simulation JSON reports |
| Simulation JSON `expectations` object | Additive candidate extension | Structured passed/failed expectation accounting | Scenario execution evidence |

---

## 4. Ownership boundary

The ownership boundary is:

```text
Core defines structured semantics.
Core computes and emits structured reports.
Studio and other downstream tools consume, navigate and render those reports.
Downstream tools do not invent private Mission Data Contract semantics.
```

Downstream tools may derive UI navigation state from these reports.

Downstream tools must not compute private substitutes for:

```text
coverage
mission health
model completeness
relationship graph behavior
dependency graph behavior
runtime behavior
ground behavior
formal verification
```

If a value is not emitted by Core, downstream tools should display one of:

```text
Unavailable
Requires Core output
Not defined by Core
```

---

## 5. Generated artifact default paths

Mission-based CLI commands resolve omitted generated artifact paths under the mission workspace.

For example:

```bash
orbitfabric export dashboard-summary examples/demo-3u/mission/
```

writes by default to:

```text
examples/demo-3u/generated/reports/dashboard_summary.json
```

and:

```bash
orbitfabric gen ground examples/demo-3u/mission/
```

writes by default to:

```text
examples/demo-3u/generated/ground/generic/
```

Explicit user-provided paths remain explicit.

For example:

```bash
orbitfabric gen docs examples/demo-3u/mission/ --output-dir custom/docs
```

continues to write to:

```text
custom/docs
```

relative to the current working directory unless the user provides an absolute path.

---

## 6. Compatibility posture

The post-v1 candidate surfaces do not change the original v1.0.0 stable Mission Data Contract.

They do not add, remove or rename Mission Model fields, model domains, controlled values, reference rules or scenario expectation syntax.

Structured expectation accounting is additive inside simulation JSON reports and preserves the legacy top-level `failed_expectations` array.

Future promotion of any candidate field or surface requires a separate reviewed decision and, where appropriate, selected regression or golden-signature protection.

---

## 7. Explicit non-goals

The post-v1 candidate integration surfaces do not introduce:

```text
Projection Profiles implementation
OSRA/SAVOIR implementation
OpenOBSW/OpenSVF-specific generation
Studio-specific APIs
mission health scoring
model completeness scoring
flight readiness scoring
runtime telemetry behavior
ground execution behavior
relationship graph behavior
dependency graph behavior
plugin discovery
plugin loading
plugin execution
CCSDS/PUS/CFDP framing
transport behavior
flight software framework behavior
ground segment behavior
```

---

## 8. v1.1.0 release implication

Core v1.1.0 consolidates these candidate surfaces.

It does not turn candidate surfaces into a broad new framework.

The release communicates:

```text
what is stable
what is candidate
what is Core-owned
what is downstream-consumer-owned
what remains explicitly out of scope
```

---

## 9. Final statement

The post-v1 candidate integration surfaces are valid Core surfaces because they keep Mission Data Contract semantics inside Core.

They are deliberately narrow:

```text
emit structured evidence
preserve provenance
declare boundaries
avoid downstream semantic invention
```
