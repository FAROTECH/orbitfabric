# Dashboard and Coverage Foundation

Status: Implemented post-v1 candidate Core boundary consolidated in v1.1.0  
Scope: dashboard and coverage enablement through candidate Core-owned structured surfaces  
Applies to: OrbitFabric Core `v1.1.0 - Candidate Integration Surface Consolidation` and later, until any future promotion decision

This page defines the implemented boundary for dashboard and coverage work in OrbitFabric Core after v1.0.0.

It began as a proposed boundary and now describes the candidate Core-owned surfaces that implement that boundary.

It does not promote those surfaces to the original v1.0.0 stable surface and does not introduce new Mission Model semantics, new YAML fields, runtime behavior, ground behavior, plugin execution, graph behavior, mission control behavior or Studio-specific APIs.

---

## 1. Purpose

OrbitFabric Core emits stable and documented machine-readable surfaces for validation, scenario evidence, contract introspection, entity indexing and relationship inspection.

The v1.1.0 dashboard and coverage surfaces build on those Core-owned surfaces instead of moving Mission Data Contract semantics into downstream tools.

The rule is:

```text
Core produces structured evidence.
Downstream tools consume and render it.
Downstream tools must not become a second source of Mission Data Contract truth.
```

This applies equally to OrbitFabric Studio, scripts, CI jobs and future integrations.

---

## 2. Current Core-owned inputs

The current Core-owned structured inputs that support dashboard-oriented and coverage-oriented views are:

```text
lint JSON report
simulation JSON report
model_summary.json
entity_index.json
relationship_manifest.json
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
structured expectation accounting
```

These surfaces can support inventory and status views such as:

```text
mission identity
Mission Model version
lint result
finding counts
domain presence
contract domain counts
entity inventory
relationship inventory
scenario execution result
scenario execution summary
data-flow evidence records
structured expectation counts
limited coverage values emitted by Core
```

These are useful dashboard facts.

They are coverage metrics only when emitted by `coverage_summary.json`.

---

## 3. What dashboard means

A dashboard view is a read-only aggregation of Core-owned structured facts.

A valid dashboard view may show:

```text
validation status
loaded domain counts
required and optional domain presence
entity counts by domain
relationship counts by type
recent scenario execution summaries
scenario evidence counts
failed expectation counts
```

A dashboard view must preserve the provenance of those facts.

It must not rename inventory, validation status or scenario evidence into coverage unless Core has explicitly emitted a coverage report.

---

## 4. What coverage means

Coverage is a Core-defined measurement of which declared Mission Data Contract entities or relationships have been exercised by scenario evidence.

Coverage is derived from Core-owned structured outputs, for example:

```text
entity_index.json
relationship_manifest.json
simulation JSON reports
scenario_run_index.json
structured expectation accounting
coverage_summary.json
```

Coverage must not be derived from:

```text
plain-text logs
human-oriented CLI output
generated Markdown documentation
generated C++ headers
generated ground dictionaries
UI state
raw YAML parsing in downstream tools
naming heuristics in downstream tools
```

When Core does not emit a specific coverage value, downstream tools must show that value as unavailable or requiring Core output.

---

## 5. Explicit non-goals

Dashboard and coverage foundation work does not introduce:

```text
mission health score
flight readiness score
operational readiness score
runtime telemetry behavior
live telemetry
command uplink
mission control behavior
ground runtime behavior
relationship graph engine
dependency graph engine
visual modeling backend
Studio-specific API
plugin discovery
plugin loading
plugin execution
security enforcement semantics
```

A future validation-oriented health indicator may be considered only if Core defines an explicit formula and emits it as a structured report.

No downstream tool should invent such a score.

---

## 6. Implemented Core sequence

The post-v1 sequence is now:

```text
1. documented dashboard and coverage boundaries
2. added a Core-owned dashboard_summary.json report
3. added a Core-owned scenario_run_index.json report
4. added structured scenario expectation accounting
5. added a Core-owned coverage_summary.json report
6. added selected regression confidence for candidate contract-significant fields
```

The sequence is intentionally staged.

Dashboard inventory can exist without being a coverage report.

Coverage is emitted only by the dedicated `coverage_summary.json` candidate surface.

---

## 7. dashboard_summary.json boundary

`dashboard_summary.json` aggregates existing Core facts without introducing coverage semantics.

Candidate identity:

```json
{
  "kind": "orbitfabric.dashboard_summary",
  "dashboard_version": "0.1-candidate"
}
```

Candidate content includes:

```text
mission identity
source mission directory
boundary flags
validation summary
model domain inventory
entity inventory summary
relationship inventory summary
coverage availability status
```

The dashboard summary explicitly marks coverage as unavailable and points to `coverage_summary.json` when coverage is required.

This prevents downstream tools from inventing coverage while still allowing a real dashboard foundation.

---

## 8. scenario_run_index.json boundary

`scenario_run_index.json` aggregates simulation JSON reports produced by Core.

Candidate identity:

```json
{
  "kind": "orbitfabric.scenario_run_index",
  "index_version": "0.1-candidate"
}
```

It reads simulation JSON reports only.

It does not read plain-text logs.

Candidate content includes:

```text
scenario run records
mission id
scenario id
result
summary counts
simulation report path
aggregate passed and failed counts
```

This report supports recent-run dashboards and provides an input to `coverage_summary.json`.

---

## 9. Structured expectation accounting boundary

Current simulation JSON reports expose additive structured expectation accounting while preserving the legacy `failed_expectations` compatibility list.

Expectation accounting is additive.

It preserves existing `failed_expectations` compatibility and adds a structured section for evaluated expectations.

Candidate content may include:

```text
time
expectation type
target identifier
expected value
actual value
result
message
```

This is required before Core can provide defensible expectation coverage.

---

## 10. coverage_summary.json boundary

`coverage_summary.json` is the first Core-owned coverage surface.

Candidate identity:

```json
{
  "kind": "orbitfabric.coverage_summary",
  "coverage_version": "0.1-candidate"
}
```

Coverage may include only measurements that Core can define, compute and test from structured inputs.

Candidate areas may include:

```text
scenario run coverage
command exercise coverage
event evidence coverage
mode transition evidence coverage
data-flow evidence coverage
relationship evidence coverage for explicitly supported relationship families
```

Coverage percentages are allowed only when Core emits both the numerator, denominator and interpretation.

Downstream tools must render the Core result, not recompute private percentages.

---

## 11. Compatibility posture

Dashboard and coverage reports are not part of the v1.0.0 stable surface.

They are candidate Core-owned structured surfaces consolidated in v1.1.0.

If any future change modifies a stable v1.0 surface, it must include a compatibility or migration note.

Candidate report families clearly state:

```text
kind
report version
source inputs
boundary flags
unsupported claims
compatibility status
```

---

## 12. Downstream tool rule

OrbitFabric Studio and other downstream tools may render dashboard and coverage data only when Core emits the relevant structured report.

If a value is not emitted by Core, downstream tools must display one of:

```text
Unavailable
Requires Core output
Not defined by Core
```

They must not infer hidden semantics from raw files, logs, terminal output or UI state.

---

## 13. Final statement

Dashboard and coverage are valid post-v1 directions for OrbitFabric Core because v1.1.0 keeps them as narrow Core-owned candidate Mission Data Contract surfaces.

They must remain Mission Data Contract surfaces, not UI features disguised as Core semantics.

The correct boundary is:

```text
Core defines, computes and emits.
Studio consumes, links and renders.
```
