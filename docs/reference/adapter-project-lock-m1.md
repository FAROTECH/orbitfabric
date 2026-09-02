# Adapter Project Lock M1

Status: **candidate Core product surface**  
Contract status: **Adapter Project Lock 0.1-candidate**

## Purpose

Adapter Manager M0 answers:

```text
What adapters are actually installed on this machine?
```

Adapter Project Lock M1 adds the project-side question:

```text
What exact adapter state does this project require?
```

The two states remain separate:

```text
Adapter Project Lock
    project-scoped desired state

Installed Adapter Inventory
    user-scoped actual state
```

## Contract

Schema:

```text
src/orbitfabric/contracts/adapter_management/
    adapter-project-lock-0.1-candidate.schema.json
```

Candidate identity:

```text
kind         orbitfabric.adapter_project_lock
lock_version 0.1-candidate
```

Example:

```json
{
  "kind": "orbitfabric.adapter_project_lock",
  "lock_version": "0.1-candidate",
  "adapters": [
    {
      "source_coordinate": {
        "authority": "registry.example",
        "publisher": "example",
        "name": "adapter"
      },
      "release_version": "1.2.3",
      "release_descriptor": {
        "sha256": "<64 lowercase hex>"
      },
      "artifact": {
        "id": "python-wheel",
        "sha256": "<64 lowercase hex>"
      },
      "installation_backend": {
        "id": "python-wheel-managed-env"
      }
    }
  ]
}
```

Optional backend-owned exact resolution material may be bound with:

```json
{
  "backend_resolution": {
    "kind": "pep751-pylock",
    "reference": "pylock.adapter.toml",
    "sha256": "<64 lowercase hex>"
  }
}
```

The generic lock does not interpret the backend dependency graph. The first M1
`lock check` validates this optional binding structurally but does not yet verify
or compare the referenced backend-resolution material against installed state.
That verification belongs to the later backend/project-install reproducibility
lane.

## Exact identity

One complete Adapter Source Coordinate may appear at most once in one lock.

An installed record matches a lock entry only when all of these agree:

```text
source_coordinate
release_version
release_descriptor_sha256
artifact_id
artifact_sha256
backend_id
```

This means that equal package versions with different Release Descriptor or artifact bytes are not exact matches.

## Comparison states

For each locked adapter Core reports:

```text
MATCH
    at least one exact installed record exists

MISSING
    no installed record has the same Source Coordinate

MISMATCH
    the Source Coordinate exists locally, but no record matches the full exact identity
```

Extra installed releases do not make a project fail when an exact match is present.

Multiple exact installed instances still produce `MATCH`. Selecting one exact local instance for project execution is a later boundary.

Overall project state:

```text
MATCH
    every lock entry MATCH

NOT_SATISFIED
    at least one lock entry MISSING or MISMATCH
```

## CLI

Validate a lock without consulting installed state:

```text
orbitfabric adapter lock validate PATH
orbitfabric adapter lock validate PATH --json
```

Compare the lock with the current user-scoped Installed Adapter Inventory:

```text
orbitfabric adapter lock check PATH
orbitfabric adapter lock check PATH --json
```

`lock check` exits non-zero when the project state is `NOT_SATISFIED`.

The first M1 lane requires an explicit lock path. No default project filesystem location is frozen by this revision.

## Portability boundary

The project lock deliberately does not contain:

```text
local instance_id
install_root
manifest_path
absolute execution endpoint
Core state-root path
mutable artifact URL
machine-local artifact path
```

Those values belong to local lifecycle state or transport resolution, not project exact identity.

## Install-from-lock

The M1 comparison slice does not install missing adapters automatically.

The future flow is intentionally:

```text
Adapter Project Lock
    exact required identity
        +
Release Source
    exact descriptor/artifact resolution
        |
        v
verify resolved identity equals lock
        |
        v
Adapter Manager installation backend
```

This keeps project reproducibility independent from the choice of GitHub Releases, registry, mirror, cache or explicit local source.

## Not included in this M1 slice

```text
default lock filesystem location
lock authoring/update workflow
install from lock
backend-resolution material verification
remote registry/source discovery
project execution selection by lock
multi-platform lock policy
Studio lifecycle UX
```
