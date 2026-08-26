# Integration Result Contract

Status: Architecture candidate — generic envelope design-frozen  
Contract version: `0.1-candidate`  
Scope: Extension-owned machine-readable result boundary for ecosystem integrations  
Parent architecture issue: #227  
Design issue: #233  
Depends on: #228, #231

---

## 1. Purpose

The Integration Result Contract defines the machine-readable output boundary produced by an external OrbitFabric Integration Adapter after attempting an integration operation against:

```text
Core Integration Input Set
+
Projection Profile
```

It answers:

```text
What did this integration operation actually resolve, validate and generate,
and how can a downstream consumer inspect that result without guessing?
```

The intended chain is:

```text
OrbitFabric Core
    ↓
Core Integration Input Set
    ↓
Projection Profile
    ↓
external Integration Adapter
    ↓
Integration Result
    ├── operation/result status
    ├── input/profile provenance
    ├── exercised capabilities
    ├── artifacts
    ├── traceability mappings
    ├── resolved-value provenance
    ├── integration diagnostics
    ├── projection coverage
    ├── evidence references
    └── external-tool provenance
```

The Integration Result exists so CLI tooling, CI and OrbitFabric Studio do not reconstruct integration meaning from generated filenames, directory conventions, target names, timestamps, stdout/stderr, private adapter state or Studio state.

---

## 2. Ownership boundary

An Integration Result is **extension-owned output**.

OrbitFabric governance defines the generic envelope and generic cross-integration semantics documented here, but an Integration Result is not a Core Mission Data Contract surface and does not become a Core semantic authority.

Ownership remains:

```text
Core-owned facts
    -> remain Core-owned and are referenced through Core identity/provenance

Profile-authored projection choices
    -> remain Profile-owned and are referenced through Profile/binding identity

Adapter-resolved mappings, artifacts and diagnostics
    -> Integration Adapter-owned

external runtime/verification facts
    -> remain external-owned and are referenced with explicit producer/ownership

Studio
    -> consumer/orchestrator, never semantic owner
```

Core structural/lint findings must not be copied into the Integration Result and presented as integration diagnostics.

Integration traceability must not be injected into Core `relationship_manifest.json`.

---

## 3. Relationship to the preceding contracts

The Phase B contracts have distinct responsibilities:

```text
Core Integration Input Contract (#228)
    -> exact Core-owned semantic/introspection inputs

Projection Profile Contract (#231)
    -> authored ecosystem-specific projection intent

Integration Result Contract (#233)
    -> what the adapter actually resolved/generated/validated
```

The authority chain is:

```text
Core semantic value
        ↓
adapter deterministic/default target representation
        ↓
permitted Profile-authored target override
        ↓
Integration Result records the resolved outcome
```

The Result may explain that chain but does not change the authority of any upstream layer.

---

## 4. Serialization and bundle boundary

The v0 Integration Result is one UTF-8 JSON document conventionally named:

```text
integration_result.json
```

The JSON data model is normative for v0.

No YAML representation, include mechanism, inheritance mechanism or overlay mechanism is required for generated Results.

The file is written **last** after the adapter has finalized the machine-readable state it can reliably establish.

Consumer invariant:

> A directory containing ecosystem artifacts but no valid `integration_result.json` is not a coherent OrbitFabric Integration Result bundle.

A failed adapter process should still write an Integration Result when technically possible.

This is best-effort rather than an impossible guarantee: a process may fail before it can construct a valid Result envelope at all. When a Result is written, it must never invent missing input identity merely to satisfy the envelope.

Partial files may exist after failure, but file presence alone never establishes a valid integration result.

---

## 5. Generic top-level envelope

A successful projection-oriented Result is conceptually:

```json
{
  "kind": "orbitfabric.integration_result",
  "result_version": "0.1-candidate",
  "result": "succeeded",
  "integration": {
    "id": "orbitfabric-openobsw-opensvf",
    "schema_version": "0.1-candidate"
  },
  "adapter": {
    "id": "orbitfabric-openobsw-opensvf",
    "version": "0.1.0"
  },
  "operation": {
    "id": "project"
  },
  "mission": {
    "status": "available",
    "id": "demo-3u",
    "model_version": "0.1.0",
    "reason": null
  },
  "inputs": {
    "core_input_set": {
      "status": "available",
      "kind": "orbitfabric.integration_input_set",
      "version": "0.1-candidate",
      "sha256": "...",
      "reason": null
    },
    "profile": {
      "status": "available",
      "kind": "orbitfabric.projection_profile",
      "profile_version": "0.1-candidate",
      "id": "openobsw-opensvf-demo",
      "version": "0.1.0",
      "sha256": "...",
      "reason": null
    }
  },
  "capabilities": [
    "profile_validation",
    "projection",
    "artifact_generation",
    "traceability"
  ],
  "artifacts": [],
  "mappings": [],
  "resolutions": [],
  "diagnostics": [],
  "coverage": {
    "status": "complete",
    "scope": {
      "domains": []
    },
    "reason": null,
    "summary": {},
    "records": []
  },
  "evidence": [],
  "external_tools": []
}
```

The generic envelope contains no OpenOBSW, OpenSVF, YAMCS, PUS, SRDB, XTCE or other ecosystem-specific semantic fields.

Target-specific meaning lives in adapter-owned identifiers, records and artifacts.

---

## 6. Required top-level fields

A v0 Result requires:

```text
kind
result_version
result
integration
adapter
operation
mission
inputs
capabilities
artifacts
mappings
resolutions
diagnostics
coverage
evidence
external_tools
```

Arrays remain present even when empty.

The presence of a top-level input/mission object does **not** imply that its identity was successfully resolved. Early-failure availability is represented explicitly as defined below.

Unknown additive fields may be tolerated only according to the compatibility rules of the supported `result_version`.

---

## 7. Version and identity separation

These identifiers have distinct purposes and must not be collapsed:

```text
result_version
    -> generic Integration Result envelope compatibility

integration.id
    -> logical ecosystem-integration family

integration.schema_version
    -> target-specific Profile/configuration schema used/requested for this run

adapter.id
    -> implementation/package identity that produced the Result

adapter.version
    -> implementation/package version

inputs.profile.profile_version
    -> generic Projection Profile envelope version

inputs.profile.version
    -> authored Profile instance revision
```

`adapter.version` must not replace `result_version` or `integration.schema_version` as a compatibility key.

`integration.id` is known from the adapter/package that was invoked and is required even for failed Results.

`integration.schema_version` may be `null` only for a failed Result when the Profile schema identity could not be resolved reliably. A successful Result requires a non-null compatible schema version.

---

## 8. Result state vocabulary

The generic result state is:

```text
succeeded
succeeded_with_warnings
failed
```

### `succeeded`

The requested operation completed validly and there are no integration-owned `ERROR` or `WARNING` diagnostics.

### `succeeded_with_warnings`

The requested operation completed validly, no integration-owned `ERROR` diagnostic exists, and at least one integration-owned `WARNING` exists.

### `failed`

The requested operation did not complete as a valid result and at least one integration-owned `ERROR` diagnostic explains the integration-level failure.

Core lint state is upstream Core-owned provenance.

Core warnings do not automatically turn an Integration Result into `succeeded_with_warnings`.

External-tool diagnostics affect top-level state only through an explicit integration-owned diagnostic describing their integration-level consequence.

---

## 9. Operation identity

Every Result records:

```json
{
  "operation": {
    "id": "project"
  }
}
```

`operation.id` is an integration-defined, non-empty identifier describing the attempted operation.

Generic consumers treat it as opaque and must not parse the string to infer behavior.

Generic behavior is driven by the declared Result state, capabilities and record families.

---

## 10. Exercised capabilities

`capabilities[]` records the generic capabilities **exercised or materially represented by this Result**.

It is not the pre-execution adapter capability-discovery contract.

Known candidate capability IDs include:

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

Capability IDs are unique within the array.

A future Integration Package Manifest (#235) advertises the full capability set of an installed adapter before execution.

Unknown additive capability IDs must not receive guessed semantics.

---

## 11. Input provenance availability

A failed operation may occur before reliable Core Input Set or Profile identity can be established.

The Result must never fabricate provenance in that case.

Both input records therefore have generic status:

```text
available
unavailable
```

`available` means the adapter could establish the contract identity/provenance required by this Result record. It does not by itself mean that the input is semantically compatible with the requested operation.

### Available Core input

```json
{
  "status": "available",
  "kind": "orbitfabric.integration_input_set",
  "version": "0.1-candidate",
  "sha256": "...",
  "reason": null
}
```

Requires:

```text
kind != null
version != null
sha256 != null
reason = null
```

The SHA-256 is the Core Input Set `input_set_sha256` defined by #228.

### Unavailable Core input provenance

```json
{
  "status": "unavailable",
  "kind": null,
  "version": null,
  "sha256": null,
  "reason": "input manifest could not be validated"
}
```

Requires:

```text
reason != null
```

The other identity fields are null; the adapter must not fill them from guesses, filenames or partial raw source reconstruction.

### Available Profile provenance

```json
{
  "status": "available",
  "kind": "orbitfabric.projection_profile",
  "profile_version": "0.1-candidate",
  "id": "openobsw-opensvf-demo",
  "version": "0.1.0",
  "sha256": "...",
  "reason": null
}
```

Requires all identity/version/digest fields and `reason = null`.

The Profile SHA-256 is the exact consumed Profile byte digest.

### Unavailable Profile provenance

```json
{
  "status": "unavailable",
  "kind": null,
  "profile_version": null,
  "id": null,
  "version": null,
  "sha256": null,
  "reason": "Profile document could not be parsed"
}
```

Requires `reason != null` and no invented identity.

A lower-level execution log may record a digest of unreadable/invalid input bytes if useful, but such a digest is not promoted into the resolved Profile provenance record in v0.

---

## 12. Successful-result input invariant

For:

```text
result = succeeded
or
result = succeeded_with_warnings
```

both input records must have:

```text
status = available
```

and `integration.schema_version` must be non-null and compatible with the consumed Profile.

A successful Result cannot be built on unresolved input provenance.

---

## 13. Mission identity availability

Mission identity is convenience/provenance copied from the consumed Core Integration Input Set and is never independently invented by the adapter.

Generic status is:

```text
available
unavailable
```

Available form:

```json
{
  "status": "available",
  "id": "demo-3u",
  "model_version": "0.1.0",
  "reason": null
}
```

Unavailable form:

```json
{
  "status": "unavailable",
  "id": null,
  "model_version": null,
  "reason": "Core input identity unavailable"
}
```

Rules:

- `mission.status = available` requires `inputs.core_input_set.status = available`;
- a successful Result requires `mission.status = available`;
- a failed Result may use `mission.status = unavailable` when the Core input could not be resolved reliably.

The Core Integration Input Set remains authoritative for Mission identity.

---

## 14. Staleness is derived, not timeless truth

The Result stores immutable fingerprints when they are available.

It does not store permanent truth such as:

```text
stale = true
current = true
```

because staleness is a relationship between a historical Result and current inputs.

When both required provenance records are available, consumers compare:

```text
result.inputs.core_input_set.sha256
        vs
current Core Input Set input_set_sha256

result.inputs.profile.sha256
        vs
current Profile exact SHA-256
```

Derived consumer view states may include:

```text
current
stale_core_input
stale_profile
stale_both
unknown
incompatible
```

If historical required provenance is unavailable, staleness is necessarily `unknown`; consumers must not fall back to timestamps.

---

## 15. No self-digest in v0

The v0 Result does not contain:

```text
result_sha256
bundle_sha256
semantic_result_fingerprint
```

A consumer may hash exact `integration_result.json` bytes externally if needed.

Artifact and evidence bytes are fingerprinted separately where appropriate.

---

## 16. Core source reference

Whenever a Result refers to an OrbitFabric semantic entity, it uses:

```json
{
  "domain": "telemetry",
  "id": "eps.obc.bus_voltage_mv"
}
```

Both fields are required and the reference must resolve against the Entity Index of the consumed Core Input Set.

Core source references are permitted only when:

```text
inputs.core_input_set.status = available
```

and the Entity Index required for resolution was compatible/readable.

Forbidden substitutes include YAML paths, source file/line, generated symbols, SRDB/XTCE/YAMCS names and Studio IDs.

---

## 17. Target identity contract

The generic target reference is:

```json
{
  "namespace": "yamcs",
  "kind": "parameter",
  "id": "/orbitfabric/eps/obc/bus_voltage_mv"
}
```

The tuple:

```text
namespace + kind + id
```

is the adapter-owned target identity inside one integration-result family.

Rules:

- all three values are required, non-empty strings;
- `namespace` and `kind` are integration-defined/documented;
- `id` is opaque to generic OrbitFabric consumers;
- generic consumers must not parse semantic meaning from target ID structure;
- the same tuple should be reused by runtime/evidence records for the same target concept;
- target references never become Core entities or Core relationships.

---

## 18. Traceability mappings

Mappings explicitly connect Core sources to resolved target concepts.

Candidate:

```json
{
  "id": "mapping.tm.bus_voltage",
  "sources": [
    {
      "domain": "telemetry",
      "id": "eps.obc.bus_voltage_mv"
    }
  ],
  "profile_bindings": [
    "tm.obc_bus_voltage"
  ],
  "targets": [
    {
      "namespace": "openobsw",
      "kind": "contract_symbol",
      "id": "OF_TM_OBC_BUS_VOLTAGE_MV"
    },
    {
      "namespace": "opensvf",
      "kind": "srdb_parameter",
      "id": "eps.obc.bus_voltage_mv"
    }
  ]
}
```

Rules:

```text
mapping IDs unique within Result
sources contains one or more Core references
profile_bindings contains zero or more Profile binding IDs
targets contains one or more explicit target references
```

If Profile provenance is unavailable, `profile_bindings` must be empty because binding identity cannot be asserted reliably.

The contract supports one-to-one, one-to-many, many-to-one and many-to-many projection structures.

The mapping asserts participation in the resolved projection only; generic consumers must not infer protocol, causal or runtime semantics.

---

## 19. Resolved-value provenance

`resolutions[]` is always present but may be empty.

It explains engineer-relevant/compatibility-sensitive target choices without requiring consumers to reverse-engineer adapter logic.

Candidate:

```json
{
  "id": "resolution.tm.bus_voltage.numeric_id",
  "mapping": "mapping.tm.bus_voltage",
  "binding": "tm.obc_bus_voltage",
  "sources": [
    {
      "domain": "telemetry",
      "id": "eps.obc.bus_voltage_mv"
    }
  ],
  "property": "numeric_id",
  "value": 16385,
  "origin": "profile"
}
```

Generic origins:

```text
core
adapter_default
profile
```

`property` and `value` remain integration-defined target-configuration data.

Rules:

- `id`, `property`, `value` and `origin` are required;
- `mapping` and `binding` may be null when not applicable;
- `sources` is present and may be empty only when another contextual anchor is present;
- at least one of `mapping`, `binding` or `sources` provides context;
- `origin = profile` requires non-null `binding` and available Profile provenance;
- non-null mapping/binding references must resolve.

Adapters are not required to serialize every internal intermediate value.

---

## 20. Artifact contract

Generated files are declared explicitly; generic consumers never discover them through filename conventions.

Candidate:

```json
{
  "id": "flight.mission_contract",
  "kind": "openobsw_contract_header",
  "requirement": "required",
  "status": "generated",
  "path": "flight/mission_contract.h",
  "media_type": "text/x-c",
  "sha256": "...",
  "reason": null,
  "retained_partial": false,
  "derived_from_mappings": [
    "mapping.tm.bus_voltage"
  ]
}
```

Generic requirement:

```text
required
optional
```

Generic status:

```text
generated
not_generated
failed
```

### `generated`

Requires:

```text
path != null
sha256 != null
reason = null
retained_partial = false
```

### `not_generated`

Requires:

```text
path = null
sha256 = null
reason != null
retained_partial = false
```

### `failed`

Requires `reason != null`.

A failed artifact may retain a partial file only when:

```text
retained_partial = true
path != null
sha256 != null
```

When `retained_partial = false`, a failed artifact has `path = null` and `sha256 = null`.

A retained failed file is diagnostic/evidence material and never a valid generated artifact.

Artifact `kind` is integration-owned; paths are relative to `integration_result.json`; `media_type` is optional convenience metadata; `derived_from_mappings` references zero or more mapping IDs.

---

## 21. Required-artifact invariant

For successful Results, every `requirement = required` artifact must be `status = generated`.

Optional artifacts may be `not_generated` with an explicit reason without forcing top-level failure.

A required artifact that is `failed` or `not_generated` forces `result = failed` and an integration-owned ERROR diagnostic.

---

## 22. Integration diagnostics

Diagnostics are explicit machine-readable records.

Candidate:

```json
{
  "id": "diag-001",
  "owner": "integration",
  "producer": "orbitfabric-openobsw-opensvf",
  "phase": "projection_validation",
  "severity": "ERROR",
  "code": "OFI-ALLOC-001",
  "message": "Numeric allocation collision",
  "sources": [],
  "profile_bindings": [
    "tm.obc_bus_voltage"
  ],
  "targets": []
}
```

Generic severities:

```text
ERROR
WARNING
INFO
```

Known generic phases include:

```text
input_compatibility
profile_schema
source_resolution
projection_validation
artifact_generation
external_tool
runtime_orchestration
verification_execution
evidence_collection
```

Unknown additive phase values must not receive guessed semantics.

---

## 23. Diagnostic ownership

Generic diagnostic owners:

```text
integration
external
```

`producer` is required for both.

### `owner = integration`

The adapter/package is the diagnostic authority.

### `owner = external`

The adapter is surfacing a diagnostic produced by an external tool/system without claiming authority over its native semantics.

Core is deliberately not an allowed diagnostic owner inside `diagnostics[]`.

Core structural/load/lint diagnostics remain in the Core Input Set.

If upstream Core state blocks projection, the adapter emits an integration-level diagnostic referencing that consequence, not copied Core findings.

Top-level Result classification is determined by **integration-owned** diagnostics.

If an external error causes operation failure, the adapter emits an integration-owned ERROR describing the integration consequence and may additionally preserve/reference the external diagnostic.

Diagnostic Core-source references are allowed only when Core source resolution is available. Diagnostic `profile_bindings` must be empty when Profile provenance is unavailable.

---

## 24. Projection coverage purpose

Integration coverage answers:

> What happened to each Core entity in the declared scope of this integration operation?

Coverage is distinct from Core `coverage_summary.json` and must not be inferred from artifacts or mappings.

The Integration Result is authoritative only for **integration projection coverage**.

---

## 25. Coverage scope

Coverage declares Core Entity Index domains considered by the Result:

```json
{
  "scope": {
    "domains": [
      "telemetry",
      "commands",
      "events",
      "faults"
    ]
  }
}
```

`coverage.scope.domains` contains unique Core Entity Index domain identifiers.

For `coverage.status = complete`:

> every Core entity whose Entity Index domain is listed in `coverage.scope.domains` has exactly one coverage record.

Domains absent from the scope have no v0 coverage-record obligation.

An entity inside a declared domain but irrelevant to this operation is represented explicitly as `not_applicable`.

Coverage records and non-empty domain scope require available/compatible Core entity resolution.

---

## 26. Coverage completeness state

Generic coverage status:

```text
complete
partial
unavailable
```

### `complete`

The declared-domain completeness invariant is satisfied and `reason = null`.

### `partial`

Some reliable entity coverage was established but the completeness invariant is not satisfied. `reason != null`.

All partial records must still refer to entities in `coverage.scope.domains`.

### `unavailable`

Reliable integration coverage could not be established.

Requires:

```text
records = []
reason != null
```

`scope.domains` may be empty when reliable scope itself could not be established.

If Core input/entity resolution is unavailable, coverage must be `unavailable`.

A successful Result that includes capability `projection` requires:

```text
coverage.status = complete
```

---

## 27. Entity-level coverage states

Each coverage record uses exactly one of:

```text
projected
partially_projected
intentionally_not_projected
not_projected
unsupported
blocked
not_applicable
```

Meanings:

```text
projected
    fully represented for this integration scope

partially_projected
    target representation exists but known projection is incomplete

intentionally_not_projected
    resolved from explicit Profile intent = do_not_project

not_projected
    no projection exists, without explicit exclusion or target impossibility

unsupported
    adapter declares the target integration cannot represent the concept

blocked
    supported/intended projection prevented by compatibility/validation/generation failure

not_applicable
    entity belongs to a declared domain but is outside relevant operation scope
```

`intentionally_not_projected` requires available Profile provenance and an explicit resolvable `do_not_project` binding.

`not_projected` is required because:

```text
Profile binding absent
!=
intentionally_not_projected
```

---

## 28. Coverage record

Candidate:

```json
{
  "source": {
    "domain": "telemetry",
    "id": "eps.obc.bus_voltage_mv"
  },
  "state": "projected",
  "mappings": [
    "mapping.tm.bus_voltage"
  ],
  "profile_bindings": [
    "tm.obc_bus_voltage"
  ],
  "diagnostics": [],
  "reason": null
}
```

Rules:

- `source` is required and unique within coverage records;
- `mappings` references zero or more mapping IDs;
- `profile_bindings` references zero or more Profile binding IDs and must be empty when Profile provenance is unavailable;
- `diagnostics` references zero or more Result diagnostic IDs;
- states requiring explanation provide a non-empty reason where diagnostics alone do not establish the cause.

`coverage.summary` is convenience metadata. If non-empty, it must be exactly derivable from `coverage.records`; entity-level records remain authoritative.

---

## 29. Evidence references

The Result may reference verification/runtime evidence without becoming the verification engine.

Generic evidence owners:

```text
integration
external
```

`producer` is always required.

Bundled evidence candidate:

```json
{
  "id": "evidence.live-hk-yamcs",
  "owner": "external",
  "producer": "opensvf",
  "kind": "campaign_result",
  "location": {
    "path": "evidence/live-hk-yamcs.json"
  },
  "sha256": "...",
  "mappings": [
    "mapping.tm.bus_voltage"
  ],
  "targets": []
}
```

External evidence candidate:

```json
{
  "id": "evidence.external-run",
  "owner": "external",
  "producer": "yamcs",
  "kind": "archive_reference",
  "location": {
    "uri": "..."
  },
  "sha256": null,
  "mappings": [],
  "targets": []
}
```

Rules:

- `id`, `owner`, `producer`, `kind` and `location` are required;
- exactly one of `location.path` or `location.uri` is used;
- bundled path is relative to `integration_result.json` and requires SHA-256;
- external URI evidence may carry SHA-256 when stable bytes are available;
- `kind` remains producer/integration-defined;
- evidence mapping references must resolve;
- evidence target references use the generic target-reference shape;
- evidence ownership remains explicit.

The Result must not reinterpret external evidence semantics as Core facts.

---

## 30. External-tool provenance

Tools that materially affect outputs may be recorded as:

```json
{
  "id": "opensvf",
  "version": "...",
  "role": "srdb_to_xtce"
}
```

External-tool IDs are unique within the Result.

`id` and `role` are integration-owned strings; version is recorded when available/materially relevant.

External-tool provenance creates no Core dependency on the tool.

---

## 31. Portability

All bundled artifact/evidence paths are relative to the directory containing `integration_result.json`.

Absolute workspace paths must not participate in identity, compatibility, staleness or portable equivalence.

Git branch names, checkout paths and Studio workspace IDs are not required Result identity fields.

---

## 32. Failure-state matrix

Representative states:

| Condition | Input identity | Mission | Result | Coverage | Required diagnostic behavior |
|---|---|---|---|---|---|
| Valid operation, no integration warnings | both available | available | `succeeded` | `complete` when projection exercised | no integration ERROR/WARNING |
| Valid operation with integration warnings | both available | available | `succeeded_with_warnings` | `complete` when projection exercised | >=1 integration WARNING, no integration ERROR |
| Core manifest/identity cannot be established | Core unavailable | unavailable | `failed` | `unavailable` | integration ERROR; no guessed Core identity |
| Core input identified but incompatible | Core available | available if Core exposes it | `failed` | usually `unavailable` | integration ERROR references incompatibility; no copied Core findings |
| Profile document cannot be identified/parsed | Profile unavailable | depends on Core | `failed` | `unavailable`, `partial`, or `complete` blocked coverage if Core scope is reliably known | integration ERROR; no invented Profile binding identity |
| Profile schema invalid after Profile identity established | Profile available | available | `failed` | depends on resolved Core context | integration ERROR identifies schema failure |
| Source/profile resolution failure | both available | available | `failed` | `partial` or `complete` with blocked entities when possible | integration ERROR identifies resolution failure |
| Projection validation failure | both available | available | `failed` | may be `complete` with affected entities `blocked` | integration ERROR identifies projection failure |
| Required artifact generation failure | both available | available | `failed` | `complete` or `partial` depending progress | failed artifact + integration ERROR |
| Required external-tool failure | depends on stage | depends on Core | `failed` | depends on stage | integration ERROR records consequence; external diagnostic may also be present |

A failure Result should preserve reliable mappings, artifacts, diagnostics and coverage already established without presenting them as complete when they are not.

---

## 33. Referential-integrity requirements

A valid Result satisfies all applicable rules:

```text
capability IDs are unique
coverage scope domains are unique
mapping IDs are unique
resolution IDs are unique
artifact IDs are unique
diagnostic IDs are unique
evidence IDs are unique
external-tool IDs are unique

Core source references exist only when Core entity resolution is available
all Core source references resolve against the consumed Entity Index
Profile binding references exist only when Profile provenance is available
all Profile binding references resolve against the consumed Profile

all artifact/coverage/evidence mapping references resolve
all coverage diagnostic references resolve
all non-null resolution mapping references resolve
all non-null resolution binding references resolve
all mapping sources resolve
all resolution sources resolve
all target references satisfy namespace+kind+id
all coverage source records are unique
all partial/complete coverage records belong to declared scope domains
coverage summary agrees exactly with coverage records when non-empty

mission available implies Core input available
successful Result implies Core input available + Profile available + Mission available
successful projection Result implies coverage complete
successful Result implies every required artifact generated
```

A consumer rejects generic-contract referential corruption rather than guessing intended references.

Target-specific semantic validation remains adapter-owned.

---

## 34. Compatibility negotiation

Generic consumers negotiate:

```text
kind
result_version
```

Target-specific compatibility is represented separately by:

```text
integration.id
integration.schema_version
adapter.id/version
external-tool provenance
```

Rules:

- unknown additive generic fields may be tolerated only where the supported Result contract permits additive evolution;
- missing required generic fields are incompatible;
- unknown target namespaces/kinds remain opaque and must not be guessed;
- unknown artifact/evidence kinds remain opaque and must not be guessed;
- unknown additive capability IDs may be preserved/displayed without invented behavior;
- generic consumers do not need target-specific schema knowledge merely to read generic Result status/provenance/artifacts/mappings/coverage.

Input `status = unavailable` is a valid failed-Result state, not a signal for a consumer to reconstruct missing identity from source files.

---

## 35. Integration-specific meaning

The v0 generic Result deliberately avoids a free-form semantic escape hatch.

Integration-specific meaning is carried through:

```text
namespaced target references
integration-owned artifact kinds
integration-owned evidence kinds
integration-owned resolution properties/values
integration diagnostic codes
operation identity
external-tool roles
```

If a generic extension object later proves necessary, it requires an explicit compatibility-reviewed contract change.

---

## 36. Relationship to Studio

Studio may use:

```text
result + diagnostics
    -> integration health/status

input availability + fingerprints
    -> provenance health and derived staleness

artifacts
    -> Artifact Explorer

mappings + targets
    -> Contract Continuity Explorer and reverse navigation

resolutions
    -> explain target values/names/allocations

coverage
    -> Projection Coverage Dashboard

evidence
    -> verification/evidence navigation

capabilities
    -> capabilities exercised by this Result
```

Studio must not scan generated files, parse target IDs for semantics, reconstruct mappings from names, infer coverage from artifact presence, copy Core lint findings, calculate staleness from timestamps or invent missing identity.

When input provenance is unavailable, Studio renders that state explicitly rather than trying to repair it from Mission YAML or private state.

---

## 37. Relationship to the OpenOBSW/OpenSVF reference integration

The OpenOBSW/OpenSVF PoC is the first concrete evidence for the generic contract.

Representative target namespaces may eventually include:

```text
openobsw
opensvf
yamcs
```

Representative artifact/evidence kinds and external-tool roles remain integration-owned and are deliberately not frozen here.

PoC PR #30 should refine those reference-integration details.

---

## 38. Regression and golden requirements

Before implementation/release, protection should include at least:

```text
clean succeeded Result
succeeded_with_warnings Result
failed Result with unavailable Core identity
failed Result with unavailable Profile identity
failed Result after partial projection
required artifact generation failure
optional artifact not generated
retained failed partial artifact
one-to-one traceability
one-to-many traceability
many-to-one traceability
resolution origin = core
resolution origin = adapter_default
resolution origin = profile
coverage complete invariant
coverage partial invariant
coverage unavailable invariant
all entity-level coverage states
bundled evidence path+digest
external evidence URI
unknown additive target namespace/kind behavior
conditional referential-integrity rules
staleness comparison from available fingerprints
unknown staleness when provenance unavailable
manifest-last/incomplete-bundle rejection
relative-path portability
```

Golden fixtures protect the generic envelope/representative records once the candidate schema is accepted for implementation.

Target-specific fixtures belong to the reference adapter package.

---

## 39. Implementation boundary

This contract does not require Core to execute adapters.

The first production execution boundary remains:

```text
OrbitFabric Core CLI
    -> emits Core Integration Input Set

external Integration Adapter/package
    -> loads Input Set + Projection Profile
    -> validates compatibility/profile schema
    -> performs target work
    -> writes Integration Result last when technically possible
```

This remains consistent with ADR-0015.

Integration Package discovery/advertised capabilities/out-of-process invocation are owned by #235 rather than duplicated here.

---

## 40. Design-freeze position

The following generic Phase B.3 decisions are frozen for `0.1-candidate`:

```text
extension-owned Integration Result
UTF-8 JSON output
conventional integration_result.json name
Result written last as coherent-bundle marker
best-effort failed Result without invented provenance
fixed generic top-level envelope
separate Result/integration-schema/adapter/Profile versions
explicit operation identity
capabilities represent exercised Result capabilities
result = succeeded | succeeded_with_warnings | failed
result classification based on integration-owned diagnostics
input provenance status = available | unavailable
Mission identity status = available | unavailable
successful Result requires resolved Core/Profile/Mission provenance
exact Core Input Set and Profile fingerprints when available
staleness derived by comparison; unavailable provenance => unknown
no Result self-digest or semantic fingerprint in v0
Core source reference = {domain,id}
target reference = {namespace,kind,id}, opaque to generic consumers
explicit one/many traceability mappings
optional resolved-value provenance with origin core|adapter_default|profile
explicit artifact requirement/status/digest records
required-artifact success invariant
integration/external diagnostic ownership separation
Core diagnostics never copied into Result diagnostics
coverage scope expressed as Core domains
coverage status = complete | partial | unavailable
exactly one coverage record per entity in declared domains when complete
entity states projected|partially_projected|intentionally_not_projected|not_projected|unsupported|blocked|not_applicable
evidence owner = integration | external with explicit producer/location
generic conditional referential-integrity rules
relative bundled paths
no generic free-form semantic escape hatch
Studio consumes the Result without reconstructing target semantics or missing provenance
```

Remaining OpenOBSW/OpenSVF details may refine target namespaces/kinds, artifact/evidence kinds, external-tool roles and adapter capabilities, but do not reopen the generic envelope unless a genuinely ecosystem-independent requirement emerges.

---

## 41. Non-goals

The v0 Integration Result Contract does not define:

```text
Core Mission Model fields or semantics
Projection Profile settings/config schema
OpenOBSW/PUS behavior
OpenSVF behavior
YAMCS behavior
SRDB/XTCE semantics
adapter package discovery/installation
full pre-execution capability discovery
runtime transport/API protocols
verification engine behavior
Studio plugin lifecycle
Core plugin discovery/loading/execution
marketplace/signing/sandboxing
a generic free-form extension object
semantic-equivalence fingerprinting
```

---

## 42. Final position

```text
Core owns mission semantics and emits exact, coherent integration inputs.

Projection Profile owns authored ecosystem-specific projection intent.

Integration Adapter owns target resolution, validation, generation and integration diagnostics.

Integration Result records what the adapter could reliably resolve/generate and makes unavailable provenance explicit rather than guessing.

External runtime/verification systems retain ownership of native behavior and evidence semantics.

Studio consumes the same machine-readable Result used by CLI/CI workflows and never reconstructs integration meaning or missing provenance from filenames, names, raw YAML or timestamps.
```
