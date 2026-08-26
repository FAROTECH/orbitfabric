# Integration Result Contract

Status: Architecture candidate — generic envelope design-frozen  
Contract version: `0.1-candidate`  
Scope: Extension-owned machine-readable result boundary for ecosystem integrations  
Parent architecture issue: #227  
Design issue: #233  
Depends on: #228, #231

---

## 1. Purpose

The Integration Result Contract defines the machine-readable output boundary produced by an external OrbitFabric Integration Adapter after consuming:

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

The Integration Result exists so CLI tooling, CI and OrbitFabric Studio do not need to reconstruct integration meaning from:

```text
generated filenames
directory conventions
target naming conventions
timestamps
stdout/stderr text
private adapter state
Studio state
```

---

## 2. Ownership boundary

An Integration Result is **extension-owned output**.

OrbitFabric governance defines the generic envelope and generic cross-integration semantics documented here, but an Integration Result is not a Core Mission Data Contract surface and does not become a new Core semantic authority.

Ownership remains:

```text
Core-owned facts
    -> remain Core-owned and are referenced through Core identity/provenance

Profile-authored projection choices
    -> remain Profile-owned and are referenced through Profile/binding identity

Adapter-resolved mappings, artifacts and diagnostics
    -> Integration Adapter-owned

OpenOBSW/OpenSVF/YAMCS runtime or verification facts
    -> external-owned and referenced with explicit producer/ownership

Studio
    -> consumer/orchestrator, never semantic owner
```

Core lint findings must not be copied into the Integration Result and presented as integration diagnostics.

Integration traceability must not be injected into Core `relationship_manifest.json`.

---

## 3. Relationship to the preceding contracts

The three Phase B contracts have different responsibilities:

```text
Core Integration Input Contract (#228)
    -> exact Core-owned semantic/introspection inputs consumed

Projection Profile Contract (#231)
    -> authored ecosystem-specific projection intent

Integration Result Contract (#233)
    -> what the adapter actually resolved/generated/validated
```

The authority chain is therefore:

```text
Core semantic value
        ↓
adapter deterministic/default target representation
        ↓
permitted Profile-authored target override
        ↓
Integration Result records the resolved outcome
```

The Result may explain that chain, but it does not change the authority of any upstream layer.

---

## 4. Serialization and bundle boundary

The v0 Integration Result is one UTF-8 JSON document conventionally named:

```text
integration_result.json
```

The JSON data model is normative for v0.

No YAML representation, include mechanism, inheritance mechanism or overlay mechanism is required for generated Results.

The file is written **last** after the adapter has finalized result status, mappings, diagnostics, coverage and artifact status.

Consumer invariant:

> A directory containing ecosystem artifacts but no valid `integration_result.json` is not a coherent OrbitFabric Integration Result bundle.

This is analogous to the manifest-last rule of the Core Integration Input Set, while preserving separate ownership.

A failed adapter process should still write an Integration Result when technically possible.

Partial files may exist after failure, but file presence alone never establishes a valid integration result.

---

## 5. Generic top-level envelope

The design-frozen v0 candidate shape is conceptually:

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
    "id": "demo-3u",
    "model_version": "0.1.0"
  },
  "inputs": {
    "core_input_set": {
      "kind": "orbitfabric.integration_input_set",
      "version": "0.1-candidate",
      "sha256": "..."
    },
    "profile": {
      "kind": "orbitfabric.projection_profile",
      "profile_version": "0.1-candidate",
      "id": "openobsw-opensvf-demo",
      "version": "0.1.0",
      "sha256": "..."
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

The generic envelope must not contain OpenOBSW, OpenSVF, YAMCS, PUS, SRDB, XTCE or other ecosystem-specific semantic fields.

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

This gives generic consumers a predictable envelope without requiring target-specific knowledge.

Unknown additive fields may be tolerated only according to the compatibility rules of the supported `result_version`.

---

## 7. Version and identity separation

These identifiers have distinct purposes and must not be collapsed:

```text
result_version
    -> generic OrbitFabric Integration Result envelope compatibility

integration.id
    -> logical ecosystem-integration family

integration.schema_version
    -> target-specific Profile/configuration schema consumed for this run

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

The `integration.id + integration.schema_version` pair must be compatible with the Projection Profile consumed by this Result.

---

## 8. Result state vocabulary

The generic result state is:

```text
succeeded
succeeded_with_warnings
failed
```

### `succeeded`

The requested integration operation completed validly and there are no integration-owned `ERROR` or `WARNING` diagnostics.

### `succeeded_with_warnings`

The requested integration operation completed validly, no integration-owned `ERROR` diagnostic exists, and at least one integration-owned `WARNING` exists.

### `failed`

The requested operation did not complete as a valid result and at least one integration-owned `ERROR` diagnostic explains the integration-level failure.

Core lint state is upstream Core-owned provenance.

For example:

```text
Core lint passed_with_warnings
```

does not automatically imply:

```text
Integration Result succeeded_with_warnings
```

The adapter may emit an integration diagnostic that an operation was blocked by upstream Core state, but it must reference that state rather than copying Core findings.

External-tool diagnostics affect top-level result state only through an explicit integration-owned diagnostic that records the integration-level consequence.

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

`operation.id` is an integration-defined identifier describing the operation that produced the Result.

Generic OrbitFabric consumers must treat it as opaque.

Generic behavior must not depend on parsing the operation ID string.

Generic behavior is instead driven by:

```text
result state
exercised capabilities
artifact records
mapping records
coverage records
diagnostics
evidence
```

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

A future Integration Package Manifest may advertise the full capability set of an installed adapter before execution.

The Result should not duplicate that future package manifest as timeless package metadata.

Unknown additive capability IDs must not receive guessed semantics.

---

## 11. Input provenance

The Result must identify the exact Core and Profile inputs consumed.

### Core input provenance

Required:

```text
Core Integration Input Set kind
Core Integration Input Set contract version
Core Integration Input Set input_set_sha256
```

Conceptually:

```json
{
  "core_input_set": {
    "kind": "orbitfabric.integration_input_set",
    "version": "0.1-candidate",
    "sha256": "..."
  }
}
```

### Profile provenance

Required:

```text
Projection Profile kind
generic Profile envelope version
Profile ID
Profile instance version
exact SHA-256 of the consumed Profile bytes
```

Conceptually:

```json
{
  "profile": {
    "kind": "orbitfabric.projection_profile",
    "profile_version": "0.1-candidate",
    "id": "openobsw-opensvf-demo",
    "version": "0.1.0",
    "sha256": "..."
  }
}
```

The exact Profile digest is a byte-level provenance fingerprint.

No semantic-equivalence Profile fingerprint is introduced in v0.

---

## 12. Mission identity

The Result repeats the Mission identity reported by the consumed Core Integration Input Set:

```json
{
  "mission": {
    "id": "demo-3u",
    "model_version": "0.1.0"
  }
}
```

This is convenience/provenance metadata.

The Core Integration Input Set remains the authority for the Core semantic input.

The adapter must verify consistency rather than silently accepting a mismatched Mission/Profile context.

---

## 13. Staleness is derived, not serialized as timeless truth

The Result stores immutable fingerprints.

It does **not** store a permanent truth such as:

```text
stale = true
current = true
```

because staleness is a relationship between a historical Result and the inputs being inspected now.

Consumers derive state by comparison:

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

That view vocabulary may evolve outside the immutable historical Result contract.

Timestamps must not be the authority for staleness.

---

## 14. No self-digest in v0

The v0 Result does not contain:

```text
result_sha256
bundle_sha256
semantic_result_fingerprint
```

A consumer may hash the exact `integration_result.json` bytes externally if needed.

Avoiding a self-digest keeps the envelope simple and avoids recursive serialization rules before a demonstrated requirement exists.

Artifact and evidence bytes are fingerprinted separately where appropriate.

---

## 15. Core source reference

Whenever a Result refers to an OrbitFabric semantic entity, it uses the same generic source reference as the Projection Profile:

```json
{
  "domain": "telemetry",
  "id": "eps.obc.bus_voltage_mv"
}
```

Both `domain` and `id` are required.

The reference must resolve against the Entity Index of the consumed Core Integration Input Set.

Forbidden substitutes include:

```text
YAML path
source file/line
C symbol
SRDB name
XTCE path
YAMCS path
Studio internal ID
```

---

## 16. Target identity contract

Integration traceability requires explicit target references.

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

- all three values are required strings;
- `namespace` is integration-defined and documented;
- `kind` is integration-defined and machine-readable;
- `id` is opaque to generic OrbitFabric consumers;
- generic consumers must not parse semantic meaning from target ID string structure;
- the same tuple should be reused by runtime/evidence records when it identifies the same target concept;
- a target reference is not a Core entity and must not enter Core Entity Index or Relationship Manifest.

---

## 17. Traceability mappings

Mappings explicitly connect Core source entities to resolved target concepts.

Candidate record:

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
    },
    {
      "namespace": "yamcs",
      "kind": "parameter",
      "id": "/orbitfabric/eps/obc/bus_voltage_mv"
    }
  ]
}
```

Rules:

```text
mapping IDs are unique within the Result
sources contains one or more Core {domain,id} references
profile_bindings contains zero or more Profile binding IDs
targets contains one or more explicit target references
```

The contract supports:

```text
one Core source -> one target
one Core source -> multiple targets
multiple Core sources -> one target construct
multiple Core sources -> multiple target constructs
one Core source participating in multiple mapping records
```

The mapping means only:

```text
these Core semantics participated in this resolved projection to these target concepts
```

Generic consumers must not infer protocol, causal or runtime meaning beyond the explicit mapping.

---

## 18. Resolved-value provenance

`resolutions[]` is an optional-detail record family represented by an always-present array.

It exists for engineer-relevant or compatibility-sensitive resolved choices that Studio/CLI should be able to explain without reverse-engineering adapter logic.

Candidate record:

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

Generic `origin` values are:

```text
core
adapter_default
profile
```

`property` and `value` remain integration-defined target-configuration data.

An adapter is not required to serialize every internal intermediate value.

Useful candidates include:

```text
stable numeric IDs
target symbols
target database names
encoding/type choices
protocol mappings
```

For `origin = profile`, the corresponding Profile binding should be referenced when the value came from binding-local authored state.

---

## 19. Artifact contract

Generated files are declared explicitly.

They must never be discovered by generic consumers from filename conventions.

Candidate artifact record:

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

Generic `requirement` values:

```text
required
optional
```

Generic `status` values:

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

Requires:

```text
reason != null
```

A failed artifact may retain a partial file only when:

```text
retained_partial = true
path != null
sha256 != null
```

Such a file is diagnostic/evidence material and must never be interpreted as a valid generated artifact.

Artifact `kind` is integration-owned.

`path` is relative to the directory containing `integration_result.json`.

`media_type` is optional convenience metadata.

`derived_from_mappings` references zero or more Result mapping IDs.

---

## 20. Required-artifact invariant

For:

```text
result = succeeded
or
result = succeeded_with_warnings
```

all artifacts with:

```text
requirement = required
```

must have:

```text
status = generated
```

Optional artifacts may be `not_generated` with an explicit reason without forcing top-level failure.

A required artifact that is `failed` or `not_generated` forces the integration operation to `failed`.

---

## 21. Integration diagnostics

Diagnostics are explicit machine-readable records.

Candidate record:

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

Generic severity values are:

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

## 22. Diagnostic ownership rules

Generic diagnostic `owner` values are:

```text
integration
external
```

### `owner = integration`

The Integration Adapter/package is the diagnostic authority.

`producer` identifies the adapter/integration component.

### `owner = external`

The adapter is faithfully surfacing a diagnostic produced by an external tool/system.

`producer` is required and identifies that external authority.

Core is deliberately **not** an allowed diagnostic owner inside `diagnostics[]`.

Core structural/load/lint diagnostics remain in the Core Integration Input Set.

When upstream Core state blocks projection, the adapter may emit an integration diagnostic such as:

```text
projection blocked because Core lint result is failed
```

but it must not duplicate the Core findings themselves.

Top-level `result` classification is determined by **integration-owned** diagnostics.

If an external error materially causes the operation to fail, the adapter emits an integration-owned diagnostic describing that integration-level consequence and may additionally preserve/reference the external diagnostic.

---

## 23. Projection coverage purpose

Integration coverage answers:

> What happened to each Core entity in the declared scope of this integration operation?

Coverage must not be inferred from generated artifacts or mappings alone.

It is distinct from Core `coverage_summary.json`.

The Integration Result is the authority only for **integration projection coverage**, not generic Mission Model coverage.

---

## 24. Coverage scope

Coverage declares the Core Entity Index domains considered by this Result:

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

This avoids ambiguity between:

```text
forgotten entity
intentionally not projected entity
unsupported entity
blocked entity
entity outside the declared domains
```

Domains absent from `coverage.scope.domains` carry no v0 coverage-record obligation.

If an entity belongs to a listed domain but is not relevant to this particular integration scope, its explicit coverage state is `not_applicable`.

---

## 25. Coverage completeness state

Generic coverage status is:

```text
complete
partial
unavailable
```

### `complete`

The declared-domain completeness invariant is satisfied.

`reason = null`.

### `partial`

Some Core entities were resolved/covered before the operation failed, but the declared-domain completeness invariant is not satisfied.

`reason != null`.

The available coverage records remain useful failure evidence.

### `unavailable`

Coverage could not be established, for example because input compatibility/source resolution failed before reliable entity enumeration.

Requires:

```text
records = []
reason != null
```

`scope.domains` may be empty when reliable scope cannot be established.

For a `succeeded` or `succeeded_with_warnings` Result that includes capability `projection`:

```text
coverage.status = complete
```

is required.

---

## 26. Entity-level coverage states

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

### `projected`

The adapter considers the Core entity fully represented for the declared integration scope.

### `partially_projected`

Some relevant target representation exists, but the adapter identifies a known incomplete projection.

### `intentionally_not_projected`

The result resolves from explicit Projection Profile:

```text
intent = do_not_project
```

### `not_projected`

No resolved projection exists, without explicit `do_not_project` intent and without claiming target impossibility.

This state is required because:

```text
Profile binding absent
!=
intentionally_not_projected
```

### `unsupported`

The adapter declares that the target integration cannot represent the relevant concept.

### `blocked`

Projection was intended/supported but compatibility, validation or generation failure prevented it.

### `not_applicable`

The entity belongs to a declared coverage domain but is outside the relevant projection scope for this result.

---

## 27. Coverage record

Candidate record:

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
- `profile_bindings` references zero or more Profile binding IDs;
- `diagnostics` references zero or more Result diagnostic IDs;
- states requiring explanation should provide a non-empty `reason` where diagnostics alone do not establish the cause.

Aggregate counts in `coverage.summary` are convenience metadata.

If present, they must be exactly derivable from `coverage.records` and must not disagree with entity-level records.

Entity-level records remain authoritative.

---

## 28. Evidence references

The Result may reference verification/runtime evidence without becoming the verification engine.

Candidate bundled evidence:

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

Candidate external evidence:

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
- bundled `path` is relative to `integration_result.json` and requires SHA-256;
- external URI evidence may carry SHA-256 when stable bytes are available;
- `kind` remains producer/integration-defined;
- evidence may reference Result mappings and target references for deterministic navigation;
- evidence ownership must remain explicit.

The Result must not reinterpret OpenSVF/YAMCS evidence semantics as Core facts.

---

## 29. External-tool provenance

Tools that materially affect integration outputs may be recorded in:

```json
{
  "id": "opensvf",
  "version": "...",
  "role": "srdb_to_xtce"
}
```

`id` and `role` are integration-owned strings.

`version` should be recorded when available and materially relevant to reproducibility/support.

External-tool provenance does not create a Core dependency on that tool.

The integration-specific adapter/schema determines which tools are relevant.

---

## 30. Portability

All bundled artifact/evidence paths are relative to the directory containing `integration_result.json`.

Absolute workspace paths must not participate in:

```text
identity
compatibility
staleness
portable equivalence
```

Absolute paths may be exposed separately by an execution environment for convenience, but they are not portable Result identity.

No Git branch name, repository checkout path or Studio workspace ID is a required Result identity field.

---

## 31. Failure-state matrix

The generic contract supports these representative states:

| Condition | Result | Coverage | Artifacts | Required diagnostic behavior |
|---|---|---|---|---|
| Valid operation, no integration warnings | `succeeded` | `complete` when projection exercised | all required generated | no integration ERROR/WARNING |
| Valid operation with integration warnings | `succeeded_with_warnings` | `complete` when projection exercised | all required generated | >=1 integration WARNING, no integration ERROR |
| Core input incompatible before entity resolution | `failed` | normally `unavailable` | required outputs not valid | integration ERROR references upstream incompatibility; no copied Core findings |
| Profile schema invalid | `failed` | `unavailable` or `partial` depending resolved context | required outputs not valid | integration ERROR identifies Profile/schema failure |
| Source/profile resolution failure | `failed` | `partial` or `unavailable` | required outputs not valid | integration ERROR identifies resolution failure |
| Projection validation failure after entity resolution | `failed` | may be `complete` with affected entities `blocked` | required outputs not valid | integration ERROR identifies projection failure |
| Required artifact generation failure | `failed` | `complete` or `partial` depending progress | failed artifact explicit | integration ERROR identifies generation failure |
| Required external tool failure | `failed` | depends on operation stage | affected outputs explicit | integration ERROR records integration consequence; external diagnostic may be referenced |

A failure Result is still valuable evidence and should preserve valid mappings/artifacts/coverage already established where doing so does not misrepresent them as complete.

---

## 32. Referential-integrity requirements

A valid Result must satisfy:

```text
all Core source references resolve against the consumed Entity Index
all profile_bindings references resolve against the consumed Profile
all mapping IDs are unique
all resolution IDs are unique
all artifact IDs are unique
all diagnostic IDs are unique
all evidence IDs are unique
all mapping references from artifacts/coverage/evidence resolve
all diagnostic references from coverage resolve
all mapping sources resolve to Core source references
all target references satisfy namespace+kind+id shape
all coverage source records are unique
coverage summary agrees with coverage records
```

A consumer must reject generic-contract referential corruption rather than guessing intended references.

Target-specific semantic validation remains adapter-owned.

---

## 33. Compatibility negotiation

Generic consumers negotiate:

```text
kind
result_version
```

They then consume known generic fields and records according to that contract.

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
- generic consumers must not require target-specific schema knowledge merely to read Result status/provenance/artifacts/mappings/coverage.

---

## 34. Integration-specific extensions

The generic Result contract deliberately avoids a generic free-form semantic override object.

Integration-specific meaning should primarily be carried through:

```text
namespaced target references
integration-owned artifact kinds
integration-owned evidence kinds
integration-owned resolution properties/values
integration diagnostic codes
operation identity
external-tool roles
```

If experience proves that a generic extension object is required, it should be introduced through an explicit compatibility-reviewed contract change rather than becoming an unstructured escape hatch in v0.

---

## 35. Relationship to Studio

Studio should be able to render the integration from the same generic Result used by CLI/CI workflows.

Studio may use:

```text
result + diagnostics
    -> integration health/status

inputs fingerprints
    -> derived staleness

artifacts
    -> artifact explorer

mappings + targets
    -> Contract Continuity Explorer and reverse navigation

resolutions
    -> explain why a target value/name/allocation exists

coverage
    -> Projection Coverage Dashboard

evidence
    -> verification/evidence navigation

capabilities
    -> show which capabilities this Result exercised
```

Studio must not:

```text
scan generated files to discover artifacts
parse target IDs to infer semantics
reconstruct mappings from matching names
infer coverage from artifact presence
copy Core lint findings into integration diagnostics
calculate staleness from timestamps alone
invent target identities
```

This keeps Studio a consumer/orchestrator rather than another integration authority.

---

## 36. Relationship to the OpenOBSW/OpenSVF reference integration

The OpenOBSW/OpenSVF PoC provides the first concrete evidence for this generic contract.

Representative target namespaces may eventually include:

```text
openobsw
opensvf
yamcs
```

Representative artifact kinds may include integration-owned values for:

```text
C contract header
SRDB
XTCE-facing/generated material
runtime/campaign descriptors
```

Those values are **not** generic Core semantics and are deliberately not frozen by this document.

The reference adapter/schema should refine them after PoC PR #30 ownership review.

---

## 37. Relationship to Gonçalo / PoC PR #30

Gonçalo's review remains important for reference-integration details such as:

```text
SRDB -> XTCE ownership
OpenOBSW generated-contract boundary
OpenSVF supported runtime/campaign interfaces
YamcsBridge reuse
compatibility/version markers
verification/campaign evidence interfaces
```

Those answers may refine:

```text
target namespace/kind values
artifact kinds
external-tool roles
evidence kinds
reference adapter capabilities
```

They must not move OpenOBSW/OpenSVF/YAMCS semantics into the generic Result envelope unless a genuinely ecosystem-independent requirement emerges.

---

## 38. Regression and golden requirements

Before implementation/release, protection should include at least:

```text
clean succeeded Result
succeeded_with_warnings Result
failed Result before source resolution
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
referential-integrity failure detection
staleness comparison from input/profile fingerprints
manifest-last/incomplete-bundle rejection
relative-path portability
```

Golden fixtures should protect the generic envelope and representative record families once the candidate schema is accepted for implementation.

Target-specific fixtures belong to the reference adapter repository/package rather than Core generic regression fixtures.

---

## 39. Implementation boundary

This document defines architecture and generic serialization semantics.

It does not require OrbitFabric Core to execute adapters.

The first production execution boundary remains:

```text
OrbitFabric Core CLI
    -> emits Core Integration Input Set

external Integration Adapter/package
    -> loads Input Set + Projection Profile
    -> validates Profile/integration schema
    -> performs target projection/integration work
    -> writes Integration Result last
```

This remains consistent with ADR-0015.

Core may later provide shared schema definitions/helpers if governance decides they are useful, but the adapter remains external execution.

---

## 40. Design-freeze position

The following generic Phase B.3 decisions are frozen for `0.1-candidate`:

```text
extension-owned Integration Result
UTF-8 JSON output
conventional integration_result.json name
manifest/result written last as coherent-bundle marker
fixed generic top-level envelope
separate Result/integration-schema/adapter/Profile versions
explicit operation identity
capabilities represent exercised Result capabilities, not full adapter discovery
result = succeeded | succeeded_with_warnings | failed
result classification based on integration-owned diagnostics
exact Core Input Set and Profile fingerprints
staleness derived by comparison, not serialized as timeless truth
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
explicit evidence ownership/producer/location
generic referential-integrity rules
relative bundled paths
no generic free-form semantic escape hatch
Studio consumes the Result without reconstructing target semantics
```

Remaining reference-integration details belong to the OpenOBSW/OpenSVF schema/adapter review rather than reopening this generic boundary unless they reveal a genuinely generic requirement.

---

## 41. Non-goals

The v0 Integration Result Contract does not define:

```text
Core Mission Model fields or semantics
Projection Profile settings/config schema
OpenOBSW/PUS behavior
OpenSVF behavior
YAMCS behavior
SRDB semantics
XTCE semantics
adapter package discovery
adapter installation
full pre-execution capability discovery
runtime transport/API protocols
verification engine behavior
Studio plugin lifecycle
Core plugin discovery/loading/execution
a marketplace
a generic free-form extension object
semantic-equivalence fingerprinting
```

---

## 42. Final position

The production boundary is:

```text
Core owns mission semantics and emits exact, coherent integration inputs.

Projection Profile owns authored ecosystem-specific projection intent.

Integration Adapter owns target resolution, validation, generation and integration diagnostics.

Integration Result records exactly what that adapter resolved/generated and how it maps back to Core/Profile identity.

External runtime/verification systems retain ownership of their native behavior and evidence semantics.

Studio consumes the same machine-readable Result used by CLI/CI workflows and never reconstructs integration meaning from filenames, names or timestamps.
```
