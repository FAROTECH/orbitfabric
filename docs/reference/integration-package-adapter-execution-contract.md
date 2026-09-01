# Integration Package Manifest and Adapter Execution Contract

Status: Candidate extension contract, design-frozen and reference-proven  
Contract version: `0.1-candidate`  
Scope: Static Integration Package metadata, compatibility discovery, Profile-schema publication and out-of-process adapter invocation  
Parent architecture issue: #227  
Design issue: #235  
Depends on: #228, #231, #233, ADR-0015

> A subsequent operation-input lane is defined by [Integration Operation-Input Contract v1](integration-contract-v1.md) and the [compatibility matrix](integration-contract-compatibility-matrix.md). This document remains the frozen v0 contract.

## 1. Purpose

This contract defines the generic package and execution boundary used to make an OrbitFabric ecosystem integration inspectable, compatibility-checkable and externally executable without importing third-party adapter code into Core.

The contract completes this chain:

```text
OrbitFabric Core
    -> coherent Core Integration Input Set

Projection Profile
    -> authored target-specific projection intent

Integration Package
    -> static manifest
    -> local Profile schema resources
    -> external adapter executable

orbitfabric.adapter_cli.v0
    -> out-of-process invocation

Integration Result
    -> machine-readable operation outcome
    -> native target artifacts
```

It answers:

```text
How is an Integration Package inspected before execution?
How does it declare identity, compatibility, capabilities and operations?
How does it publish its target-specific Profile schema?
How is an adapter invoked without Core importing third-party code?
How do CLI, CI and Studio consume the same package boundary?
```

The generic manifest and `orbitfabric.adapter_cli.v0` execution boundary are design-frozen and reference-proven. The contract remains `0.1-candidate` and extension-owned; v1.2.0 stabilizes the Core input boundary, not the external package/execution contract.

## 2. Ownership boundary

The Integration Package is ecosystem-integration-owned.

OrbitFabric governance defines the generic manifest and execution protocol, but the package remains external to Core and is never a Core Mission Data Contract authority.

Ownership is:

```text
OrbitFabric Core
    Mission Model semantics
    coherent Core Integration Input Set

Projection Profile
    authored target-specific projection intent

Integration Package / Adapter
    package metadata
    compatibility declarations
    target Profile schema
    target validation and projection logic
    external execution

Integration Result
    extension-owned machine-readable operation result

Studio / CLI / CI
    discovery, preflight, orchestration and presentation
```

These concepts are distinct:

```text
Projection Profile
!= Integration Package / Adapter
!= Studio Integration Plugin
```

A Studio Integration Plugin may enrich UX around an Integration Package. It must not become a second implementation of the adapter.

## 3. ADR-0015 and execution boundary

ADR-0015 established extensibility without third-party execution inside the stable Core boundary.

Therefore v0 requires:

```text
Core does not import adapter implementation modules
Core does not dynamically load adapter packages in-process
Core does not discover arbitrary executable plugins and run them automatically
```

The production execution boundary is out-of-process:

```text
Core emits versioned surfaces
        -> external adapter process consumes them
        -> external process writes Integration Result + native artifacts
```

The protocol is implementation-language neutral.

## 4. Static package manifest

Every v0 Integration Package exposes a static UTF-8 JSON manifest conventionally named:

```text
integration_package.json
```

The manifest must be inspectable without executing target-specific code.

It contains package/integration metadata only. It must not contain:

```text
Mission Model semantics
Mission instance values
Projection Profile instance state
runtime telemetry
verification evidence
private Studio state
```

No manifest self-digest is defined in v0.

## 5. Generic manifest envelope

The design-frozen candidate envelope is conceptually:

```json
{
  "kind": "orbitfabric.integration_package",
  "manifest_version": "0.1-candidate",
  "integration": {
    "id": "orbitfabric-openobsw-opensvf"
  },
  "adapter": {
    "id": "orbitfabric-openobsw-opensvf",
    "version": "0.1.0"
  },
  "core_input_compatibility": {
    "input_set_versions": ["0.1-candidate"],
    "surfaces": [
      {
        "role": "mission_snapshot",
        "kind": "orbitfabric.mission_snapshot",
        "format_versions": ["0.1-candidate"]
      }
    ],
    "relationship_families": []
  },
  "profile_compatibility": {
    "profile_versions": ["0.1-candidate"]
  },
  "result_compatibility": {
    "result_versions": ["0.1-candidate"],
    "default_result_version": "0.1-candidate"
  },
  "capabilities": [
    "profile_validation",
    "projection",
    "artifact_generation",
    "traceability"
  ],
  "operations": [
    {
      "id": "project",
      "capabilities": [
        "profile_validation",
        "projection",
        "artifact_generation",
        "traceability"
      ]
    }
  ],
  "profile_schemas": [
    {
      "schema_version": "0.1-candidate",
      "format": "json-schema-2020-12",
      "path": "schemas/profile-0.1.schema.json",
      "sha256": "..."
    }
  ],
  "execution": {
    "protocol": "orbitfabric.adapter_cli.v0",
    "argv_prefix": ["orbitfabric-openobsw-opensvf"]
  }
}
```

The OpenOBSW/OpenSVF identifiers are reference-integration values, not generic Core semantics.

Required top-level fields are:

```text
kind
manifest_version
integration
adapter
core_input_compatibility
profile_compatibility
result_compatibility
capabilities
operations
profile_schemas
execution
```

Missing required generic fields are incompatible. Unknown additive fields may be tolerated only according to the compatibility rules of the supported `manifest_version`.

## 6. Identity separation

The following identities have distinct meanings:

```text
manifest_version
    generic Integration Package Manifest compatibility

integration.id
    logical target-integration family

adapter.id
    concrete adapter/package implementation identity

adapter.version
    implementation/package release version

profile_schemas[].schema_version
    target-specific Profile schema version
```

`integration.id` and `adapter.id` are not required to be equal.

`adapter.version` is implementation provenance. It must not replace generic compatibility keys.

## 7. Explicit discovery and registration

The canonical v0 discovery mechanism is explicit: a caller is given or explicitly registers the path to `integration_package.json`.

A shell workflow, CI environment or Studio installation may maintain a local list of registered manifest paths. That list is local orchestration state, not Mission Model, Projection Profile or Integration Result state.

The v0 contract deliberately does not define a global filesystem scan directory, package marketplace or automatic installer.

Therefore:

```text
discovery != filesystem scanning
discovery != installation
discovery != execution
discovery != trust
```

A future convenience discovery convention may be added only as a separately reviewed convenience layer.

## 8. Manifest validation before use

A generic consumer validates at least:

```text
JSON syntax
kind
manifest_version
required generic fields
record uniqueness and invariants
path containment
capability/operation consistency
Profile schema declaration consistency
execution protocol support
```

A syntactically valid manifest is not automatically trusted for execution.

Unknown manifest versions must not be interpreted by guessing field meaning.

## 9. Core Input Set compatibility

`core_input_compatibility` declares the Core integration-input contracts understood by the package.

It contains:

```text
input_set_versions
surfaces
relationship_families
```

`input_set_versions` is a non-empty list of exact supported Core Integration Input Set versions. Version ranges are deliberately not part of v0.

Each surface declaration contains:

```text
role
kind
format_versions
```

`role` uses the Core Integration Input Contract vocabulary. `kind` identifies the Core-owned surface kind. `format_versions` lists exact understood versions for that role/kind.

`relationship_families` is the positive list of Relationship Manifest families whose semantics the integration explicitly understands where that distinction matters.

Unknown additive relationship families remain subject to the Core compatibility rules. Neither generic consumers nor adapters may invent semantics for an unknown family.

## 10. No raw-YAML compatibility fallback

If a package cannot consume a required Core Integration Input Set version or required surface, it must fail explicitly.

Forbidden behavior:

```text
Core surface incompatible
        -> read raw Mission Model YAML
        -> reconstruct OrbitFabric semantics privately
```

The adapter must not recover compatibility by becoming a second Mission Model interpreter.

## 11. Projection Profile compatibility

`profile_compatibility.profile_versions` declares exact supported generic Projection Profile envelope versions.

This is distinct from the integration-specific Profile schema version.

Compatibility therefore has two axes:

```text
generic Projection Profile envelope version
+
integration-specific schema version
```

Both must be supported before an operation that consumes the Profile can proceed validly.

## 12. Integration Result compatibility

`result_compatibility` declares:

```text
result_versions
default_result_version
```

`result_versions` is non-empty. `default_result_version` must be one member of it.

`orbitfabric.adapter_cli.v0` does not require a generic result-version negotiation flag. The package emits its declared default Result version.

A later protocol revision may add explicit negotiation only if demonstrated by real compatibility needs.

## 13. Capability model

Known candidate generic capability IDs include:

```text
profile_validation
projection
artifact_generation
traceability
runtime_discovery
runtime_orchestration
verification_execution
evidence_discovery
live_telemetry
commanding
```

The following separation is normative:

```text
Package capabilities
    what the installed package advertises before execution

Operation capabilities
    capabilities associated with one advertised operation

Integration Result capabilities
    capabilities actually exercised/materialized by one Result
```

Unknown additive capability IDs may be preserved or displayed but must not receive guessed behavior.

## 14. Operation declarations

`operations[]` advertises executable integration operations.

Representative record:

```json
{
  "id": "project",
  "capabilities": [
    "profile_validation",
    "projection",
    "artifact_generation",
    "traceability"
  ]
}
```

Rules:

```text
operation IDs are unique within the package
operation.id is integration-defined and opaque to generic consumers
operation capability IDs are unique
every operation capability also exists in package capabilities
```

Generic consumers must not parse an operation name such as `project` to infer hidden behavior.

## 15. Operation context

A `run` operation executes against an explicit integration context containing:

```text
Core Integration Input Set manifest
Projection Profile file
```

Static package inspection and Profile-schema lookup require no adapter execution.

If a future operation needs a materially different context, it requires reviewed protocol evolution rather than optional positional guessing.

## 16. Profile schema publication

The Integration Package publishes target-specific Projection Profile schema resources using JSON Schema Draft 2020-12.

A schema record contains:

```json
{
  "schema_version": "0.1-candidate",
  "format": "json-schema-2020-12",
  "path": "schemas/profile-0.1.schema.json",
  "sha256": "..."
}
```

Rules:

```text
schema_version is unique within the package
format = json-schema-2020-12 for v0
path is package-relative
sha256 fingerprints exact schema bytes
```

The lookup identity is:

```text
integration.id + integration.schema_version
```

CLI, CI and Studio should consume the same package-published schema rather than maintaining separate target-specific copies.

## 17. Local schema-resolution boundary

Profile validation must not require network access.

All schema resources required by the published Profile schema resolve locally inside the trusted package root.

The v0 contract performs no remote `$ref` retrieval.

Schema resolution rejects escape attempts such as:

```text
absolute path substitution
.. traversal
symlink/equivalent escape from package root
```

The primary schema SHA-256 must match before the resource is treated as the declared package schema.

Ordinary structural JSON Schema validation does not require invoking the adapter process. Integration-specific semantic validation remains adapter-owned and is reported through Integration Result diagnostics.

## 18. Execution protocol identifier

The design-frozen out-of-process protocol identifier is:

```text
orbitfabric.adapter_cli.v0
```

A consumer that does not support the declared protocol must not execute the package by guessing an invocation shape.

The protocol is language-neutral; an adapter may be implemented in Python, Rust, C++, Node.js or another language without changing the generic contract.

## 19. argv prefix, never a shell command

The manifest exposes an argument-vector prefix:

```json
{
  "execution": {
    "protocol": "orbitfabric.adapter_cli.v0",
    "argv_prefix": ["orbitfabric-openobsw-opensvf"]
  }
}
```

The caller constructs an argv vector and passes it directly to OS process creation.

The generic protocol does not provide:

```text
shell interpolation
shell pipelines
command substitution
shell environment expansion
quoting/re-parsing of a command string
```

The manifest does not grant permission to execute `argv_prefix[0]`.

## 20. Generic run invocation

The v0 invocation is:

```text
<argv_prefix...> run
    --operation <operation-id>
    --input-set-manifest <path/to/integration_input_manifest.json>
    --profile <path/to/projection-profile.yaml>
    --output-dir <directory>
```

The argument names and ordering above are part of `orbitfabric.adapter_cli.v0`.

Invariants:

```text
--operation
    exact advertised operation ID

--input-set-manifest
    explicit path to integration_input_manifest.json
    not merely a directory whose contents the adapter guesses

--profile
    explicit authored Projection Profile path

--output-dir
    explicit Result bundle root
```

No generic adapter RPC daemon is required by v0.

## 21. Input path semantics

Invocation paths are local process paths supplied by the caller. They are execution-location data, not portable semantic identity.

The adapter resolves Core surfaces only through the explicit Core Integration Input Manifest.

It must not discover alternate Core inputs by filename heuristic when the manifest is absent or incompatible.

It consumes exactly the Profile file supplied by `--profile` and must not silently substitute another Profile found in a workspace.

## 22. Output bundle boundary

All operation output is rooted in `--output-dir`.

When technically possible, the adapter writes:

```text
<output-dir>/integration_result.json
```

last, after finalizing declared artifact/evidence status.

The Integration Result is the semantic operation result. Generated artifact presence alone is not proof of a coherent operation.

Portable bundle artifacts/evidence must not be materialized outside the requested output root.

All bundled paths declared by the Integration Result resolve inside the Result bundle root.

Portable paths reject:

```text
absolute paths
.. traversal
normalization that escapes output root
symlink/equivalent escape from output root
```

Absolute host paths may exist as private execution details but must not replace portable relative Result paths.

## 23. stdout and stderr

`stdout` and `stderr` are operational/logging channels only.

Consumers must not reconstruct result state, mappings, coverage, artifact identity, staleness or evidence identity from console text.

Machine-readable semantics come from `integration_result.json` when available.

## 24. Process exit status

Exit zero requires:

```text
a valid integration_result.json exists
result = succeeded OR succeeded_with_warnings
```

Non-zero exit means invocation/operation failure.

A failed `integration_result.json` should exist when technically possible, but may be absent if failure occurred before a reliable Result could be built.

Callers must not derive semantic failure categories from arbitrary non-zero numbers. They inspect Integration Result diagnostics when a valid failed Result exists.

No generic non-zero exit taxonomy is frozen in v0.

Protocol violations include:

```text
exit 0 + no valid Integration Result
exit 0 + Result.result = failed
exit non-zero + Result.result = succeeded
exit non-zero + Result.result = succeeded_with_warnings
Result operation ID contradicts requested --operation
successful required artifact resolves outside output bundle root
```

A caller surfaces these as adapter/protocol violations rather than guessing which channel is authoritative.

## 25. Compatibility preflight

Before execution a generic caller can check:

```text
manifest kind/version supported
requested operation exists
operation capability declarations are consistent
Core Input Set version supported
required Core surface role/kind/format versions supported
Projection Profile generic version supported
Profile integration.id matches package integration.id
Profile integration.schema_version has a published schema
published Profile schema digest is valid
Integration Result default version supported
execution protocol supported
```

Target-specific semantic validation remains adapter-owned and may still fail during execution.

Preflight means only:

```text
generic contract appears consumable
```

not:

```text
target-specific operation is guaranteed to succeed
```

## 26. Trust boundary

These distinctions are normative:

```text
manifest syntax validity != package trust
manifest registration != execution authorization
discovery != execution
Studio Integration Plugin trust != adapter executable trust
schema validity != executable trust
```

A caller decides whether a registered Integration Package is trusted for execution.

The v0 generic contract does not define code signing, publisher PKI, marketplace review, full sandboxing or OS installation policy.

Discovering or parsing a manifest never grants execution authority.

## 27. Studio relationship

Studio may consume the same generic package boundary as CLI and CI:

```text
integration_package.json
    -> package identity/version
    -> compatibility
    -> advertised capabilities
    -> advertised operations

package Profile JSON Schema
    -> Profile rendering/edit assistance
    -> structural validation

orbitfabric.adapter_cli.v0
    -> external adapter invocation

integration_result.json
    -> status and provenance
    -> artifacts
    -> traceability
    -> coverage
    -> evidence
```

Generic Studio code must not:

```text
import adapter implementation modules
hard-code ecosystem Profile schemas
reimplement projection logic
infer capabilities from generated filenames
construct a private Studio-only adapter protocol
execute a package merely because its manifest was discovered
```

A Studio Integration Plugin may add richer views/actions but must orchestrate the same external package boundary.

## 28. OpenOBSW/OpenSVF reference package

The OpenOBSW/OpenSVF PoC supplied the first concrete forcing function for this contract. The extracted reference Integration Package has now exercised the design-frozen manifest, local Profile schema and `orbitfabric.adapter_cli.v0` execution boundary against a real Core Integration Input Set, with independent Studio acceptance.

The current reference package advertises the static `project` operation and the capabilities it actually implements:

```text
profile_validation
projection
artifact_generation
traceability
```

Additional capabilities such as:

```text
runtime_discovery
runtime_orchestration
verification_execution
evidence_discovery
live_telemetry
commanding
```

may be advertised only when the reference adapter truly implements them.

PoC PR #30 completed the ownership review for the reference integration. In particular:

```text
OpenSVF remains owner of SRDB -> XTCE generation
YamcsBridge remains the YAMCS boundary
runtime/verification evidence remains owned by OpenSVF/external systems
reference integration must not implement a second verification engine
PoC monkey patches/private injection are not production public APIs
```

Those reference-specific decisions do not move OpenOBSW/OpenSVF/YAMCS semantics into this generic manifest or protocol.

## 29. Regression protection

Regression protection should cover at least:

```text
valid minimal package manifest
unknown manifest version rejection
missing required manifest field
integration.id distinct from adapter.id
exact-version compatibility success/failure
required Core surface mismatch
unknown relationship-family non-guessing behavior
Profile generic-version mismatch
Profile schema lookup by integration.id + schema_version
Profile schema digest mismatch
schema path traversal rejection
remote $ref rejection
operation ID uniqueness
operation capability subset invariant
unknown additive capability preservation
explicit manifest registration
no filesystem auto-scan dependency
argv prefix passed without shell evaluation
unsupported execution protocol rejection
correct generic run argv construction
input-set manifest path used directly
Profile path used directly
output bundle root containment
exit-0 successful Result invariant
non-zero failed Result behavior
protocol contradiction detection
manifest discovery without execution
registration without execution authorization
```

Target-specific fixtures belong to the reference Integration Package rather than Core generic fixtures.

## 30. Design-freeze position

The following decisions are frozen for `0.1-candidate`:

```text
static integration_package.json
manifest is integration-owned, not Core semantic state
explicit manifest-path discovery/registration
no v0 OS-specific scan directory or marketplace
manifest inspection requires no adapter execution
separate integration.id and adapter.id/version
exact supported-version lists; no range syntax in v0
Core Input Set and required-surface compatibility declarations
positive Relationship Manifest family declarations
no raw-YAML semantic fallback
separate generic Profile and integration-schema compatibility
static local JSON Schema Draft 2020-12 publication
schema exact SHA-256
local contained schema refs; no remote retrieval in v0
Package vs Operation vs Result capability separation
opaque integration-defined operation IDs
operation capabilities subset of package capabilities
out-of-process language-neutral execution
execution protocol = orbitfabric.adapter_cli.v0
argv prefix, never shell command string
generic run command with explicit operation/input-manifest/Profile/output-root
no generic adapter RPC daemon in v0
Integration Result is semantic result; stdout/stderr are operational only
exit 0 requires successful valid Result
non-zero means failure; failed Result best-effort
no detailed generic non-zero exit taxonomy
output bundle containment
manifest discovery != trust or execution authorization
Studio, CLI and CI share the same package/execution boundary
```

## 31. Non-goals

The v0 Integration Package / Adapter Execution Contract does not define:

```text
package marketplace
package download/update service
OS-specific installer
package-manager integration
code-signing infrastructure
publisher PKI
full process sandbox
container runtime requirement
adapter RPC daemon
streaming telemetry protocol
command authorization/security policy
Studio plugin lifecycle/UI contribution API
OpenOBSW/OpenSVF/YAMCS operation implementations
Mission Model semantics
Projection Profile instance contents
Integration Result record details defined by the Result contract
Core in-process third-party plugin loading/execution
```

## 32. Current maturity and final position

The generic packaging/execution boundary is design-frozen and reference-proven while remaining independently versioned:

```text
0.1-candidate
```

The production integration boundary is:

```text
OrbitFabric Core
    owns mission semantics
    and emits coherent versioned integration inputs

Projection Profile
    owns authored target-specific projection intent

Integration Package
    statically declares identity, compatibility,
    capabilities, operations and Profile schemas

External Integration Adapter
    executes out-of-process through orbitfabric.adapter_cli.v0
    and never requires Core to import third-party code

Integration Result
    records the machine-readable outcome
    and is the semantic operation result

Studio / CLI / CI
    inspect and invoke the same package boundary
    without reconstructing ecosystem semantics
```

This generic architecture gate has been exercised by the extracted OpenOBSW/OpenSVF reference Integration Package and the independent Studio acceptance path. Reference proof does not promote the package/execution contract to a stable Core Mission Data Contract surface.
