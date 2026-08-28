# Security Policy

## Supported versions

OrbitFabric has a stable v1 Mission Data Contract baseline.

Security fixes are considered for:

```text
the latest public OrbitFabric Core release
the current main branch
```

Older releases may remain available for reproducibility and historical reference, but they are not maintained as security-supported baselines unless explicitly stated otherwise.

The current Core version is:

```text
v1.2.0 - Core Integration Input Consolidation
```

## Reporting a vulnerability

Do not report suspected security vulnerabilities through public issues, discussions or pull requests.

Use GitHub private vulnerability reporting when available, or contact the maintainers through a private channel.

A useful report should describe:

- the affected OrbitFabric version or commit;
- the affected component or workflow;
- the observed behavior;
- the security impact;
- reproducible steps using synthetic or otherwise safe data;
- any known mitigation.

Do not include proprietary mission data, private spacecraft information, operational logs, credentials, tokens, export-controlled material, NDA-protected details or other confidential information in a vulnerability report.

## Security scope

OrbitFabric is a Mission Data Contract framework and engineering toolchain.

Relevant security reports may include issues involving:

- Mission Model and scenario parsing;
- unsafe file handling or path handling;
- generated artifact handling;
- CLI behavior with security impact;
- dependency handling;
- repository and CI workflows;
- documentation behavior that could create a material security misunderstanding;
- Integration Input Set integrity or provenance handling;
- external adapter execution boundaries documented by OrbitFabric when the issue concerns the generic contract or invocation boundary.

OrbitFabric Core does not dynamically load or execute ecosystem-specific adapters in-process.

## Operational boundary

OrbitFabric is not flight-ready onboard software, a ground segment, command uplink service, authentication system, authorization service, cryptographic key manager or operational spacecraft control system.

Generated runtime-facing bindings are contract artifacts, not flight software. Generated ground-facing artifacts are integration artifacts, not a ground segment.

A security property demonstrated by the OrbitFabric host-side toolchain must not be interpreted as qualification of an operational spacecraft or ground system.

## Clean-room and sensitive information

Security reporting does not relax the OrbitFabric clean-room policy.

Do not use a public or private vulnerability report as a channel for sharing material that you are not authorized to disclose.

See [Clean-Room Policy](docs/CLEAN_ROOM_POLICY.md).
