# ADR-0022: Result-Owned Scenario Projection Accounting

Status: Accepted  
Date: 2026-09-10

## Context

Generic consumers need the projection disposition declared by the projection
authority for each exact Scenario atom. Integration mappings, evidence absence
and shared EntityRefs cannot establish that claim. Reading target-specific
projection plans in a generic consumer would move adapter semantics across the
ownership boundary.

## Decision

Publish `orbitfabric.scenario_projection_accounting` as an independently
versioned Result-owned artifact at `0.1-candidate`.

Core owns its generic schema, vocabulary and conformance. Adapters own the
records. The payload uses exact Scenario id/source SHA, atom id, explicit
complete or partial accounting, producer-owned reasons and zero or more
parent-local `mapping_ids`.

The only dispositions are `projected`, `not_projected` and
`unsupported`. Negative dispositions require an empty mapping list and a
nonblank reason. `projected` permits an empty mapping list.

The parent owns artifact id, path and digest. The sidecar omits the final
Result SHA. Consumer identity combines the exact Result SHA, artifact id and
artifact SHA.

## Consequences

- Mission and Scenario semantics remain unchanged.
- A Scenario-free operation cannot declare atom projection accounting.
- Missing records in partial accounting remain unavailable.
- Existing Results remain valid without the new artifact.
- Consumers validate structure, parent binding, Scenario binding and bundle
  integrity as separate domains.
- New producer emission creates a new Result identity.

