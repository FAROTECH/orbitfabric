# ADR-0017: Adapter Manager M0 Lifecycle Boundary

Status: Accepted  
Date: 2026-09-02

## Context

OrbitFabric already owns the generic Integration Package, Adapter Execution and
Integration Result contracts, but external adapters were still installed and
invoked through repository-specific development setup.

Cross-downstream architecture work established a separation between adapter
release identity, local installed state, project-selected desired state and the
existing adapter execution plane. Concrete Python backend proofs also showed
that exact adapter artifact bytes and backend dependency closure are distinct
provenance layers.

A Core-owned lifecycle capability is needed before Studio, official adapter
packaging or remote registry integration can rely on one installation authority.

## Decision

Introduce the first Core-owned Adapter Manager lifecycle lane under:

```text
orbitfabric adapter ...
```

M0 provides:

```text
install
list
inspect
verify
execute
remove
```

Adapter Manager is a bounded Core subsystem and is not Mission Model semantics.
Installed adapter state does not enter Mission Model YAML, Mission Snapshot,
Scenario models or the Core Integration Input Set.

The first source lane consumes an explicit exact Adapter Release Descriptor and
one exact local artifact. The first installation backend supports Python wheels
through a dedicated managed Python environment.

The lifecycle preserves these boundaries:

```text
Release Source / Resolver
    != Installation Backend

Installed Adapter Inventory
    != Adapter Project Lock

Adapter Release Descriptor
    != Integration Package Manifest

Adapter Manager lifecycle
    != adapter execution semantics
```

The default installed inventory is user-scoped Core-owned actual state. Its raw
persistence format, state path layout, local instance identifier and backend
receipt representation remain implementation-private.

No machine-global active/default adapter release is introduced in M0.

## Public candidate contract

M0 introduces one new external candidate contract:

```text
Adapter Release Descriptor 0.1-candidate
```

Core owns its JSON Schema and conformance semantics. The descriptor retains
release/distribution facts such as Source Coordinate, exact release version,
artifact membership, artifact SHA-256 identity and the exact expected
Integration Package Manifest digest.

The descriptor does not duplicate capabilities, operations, operation input
requirements, Profile schemas or execution protocol. Those remain owned by the
Integration Package Manifest.

The raw Installed Adapter Inventory is not a public contract.

Adapter Project Lock remains a later lane and is not introduced by M0.

## Execution

Adapter execution reuses the already promoted lane unchanged:

```text
Integration Package Manifest 0.2-candidate
orbitfabric.adapter_cli.v1
Integration Result 0.2-candidate
```

Before execution, Core verifies current installed state, validates the selected
operation and required operation-input bindings against the installed manifest,
invokes the recorded absolute environment-local endpoint, and validates the
result against the same manifest.

M0 does not introduce a second adapter runtime protocol.

## Transaction rules

Install publishes authoritative inventory state last:

```text
resolve exact release
    -> verify artifact
    -> evaluate acceptance
    -> materialize backend state
    -> verify installed descriptor and endpoint
    -> publish Installed Adapter Record LAST
```

Removal deletes authoritative inventory state last:

```text
load Installed Adapter Record
    -> remove backend-owned materialization
    -> verify removal
    -> remove Installed Adapter Record LAST
```

## Python backend boundary

Python wheel, pip, venv and Python dependency solving remain backend-specific
implementation mechanics.

An adapter package owns declaration of runtime dependencies required by the
capabilities it exposes. The installation backend owns materialization of those
dependencies. Adapter Manager does not silently inject undeclared packages into
an adapter environment.

Real OpenOBSW/OpenSVF acceptance testing demonstrated this boundary: isolation
exposed an undeclared Core runtime dependency used for Scenario validation, and
the operation succeeded once the temporary proof package declared Core and the
backend consumed a complete local wheel closure.

This does not decide the final production dependency constraint for that
adapter, nor does it require every adapter to depend on the OrbitFabric package.

## Acceptance evidence

M0 was validated against two existing adapters:

```text
F Prime
    zero-input project operation
    install -> verify -> execute -> remove       PASS

OpenOBSW/OpenSVF
    Scenario-required verification_projection
    install -> verify -> execute -> remove       PASS
```

The OpenOBSW control also retained exact Scenario provenance through the
promoted operation-input v1 Result boundary.

## Consequences

- Core becomes the single generic adapter lifecycle authority.
- Studio can later consume supported Core lifecycle surfaces instead of owning
  separate installed-adapter state.
- Exact adapter release identity remains separate from backend dependency
  closure and local environment identity.
- Managed-environment isolation becomes useful verification evidence because it
  exposes undeclared runtime dependencies.
- Remote registry discovery, project lock IO, automatic updates, publisher
  administration and Studio lifecycle UX remain outside M0.
- The Adapter Release Descriptor remains candidate and independently versioned.
- Existing Mission Model and promoted adapter execution contracts are unchanged.
