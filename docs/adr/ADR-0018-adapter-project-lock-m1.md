# ADR-0018: Adapter Project Lock M1

Status: Accepted  
Date: 2026-09-02

## Context

Adapter Manager M0 introduced Core-owned user-scoped actual installed adapter state.

Projects also need a reproducible declaration of the exact adapter releases they require. That declaration must remain portable and must not absorb machine-local instance ids, installation paths, executable bindings or mutable artifact locators.

## Decision

Introduce the candidate project-level contract:

```text
kind         orbitfabric.adapter_project_lock
lock_version 0.1-candidate
```

Each lock entry retains:

```text
Adapter Source Coordinate
exact release version
Release Descriptor SHA-256
selected artifact id
selected artifact SHA-256
installation backend id
optional backend-resolution binding
```

A complete Source Coordinate may appear at most once in one lock.

Core compares each lock entry against the Installed Adapter Inventory using:

```text
MATCH
MISSING
MISMATCH
```

`MATCH` requires equality of Source Coordinate, release version, Release Descriptor digest, artifact id, artifact digest and backend id.

The overall project state is `MATCH` only when every locked adapter entry matches at least one installed record. Otherwise it is `NOT_SATISFIED`.

Extra installed versions do not invalidate a project when an exact match also exists. Multiple exact local instances still satisfy project availability.

## Consequences

- Project desired state remains separate from user-scoped actual installed state.
- Release version alone is never treated as exact project identity.
- The lock remains portable because it contains no local lifecycle paths or instance ids.
- M1 validation and comparison require no remote registry.
- The first CLI accepts an explicit lock path rather than freezing a default filesystem location.
- Install-from-lock remains a later operation that combines lock identity with a Release Source.
- Project execution selection from multiple exact local instances remains outside this revision.
