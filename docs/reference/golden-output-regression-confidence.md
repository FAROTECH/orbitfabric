# Golden Output and Regression Confidence Policy

Status: Active v1.0 policy  
Scope: regression confidence and selected golden-signature protection  
Applies to: generated outputs, JSON reports, Core-owned structured surfaces and CI artifacts after `v1.0.0 - Stable Mission Data Contract`

This page defines how OrbitFabric reasons about golden outputs and regression confidence after the v1.0.0 stable Mission Data Contract release.

It is a policy document only.

It does not introduce new generated surfaces, new JSON report fields, new CLI behavior, new Mission Model semantics, schema migration tooling, JSON Schema publication, runtime behavior, ground behavior, plugin discovery, plugin loading, plugin execution, metadata schema, metadata parser, metadata loader, metadata validator or Studio-specific APIs.

---

## 1. Purpose

OrbitFabric v1.0.0 includes selected golden signatures for Core-owned structured surfaces.

The purpose of this policy is to separate:

```text
CI-generated evidence
committed golden signatures
future golden-output candidates
human-reviewable generated artifacts
disposable generated artifacts
internal test assets
```

This distinction matters because not every reproducible output should become a committed golden baseline.

A golden output is useful only when it protects a public or stable contract surface from accidental drift.

A golden output is harmful when it freezes incidental formatting, demo wording, implementation order or disposable artifact details too early.

---

## 2. Current CI confidence baseline

The current CI pipeline provides regression confidence by running the main project checks and regenerating representative outputs.

The current CI baseline includes:

```text
ruff check .
pytest
orbitfabric lint examples/demo-3u/mission/ --json generated/reports/lint_report.json
orbitfabric gen docs examples/demo-3u/mission/
orbitfabric gen data-flow examples/demo-3u/mission/ --output-file generated/docs/data_flow.md
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml --json generated/reports/battery_low_during_payload_report.json --log generated/logs/battery_low_during_payload.log
orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml --json generated/reports/payload_data_flow_evidence_report.json --log generated/logs/payload_data_flow_evidence.log
mkdocs build --strict
```

The CI also uploads generated reports, logs and generated mission documentation as workflow artifacts.

This gives build-time confidence.

It does not automatically make every uploaded artifact a committed golden-output baseline.

---

## 3. Terminology

### 3.1 Generated evidence

Generated evidence is output produced during CI or local checks to demonstrate that the toolchain still works.

Examples include:

```text
generated/reports/lint_report.json
generated/reports/*_report.json
generated/logs/*.log
generated/docs/
```

Generated evidence may be uploaded as CI artifacts.

It is not automatically a golden baseline.

### 3.2 Golden output

A golden output is a deliberately selected expected output committed to the repository or otherwise preserved as a stable reference for regression comparison.

A golden output must have an explicit purpose.

It must protect a specific public or stable contract behavior.

### 3.3 Golden signature

A golden signature is a reduced, contract-significant subset of a larger generated output.

It protects selected meaning without freezing incidental formatting or full-file structure.

v1.0.0 uses this strategy for selected Core-owned structured surfaces.

### 3.4 Snapshot test

A snapshot test compares current output against a stored expected output.

Snapshot tests are useful only when the stored output represents a meaningful public or stable contract surface.

Snapshot tests should not freeze incidental ordering, whitespace or human-oriented wording unless those details are intentionally part of the contract.

### 3.5 Confidence anchor

A confidence anchor is an output, command or check that increases confidence in release stability.

Not every confidence anchor is a golden output.

For example, `mkdocs build --strict` is a confidence anchor, but not a golden output.

---

## 4. Current v1.0 golden signatures

v1.0.0 includes committed golden signatures for selected contract-significant fields of the demo-3u Core-owned structured surfaces:

```text
tests/golden/demo_3u_core_surfaces/model_summary_contract_signature.json
tests/golden/demo_3u_core_surfaces/entity_index_contract_signature.json
tests/golden/demo_3u_core_surfaces/relationship_manifest_contract_signature.json
```

The related regression tests are in:

```text
tests/test_v1_golden_core_surfaces.py
```

These signatures protect selected contract-significant fields such as:

```text
surface kind
surface version
mission identity
boundary flags
domain counts
entity identifiers
relationship family counts
selected relationship records
```

They do not freeze:

```text
full generated JSON files
absolute paths
human-oriented terminal output
Markdown wording
generated runtime bindings
generated ground dictionaries
disposable artifact formatting
```

---

## 5. Future golden-output candidates

The following families may be candidates for future golden-output review after v1.0.0.

| Family | Current posture | Golden-output suitability | Reason |
|---|---|---|---|
| Lint JSON report | Stable selected surface | Strong candidate | Machine-readable validation reports matter for CI users. |
| Simulation JSON report | Stable selected surface | Strong candidate | Scenario evidence is a stable selected surface. |
| `model_summary.json` | Stable selected surface | Already protected by selected golden signature | Core-owned structured inspection surface. |
| `entity_index.json` | Stable selected surface | Already protected by selected golden signature | Core-owned entity-level surface for downstream tools. |
| `relationship_manifest.json` | Stable selected surface for admitted families | Already protected by selected golden signature | Core-owned relationship-level surface for downstream tools. |
| `runtime_contract_manifest.json` | Public preview generated artifact | Possible candidate | Manifest fields may matter more than generated C++ formatting. |
| `ground_contract_manifest.json` | Public preview generated artifact | Possible candidate | Manifest boundary claims may matter more than generated dictionary formatting. |
| Generated Markdown docs | Disposable generated artifact | Weak candidate | Human-reviewable docs may change wording without changing contract semantics. |
| Plain-text simulation logs | Human-oriented output | Weak candidate | Logs should remain human-readable, not machine contracts. |
| Generated C++17 runtime bindings | Disposable generated artifact | Selective candidate only | Specific semantic fragments may matter, but formatting should not be frozen prematurely. |
| Generated CSV ground dictionaries | Disposable generated artifact | Selective candidate only | Useful for review, but CSV formatting should not become stable accidentally. |

A future PR may turn one or more of these into committed golden baselines only after the intended comparison scope is documented.

---

## 6. What should be protected

Golden-output review should prioritize outputs that represent stable or candidate contract meaning.

High-value comparison targets include:

```text
top-level JSON fields
kind values
version fields
result values
diagnostic code records
entity kind records
entity identifier records
relationship family records
relationship endpoint records
boundary flags
manifest profile names
manifest non-runtime and non-ground claims
scenario evidence records
```

Low-value comparison targets include:

```text
human-oriented terminal wording
Markdown prose wording
incidental whitespace
implementation-dependent ordering that is not documented
file formatting unrelated to machine-readable meaning
plain-text logs intended for humans
example narrative text
```

The project should protect meaning first.

It should freeze formatting only when formatting is part of the documented contract.

---

## 7. Required golden-output acceptance criteria

A future golden-output PR should answer these questions before adding committed baselines:

```text
Which public or stable surface is protected?
Which command produces the output?
Which fixture or example mission is used?
Which fields are contract-significant?
Which fields are intentionally ignored?
Is ordering contract-significant?
Is formatting contract-significant?
Is the output stable across supported Python versions?
What compatibility class applies if the output changes?
What migration or compatibility note is required if the output changes?
```

A golden-output PR should not combine unrelated functional changes.

If a golden baseline changes, the PR must explain whether the change is:

```text
corrective
clarifying
additive
compatibility-sensitive
breaking preview change
internal-only
```

---

## 8. Downstream consumer rule

Downstream tools should rely on documented Core-owned structured surfaces, not on CI artifact locations or human-oriented output.

The preferred downstream inspection chain remains:

```text
model_summary.json
entity_index.json
relationship_manifest.json
```

If those surfaces are golden-signature protected, the protected meaning should match the documented downstream consumption boundary.

A downstream tool must not treat generated Markdown, generated C++ files, generated CSV files, plain-text logs or terminal output as stronger contracts than the Core-owned structured surfaces.

---

## 9. Non-goals

This policy does not introduce:

```text
new generated surfaces
new JSON report fields
new Mission Model semantics
new YAML fields
new CLI behavior
schema migration tooling
JSON Schema publication
runtime behavior
ground behavior
plugin discovery
plugin loading
plugin execution
metadata schema
metadata parser
metadata loader
metadata validator
Studio-specific API
```

This policy defines how OrbitFabric decides what deserves golden-output protection after v1.0.0.
