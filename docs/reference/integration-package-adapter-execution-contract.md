# Integration Package Manifest and Adapter Execution Contract

Status: Architecture candidate — generic packaging/execution boundary design-frozen  
Contract version: `0.1-candidate`  
Scope: Static Integration Package metadata, compatibility discovery, Profile-schema publication, and out-of-process adapter invocation  
Parent architecture issue: #227  
Design issue: #235  
Depends on: #228, #231, #233, ADR-0015

---

## 1. Purpose

The Integration Package Manifest and Adapter Execution Contract defines the final generic boundary required to turn the Phase B integration contracts into an installable and externally executable integration package.

The preceding contracts answer:

```text
Core Integration Input Contract (#228)
    -> what exact Core-owned inputs an adapter consumes

Projection Profile Contract (#231)
    -> what authored ecosystem-specific projection intent looks like

Integration Result Contract (#233)
    -> what machine-readable result an adapter produces
```

This contract answers:

```text
How is an Integration Package inspected before execution?
How does it declare compatibility and capabilities?
How does it publish its target-specific Profile schema?
How is an adapter invoked without Core importing third-party code?
How can shell workflows, CI and Studio use the same boundary?
```

The intended chain is:

```text
OrbitFabric Core
    -> Core Integration Input Set

Projection Profile
    -> authored target-specific intent

Integration Package
    ├── integration_package.json
    ├── local Profile JSON Schema resources
    └── external adapter executable
            ↓
       orbitfabric.adapter_cli.v0
            ↓
       Integration Result
       + native target artifacts
```

---

## 2. Ownership boundary

The Integration Package is ecosystem-integration-owned.

OrbitFabric governance defines the generic manifest and execution protocol documented here, but the package remains external to Core and does not become a Core Mission Data Contract authority.

Ownership remains:

```text
OrbitFabric Core
    -> Mission Model semantics and Core Integration Input Set

Projection Profile
    -> authored ecosystem-specific projection intent

Integration Package / Adapter
    -> package metadata, compatibility declarations,
       target schema, projection logic and external execution

Integration Result
    -> extension-owned machine-readable operation result

Studio
    -> discovery/orchestration/visualization consumer
```

These concepts remain distinct:

```text
Projection Profile
!= Integration Package / Adapter
!= Studio Integration Plugin
```

A Studio plugin may enrich the user experience around an Integration Package, but it must not become a second implementation of the adapter.

---

## 3. ADR-0015 constraint

ADR-0015 established extensibility without third-party execution inside the stable Core boundary.

Therefore v0 requires:

```text
Core does not import adapter implementation modules
Core does not dynamically load adapter Python packages in-process
Core does not discover arbitrary executable plugins and run them automatically
```

The first production execution model is out-of-process:

```text
Core emits versioned surfaces
        ↓
external process consumes them
        ↓
external process writes Integration Result + native artifacts
```

The generic protocol is deliberately implementation-language neutral.

---

## 4. Static package manifest

Every v0 Integration Package exposes a static UTF-8 JSON manifest conventionally named:

```text
integration_package.json
```

The manifest must be inspectable without executing target-specific adapter code.

It contains package/integration metadata only.

It must not contain:

```text
Mission Model semantics
Mission instance values
Projection Profile instance state
runtime telemetry
verification evidence
private Studio state
```

No manifest self-digest is introduced in v0.

---

## 5. Generic manifest envelope

The design-frozen v0 candidate shape is conceptually:

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
    "input_set_versions": [
      "0.1-candidate"
    ],
    "surfaces": [
      {
        "role": "mission_snapshot",
        "kind": "orbitfabric.mission_snapshot",
        "format_versions": [
          "0.1-candidate"
        ]
      }
    ],
    "relationship_families": []
  },
  "profile_compatibility": {
    "profile_versions": [
      "0.1-candidate"
    ]
  },
  "result_compatibility": {
    "result_versions": [
      "0.1-candidate"
    ],
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
    "argv_prefix": [
      "orbitfabric-openobsw-opensvf"
    ]
  }
}
```

The OpenOBSW/OpenSVF identifiers above are illustrative reference-integration values, not generic Core semantics.

---

## 6. Required top-level fields

A v0 manifest requires:

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

Arrays remain present when empty unless the relevant record has a stronger non-empty invariant.

Unknown additive fields may be tolerated only according to the compatibility policy of the supported `manifest_version`.

Missing required generic fields are incompatible.

---

## 7. Identity separation

The following identifiers have distinct roles:

```text
manifest_version
    -> generic Integration Package Manifest compatibility

integration.id
    -> logical target-integration family

adapter.id
    -> concrete adapter/package implementation identity

adapter.version
    -> implementation/package release version

profile_schemas[].schema_version
    -> target-specific Profile schema version
```

`integration.id` and `adapter.id` are not required to be equal.

This permits, for example, multiple independently versioned adapter implementations of one logical integration family without changing Profile identity semantics.

`adapter.version` is support/provenance information and must not replace the generic compatibility keys.

---

## 8. Canonical discovery mechanism

The canonical v0 discovery mechanism is explicit.

A caller is given or explicitly registers a path to:

```text
integration_package.json
```

A shell workflow, CI environment or Studio installation may maintain a local list of registered manifest paths.

That list is local installation/orchestration state.

It is not:

```text
Mission Model state
Projection Profile state
Integration Result state
```

The v0 contract deliberately does not define an OS-specific global discovery directory.

Therefore:

```text
discovery != filesystem scanning
discovery != installation
discovery != execution
discovery != trust
```

A future convenience discovery convention may be added without changing the package manifest contract.

---

## 9. Manifest validation before use

A generic consumer must validate at least:

```text
JSON syntax
kind
manifest_version
required generic fields
record uniqueness/invariants
path containment rules
capability/operation consistency
Profile schema declaration consistency
execution protocol support
```

A syntactically valid manifest is not automatically trusted for execution.

Unknown manifest versions must not be interpreted by guessing field meaning.

---

## 10. Core Input Set compatibility declaration

`core_input_compatibility` declares the Core integration input contracts understood by the adapter.

It includes:

```text
input_set_versions
surfaces
relationship_families
```

### Input-set versions

`input_set_versions` is a non-empty list of exact supported Core Integration Input Set contract versions.

Version ranges are deliberately deferred in v0.

### Surface declarations

A surface record declares:

```text
role
kind
format_versions
```

`role` matches the Core Integration Input Contract role vocabulary.

`kind` identifies the expected Core-owned surface kind.

`format_versions` lists exact versions understood by the adapter for that role/kind.

A generic caller may use these declarations for compatibility preflight without reading target-specific adapter code.

### Relationship families

`relationship_families` is the positive list of Core Relationship Manifest families whose semantics the integration explicitly understands when that distinction is relevant.

Unknown additive relationship families remain governed by the Core Integration Input Contract compatibility rules.

A consumer or adapter must never invent semantics for an unknown relationship family.

---

## 11. No raw-YAML compatibility fallback

If the package cannot consume a required Core Integration Input Set version/surface, it must not recover by reparsing OrbitFabric Mission Model YAML.

Forbidden fallback:

```text
Core surface incompatible
        ↓
read raw Mission YAML
        ↓
reconstruct semantics privately
```

Required behavior is explicit incompatibility/failure through the external adapter boundary.

This preserves Core as the sole Mission Model semantic authority.

---

## 12. Projection Profile generic compatibility

`profile_compatibility.profile_versions` declares exact supported generic Projection Profile envelope versions from #231.

This is distinct from the integration-specific schema version.

Compatibility therefore has two separate axes:

```text
generic Projection Profile envelope version
+
integration-specific schema version
```

Both must be supported before an operation that consumes the Profile can proceed validly.

---

## 13. Integration Result compatibility

`result_compatibility` declares:

```text
result_versions
default_result_version
```

`result_versions` is a non-empty list of exact Integration Result Contract versions that the adapter can emit.

`default_result_version` must be one member of `result_versions`.

The v0 process protocol does not require a generic command-line result-version negotiation flag.

The package emits its declared default Result version for the generic v0 run protocol.

A future protocol revision may add explicit output-version negotiation if demonstrated by real compatibility needs.

---

## 14. Advertised package capabilities

`capabilities[]` declares the generic capabilities the installed package advertises before execution.

Known generic capability IDs align with #233 where applicable:

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

The separation is normative:

```text
Package capabilities
    -> what this installed package advertises before execution

Operation capabilities
    -> generic capabilities associated with one advertised operation

Integration Result capabilities
    -> capabilities actually exercised/materialized by one historical Result
```

Unknown additive capability IDs may be preserved/displayed but must not receive guessed behavior.

---

## 15. Operation declarations

`operations[]` advertises executable integration operations.

Candidate record:

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
operation IDs are unique within the package manifest
operation.id is integration-defined and opaque to generic consumers
operation.capabilities contains unique generic capability IDs
every operation capability is also present in package capabilities
```

Generic consumers must not parse operation names to infer behavior.

For example, the string `project` has no generic semantics by itself.

Consumers use declared capabilities and the execution protocol.

---

## 16. v0 operation context

The `run` operations covered by `orbitfabric.adapter_cli.v0` execute against an explicit integration context containing both:

```text
Core Integration Input Set manifest
Projection Profile file
```

Static package inspection and Profile-schema lookup do not require adapter execution.

If future integration operations need a materially different invocation context, they require a reviewed protocol evolution rather than optional positional guessing in v0.

---

## 17. Profile schema publication

Target-specific Projection Profile configuration is described by JSON Schema Draft 2020-12 as defined by #231.

The Integration Package publishes each supported schema statically in `profile_schemas[]`.

Record shape:

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
schema_version values are unique within the package
format = json-schema-2020-12 for v0
path is relative to the package manifest directory
sha256 fingerprints the exact schema bytes
```

Schema lookup key remains:

```text
integration.id + integration.schema_version
```

where the Profile's `integration.schema_version` selects the matching package-published schema record.

---

## 18. Local schema-resolution boundary

Profile validation must not require network access.

All schema resources required by the published Profile schema must resolve locally within the trusted package root.

The v0 contract does not perform remote `$ref` retrieval.

Schema resolution must reject escape attempts including:

```text
absolute path substitution
.. traversal
symlink/equivalent resolution that escapes the trusted package root
```

The exact SHA-256 of the primary schema resource is validated before it is treated as the declared package schema.

CLI, CI and Studio should consume the same package-published schema rather than maintaining separate target-specific copies.

---

## 19. No mandatory adapter process for schema validation

A separate adapter subprocess command for ordinary JSON Schema validation is not required in v0.

A generic consumer may validate the Profile directly against the statically published schema.

The adapter still owns integration-specific semantic validation that cannot be represented by JSON Schema.

Such validation occurs as part of the requested operation and is reported through Integration Result diagnostics.

This preserves:

```text
structural target schema validation
    -> shared static schema

integration semantic validation
    -> adapter operation
```

---

## 20. Execution protocol identifier

The design-frozen generic out-of-process protocol identifier is:

```text
orbitfabric.adapter_cli.v0
```

A consumer that does not support the declared execution protocol must not execute the package by guessing an invocation shape.

The protocol is language-neutral.

An adapter may be implemented in:

```text
Python
Rust
C++
Node.js
or another implementation language
```

without changing the generic boundary.

---

## 21. argv prefix, not shell command

The manifest exposes:

```json
{
  "execution": {
    "protocol": "orbitfabric.adapter_cli.v0",
    "argv_prefix": [
      "orbitfabric-openobsw-opensvf"
    ]
  }
}
```

`argv_prefix` is a non-empty array of process argument strings.

Generic execution is constructed as an argument vector and passed directly to OS process creation.

The protocol does not include:

```text
shell interpolation
shell pipelines
command substitution
environment-variable expansion by a shell
quoting/re-parsing of a command string
```

`argv_prefix[0]` is resolved by the invoking environment according to its explicitly trusted installation/path policy.

The manifest itself does not grant permission to execute that program.

---

## 22. Generic run invocation

The v0 run invocation is:

```text
<argv_prefix...> run
    --operation <operation-id>
    --input-set-manifest <path/to/integration_input_manifest.json>
    --profile <path/to/projection-profile.yaml>
    --output-dir <directory>
```

The argument names and ordering above are part of `orbitfabric.adapter_cli.v0`.

Important invariants:

```text
--operation
    -> exact advertised operation ID

--input-set-manifest
    -> path to integration_input_manifest.json,
       not merely a directory whose contents the adapter guesses

--profile
    -> explicit authored Projection Profile path

--output-dir
    -> explicit root for this operation's Result bundle
```

No generic adapter RPC daemon is required by v0.

---

## 23. Input path semantics

Invocation arguments are local process paths supplied by the caller.

They are execution-location data, not portable semantic identity.

The adapter resolves Core surfaces from the explicit Core Integration Input Manifest according to #228.

It must not discover alternate Core inputs by filename heuristics when the manifest is absent/incompatible.

The adapter consumes the explicit Profile file supplied by `--profile`.

It must not silently substitute a different Profile found in a workspace.

---

## 24. Output bundle boundary

All operation output is rooted in `--output-dir`.

When technically possible, the adapter writes:

```text
<output-dir>/integration_result.json
```

last, after finalizing declared artifact/evidence status.

The Integration Result remains the semantic operation result.

Generated artifact presence alone is not proof of a coherent integration operation.

The adapter must not materialize portable bundle artifacts/evidence outside the requested output root.

---

## 25. Output path containment

All bundled paths declared by the Integration Result must resolve inside the Result bundle root.

Portable bundle paths must reject:

```text
absolute paths
.. traversal
path normalization that escapes output root
symlink/equivalent escape from output root
```

Absolute host paths may exist as private execution-environment details but are not portable Result identity and must not replace relative Result paths.

---

## 26. stdout and stderr

`stdout` and `stderr` are operational/logging channels only.

They may contain human-readable progress and diagnostics for operators.

They are not the Integration Contract.

Consumers must not reconstruct:

```text
result state
mappings
coverage
artifact identity
staleness
evidence identity
```

from console text.

Machine-readable operation semantics come from `integration_result.json` when available.

---

## 27. Process exit status

The v0 protocol deliberately keeps process status small.

### Exit zero

```text
exit code = 0
```

requires:

```text
a valid integration_result.json exists
result = succeeded OR succeeded_with_warnings
```

### Non-zero exit

```text
exit code != 0
```

means the invocation/operation failed.

A failed `integration_result.json` should exist when technically possible, but may be absent if failure occurred before a Result could be constructed reliably.

Callers must not derive detailed semantic failure causes from the numeric non-zero exit code.

They inspect Integration Result diagnostics when a valid failed Result exists.

No generic taxonomy of non-zero exit codes is frozen in v0.

---

## 28. Protocol-violation examples

The following combinations violate `orbitfabric.adapter_cli.v0`:

```text
exit 0 + no valid Integration Result
exit 0 + Integration Result.result = failed
exit non-zero + Integration Result.result = succeeded
exit non-zero + Integration Result.result = succeeded_with_warnings
Result operation ID contradicts requested --operation
Result claims a successful required artifact outside output bundle root
```

A generic caller must surface these as adapter/protocol violations rather than guessing which channel is authoritative.

---

## 29. Compatibility preflight

Before executing an operation, a generic caller can preflight:

```text
manifest kind/version supported
requested operation exists
requested operation capabilities are declared consistently
Core Input Set version supported
required Core surface role/kind/format versions supported
Projection Profile generic version supported
Profile integration.id matches package integration.id
Profile integration.schema_version has a published schema
published Profile schema digest is valid
Integration Result default version supported by the caller
execution protocol supported
```

Target-specific semantic constraints remain adapter-owned and may still fail during execution.

Preflight compatibility therefore means:

```text
generic contract appears consumable
```

not:

```text
the target-specific operation is guaranteed to succeed
```

---

## 30. Trust boundary

The following distinctions are normative:

```text
manifest syntax validity != package trust
manifest registration != execution authorization
discovery != execution
Studio Integration Plugin trust != adapter executable trust
schema validity != executable trust
```

A caller decides whether a registered Integration Package is trusted for execution.

The v0 generic contract does not define:

```text
code signing
sandboxing
publisher identity infrastructure
marketplace review
OS installation policy
```

It nevertheless must not imply that discovering or parsing a manifest grants authorization to execute its `argv_prefix`.

---

## 31. Studio relationship

Studio can consume the same generic package boundary as CLI and CI.

Conceptually:

```text
registered integration_package.json
    -> package identity/version
    -> compatibility
    -> advertised capabilities
    -> advertised operations

package Profile JSON Schema
    -> Profile editor rendering
    -> Profile structural validation

orbitfabric.adapter_cli.v0
    -> external adapter invocation

integration_result.json
    -> status
    -> provenance/staleness
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

An ecosystem-specific Studio Integration Plugin may add richer views/actions but orchestrates the same external package boundary.

---

## 32. Reference OpenOBSW/OpenSVF integration

The OpenOBSW/OpenSVF PoC is the first reference case for this contract.

A future reference package may advertise, where actually supported:

```text
Profile validation/projection
flight and ground artifact generation
traceability
OpenSVF/YAMCS runtime discovery/orchestration
verification execution
evidence discovery
live telemetry
commanding
```

The exact operation IDs, target tool compatibility markers, artifact kinds and runtime/verification boundaries are not generic v0 decisions.

They remain gated by the ownership review in:

```text
lipofefeyt/OrbitFabric-OpenOBSW-PoC#30
```

OpenOBSW/OpenSVF/YAMCS semantics must not be moved into this generic manifest or protocol.

---

## 33. Regression and golden requirements

Before implementation/release, protect at least:

```text
valid minimal package manifest
unknown manifest version rejection
missing required manifest field
integration.id distinct from adapter.id
exact-version compatibility success/failure
required Core surface version mismatch
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

Target-specific package fixtures belong to the reference integration package/repository rather than Core generic fixtures.

---

## 34. Design-freeze position

The following Phase B.4 decisions are frozen for `0.1-candidate`:

```text
static integration_package.json
manifest is integration-owned, not Core semantic state
explicit manifest-path discovery/registration
no v0 OS-specific scan directory or marketplace
manifest inspection requires no adapter execution
separate integration.id and adapter.id/version
exact supported-version lists, no range syntax v0
Core Input Set/surface compatibility declarations
positive Relationship Manifest family declarations
no raw-YAML semantic fallback
separate generic Profile and integration-schema compatibility
static local JSON Schema Draft 2020-12 publication
schema exact SHA-256
local contained schema refs; no remote retrieval v0
Package vs Operation vs Result capability separation
opaque integration-defined operation IDs
operation capabilities subset of package capabilities
out-of-process language-neutral execution
execution protocol = orbitfabric.adapter_cli.v0
argv prefix, never shell command string
generic run command with explicit operation/input-manifest/Profile/output-root
no generic adapter RPC daemon v0
Integration Result is semantic result; stdout/stderr are operational only
exit 0 requires successful valid Result
non-zero means failure; failed Result best-effort
no detailed generic non-zero exit taxonomy
output bundle containment
manifest discovery != trust or execution authorization
Studio/CLI/CI share the same package and execution boundary
```

---

## 35. Non-goals

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
Integration Result record details already defined by #233
Core in-process third-party plugin loading/execution
```

---

## 36. Final position

The production integration boundary after Phase B is:

```text
OrbitFabric Core
    owns mission semantics
    and emits coherent versioned integration inputs

Projection Profile
    owns authored ecosystem-specific projection intent

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

This is the final generic architecture gate before extracting the OpenOBSW/OpenSVF reference adapter from the PoC.