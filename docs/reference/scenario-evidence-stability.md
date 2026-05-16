# Scenario Evidence Stability

Status: Development preview  
Scope: v0.10.0 scenario and evidence compatibility classification  
Applies to: OrbitFabric scenario inputs and scenario evidence before v1.0.0

This page classifies OrbitFabric scenario and evidence compatibility expectations on the path toward v1.0.0.

It is a documentation contract. It does not introduce new scenario fields, new scenario behavior, new JSON report fields, new CLI behavior, new Mission Model semantics, plugin execution, runtime behavior, ground behavior or Studio-specific APIs.

---

## 1. Purpose

OrbitFabric scenarios provide deterministic host-side evidence for Mission Data Contract behavior.

Before v1.0.0, scenarios and scenario evidence are still development-preview surfaces. However, documented scenario structure, validation behavior, expectation semantics, result values and machine-readable evidence outputs are compatibility-sensitive.

This document defines how scenario inputs and generated evidence should evolve before v1.0.0.

It covers:

- scenario YAML classification;
- validation versus execution boundaries;
- expectation stability;
- simulation report stability;
- plain-text log stability;
- data-flow evidence stability;
- downstream tooling expectations;
- non-goals.

The detailed field-level report structures remain documented in `JSON Reports v0.1` and `Data Flow Evidence`.

---

## 2. Source of truth

Scenario evidence is derived from:

```text
Mission Model YAML
scenario YAML
```

The Mission Model defines the Mission Data Contract.

The scenario YAML defines host-side scenario inputs and expectations.

Simulation JSON reports and plain-text logs are generated evidence outputs.

They are not editable mission contract sources.

---

## 3. Current classification

Current scenario and evidence surfaces are classified as follows:

| Surface | Classification | Notes |
|---|---|---|
| scenario YAML files | Public preview | Host-side scenario input surface. |
| scenario file path argument | Public preview | Used by `orbitfabric validate scenario` and `orbitfabric sim`. |
| scenario loader diagnostics | Public preview | Uses `OF-SCN-*` diagnostics. |
| scenario reference validation | Public preview | Validates references before execution. |
| scenario execution result | Public preview | Deterministic host-side evidence result. |
| simulation JSON report | Public preview | Machine-readable scenario evidence. |
| simulation plain-text log | Human-oriented public preview | Reviewable timeline, not a machine contract. |
| data-flow evidence records | Public preview | Derived evidence for declared data-flow expectations. |
| scenario runner internals | Internal implementation detail | Not a public compatibility surface. |
| test helper structure | Internal validation asset | Not a public compatibility surface. |

No scenario or evidence surface is classified as a stable v1.0 contract yet.

---

## 4. Validation versus execution

OrbitFabric separates scenario validation from scenario execution.

Current validation command:

```bash
orbitfabric validate scenario <scenario_file>
```

Current execution command:

```bash
orbitfabric sim <scenario_file>
```

Validation checks scenario loadability and references without executing scenario behavior.

Execution runs the scenario deterministically against the referenced Mission Model and may produce JSON and plain-text evidence outputs.

Changing this boundary is compatibility-sensitive.

---

## 5. Scenario expectation stability

Scenario expectations are compatibility-sensitive because they define what evidence the scenario is asserting.

Changing documented expectation semantics can affect:

- scenario pass/fail results;
- simulation JSON reports;
- plain-text evidence logs;
- data-flow evidence records;
- CI workflows;
- downstream inspection tools.

Scenario expectations should remain declarative host-side evidence checks.

They should not silently become runtime execution behavior, onboard scheduling, command dispatch implementation, ground automation or plugin behavior.

---

## 6. Data-flow evidence stability

Data-flow evidence links declared command effects to declared data product, storage, downlink and contact assumptions.

The evidence chain remains:

```text
command expected effect
        -> data product
        -> storage intent
        -> downlink intent
        -> eligible downlink flow
        -> matching contact window
```

This is contract-level evidence.

It is not a runtime downlink queue, onboard storage implementation, contact scheduler, RF model, ground station workflow or mission operations system.

Changing the meaning of this chain is compatibility-sensitive.

---

## 7. Simulation JSON report stability

Simulation JSON reports are machine-readable public preview evidence outputs.

The following changes are compatibility-sensitive before v1.0.0:

- removing a documented top-level simulation report field;
- renaming a documented top-level simulation report field;
- changing documented result values;
- changing documented data-flow evidence field names;
- changing the meaning of data-flow evidence records;
- changing whether a scenario expectation affects pass/fail status;
- changing how failed expectations are represented;
- changing the machine-readable timeline or evidence representation where documented.

Compatibility-sensitive does not mean forbidden.

It means the change must be explicit, reviewed and documented.

---

## 8. Plain-text log stability

Plain-text simulation logs are human-reviewable evidence.

They are useful for demonstrations, inspection and debugging.

They are not a strict machine compatibility contract.

Downstream tools should not parse plain-text simulation logs when a JSON report or Core-owned structured surface exists.

Formatting, wording and line layout may improve over time without becoming a v1.0 machine contract.

---

## 9. Scenario diagnostics

Scenario diagnostics use the `OF-SCN-*` family.

Diagnostic code meaning is compatibility-sensitive and is classified in `Lint Rule Code Stability`.

Scenario diagnostics should remain actionable.

They should identify invalid scenario structure, invalid references or unsupported scenario expectations without requiring downstream tools to parse human-oriented terminal text.

---

## 10. Preferred evolution rules

Before v1.0.0, scenario and evidence surfaces should evolve with these rules.

### 10.1 Prefer additive changes

Prefer adding optional scenario fields or optional report fields over renaming or removing existing documented fields.

### 10.2 Preserve expectation meaning

Do not change the meaning of a documented expectation without an explicit compatibility note.

### 10.3 Preserve deterministic evidence

Scenario execution should remain deterministic for the same validated inputs.

### 10.4 Keep host-side evidence separate from runtime behavior

Scenario evidence should remain host-side Mission Data Contract evidence.

It should not become flight software behavior, ground software behavior or plugin execution behavior.

### 10.5 Keep machine-readable evidence separate from human logs

Downstream tools should consume simulation JSON reports, not plain-text logs.

---

## 11. Downstream tool rule

Downstream tools may consume scenario JSON reports for evidence inspection.

They must not infer hidden semantics from:

```text
plain-text log wording
terminal formatting
finding order
scenario YAML comments
YAML ordering
private runner implementation details
private test helper names
UI state
```

For contract inspection, downstream tools should prefer Core-owned structured surfaces.

For scenario evidence, downstream tools should prefer documented simulation JSON report fields.

---

## 12. Current non-goals

This scenario evidence stability classification does not introduce:

```text
new scenario fields
new scenario behavior
new expectation types
new JSON report fields
new CLI behavior
new Mission Model semantics
new lint diagnostics
runtime execution behavior
ground execution behavior
contact scheduling runtime
RF or link-budget simulation
onboard storage runtime
command dispatcher behavior
plugin execution
plugin discovery
plugin loader
relationship graph
dependency graph
Studio-specific API
stable v1.0 scenario guarantee
```

---

## 13. Relationship to existing references

This page complements, but does not replace:

```text
Data Flow Evidence
JSON Reports v0.1
CLI Contract v1 Preview
Mission Model Stability Contract
JSON Report Compatibility
Lint Rule Code Stability
Stability and Compatibility Contract
```

`Data Flow Evidence` remains the reference for the current data-flow evidence chain.

`JSON Reports v0.1` remains the reference for the current simulation JSON report structure.

This page defines how those scenario and evidence surfaces should be treated as compatibility-sensitive before v1.0.0.

---

## 14. v1.0 direction

Before v1.0.0, OrbitFabric should decide which scenario inputs, expectation semantics and evidence report fields become stable.

Likely v1.0 candidates include:

```text
scenario file role
scenario validation workflow
scenario execution workflow
core scenario result values
simulation JSON report family
data-flow evidence semantics
scenario diagnostic code meanings
```

v1.0.0 should stabilize scenario evidence enough for CI and downstream inspection tools to rely on it, without turning OrbitFabric into a runtime simulator, flight software framework, ground segment, mission control system or plugin execution platform.
