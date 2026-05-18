# Golden Output and Regression Confidence Policy

Status: Development preview  
Scope: v0.12.0 release candidate hardening  
Applies to: generated outputs, JSON reports, Core-owned structured surfaces, CI artifacts and future golden-output decisions before v1.0.0

This page defines how OrbitFabric should reason about golden outputs and regression confidence on the path toward `v1.0.0 - Stable Mission Data Contract`.

It is a policy document only.

It does not introduce new tests, new golden files, new snapshot infrastructure, new generated surfaces, new JSON report fields, new CLI behavior, new Mission Model semantics, schema migration tooling, JSON Schema publication, runtime behavior, ground behavior, plugin discovery, plugin loading, plugin execution, metadata schema, metadata parser, metadata loader, metadata validator or Studio-specific APIs.

---

## 1. Purpose

v0.12.0 is a release candidate hardening milestone.

As OrbitFabric moves toward v1.0.0, some outputs become important confidence anchors for users, CI and downstream tools.

The purpose of this policy is to separate:

```text
current CI-generated evidence
candidate golden outputs
future committed golden baselines
human-reviewable generated artifacts
disposable generated artifacts
internal test assets
```

This distinction matters because not every reproducible output should become a committed golden baseline.

A golden output is useful only when it protects a public or candidate contract surface from accidental drift.

A golden output is harmful when it freezes incidental formatting, demo wording, implementation order or disposable artifact details too early.

---

## 2. Current CI confidence baseline

The current CI pipeline already provides regression confidence by running the main project checks and regenerating representative outputs.

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

It does not automatically create committed golden-output baselines.

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

It must protect a specific public or candidate contract behavior.

### 3.3 Snapshot test

A snapshot test compares current output against a stored expected output.

Snapshot tests are useful only when the stored output represents a meaningful public or candidate contract surface.

Snapshot tests should not freeze incidental ordering, whitespace or human-oriented wording unless those details are intentionally part of the contract.

### 3.4 Confidence anchor

A confidence anchor is an output, command or check that increases confidence in release stability.

Not every confidence anchor is a golden output.

For example, `mkdocs build --strict` is a confidence anchor, but not a golden output.

---

## 4. Candidate golden-output families

The following families are candidates for future golden-output review before v1.0.0.

| Family | Current posture | Golden-output suitability | Reason |
|---|---|---|---|
| Lint JSON report | Public preview | Strong candidate | Machine-readable validation reports are likely to matter for CI users. |
| Simulation JSON report | Public preview | Strong candidate | Scenario evidence is a candidate v1.0 surface and should not drift silently. |
| `model_summary.json` | Candidate contract | Strong candidate | Core-owned structured inspection surface with narrow semantics. |
| `entity_index.json` | Candidate contract | Strong candidate | Core-owned entity-level surface for downstream tools. |
| `relationship_manifest.json` | Candidate contract | Strong candidate | Core-owned relationship-level surface for downstream tools. |
| `runtime_contract_manifest.json` | Public preview generated artifact | Possible candidate | Manifest fields may matter more than generated C++ formatting. |
| `ground_contract_manifest.json` | Public preview generated artifact | Possible candidate | Manifest boundary claims may matter more than generated dictionary formatting. |
| Generated Markdown docs | Disposable generated artifact | Weak candidate | Human-reviewable docs may change wording without changing contract semantics. |
| Plain-text simulation logs | Human-oriented output | Weak candidate | Logs should remain human-readable, not machine contracts. |
| Generated C++17 runtime bindings | Disposable generated artifact | Selective candidate only | Specific semantic fragments may matter, but formatting should not be frozen prematurely. |
| Generated CSV ground dictionaries | Disposable generated artifact | Selective candidate only | Useful for review, but CSV formatting should not become stable accidentally. |

A future PR may turn one or more of these into committed golden baselines only after the intended comparison scope is documented.

---

## 5. What should be protected before v1.0.0

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

## 6. Required golden-output acceptance criteria

A future golden-output PR should answer these questions before adding committed baselines:

```text
Which public or candidate surface is protected?
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

## 7. Current no-golden-baseline rule

At the start of v0.12.0, OrbitFabric should not assume that CI artifacts are committed golden baselines.

Current generated reports and generated docs are useful release confidence artifacts.

They are not automatically stable expected outputs.

A future PR must explicitly introduce any golden-output baseline.

That PR should be small, reviewed and tied to one output family at a time.

---

## 8. Recommended v0.12.0 review sequence

The recommended v0.12.0 sequence is:

```text
1. inventory candidate v1.0 surfaces
2. define golden-output and regression confidence policy
3. decide first golden-output candidate family
4. add golden baselines only if the comparison scope is clear
5. document compatibility or migration notes for any intentional drift
6. defer unstable or overly broad outputs beyond v1.0.0
```

The first likely golden-output families are:

```text
model_summary.json
entity_index.json
relationship_manifest.json
lint JSON report
simulation JSON report
```

Generated C++17 bindings, generated Markdown docs, CSV dictionaries and plain-text logs should not be first candidates unless a narrow comparison target is defined.

---

## 9. Downstream consumer rule

Downstream tools should rely on documented Core-owned structured surfaces, not on CI artifact locations or human-oriented output.

The preferred downstream inspection chain remains:

```text
model_summary.json
entity_index.json
relationship_manifest.json
```

If those surfaces become golden-output protected, the protected meaning should match the documented downstream consumption boundary.

A downstream tool must not treat generated Markdown, generated C++ files, generated CSV files, plain-text logs or terminal output as stronger contracts than the Core-owned structured surfaces.

---

## 10. Non-goals

This policy does not introduce:

```text
new golden files
new snapshot tests
new CI jobs
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
stable v1.0 compatibility guarantee
```

This policy only defines how OrbitFabric should decide what deserves golden-output protection on the path toward v1.0.0.
