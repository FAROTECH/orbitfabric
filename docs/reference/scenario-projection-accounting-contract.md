# Scenario Projection Accounting Contract

Status: Candidate generic integration contract  
Kind: `orbitfabric.scenario_projection_accounting`  
Version: `0.1-candidate`

## Purpose and ownership

Scenario Projection Accounting is a Result-owned JSON artifact. It records the
projection disposition declared by an adapter for each exact Scenario atom.

Core publishes the generic vocabulary, schema and conformance rules. The
adapter owns every disposition, reason and mapping association. Consumers
validate and present those claims without deriving them from EntityRef
co-membership, absent evidence or target-specific files.

This contract does not change Mission or Scenario semantics.

## Exact identity

The payload identifies a Scenario with its id and SHA-256 over the exact source
bytes. Each record identifies one `atom_id` within that exact source.

The parent Integration Result `0.2-candidate` must:

- explicitly contain one available `scenario` operation input with the same
  id and SHA-256;
- register the artifact by id, generic kind, relative path and content SHA-256;
- own every referenced `mapping_id`;
- list the exact union of payload mappings in
  `artifact.derived_from_mappings`.

The sidecar contains no parent Result SHA and no self-digest. A consumer
identifies it with:

```text
exact Result SHA + artifact id + exact artifact SHA
```

This direction avoids a digest cycle.

## Dispositions

| Value | Producer declaration | Mapping ids | Reason |
|---|---|---|---|
| `projected` | The atom is represented in this operation's projection scope | Zero, one or more | Optional |
| `not_projected` | The producer accounted for the atom and did not project it | Empty | Required |
| `unsupported` | The producer declares the atom unrepresentable in the current target or projection contract | Empty | Required |

Reasons are producer-owned text. Consumers do not parse them for generic
semantics. `projected` does not imply execution, runtime success or semantic
equivalence.

## Completeness

`complete` contains every atom from the exact loaded Scenario Declaration,
once each. `partial` contains an explicit subset and requires a nonblank
top-level reason. An omitted atom in partial accounting has unavailable
disposition. Absence never means `not_projected` or `unsupported`.

## Validation domains

Conformance is split into four checks:

1. Sidecar schema and unique atom accounting.
2. Binding to the exact parent Result, Scenario input and local mappings.
3. Binding to the exact loaded Scenario Declaration and its atom inventory.
4. Bundle containment and exact Result/artifact byte digests.

Schema validation alone establishes only the first domain.

## Checker

```sh
python -m orbitfabric.conformance.scenario_projection_accounting \
  integration_result.json scenario-accounting scenario_declaration.json
```

Use `--result-sha256` when the caller has already selected an exact retained
Result identity.

The public fixtures include complete eight-atom R1 accounting, explicit
`projected` metadata with zero mappings, `atom-0003` as
`not_projected`, `atom-0006` as `projected` through
`mapping.op-0002`, and synthetic partial/unsupported controls.

## Compatibility

The payload version evolves independently of Integration Result
`0.2-candidate`. Existing Results without this artifact remain valid and
mean that Scenario atom projection disposition is unavailable. An unknown
accounting version is an unsupported presentation surface and must not be
decoded by shape.

