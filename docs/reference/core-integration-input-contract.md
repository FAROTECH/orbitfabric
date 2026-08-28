# Core Integration Input Contract

Status: **Stable Core-owned integration input contract from v1.2.0**  
Contract version: `0.1-candidate`  
Scope: Core-owned machine-readable input boundary for external ecosystem integrations  
Parent architecture issue: #227  
Design issue: #228  
Release classification: v1.2.0 / #224

---

## 1. Purpose

The Core Integration Input Contract defines the machine-readable boundary between OrbitFabric Core and an external ecosystem Integration Adapter.

It answers:

```text
What exact Core-owned inputs may an external integration consume,
and how can it prove that those inputs are compatible and coherent?
```

The contract exists so an Integration Adapter does not need to parse OrbitFabric Mission Model YAML or reconstruct OrbitFabric semantics privately.

The intended boundary is:

```text
Mission Model
    ↓
OrbitFabric Core
    ↓
coherent Core Integration Input Set
    ↓
external Integration Adapter
    ↓
Projection Profile + target-specific projection
```

The Mission Model remains the source of truth.

The Integration Input Set is derived, read-only and non-authoritative.

From OrbitFabric v1.2.0, this documented Core input boundary is a stable v1.x compatibility commitment. The existing wire identifier remains `0.1-candidate`; OrbitFabric stability classification and format-version text are intentionally independent concepts.

---

## 2. Architectural constraints

The Integration Input Contract preserves these existing OrbitFabric rules:

```text
Mission Model semantics are Core-owned.
Core-owned structured surfaces are the downstream inspection boundary.
External integrations must not reconstruct semantics from raw YAML.
Core diagnostics remain Core-owned.
Integration diagnostics remain extension-owned.
Core does not dynamically load or execute ecosystem adapters.
Studio does not become a second semantic authority.
```

This contract does not weaken ADR-0015.

It introduces no plugin discovery, plugin loading or in-process adapter execution.

---

## 3. Why a coherent input set is required

OrbitFabric exposes multiple machine-readable Core-owned surfaces.

Stable Core-owned surfaces relevant to this boundary include:

```text
mission_snapshot.json
model_summary.json
entity_index.json
relationship_manifest.json for admitted families
lint JSON report
```

Independently generated files are not sufficient as a production integration contract because they may have been produced:

```text
from different Mission Model revisions
from different OrbitFabric versions
from different load/lint operations
with different surface compatibility assumptions
```

A production adapter must not infer coherence from:

```text
matching file names
matching timestamps
matching mission directory paths
matching Mission IDs alone
matching model_version alone
```

The canonical production boundary is therefore a **Core Integration Input Set** produced by Core as one logical operation.

---

## 4. Frozen canonical input-set roles

### 4.1 Required projection surfaces

A loaded input set is projection-capable only when these four roles are available and compatible:

```text
mission_snapshot
entity_index
relationship_manifest
lint_report
```

Their canonical files are:

```text
mission_snapshot.json
entity_index.json
relationship_manifest.json
lint_report.json
```

#### `mission_snapshot`

Role:

```text
complete loaded Mission Model semantics
```

The adapter consumes Mission Model fields from this surface instead of reading Mission Model YAML.

From v1.2.0, Mission Snapshot is a stable Core-owned integration/inspection surface for its documented envelope, failure behavior, boundary semantics and complete-loaded-model role. Its format identifier remains `0.1-candidate` for compatibility with the already reference-proven producer/consumer chain.

The stable Snapshot commitment does not freeze the complete serialized `model` object byte-for-byte. The `model` payload remains a faithful serialization of the loaded Mission Model and follows Mission Model compatibility rules.

#### `entity_index`

Role:

```text
canonical indexed entity identity/domain inventory
```

The adapter must use Core-owned entity identity rather than inventing entity records or deriving identities from target naming conventions.

#### `relationship_manifest`

Role:

```text
canonical admitted Core relationship records
```

The adapter must not reconstruct missing Core relationship semantics from Mission Snapshot fields, naming conventions or generated artifacts unless a future Core contract explicitly changes this boundary.

Unknown additive relationship families must follow the Relationship Manifest compatibility rules. Their semantics must never be guessed.

The seven FDIR relationship families classified in v1.2.0 are additive stable-compatible admitted families; they do not redefine the original v1 relationship contract.

#### `lint_report`

Role:

```text
Core-owned semantic lint result and findings
```

Loadability and semantic lint remain different questions.

The lint report is required because a production adapter must know the Core semantic-validation state before projection/generation.

An Integration Adapter may use lint state as a generation gate, but it must not rewrite Core findings as integration diagnostics.

---

### 4.2 Canonical companion surface

The input set also defines one canonical companion role:

```text
model_summary
```

Canonical file:

```text
model_summary.json
```

Role:

```text
domain-level introspection and consistency information
```

`model_summary` is useful to downstream inspection, orchestration and UI composition, but it is not required for semantic projection.

Therefore:

```text
model_summary unavailable
    -> input set is degraded for introspection
    -> projection may still proceed when every required role is valid
```

An adapter must not depend on model-summary-only information that cannot be obtained through documented Core-owned semantics.

---

## 5. Frozen Integration Input Manifest envelope

The input set is described by a small Core-owned manifest:

```text
integration_input_manifest.json
```

The manifest is metadata/provenance only.

It must not duplicate Mission Model semantic payloads.

The stable v1.2 contract retains the already reference-proven v0 envelope and wire identifier:

```json
{
  "kind": "orbitfabric.integration_input_set",
  "input_set_version": "0.1-candidate",
  "orbitfabric_version": "1.x",
  "mission": {
    "id": "demo-3u",
    "model_version": "0.1.0"
  },
  "load_result": "loaded",
  "lint_result": "passed",
  "surfaces": [
    {
      "role": "entity_index",
      "requirement": "required",
      "status": "available",
      "kind": "orbitfabric.entity_index",
      "format_version": "0.1",
      "path": "entity_index.json",
      "sha256": "...",
      "unavailable_reason": null
    },
    {
      "role": "lint_report",
      "requirement": "required",
      "status": "available",
      "kind": "orbitfabric-lint",
      "format_version": "v1",
      "path": "lint_report.json",
      "sha256": "...",
      "unavailable_reason": null
    },
    {
      "role": "mission_snapshot",
      "requirement": "required",
      "status": "available",
      "kind": "orbitfabric.mission_snapshot",
      "format_version": "0.1-candidate",
      "path": "mission_snapshot.json",
      "sha256": "...",
      "unavailable_reason": null
    },
    {
      "role": "model_summary",
      "requirement": "companion",
      "status": "available",
      "kind": "orbitfabric.model_summary",
      "format_version": "0.1",
      "path": "model_summary.json",
      "sha256": "...",
      "unavailable_reason": null
    },
    {
      "role": "relationship_manifest",
      "requirement": "required",
      "status": "available",
      "kind": "orbitfabric.relationship_manifest",
      "format_version": "0.1-candidate",
      "path": "relationship_manifest.json",
      "sha256": "...",
      "unavailable_reason": null
    }
  ],
  "input_set_sha256": "..."
}
```

The `surfaces` array is emitted in ascending lexical order by `role` for deterministic serialization.

Every canonical role has exactly one surface record.

A surface record is never silently omitted merely because the surface could not be produced.

---

## 6. Surface record contract

Every surface record contains:

```text
role
requirement
status
kind
format_version
path
sha256
unavailable_reason
```

### `requirement`

Allowed values:

```text
required
companion
```

Meaning:

```text
required
    -> unavailable/incompatible blocks semantic projection

companion
    -> unavailable/incompatible degrades inspection/orchestration
       but does not by itself block projection
```

### `status`

Allowed values:

```text
available
unavailable
```

### Available record

When:

```text
status = available
```

then:

```text
path                  = non-null relative path
sha256                = non-null lowercase hexadecimal SHA-256
unavailable_reason    = null
```

### Unavailable record

When:

```text
status = unavailable
```

then:

```text
path                  = null
sha256                = null
unavailable_reason    = non-null controlled value
```

`kind` and `format_version` remain present even for an unavailable record because they identify the contract role Core attempted to produce.

Initial controlled `unavailable_reason` values are:

```text
load_failed
generation_failed
```

A later additive reason may be introduced only with documented meaning.

Consumers must not infer a reason from file-system state when the manifest already declares one.

---

## 7. Surface-version normalization

Different Core surfaces expose different native version-field names.

Examples include:

```text
snapshot_version
index_version
manifest_version
summary_version
version
```

The Integration Input Manifest normalizes the relevant compatibility identifier into:

```text
surfaces[].format_version
```

This does not replace or change the version field inside the underlying surface.

It records the Core-declared compatibility identifier that an Integration Adapter negotiates for that role.

### Lint JSON compatibility label

The stable lint JSON report does not currently expose an independent report-format version field. Its top-level:

```text
version
```

is the OrbitFabric package version, not a report-schema identifier.

For the Core Integration Input Contract, the lint JSON shape stabilized from the v1.0 Mission Data Contract baseline is identified by the normalized compatibility label:

```text
v1
```

Thus the role record is:

```json
{
  "role": "lint_report",
  "kind": "orbitfabric-lint",
  "format_version": "v1"
}
```

`v1` is an Integration Input Contract compatibility label.

It does not reinterpret the lint report's native package `version` field.

A future breaking lint JSON contract would require a new normalized label such as `v2`; an additive change compatible with the documented v1 lint contract need not do so.

---

## 8. Compatibility negotiation

An Integration Adapter must negotiate compatibility using:

```text
input-set kind
input-set version
surface role
surface kind/report identity
surface format version
supported typed records where applicable
```

`orbitfabric_version` is provenance and support information.

It must not be treated as the only compatibility key.

A compatible consumer must:

- tolerate unknown additive fields where the underlying Core surface contract permits additive evolution;
- reject missing fields required by the supported contract;
- consume only relationship families whose semantics it understands;
- safely ignore or preserve unknown additive relationship families according to the Relationship Manifest contract;
- reject incompatible required surface versions;
- never guess unknown semantic meaning.

No raw-YAML fallback is permitted when a required Core surface is incompatible.

---

## 9. Coherent generation invariant

The canonical Integration Input Set is produced from one logical Core load/lint operation.

Conceptually:

```text
load Mission Model once
        ↓
structural validation
        ↓
if loaded: semantic lint
        ↓
produce all technically valid Core surfaces
        ↓
compute exact surface digests
        ↓
record unavailable roles explicitly
        ↓
compute input-set digest
        ↓
write Integration Input Manifest LAST
```

The manifest is written last deliberately.

Consumer invariant:

> A directory containing integration-input files but no valid Integration Input Manifest is not a coherent Integration Input Set.

Implementation may use temporary files/directories and atomic replacement where practical, but the public contract is the manifest-last completeness rule.

---

## 10. Stable CLI boundary

The stable v1.2 CLI shape is:

```bash
orbitfabric export integration-input-set <mission_dir> \
  [--output-dir <dir>]
```

When `--output-dir` is omitted, the default is:

```text
<mission_workspace>/generated/reports/integration_input/
```

The canonical file names inside that directory are:

```text
integration_input_manifest.json
mission_snapshot.json
entity_index.json
relationship_manifest.json
lint_report.json
model_summary.json
```

The command does not expose `--json` because the output is a coherent multi-file set.

The v1.2 command does not expose `--warnings-as-errors`.

Warnings remain represented by:

```text
lint_result = passed_with_warnings
```

A stricter workflow policy may be imposed by a caller or adapter without changing the Core semantic lint result.

The command is implemented, reference-proven and classified as the stable Core integration-input workflow from v1.2.0.

The adapter must not depend on OrbitFabric internal Python module APIs as a substitute for this public boundary.

---

## 11. Frozen load/lint state model

The input contract preserves separate machine-readable states:

```text
process exit status
!=
manifest availability
!=
load_result
!=
lint_result
!=
surface availability
!=
adapter compatibility result
```

Allowed `load_result` values:

```text
loaded
failed
```

Allowed `lint_result` values:

```text
passed
passed_with_warnings
failed
not_run
```

`not_run` is valid only when semantic lint could not be executed because the Mission Model was not successfully loaded.

---

## 12. Failure-state matrix

The stable producer/consumer behavior is:

| Condition | Manifest | Mission Snapshot | Entity Index | Relationship Manifest | Lint Report | Model Summary | CLI exit | Projection |
|---|---|---|---|---|---|---|---|---|
| loaded + lint passed | available | available | available | available | available | available | `0` | allowed |
| loaded + lint warnings | available | available | available | available | available | available | `0` | allowed; warnings preserved |
| loaded + lint failed | available | available | available | available | available | available | non-zero | blocked by default |
| structural load failed | available when technically possible | failed-envelope available | unavailable | unavailable | unavailable | unavailable | non-zero | blocked |
| required-surface generation failed after load | available when technically possible | per-role state | per-role state | per-role state | per-role state | per-role state | non-zero | blocked |
| companion-only generation failed | available when technically possible | available | available | available | available | unavailable | non-zero | allowed, degraded |
| manifest write failed | unavailable/invalid | partial files may exist | partial files may exist | partial files may exist | partial files may exist | partial files may exist | non-zero | rejected as incoherent |

### Structural load failure envelope

When structural loading fails:

```text
load_result = failed
lint_result = not_run
mission = null
```

`mission_snapshot` is still `available` when Core can write its documented failed envelope:

```text
Mission Snapshot result = failed
mission = null
model = null
structured Core load diagnostics present
```

The remaining loaded-model-dependent roles are explicitly represented as:

```text
status = unavailable
unavailable_reason = load_failed
```

Example:

```json
{
  "kind": "orbitfabric.integration_input_set",
  "input_set_version": "0.1-candidate",
  "orbitfabric_version": "1.x",
  "mission": null,
  "load_result": "failed",
  "lint_result": "not_run",
  "surfaces": [
    {
      "role": "entity_index",
      "requirement": "required",
      "status": "unavailable",
      "kind": "orbitfabric.entity_index",
      "format_version": "0.1",
      "path": null,
      "sha256": null,
      "unavailable_reason": "load_failed"
    }
  ],
  "input_set_sha256": "..."
}
```

Core must not expose a partial semantic Mission Model and must not synthesize loaded-model surfaces from partial YAML.

---

## 13. Diagnostic ownership

Diagnostic authority remains explicit:

```text
Core structural/load diagnostic
!=
Core semantic lint diagnostic
!=
Integration Adapter diagnostic
!=
external runtime/verification diagnostic
```

An adapter may produce an integration diagnostic such as:

```text
projection blocked because Core lint result is failed
```

but it must reference the Core result rather than copying or rewriting Core findings into a new authority domain.

Adapter diagnostics must never be injected into Core lint output.

The Integration Input Manifest does not duplicate diagnostic arrays.

It points consumers to the Core-owned surfaces whose responsibility already includes those diagnostics:

```text
mission_snapshot -> structural/load diagnostics
lint_report      -> semantic lint findings
```

---

## 14. Exact per-surface digest

For every available role:

```text
surfaces[].sha256
```

is the lowercase hexadecimal SHA-256 of the exact serialized bytes referenced by `surfaces[].path`.

This provides:

```text
exact input identity
artifact-to-input provenance
later staleness comparison
corruption/change detection
```

Because this is an exact-byte digest, independently regenerated surfaces may differ when their serialized provenance differs even if the underlying Mission Model semantics are equivalent.

The contract intentionally does not claim cross-generation semantic equivalence.

Moving an already-generated input set without modifying its files does not invalidate these digests because manifest paths are relative to the manifest location.

---

## 15. Frozen `input_set_sha256` algorithm

`input_set_sha256` fingerprints the coherent input-set contract/provenance state.

The producer constructs a **digest payload** from the manifest containing exactly:

```text
kind
input_set_version
orbitfabric_version
mission
load_result
lint_result
surfaces[]
```

For each surface record, the digest payload contains:

```text
role
requirement
status
kind
format_version
sha256
unavailable_reason
```

The digest payload deliberately excludes:

```text
surfaces[].path
input_set_sha256
file timestamps
filesystem metadata
absolute source/workspace paths not otherwise part of a surface digest
```

Before hashing:

1. `surfaces` records are sorted in ascending lexical order by `role`;
2. the digest payload is serialized using **RFC 8785 JSON Canonicalization Scheme (JCS)**;
3. `input_set_sha256` is the lowercase hexadecimal SHA-256 of the resulting UTF-8 canonical bytes.

Conceptually:

```text
manifest
  ↓ select digest fields
  ↓ sort surfaces by role
  ↓ RFC 8785 / JCS
  ↓ UTF-8 bytes
  ↓ SHA-256
input_set_sha256
```

This avoids a Python-specific or whitespace-sensitive manifest fingerprint and makes the algorithm reproducible by integration adapters implemented in other languages.

---

## 16. No semantic Mission fingerprint

The contract deliberately does **not** define a canonical Mission semantic fingerprint independent of serialized Core surfaces.

A semantic fingerprint would require a compatibility-sensitive canonicalization policy for concepts such as:

```text
object ordering
collections with stable entity IDs
collections without stable entity IDs
controlled values
aliases
optional/defaulted fields
future additive fields
```

Incorrect canonicalization could create false semantic equivalence or false semantic difference.

The stable v1.2 contract therefore uses:

```text
exact per-surface SHA-256
+
input-set SHA-256
```

This safely answers:

```text
Were these exact Core integration inputs used?
```

It does not answer:

```text
Are two independently generated input sets semantically equivalent?
```

A future canonical semantic fingerprint may be introduced only through a separate reviewed compatibility decision.

---

## 17. Missing, corrupt or incompatible surfaces

A required role that is:

```text
unavailable
missing from the manifest
duplicated in the manifest
unreadable
digest-invalid
kind-incompatible
format-version-incompatible
```

blocks projection.

A companion role with those conditions degrades companion functionality but does not by itself block projection.

The adapter must not recover by:

```text
parsing Mission Model YAML
scanning generated Markdown
scanning generated C/C++ artifacts
scanning ground dictionaries
inferring relationships from Mission Snapshot
inferring relationships from names
using Studio state
```

The boundary remains Core-owned.

---

## 18. Inputs deliberately excluded from the projection contract

The Core Integration Input Set does not require:

```text
dashboard_summary.json
coverage_summary.json
scenario_run_index.json
simulation JSON reports
runtime_contract_manifest.json
ground_contract_manifest.json
generated runtime bindings
generated ground dictionaries
generated Markdown documentation
Studio state
OpenOBSW artifacts
OpenSVF artifacts
YAMCS state
```

These belong to dashboard/evidence/runtime/integration-output concerns, not to the minimum semantic projection boundary.

---

## 19. Frozen consumer algorithm

A projection-capable Integration Adapter performs conceptually:

```text
1. Load integration_input_manifest.json.
2. Verify kind and input_set_version.
3. Verify exactly one record exists for every canonical role.
4. Verify input_set_sha256 using the frozen JCS algorithm.
5. Inspect load_result.
6. Stop if load_result != loaded.
7. Verify every required role has status = available.
8. Verify each available surface SHA-256.
9. Verify supported role/kind/format_version combinations.
10. Verify Mission identity consistency exposed by Core surfaces.
11. Inspect lint_result.
12. Apply the documented generation gate without rewriting Core findings.
13. Load Mission Snapshot semantics.
14. Resolve authored Profile references against Entity Index identities.
15. Consume admitted Core relationships from Relationship Manifest.
16. Optionally consume Model Summary for introspection/orchestration.
17. Perform projection-specific validation.
18. Produce extension-owned Integration Result and target artifacts.
```

At no point does the adapter reconstruct OrbitFabric semantics from raw YAML.

---

## 20. Relationship to Projection Profiles

The Projection Profile contract depends on this input contract.

A Profile references OrbitFabric semantic entities through Core-owned identities exposed by the input set.

The Profile must not copy Core semantic fields merely to compensate for unavailable adapter input.

The intended layering is:

```text
Core Integration Input Set
        ↓
Projection Profile
        ↓
Integration Adapter
        ↓
Integration Result
```

The Projection Profile contract remains independently versioned and extension-owned. Stabilizing the Core input boundary in v1.2.0 does not promote Profile target semantics into Core.

---

## 21. Relationship to Studio

Studio may orchestrate generation of the Core Integration Input Set or inspect it through generic integration surfaces.

Studio must not:

```text
parse Mission Model YAML to fill missing integration inputs
invent entity identities
infer missing Core relationships
replace Core lint findings
calculate integration provenance from timestamps alone
```

The same input contract is usable from CLI-only workflows, CI workflows and Studio workflows.

Studio Phase 0B has independently exercised the real reference Integration Package against this Core boundary, demonstrating that a downstream consumer does not need private Core or raw-YAML semantics.

---

## 22. Relationship to ecosystem-specific tools

The Core Integration Input Contract contains no OpenOBSW, OpenSVF, YAMCS, PUS, SRDB or other ecosystem-specific semantics.

Target-specific mapping belongs to the Projection Profile and Integration Adapter.

The OpenOBSW/OpenSVF PoC is evidence used to derive and reference-prove this architecture; it is not encoded into the Core contract.

---

## 23. Regression-protection requirements

The stable contract is protected at multiple levels.

### 23.1 Manifest contract fixture

Maintain a reviewed fixture for a successful loaded mission that protects:

```text
top-level field names
kind
input_set_version
canonical role set
requirement values
status values
kind/format_version mapping
relative-path rule
controlled result values
```

Fields expected to vary between releases or generated content, such as `orbitfabric_version` and SHA-256 values, may be normalized by the fixture helper rather than hard-coded as false stability commitments.

### 23.2 Failure-envelope fixture

Maintain a structural-load-failure fixture protecting:

```text
mission = null
load_result = failed
lint_result = not_run
failed Mission Snapshot availability
loaded-model role unavailability
unavailable_reason = load_failed
no partial Mission Model reconstruction
```

### 23.3 Digest algorithm vector

Maintain at least one fixed synthetic digest test vector for:

```text
digest payload
RFC 8785 canonical bytes
expected SHA-256
```

This vector must not depend on the current OrbitFabric package version or filesystem paths.

### 23.4 End-to-end determinism

Generate the same input set twice from the same mission, Core version and workspace state and verify:

```text
same surface bytes
same surface digests
same input_set_sha256
```

Existing regression protection for underlying stable surfaces remains authoritative for those surfaces and is not replaced by the input-set tests.

From v1.2.0, Mission Snapshot additionally has a selected golden signature protecting contract-significant envelope/boundary fields and representative serialization invariants without freezing the complete Mission Model payload.

The original v1 Relationship Manifest golden remains unchanged; dedicated FDIR extension tests protect the additive v1.2 families.

---

## 24. Implementation test matrix

The implementation must cover at least:

```text
valid loaded mission + lint passed
valid loaded mission + lint warnings
valid loaded mission + lint failed
structural load failure with machine-readable manifest
companion-only generation failure
required-surface generation failure
missing required surface detection
duplicate canonical role detection
surface digest mismatch detection
input-set digest mismatch detection
unsupported input-set version
unsupported Mission Snapshot version
unsupported Entity Index version
unknown additive Relationship Manifest family behavior
lint format label v1 behavior
manifest written last / incomplete-set rejection
relative-path relocation of an already-generated set
repeat generation determinism
RFC 8785 digest test vector
no raw-YAML fallback in the reference adapter
```

The current producer and reference-adapter handshake exercise these invariants through CI, and the v1.2 release gate requires the full Core CI matrix to remain green on the exact release head.

---

## 25. Compatibility and release classification

The following contract points are stable compatibility commitments from v1.2.0:

```text
required surface roles
companion surface role
manifest envelope and surface-record fields
lint format-version label
load/lint result vocabularies
failure-surface availability behavior
per-surface digest rule
input_set_sha256 canonical algorithm
CLI command/options/default path
manifest-last coherence rule
consumer no-raw-YAML fallback rule
regression/golden strategy
```

Release gate #224 is resolved by the v1.2 Integration Input Stability Decision.

The existing contract identifier remains:

```text
input_set_version = 0.1-candidate
```

This identifier is not a statement that the v1.2 stability classification is provisional. It is retained to preserve compatibility with the already implemented and reference-proven producer/consumer chain.

Any future breaking change to the stable semantics above requires an explicit compatibility decision, release note and new format/version identity as appropriate.

---

## 26. Non-goals

This contract does not define:

```text
Projection Profile schema
Integration Result schema
target numeric allocation semantics
PUS mappings
SRDB generation
XTCE generation
OpenOBSW integration behavior
OpenSVF integration behavior
YAMCS behavior
runtime orchestration
verification execution
Studio plugin lifecycle
plugin discovery/loading/execution
new Mission Model fields
new Mission Model semantics
semantic equivalence fingerprinting
```

---

## 27. Final position

The stable v1.2 Core boundary is:

```text
OrbitFabric Core owns mission semantics.

Core emits one coherent, versioned, digest-addressable Integration Input Set.

Mission Snapshot provides complete loaded semantics through its stable v1.2 role.
Entity Index provides canonical entity identity.
Relationship Manifest provides admitted Core relationships.
Lint Report provides Core semantic-validation state.
Model Summary is a non-blocking introspection companion.

The manifest records every canonical role explicitly, including unavailable states.

Exact surface bytes are SHA-256 addressed.
The coherent input set is SHA-256 addressed through RFC 8785 canonical JSON.

External adapters consume that set and never reconstruct OrbitFabric semantics from raw source files.

Projection Profiles own ecosystem-specific authored mapping choices.

Integration Adapters own target projection, integration diagnostics and extension-owned outputs.

Studio may visualize and orchestrate the same contracts without becoming a semantic authority.
```
