# Explicit-Source Install from Adapter Project Lock

Status: **candidate Core product surface**  
Depends on: **Adapter Manager M0 + Adapter Project Lock M1**

## Purpose

Adapter Project Lock tells Core what exact adapter state a project requires.

Installed Adapter Inventory tells Core what adapter state actually exists on the machine.

This candidate lane adds the first controlled way to satisfy one lock entry through exact source material:

```text
Project Lock entry
    + explicit Release Descriptor
    + explicit artifact
        -> exact verification
        -> existing Adapter Manager installation transaction
        -> Project Lock re-check
```

It does not introduce a registry.

## Command

```text
orbitfabric adapter lock install LOCK_PATH \
  --source-coordinate AUTHORITY:PUBLISHER/NAME \
  --release-descriptor RELEASE_DESCRIPTOR \
  --artifact ARTIFACT
```

Machine-readable output:

```text
orbitfabric adapter lock install ... --json
```

The `--source-coordinate` option selects exactly one entry from a potentially multi-adapter lock. The syntax is an invocation surface for the current candidate lane and does not define a public registry namespace format beyond the already modeled Source Coordinate fields.

## State transitions

### MISSING

```text
before MISSING
    -> resolve explicit source material
    -> verify exact identity
    -> install
    -> after MATCH
```

### MATCH

```text
before MATCH
    -> no source resolution or install required
    -> action NOOP
    -> after MATCH
```

This makes repeated calls idempotent at the project-satisfaction level.

### MISMATCH

```text
before MISMATCH
    -> resolve exact locked release
    -> install side-by-side
    -> retain mismatching installed release
    -> after MATCH
```

The first lane does not perform implicit replacement, removal or update.

## Exact identity gate

The explicit Release Source first validates its own Release Descriptor and artifact relationship.

Install-from-lock then requires the resolved release to agree with the selected lock entry for:

```text
source_coordinate
release_version
release_descriptor_sha256
artifact_id
artifact_sha256
```

After Core selects an installation backend, its backend id must equal the locked `installation_backend.id` before materialization begins.

A mismatch fails closed.

## Shared installation transaction

There is one Adapter Manager installation transaction after source resolution.

Both paths converge on it:

```text
orbitfabric adapter install
    -> ExplicitReleaseSource
    -> shared install transaction

orbitfabric adapter lock install
    -> ExplicitReleaseSource
    -> exact Project Lock check
    -> shared install transaction
```

The shared transaction retains acceptance evaluation, backend materialization, post-install verification, inventory publication last and cleanup on failure.

## Structured report

The candidate report contains:

```text
lock_path
source_coordinate
before_status
action
installed_instance_id
after_status
matching_instance_ids
```

`action` is currently:

```text
NOOP
INSTALLED
```

`installed_instance_id` is present only when a new local adapter instance is installed.

## Failure behavior

The operation fails before backend materialization when the supplied exact source material does not satisfy the lock or when the selected backend differs from the locked backend.

Examples:

```text
wrong Release Descriptor digest
wrong Source Coordinate
wrong Release Version
wrong Artifact ID
wrong Artifact SHA-256
wrong installation backend id
```

If the shared installation transaction fails, its normal M0 cleanup and inventory-coherence behavior applies.

If installation succeeds but the subsequent lock re-check does not become `MATCH`, the newly installed instance is removed as a failed install-from-lock operation.

## Trust boundary

These questions remain separate:

```text
Are source bytes internally valid?
Do the resolved bytes satisfy this Project Lock entry?
Does the release satisfy the selected acceptance policy?
```

Project Lock exact identity is not a trust verdict.

## Source boundary

The current proof uses explicit local source material.

The Project Lock itself remains locator-free. It does not gain local paths, GitHub URLs or registry URLs.

A future remote Release Source can replace the explicit source step as long as it produces the same `ResolvedAdapterRelease` handoff and the same exact lock checks run before installation.

## Deliberately not included

```text
remote Release Source
public registry discovery
project-wide reconcile
batch transaction semantics
automatic removal/update
backend-resolution material verification
multi-platform lock selection
Studio lifecycle UX
```
