# Adapter Catalog CLI

Status: **candidate Core product surface**  
Catalog format: **0.1-candidate**

## Purpose

OrbitFabric Core owns the provider-neutral Adapter Catalog model and exact release selection semantics.

The first Catalog CLI exposes those existing Core capabilities without adding remote acquisition or provider dispatch to Core.

The supported boundary is:

```text
local catalog.json
    -> Core AdapterCatalog validation
    -> Core exact selection
    -> inspect selected Source Coordinate, version, digest and source references
```

It is not:

```text
Catalog
    -> remote provider lookup
    -> artifact download
    -> installation
```

Provider-specific acquisition remains outside Core.

## Validate a local Catalog

```bash
orbitfabric adapter catalog validate path/to/catalog.json
```

Machine-readable output:

```bash
orbitfabric adapter catalog validate path/to/catalog.json --json
```

Validation uses the Core-owned `AdapterCatalog` model. It does not define a second CLI-specific schema.

## List exact releases

```bash
orbitfabric adapter catalog list path/to/catalog.json
```

Example output:

```text
github.com/FAROTECH:orbitfabric/openobsw-opensvf@0.1.0
github.com/FAROTECH:orbitfabric/openc3-cosmos@0.1.0
github.com/FAROTECH:orbitfabric/fprime@0.1.1
```

JSON output returns the corresponding Core Catalog adapter records:

```bash
orbitfabric adapter catalog list path/to/catalog.json --json
```

## Select one exact release

The first CLI requires the complete Adapter Source Coordinate and exact release version:

```bash
orbitfabric adapter catalog select \
  path/to/catalog.json \
  github.com/FAROTECH:orbitfabric/fprime \
  --version 0.1.1
```

The identity is deliberately explicit:

```text
AUTHORITY:PUBLISHER/NAME @ EXACT_VERSION
```

The selector uses exact string equality. For example:

```text
0.1.1 != v0.1.1
```

Unknown Source Coordinates and unknown exact versions fail closed.

Machine-readable selection:

```bash
orbitfabric adapter catalog select \
  path/to/catalog.json \
  github.com/FAROTECH:orbitfabric/fprime \
  --version 0.1.1 \
  --json
```

The JSON result is the Core `ExactCatalogReleaseSelection` model, including the exact Release Descriptor digest and resolved source-binding records.

## Boundary

This CLI deliberately does not perform:

```text
network access
GitHub API calls
provider package discovery
provider registration or dispatch
artifact download
installation
latest/stable/range selection
automatic upgrades
default remote Catalog discovery
```

Core therefore remains provider-neutral.

Provider/source products consume the Core exact selection and return `ResolvedAdapterRelease` to the existing Core lifecycle.

The generic handoff remains:

```text
local Catalog
    -> Core exact selection
    -> provider/source implementation outside Core
    -> ResolvedAdapterRelease
    -> Core Project Lock / installation lifecycle
```

## Catalog data ownership

The maintained ecosystem Catalog is not embedded into the Core package and is not coupled to the Core release cadence.

This CLI accepts an explicit local Catalog file. How that file is obtained, mirrored, cached or distributed remains outside this first Core CLI boundary.

## Unified install-from-Catalog command

A provider-neutral command that automatically maps Catalog provider bindings to installed provider implementations is intentionally not part of this surface.

Promoting such dispatch requires evidence from more than one materially different provider. Core must not hard-code GitHub-specific acquisition semantics merely to provide a shorter command.
