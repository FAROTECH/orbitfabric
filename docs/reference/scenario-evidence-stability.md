# Scenario Evidence Stability

Status: Active v1.x reference through v1.2.0  
Scope: scenario input and evidence compatibility  
Applies to: OrbitFabric scenario workflows from v1.0.0 onward

OrbitFabric scenarios provide deterministic host-side evidence for Mission Data Contract behavior.

v1.2.0 introduces no new scenario YAML semantics and no change to stable scenario result meaning. The additive structured expectation accounting introduced in v1.1 remains candidate.

## 1. Source of truth

Scenario evidence is derived from:

```text
Mission Model YAML
scenario YAML
```

The Mission Model defines mission semantics. Scenario YAML defines host-side scenario inputs and expectations.

Simulation JSON reports and plain-text logs are generated evidence outputs, not editable mission contract sources.

## 2. Current classification

| Surface | Classification | Notes |
|---|---|---|
| scenario YAML | Stable | Host-side scenario input contract. |
| scenario path argument | Stable workflow | Used by validation and simulation. |
| scenario loader diagnostics | Stable policy | Core-owned diagnostic behavior. |
| scenario reference validation | Stable behavior | References are checked before execution. |
| scenario execution result | Stable behavior | Deterministic host-side evidence. |
| simulation JSON report | Stable | Machine-readable scenario evidence. |
| `failed_expectations` | Stable compatibility field | Legacy failed-expectation list. |
| structured `expectations` object | Candidate additive v1.1 extension | Passed/failed structured accounting. |
| data-flow evidence records | Stable | Contract-level data-flow evidence. |
| plain-text simulation log | Human-oriented preview | Not a machine contract. |
| scenario runner internals | Internal | Not a public compatibility surface. |

## 3. Validation and execution

Validation without execution:

```bash
orbitfabric validate scenario <scenario_file>
```

Deterministic execution:

```bash
orbitfabric sim <scenario_file>
```

Simulation may emit JSON and plain-text evidence outputs. Changing the distinction between validation and execution is compatibility-sensitive.

## 4. Scenario expectation stability

Scenario expectations define what evidence a scenario asserts.

Changing documented expectation meaning can change:

```text
scenario pass/fail status
simulation JSON reports
plain-text evidence logs
data-flow evidence
CI behavior
downstream inspection results
```

Expectation semantics therefore remain compatibility-sensitive.

Scenario expectations remain declarative host-side checks. They must not silently become flight runtime behavior, ground automation, onboard scheduling, command-dispatch implementation or plugin execution.

## 5. Structured expectation accounting

v1.1 added structured expectation accounting to simulation JSON reports.

The addition is machine-readable and additive, but remains candidate after v1.2.

The stable legacy field remains:

```text
failed_expectations
```

Structured accounting may expose totals, passed/failed counts and records describing evaluated expectations.

It does not change scenario YAML syntax or the stable overall scenario result meaning.

## 6. Data-flow evidence

Data-flow evidence traces declared contract continuity such as:

```text
command expected effect
    -> data product
    -> storage intent
    -> downlink intent
    -> eligible downlink flow
    -> contact window
```

This is contract-level host-side evidence.

It is not an onboard storage implementation, downlink queue, contact scheduler, RF model or ground operations record.

## 7. Simulation JSON stability

Compatibility-sensitive changes include:

- removing or renaming stable documented top-level fields;
- changing stable result tokens;
- changing the meaning of data-flow evidence records;
- changing whether a documented expectation affects pass/fail status;
- changing stable failed-expectation representation;
- changing documented machine-readable evidence meaning.

Compatibility-sensitive does not mean forbidden. It means the change must be explicit, reviewed and documented.

## 8. Plain-text logs

Plain-text logs are intended for human review, demonstrations and debugging.

They are not a strict machine compatibility contract. Downstream tools should consume simulation JSON instead of parsing log wording or formatting.

## 9. Evolution rules

Scenario and evidence evolution should:

1. prefer additive changes;
2. preserve existing documented expectation meaning;
3. preserve deterministic execution for the same validated inputs;
4. keep host-side evidence separate from operational runtime behavior;
5. keep machine-readable evidence separate from human-oriented logs;
6. document compatibility impact explicitly.

## 10. Downstream consumer rule

Downstream tools may consume documented simulation JSON fields.

They must not infer hidden semantics from:

```text
plain-text log wording
terminal formatting
scenario comments
YAML ordering
private runner implementation
private test helper names
UI state
```

For Mission Data Contract structure, consumers should use Core-owned structured surfaces. For scenario evidence, they should use the documented simulation JSON report.

## 11. Current non-goals

Scenario evidence does not introduce:

```text
spacecraft dynamics simulation
flight runtime behavior
ground runtime behavior
real contact scheduling
RF or link-budget simulation
onboard storage execution
live command dispatch
plugin execution
relationship inference
Studio-specific semantic authority
```

## 12. Relationship to other references

This page complements:

- Data Flow Evidence;
- JSON Reports and Core Structured Surfaces;
- JSON Report Compatibility;
- CLI Contract v1;
- Mission Model Stability Contract;
- Stability and Compatibility Contract.

## 13. Final statement

The stable scenario contract remains the v1 host-side evidence mechanism.

v1.2.0 changes no scenario semantics. The v1.1 structured expectation object remains a candidate additive extension inside the stable simulation report family.
