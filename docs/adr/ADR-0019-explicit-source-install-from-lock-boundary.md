# ADR-0019: Explicit-Source Install-from-Lock Boundary

Status: **Candidate**  
Date: **2026-09-02**

## Context

Adapter Manager M0 owns actual installed adapter state and a verified installation transaction.

Adapter Project Lock M1 owns exact project-required adapter state and can report `MATCH`, `MISSING` or `MISMATCH` against that inventory.

The remaining first-lane gap is to move one unsatisfied lock entry toward `MATCH` without embedding source locators in the lock, creating a second installer, or introducing remote registry semantics prematurely.

## Decision

Core introduces a candidate single-entry install-from-lock orchestration that composes the existing boundaries:

```text
Adapter Project Lock entry
    + explicit Release Descriptor + artifact
        |
        v
Explicit Release Source
        |
        v
ResolvedAdapterRelease
        |
        v
exact lock identity verification
        |
        v
locked installation backend verification
        |
        v
shared Adapter Manager installation transaction
        |
        v
Installed Adapter Record
        |
        v
M1 re-check
        |
        v
MATCH
```

The existing explicit `orbitfabric adapter install` path and install-from-lock converge on the same post-resolution installation transaction.

## Exact verification ordering

Before installation backend materialization, Core requires the resolved release to match the selected lock entry for:

```text
source_coordinate
release_version
release_descriptor_sha256
artifact_id
artifact_sha256
```

Core then selects the installation backend and requires its id to equal the lock entry's `installation_backend.id` before invoking the backend.

Release acceptance remains a separate concern and is evaluated by the shared Adapter Manager transaction.

## State behavior

The first lane is intentionally non-destructive:

```text
MATCH
    -> NOOP

MISSING
    -> install exact locked release
    -> MATCH

MISMATCH
    -> install exact locked release side-by-side
    -> retain the existing mismatching release
    -> MATCH
```

No machine-global active/default release is introduced.

## Project Lock portability

Install-from-lock does not add transport locators to the Adapter Project Lock.

The lock remains exact desired identity and does not contain local paths, GitHub URLs, registry URLs, mirror URLs or cache locations.

Explicit descriptor and artifact paths are invocation inputs to the current Release Source, not Project Lock identity.

## One installation transaction

`AdapterManager.install()` continues to provide the existing explicit-source behavior, but delegates the resolved release to the same shared transaction used by install-from-lock.

That shared transaction retains:

```text
acceptance evaluation
backend selection
backend materialization
post-install verification
Installed Adapter Record construction
inventory publication LAST
failure cleanup
```

This avoids lifecycle drift between installation entry points.

## Candidate CLI

The proof surface is:

```text
orbitfabric adapter lock install LOCK_PATH \
  --source-coordinate AUTHORITY:PUBLISHER/NAME \
  --release-descriptor RELEASE_DESCRIPTOR \
  --artifact ARTIFACT
```

`--json` returns the structured report.

The report distinguishes:

```text
before_status
action = NOOP | INSTALLED
installed_instance_id when applicable
after_status
matching_instance_ids
```

The command is a candidate product surface. It is not a registry or project-wide reconcile command.

## Consequences

Positive consequences:

- M0 and install-from-lock use one lifecycle transaction.
- exact lock identity is checked before materialization.
- `MATCH` is idempotent.
- `MISMATCH` can be satisfied without implicit destructive update.
- Release Source transport remains replaceable.
- the promoted Project Lock contract remains unchanged.

Tradeoffs:

- callers currently provide explicit source material.
- the first lane operates on one lock entry at a time.
- mismatching installed releases remain present until an explicit future policy removes them.
- optional `backend_resolution` material is retained but not yet enforced.

## Not decided here

```text
remote Release Source implementation
public registry topology
source configuration persistence
project-wide reconcile semantics
automatic update/removal policy
backend-resolution verification
multi-platform lock policy
Studio lifecycle UX
publisher trust provider implementation
```
