# Dashboard and Coverage Foundation

Status: Proposed post-v1 Core boundary  
Scope: dashboard and coverage enablement for downstream tools  
Applies to: OrbitFabric Core after `v1.0.0 - Stable Mission Data Contract`

This page defines the boundary for future dashboard and coverage work in OrbitFabric Core.

It is a documentation boundary only.

It does not introduce new Mission Model semantics, new YAML fields, new CLI commands, new JSON report fields, new generated surfaces, runtime behavior, ground behavior, plugin execution, graph behavior, mission control behavior or Studio-specific APIs.

---

## 1. Purpose

OrbitFabric Core already emits stable and documented machine-readable surfaces for validation, scenario evidence, contract introspection, entity indexing and relationship inspection.

Future dashboard and coverage work must build on those Core-owned surfaces instead of moving Mission Data Contract semantics into downstream tools.

The rule is:

```text
Core produces structured evidence.
Downstream tools consume and render it.
Downstream tools must not become a second source of Mission Data Contract truth.
```

This applies equally to OrbitFabric Studio, scripts, CI jobs and future integrations.

---

## 2. Current Core-owned inputs

The current Core-owned structured inputs that may support dashboard-oriented views are:

```text
lint JSON report
simulation JSON report
model_summary.json
entity_index.json
relationship_manifest.json
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
failed scenario expectations
```

These are useful dashboard facts.

They are not coverage metrics by themselves.

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

Coverage must be derived from Core-owned structured outputs, for example:

```text
entity_index.json
relationship_manifest.json
simulation JSON reports
future scenario_run_index.json
future structured expectation accounting
future coverage_summary.json
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

Until Core emits a coverage summary, downstream tools must show coverage as unavailable or requiring Core output.

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

## 6. Required Core sequence

The preferred post-v1 sequence is:

```text
1. document dashboard and coverage boundaries
2. add a Core-owned dashboard_summary.json report
3. add a Core-owned scenario_run_index.json report
4. add structured scenario expectation accounting
5. add a Core-owned coverage_summary.json report
6. protect selected mature fields with golden signatures
```

The sequence is intentionally staged.

Dashboard inventory can come before coverage.

Coverage must come after Core can index scenario runs and account for expectations structurally.

---

## 7. dashboard_summary.json boundary

A future `dashboard_summary.json` report should aggregate existing Core facts without introducing coverage semantics.

Candidate identity:

```json
{
  "kind": "orbitfabric.dashboard_summary",
  "dashboard_version": "0.1-candidate"
}
```

Candidate content may include:

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

The first dashboard summary should explicitly mark coverage as unavailable, for example:

```json
{
  "coverage": {
    "status": "not_available",
    "reason": "Coverage metrics are not emitted by OrbitFabric Core in this report version."
  }
}
```

This prevents downstream tools from inventing coverage while still allowing a real dashboard foundation.

---

## 8. scenario_run_index.json boundary

A future `scenario_run_index.json` report should aggregate simulation JSON reports produced by Core.

Candidate identity:

```json
{
  "kind": "orbitfabric.scenario_run_index",
  "index_version": "0.1-candidate"
}
```

It should read simulation JSON reports only.

It must not read plain-text logs.

Candidate content may include:

```text
scenario run records
mission id
scenario id
result
summary counts
simulation report path
aggregate passed and failed counts
```

This report would support recent-run dashboards and prepare coverage derivation.

---

## 9. Structured expectation accounting boundary

Current simulation JSON reports expose failed expectations, but they do not expose a complete structured list of evaluated expectations.

Future expectation accounting should be additive.

It should preserve existing `failed_expectations` compatibility and add a structured section for evaluated expectations.

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

A future `coverage_summary.json` report should be the first Core-owned coverage surface.

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

When first introduced, they should start as candidate or public preview Core-owned structured surfaces.

If any future change modifies a stable v1.0 surface, it must include a compatibility or migration note.

Additive report families should clearly state:

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

Dashboard and coverage are valid post-v1 directions for OrbitFabric Core.

They must remain Mission Data Contract surfaces, not UI features disguised as Core semantics.

The correct boundary is:

```text
Core defines, computes and emits.
Studio consumes, links and renders.
```
