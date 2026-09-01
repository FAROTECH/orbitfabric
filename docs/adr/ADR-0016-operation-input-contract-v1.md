# ADR-0016: Versioned Operation-Input Contract Lane

Status: Accepted  
Date: 2026-09-01

## Context

The design-frozen external integration lane uses Manifest `0.1-candidate`,
`orbitfabric.adapter_cli.v0`, and Result `0.1-candidate` with fixed IISS and
Projection Profile context.

Independent OpenSVF and COSMOS integrations demonstrated one additional
Core-owned Scenario input. F´ and project-only controls demonstrated that no
additional input must remain a natural operation shape. The frozen v0 lane
continued to pass through the same generic Studio consumer.

Adding required operation semantics under v0 identifiers would allow an old
consumer to execute with incomplete context and then overclaim Result
freshness.

## Decision

Introduce one coherent package-level lane:

```text
Manifest 0.2-candidate
orbitfabric.adapter_cli.v1
Result 0.2-candidate
```

Manifest operations explicitly declare `input_requirements`. The initial
contract supports zero or one required file-backed role, with `scenario` as
the first contract-defined role.

Protocol v1 carries the binding as direct argv:

```text
--operation-input ROLE PATH
```

Result 0.2-candidate records exact consumed provenance under:

```text
inputs.operation_inputs
```

The frozen v0 triple remains supported unchanged. Mixed triples, optional or
multiple roles, non-file resources, protocol negotiation, and per-operation
protocol selection are not supported by this revision.

## Consequences

- Old consumers fail clearly on the new version instead of ignoring meaning.
- Zero-input operations retain explicit empty requirement/provenance arrays.
- Required Scenario operations fail closed before execution.
- Positive freshness includes every declared semantic input.
- Core owns contract schemas and conformance semantics but does not execute
  target adapters in-process.
- Studio remains a generic consumer and adapters retain target projection.
- Later cardinality or resource expansion requires new evidence and review.

