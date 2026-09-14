# ADR-0023: Core Interface Manifest

Status: Accepted

## Context

OrbitFabric product version is provenance, not a complete structured-interface compatibility identity. The public v1.3.0 release and later Core revisions can both report `1.3.0` while exposing different structured capabilities. Inferring support from semantic version, `--help`, guessed command names, repository co-location, or repository coordinates is not authoritative.

## Decision

Core exposes `orbitfabric export core-interface --json <path>`. It requires no Mission Model and emits the candidate `orbitfabric.core_interface` manifest.

The manifest declares Core-owned capability ids with their contract kinds and versions in capability-id order. Its `interface_sha256` is SHA-256 over RFC 8785/JCS canonical bytes for the manifest kind, interface version, and normalized capability array. Product version is present only as provenance and is excluded from the fingerprint.

Consumers compare required capabilities and versions. A fingerprint is a compact identity for a complete known declaration; it does not replace capability negotiation.

## Consequences

- Equivalent declarations have the same fingerprint regardless of implementation ordering.
- Any declared capability addition, removal, kind change, or version change changes the fingerprint.
- The identity contains no executable bytes, Git identity, repository owner/path, build host, timestamp, or environment-specific data.
- Malformed internal declarations fail closed.
- The candidate manifest does not stabilize every CLI payload or expand Adapter Lifecycle semantics.
- Studio consumption is outside this decision.
