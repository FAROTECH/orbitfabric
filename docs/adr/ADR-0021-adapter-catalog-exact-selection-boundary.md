# ADR-0021 - Adapter Catalog Exact Selection Boundary

Status: **Accepted candidate Core architecture**  
Date: **2026-09-04**

## Context

OrbitFabric Core already owns the lower half of the adapter lifecycle:

```text
ResolvedAdapterRelease
    -> exact Adapter Project Lock verification
    -> locked Installation Backend
    -> AdapterManager.install_resolved(...)
    -> Installed Adapter State
    -> MATCH
```

The remaining acquisition question was how a consumer identifies one exact available adapter release before a provider-specific source acquires its bytes.

Architecture Lab investigation across the independently published OpenOBSW/OpenSVF, OpenC3 COSMOS and F Prime adapters demonstrated one common provider-neutral Catalog shape and exact selection rule.

The same investigation also demonstrated that provider repository/location semantics are acquisition configuration, not adapter release identity.

## Decision

Core owns a minimal provider-neutral Adapter Catalog model and exact release selector.

The Catalog model contains:

```text
AdapterCatalog
    kind
    catalog_version
    adapters[]
    source_bindings[]

CatalogAdapterRecord
    source_coordinate
    releases[]

CatalogReleaseRecord
    version
    release_descriptor_digest
    sources[]

CatalogReleaseSourceRef
    binding
    release_ref

CatalogSourceBinding
    id
    provider
    config
```

The Catalog binds one exact release to its expected Release Descriptor SHA-256 and one or more source-binding references.

It does not duplicate descriptor-owned artifact membership.

## Exact selection

The normative first selector is:

```text
Adapter Source Coordinate + exact Release Version
```

Selection uses exact string equality.

Required behavior:

```text
zero adapter matches    -> fail closed
zero release matches    -> fail closed
multiple matches        -> fail closed
```

No version normalization or ordering occurs.

Therefore:

```text
0.1.1 != v0.1.1
```

unless a future, separately defined version-selection layer explicitly says otherwise.

A convenience selector by logical `publisher/name` may be used only when exactly one Source Coordinate exists across all authorities. Multiple authorities make the request ambiguous and must fail closed.

## Source bindings

`CatalogSourceBinding.provider` identifies the provider implementation family.

`CatalogSourceBinding.config` is opaque to generic Core Catalog logic.

`CatalogReleaseSourceRef.release_ref` is also provider-owned opaque lookup material.

Core does not assume that a provider release reference is equal to the OrbitFabric Release Version.

For example, a GitHub provider may currently use:

```text
OrbitFabric Release Version: 0.1.1
provider release_ref:         v0.1.1
```

without making that convention generic Core semantics.

Multiple source bindings for the same exact Catalog release represent alternate acquisition paths or mirrors. They do not create a different OrbitFabric release identity.

## Provider neutrality

This ADR does not introduce provider/network implementation into Core.

Core does not own:

```text
GitHub REST calls
repository naming conventions
release URL construction
provider authentication credentials
provider retries or rate limits
asset download policy
PyPI/OCI/GitHub-specific source schemas
```

Provider-specific source code remains responsible for acquiring and verifying exact release material before returning the existing `ResolvedAdapterRelease` handoff defined by ADR-0020.

## Catalog data ownership

The Core package owns the Catalog model and selection semantics, not the maintained ecosystem Catalog contents.

Canonical adapter/release data may evolve independently of Core release cadence and therefore belongs in a separate maintained data product.

No registry server is required by this ADR.

A static version-controlled Catalog is sufficient for the first productized lifecycle.

## Trust separation

Catalog membership and exact byte resolution do not grant publisher trust or official status.

Provider-specific resolution may populate factual `ReleaseTrustEvidence` dimensions only when those dimensions were actually verified or observed.

Acceptance remains a separate policy operation.

In particular, this ADR does not imply:

```text
Catalog listed == trusted
repository owner == publisher identity
provider actor == authenticated publisher
immutable release == official release
```

## Project Lock compatibility

No Adapter Project Lock field changes.

Provider locators and Catalog source-binding configuration do not become Project Lock identity.

The existing exact Project Lock gates remain authoritative:

```text
Source Coordinate
Release Version
Release Descriptor SHA-256
Artifact ID
Artifact SHA-256
Installation Backend ID
```

## Compatibility

This is an additive Adapter Manager capability.

It does not change:

```text
Mission Model semantics
Adapter Release Descriptor 0.1-candidate
Adapter Project Lock 0.1-candidate
Installed Adapter State
Integration Package Manifest
adapter execution protocol
ResolvedAdapterRelease
existing explicit-source installation behavior
```

## Deferred

```text
latest/stable channels
SemVer ordering
version ranges
implicit upgrades
registry service topology
catalog distribution/signing framework
built-in GitHub source provider
universal source-provider protocol
publisher administration
marketplace UX
automatic adapter updates
```

Those require separate product evidence.
