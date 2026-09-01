# Integration Contract Compatibility Matrix

Status: Candidate extension contract

## Supported package-level lanes

| Manifest | Protocol | Result | Status |
|---|---|---|---|
| `0.1-candidate` | `orbitfabric.adapter_cli.v0` | `0.1-candidate` | frozen supported lane |
| `0.2-candidate` | `orbitfabric.adapter_cli.v1` | `0.2-candidate` | operation-input lane |

Only coherent rows are supported.

## Incompatible combinations

```text
0.1 Manifest + v1 protocol
0.2 Manifest + v0 protocol
v0 protocol + 0.2 Result
v1 protocol + 0.1 Result
one package advertising both protocols
per-operation protocol selection
runtime protocol negotiation
```

## Initial v1 scope

```text
fixed common context: IISS + Projection Profile
additional roles per operation: zero or one
declared role cardinality: exactly one
transport: local file path through direct argv
defined role: scenario
```

Optional, repeated, multi-role, remote, streamed, inline, and other non-file
resources are outside this revision.

## v0 normalization

A dual-lane consumer may normalize v0 internally as having no additional
requirements or provenance. This knowledge comes from the v0 contract. It
must not rewrite v0 JSON or infer semantics from an unknown manifest version.

