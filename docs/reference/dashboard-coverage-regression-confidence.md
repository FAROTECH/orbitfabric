# Dashboard and Coverage Regression Confidence

Status: Candidate post-v1 regression-confidence policy  
Scope: selective contract-significant tests for candidate dashboard and coverage surfaces  
Applies to: post-v1 Core-owned candidate surfaces used by downstream tools

This page documents the regression-confidence posture for the post-v1 Core-owned candidate surfaces introduced after `v1.0.0 - Stable Mission Data Contract`.

It covers:

```text
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
simulation JSON expectation accounting
```

These surfaces are candidate post-v1 surfaces.

They are not promoted to the v1.0.0 stable surface by this policy.

---

## Purpose

The goal is to protect the fields that downstream renderers can safely depend on while avoiding brittle full-file golden snapshots.

Regression-confidence tests protect selected contract-significant structure:

```text
kind
report version
mission identity
boundary flags
source derivation posture
coverage derivation flags
scenario run summary shape
scenario run record shape
entity coverage shape
expectation accounting shape
relationship coverage shape
unsupported section shape
legacy failed_expectations compatibility
```

The tests intentionally avoid freezing:

```text
full generated JSON files
absolute paths beyond explicit source-path posture
complete Markdown wording
incidental ordering outside selected signatures
human-oriented CLI output
future non-breaking additive fields
```

---

## Why not golden full-file snapshots

Golden full-file snapshots are appropriate only for stable, reviewed, contract-significant surfaces.

The dashboard and coverage candidate surfaces are still post-v1 candidates.

Freezing entire files now would be too rigid because it would treat every incidental detail as stable, including implementation-adjacent formatting, derived inventories and additive report details.

The correct protection level is therefore selective regression confidence.

---

## Protected candidate surfaces

### dashboard_summary.json

Protected aspects:

```text
kind = orbitfabric.dashboard_summary
dashboard_version = 0.1-candidate
mission identity
source derivation from Core summaries and indexes
boundary flags
coverage unavailable posture
```

The dashboard summary remains an inventory and dashboard foundation surface.

It does not become a coverage report, health score, completeness score, runtime surface, ground surface or Studio-specific API.

### scenario_run_index.json

Protected aspects:

```text
kind = orbitfabric.scenario_run_index
index_version = 0.1-candidate
source_of_truth = simulation_json_reports
derived_from_simulation_json = true
derived_from_logs = false
summary shape: total, passed, failed
run record shape
non-simulation JSON exclusion posture
```

The scenario run index remains an index over simulation JSON reports.

It does not become a coverage report or structured expectation accounting surface.

### simulation JSON expectation accounting

Protected aspects:

```text
summary.expectations
summary.passed_expectations
summary.failed_expectations
expectations.total
expectations.passed
expectations.failed
expectations.records[] shape
legacy failed_expectations array compatibility
```

The structured `expectations` object is additive.

The legacy top-level `failed_expectations` array remains protected for existing consumers.

### coverage_summary.json

Protected aspects:

```text
kind = orbitfabric.coverage_summary
coverage_version = 0.1-candidate
mission identity
source derivation from Core structured outputs
boundary flags
coverage derivation flags
scenario_runs shape
entity_coverage shape
expectation_coverage shape
relationship_coverage shape
unsupported section shape
```

Coverage summary values are derived from Core-owned structured outputs only:

```text
entity_index.json
relationship_manifest.json
scenario_run_index.json
simulation JSON reports referenced by scenario_run_index.json
```

The coverage summary must not read plain-text logs, scan raw YAML, consume downstream UI state or depend on private Studio heuristics.

---

## Non-goals

This regression-confidence policy does not introduce:

```text
new CLI commands
new JSON surfaces
new Mission Model semantics
new YAML fields
additional coverage domains
mission health scoring
model completeness scoring
runtime behavior
ground behavior
relationship graph behavior
Studio-specific APIs
promotion to stable surface
release preparation
tagging
```

---

## Validation

The focused validation command is:

```bash
pytest tests/test_post_v1_candidate_core_surfaces.py
```

Full validation remains:

```bash
ruff check .
pytest
mkdocs build --strict
```

---

## Final statement

This policy adds confidence, not new product behavior.

The candidate surfaces remain candidate post-v1 surfaces until a separate reviewed decision promotes them to a stronger compatibility class.
