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
v1.3.0 - Adapter Management Foundation
```

The v1.3 Adapter Management contracts and lifecycle are candidate product surfaces. Their candidate status does not remove them from security review when they are used.

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
- external adapter execution boundaries documented by OrbitFabric when the issue concerns the generic contract or invocation boundary;
- Adapter Release Descriptor parsing and integrity validation;
- Adapter Project Lock parsing, exact-identity checks or desired/actual-state comparison;
- artifact digest/size verification before adapter installation;
- managed adapter environment creation and file ownership/path handling;
- installed adapter manifest discovery and conformance checks;
- installed execution binding and verification;
- Adapter Catalog parsing, binding validation and exact-selection ambiguity handling;
- `ResolvedAdapterRelease` handoff semantics between an external Release Source and the Core lifecycle.

OrbitFabric Core does not import ecosystem-specific adapter implementations into the Core process. Adapter Manager may execute an installed external adapter through the documented execution contract and an environment-local entrypoint.

Provider-specific acquisition, provider authentication and provider APIs remain outside Core. A vulnerability in the separate GitHub Release Source or another future Release Source should be reported against the affected provider product unless the issue is in the generic Core handoff or lifecycle contract.

## Adapter supply-chain boundary

OrbitFabric v1.3 verifies exact release and artifact identity where the candidate Adapter Management contracts define it.

Core can verify facts such as:

```text
Release Descriptor SHA-256
artifact id
artifact size and SHA-256
Project Lock exact identity
installed manifest integrity/conformance
installed execution binding
backend materialization
```

Those checks must not be interpreted as stronger trust claims than the available evidence supports.

In particular, digest verification alone does not prove:

```text
publisher identity
publisher authorization
source-build provenance
signature/attestation validity
absence of malicious behavior in an adapter
trustworthiness of a provider account
```

Provider facts and Core trust/acceptance evidence remain distinct. Unknown trust dimensions must not be silently promoted to PASS.

Project Lock records exact desired identity and must not absorb mutable provider URLs, machine-local installation paths, local instance ids or provider credentials.

## Operational boundary

OrbitFabric is not flight-ready onboard software, a ground segment, command uplink service, authentication system, authorization service, cryptographic key manager or operational spacecraft control system.

Generated runtime-facing bindings are contract artifacts, not flight software. Generated ground-facing artifacts are integration artifacts, not a ground segment.

Installed external adapters are engineering integration tooling. Their successful Core verification does not qualify their generated artifacts, downstream runtime behavior or third-party code for operational spacecraft use.

A security property demonstrated by the OrbitFabric host-side toolchain must not be interpreted as qualification of an operational spacecraft or ground system.

## Clean-room and sensitive information

Security reporting does not relax the OrbitFabric clean-room policy.

Do not use a public or private vulnerability report as a channel for sharing material that you are not authorized to disclose.

See [Clean-Room Policy](docs/CLEAN_ROOM_POLICY.md).
