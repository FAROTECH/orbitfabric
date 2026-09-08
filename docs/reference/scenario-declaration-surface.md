# Scenario Declaration Surface

Status: **candidate Core-owned structured surface**  
Surface kind: `orbitfabric.scenario_declaration`  
Declaration version: `0.1-candidate`

## Purpose

The Scenario Declaration Surface exposes the authored meaning of one validated OrbitFabric Scenario as a deterministic machine-readable Core product.

It exists so external consumers can understand declared Scenario intent without becoming a second Scenario YAML interpreter.

```text
Scenario YAML
    -> Core ScenarioLoader
    -> Mission binding and reference validation
    -> Core-owned semantic normalization
    -> scenario_declaration JSON
```

The surface is declaration, not execution evidence.

```text
DECLARED != EXECUTED != OBSERVED
```

It does not replace `orbitfabric sim --json`, which remains Core host-side execution/evidence output.

## CLI

```bash
orbitfabric export scenario-declaration path/to/scenario.yaml \
  --json path/to/scenario_declaration.json
```

The command writes a JSON envelope on both success and semantic/load failure when the output path itself is writable.

A failed declaration exits non-zero after writing the structured failure envelope.

## Loaded envelope

Conceptual shape:

```json
{
  "kind": "orbitfabric.scenario_declaration",
  "declaration_version": "0.1-candidate",
  "orbitfabric_version": "1.3.0",
  "result": "loaded",
  "scenario": {
    "id": "battery_low_during_payload",
    "name": "Battery degradation during payload operation",
    "description": "..."
  },
  "mission": {
    "id": "demo-3u",
    "model_version": "0.1.0"
  },
  "source": {
    "scenario_sha256": "..."
  },
  "atom_count": 21,
  "atoms": [],
  "diagnostics": []
}
```

`source.scenario_sha256` is SHA-256 over the exact consumed Scenario bytes. It is the exact source freshness anchor for this surface.

The surface does not invent a new Mission Model byte fingerprint. Mission binding is represented by the Core-validated mission id and model version.

## Failed envelope

Conceptual shape:

```json
{
  "kind": "orbitfabric.scenario_declaration",
  "declaration_version": "0.1-candidate",
  "orbitfabric_version": "1.3.0",
  "result": "failed",
  "scenario": null,
  "mission": null,
  "source": {
    "scenario_sha256": "... or null"
  },
  "atom_count": null,
  "atoms": null,
  "diagnostics": [
    {
      "severity": "ERROR",
      "code": "OF-SCN-...",
      "file": "...",
      "domain": "scenario",
      "object_id": "...",
      "message": "...",
      "suggestion": "..."
    }
  ]
}
```

The failure rule is:

```text
complete normalized Scenario
OR
structured Core failure with no partial fabricated Scenario semantics
```

Consumers must not parse CLI error wording or stderr to recover Scenario meaning.

## Declared atoms

A Scenario source step is not assumed to be one semantic atom.

Core normalizes one source step into zero or more explicit semantic atoms. Examples include:

```text
command + command-status expectation
multiple telemetry expectations at one Scenario time
data-flow expectation with several role-distinct Mission references
```

Each loaded atom has:

```text
id
role
kind
step_index
within_step_ordinal
scenario_time_s
references[]
declaration
```

### Atom identity

Atom ids are deterministic within one normalized declaration and currently use:

```text
atom-0001
atom-0002
...
```

The correlation scope is:

```text
scenario_sha256 + atom_id
```

No cross-revision atom-id stability is promised by `0.1-candidate`.

### Step position

`step_index` is the zero-based position of the source step.

`within_step_ordinal` is Core's deterministic normalization order inside that step. It is not a claim that the author declared micro-timing between semantics sharing the same Scenario time.

For Scenario metadata and initial-state atoms, both fields are `null` because those facts are not source-step members.

### Scenario time

For step-derived atoms, `scenario_time_s` is the authored `t` value.

The stable Scenario contract defines `t` as Scenario time in seconds from Scenario start.

It must not be reinterpreted as:

```text
downstream target scheduling
spacecraft clock time
wall-clock timestamp
execution latency
ground automation timing
```

Metadata and initial-state atoms use `scenario_time_s: null`.

## Atom kinds

The first candidate producer emits these Core-owned kinds when present:

```text
scenario_metadata
initial_mode
initial_telemetry
command
telemetry_injection
expect_event
expect_mode
expect_command
expect_telemetry
expect_command_status
expect_payload_lifecycle
expect_data_flow
expect_scenario_status
```

These names belong to this candidate structured surface. They do not define adapter projection support.

## Deterministic normalization order

Top-level declaration ordering is:

```text
1. scenario_metadata
2. initial_mode
3. initial_telemetry sorted by telemetry id
4. source steps in authored step order
```

Within each source step the current `0.1-candidate` order is:

```text
command
expect_command_status
telemetry_injection
expect_event
expect_mode
expect_command
expect_telemetry sorted by telemetry id
expect_payload_lifecycle
expect_data_flow
expect_scenario_status
```

This is a producer normalization rule. YAML mapping-key order is not a semantic input.

## Entity references

Mission references are emitted explicitly as role-labelled Core EntityRefs:

```json
{
  "role": "command",
  "entity": {
    "domain": "commands",
    "id": "payload.start_acquisition"
  }
}
```

The domain vocabulary reuses the Core Entity Index vocabulary, including:

```text
modes
telemetry
commands
events
payloads
data_products
downlink_flows
contact_windows
```

A data-flow atom can carry several references with different semantic roles. Consumers must use the emitted role and EntityRef rather than inspect keys inside the declaration payload to infer navigation identity.

The producer fails closed rather than emit an EntityRef it cannot validate against the referenced Mission Model.

## Kind-specific declaration data

`declaration` carries the authored value required by the atom kind.

Examples:

```text
command
    authored arguments

initial_telemetry / telemetry_injection
    authored value

expect_telemetry
    expected value

expect_command
    dispatch + expected presence

expect_payload_lifecycle
    payload + expected lifecycle state

expect_data_flow
    authored data-flow expectation object

expect_scenario_status
    expected Scenario status
```

`declaration` is not a YAML AST. A consumer must not use it to rediscover references that Core already emits through `references[]`.

## Complete accounting and unknown semantics

The producer promises complete accounting for the Scenario semantics it supports.

An `expect` key that the candidate declaration surface cannot normalize is not silently dropped and is not exposed as an opaque extension for the consumer to interpret.

Instead:

```text
unknown / unnormalizable semantic content
    -> result = failed
    -> atoms = null
    -> structured Core diagnostic
```

This keeps Core as the semantic authority.

The rule does not redefine the stable behavior of `orbitfabric validate scenario` or `orbitfabric sim`. It defines only the candidate Scenario Declaration producer contract.

## Boundaries

The envelope explicitly declares:

```text
source_of_truth                    scenario_yaml
core_derived_report                true
read_only                          true
contains_declared_scenario         true
contains_complete_atom_accounting  true
contains_structured_diagnostics    true
contains_yaml_ast                  false
contains_simulation_evidence       false
contains_target_projection         false
contains_runtime_behavior          false
contains_ground_behavior           false
contains_plugin_api                false
contains_studio_api                false
```

## Consumer rules

Compatible consumers must:

- check `kind` and `declaration_version`;
- treat `result=failed` as a structured Core failure, not as a partial Scenario;
- use exact `scenario_sha256` for source freshness/correlation;
- use emitted `references[]` for Mission entity identity;
- preserve Scenario time semantics without promoting it into downstream timing;
- tolerate additive fields where future candidate compatibility rules permit them;
- avoid raw Scenario YAML fallback for missing meaning.

## Non-goals

The first candidate surface does not provide:

```text
Scenario directory discovery
Scenario editing or write-back
simulation results
runtime telemetry or command evidence
adapter projection disposition
generated target artifacts
target-native identities
a universal execution timeline
Studio-specific API fields
plugin semantics
```

Scenario discovery remains a separate workspace concern.

## Compatibility posture

`orbitfabric.scenario_declaration` `0.1-candidate` is an additive candidate structured surface.

It does not change the stable Scenario YAML contract, stable Mission Data Contract semantics, existing simulation evidence formats, Integration Input Set or adapter execution protocols.

Candidate evolution requires explicit compatibility review and regression protection.