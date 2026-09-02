# Adapter Manager M0

Status: **candidate Core product surface**  
Contract status: **Adapter Release Descriptor 0.1-candidate**

## Purpose

Adapter Manager provides the first Core-owned lifecycle boundary for installing,
inspecting, verifying, executing and removing OrbitFabric adapters.

It is intentionally separate from Mission Model semantics.

```text
Mission Model
    owns mission intent and contract data

Adapter Manager
    owns local adapter lifecycle state
```

## M0 lifecycle

```text
Adapter Release Descriptor + exact artifact
        |
        v
Explicit Release Source
        |
        v
artifact integrity + acceptance
        |
        v
Installation Backend
        |
        v
Installed Adapter Record
        |
        v
verify / execute / remove
```

The first supported backend is:

```text
Python wheel
    -> dedicated managed Python environment
    -> installed Integration Package Manifest
    -> absolute environment-local endpoint
```

Python packaging mechanics are not generic OrbitFabric contracts.

## CLI

M0 exposes:

```text
orbitfabric adapter install RELEASE_DESCRIPTOR --artifact ARTIFACT [--artifact-id ID]
orbitfabric adapter list [--json]
orbitfabric adapter inspect INSTANCE_ID [--json]
orbitfabric adapter verify INSTANCE_ID [--json]
orbitfabric adapter execute INSTANCE_ID ...
orbitfabric adapter remove INSTANCE_ID [--json]
```

The exact CLI remains a candidate product surface while the M0 lane is being
stabilized.

### Install

The explicit-source lane consumes exact local inputs:

```text
Adapter Release Descriptor
exact adapter artifact
```

The artifact SHA-256 is always verified against the descriptor.

An optional expected descriptor SHA-256 may be supplied to convert descriptor
integrity from unknown source evidence to an explicit exact digest check.

The M0 explicit-source acceptance policy is a development policy. Missing
publisher, provenance, immutability or attestation evidence remains visible as
unknown/warning state and is not converted into official trust.

### List and inspect

`list` and `inspect` expose supported Core lifecycle information. Their output is
not the raw inventory persistence contract.

The raw inventory file, local instance-id encoding, managed-environment layout
and backend receipt format are implementation-private.

### Verify

Current verification is derived rather than persisted as one `healthy` boolean.

M0 verifies at least:

```text
installed Release Descriptor integrity
installed Integration Package Manifest integrity
Integration Package conformance
absolute execution binding readiness
backend materialization presence
```

### Execute

Execution reuses the promoted integration execution lane:

```text
Integration Package Manifest 0.2-candidate
orbitfabric.adapter_cli.v1
Integration Result 0.2-candidate
```

For an operation with no additional input:

```text
orbitfabric adapter execute INSTANCE_ID \
  --operation project \
  --input-set-manifest PATH \
  --profile PATH \
  --output-dir PATH
```

For the first required file-backed role:

```text
orbitfabric adapter execute INSTANCE_ID \
  --operation verification_projection \
  --input-set-manifest PATH \
  --profile PATH \
  --operation-input scenario=PATH \
  --output-dir PATH
```

Core validates operation requirements before invoking the installed endpoint.
The adapter-produced `integration_result.json` is then validated against the
installed Integration Package Manifest.

### Remove

Backend-owned materialization is removed before the Installed Adapter Record is
deleted. If backend removal fails, Core retains the record rather than losing
lifecycle ownership evidence.

## Adapter Release Descriptor 0.1-candidate

Schema:

```text
src/orbitfabric/contracts/adapter_management/
    adapter-release-descriptor-0.1-candidate.schema.json
```

Conceptual shape:

```json
{
  "kind": "orbitfabric.adapter_release",
  "descriptor_version": "0.1-candidate",
  "source_coordinate": {
    "authority": "registry.example",
    "publisher": "example",
    "name": "adapter"
  },
  "release_version": "1.2.3",
  "source_provenance": {
    "commit": "..."
  },
  "artifacts": [
    {
      "id": "python-wheel",
      "artifact_type": "python-wheel",
      "filename": "example_adapter-1.2.3-py3-none-any.whl",
      "sha256": "...",
      "size": 1234,
      "selectors": {
        "python": ">=3.11"
      }
    }
  ],
  "integration_package": {
    "sha256": "..."
  }
}
```

The Release Descriptor owns release/distribution identity and exact artifact
bindings. It does not own adapter operations, Profile schemas or execution
protocol semantics.

Artifact IDs are release-local and must be unique. SHA-256 is the initial digest
baseline.

Artifact transport locators are intentionally not release identity and need not
be embedded in this M0 explicit-source descriptor lane.

## Installed state

The default inventory is user-scoped Core-owned actual state.

The state root follows platform-appropriate user state conventions and can be
overridden for controlled environments with:

```text
ORBITFABRIC_STATE_DIR
```

This environment variable is an implementation control, not part of the public
release contract.

No global `active`, `current` or `default` adapter version exists in M0.
Selection is through an exact installed instance reference. A future Project
Lock will provide project-scoped desired resolution.

## Runtime dependencies and backend closure

Adapter artifact identity and Python environment identity are distinct:

```text
Adapter Artifact Digest
    != Python Backend Dependency Closure
```

An adapter must declare runtime dependencies required by the capabilities it
executes. The Python backend materializes those dependencies using normal Python
package metadata and pip behavior.

A pre-materialized wheelhouse can be supplied through normal pip configuration,
for example:

```text
PIP_NO_INDEX=1
PIP_FIND_LINKS=<wheelhouse>
```

This was used to validate the OpenOBSW/OpenSVF Scenario path with an isolated
managed environment.

Adapter Manager does not infer missing adapter dependencies from the host Core
process and does not silently inject them.

Exact backend dependency locking remains a later reproducibility lane.

## Not included in M0

```text
public registry discovery
remote release selection
Adapter Project Lock IO
automatic update
publisher namespace administration
official/community marketplace policy
non-Python installation backends
Studio lifecycle UX
```

These can extend the source, lock, trust and backend boundaries without changing
the promoted `orbitfabric.adapter_cli.v1` execution protocol.
