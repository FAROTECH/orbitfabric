# Core Integration Input Contract

Status: Architecture candidate  
Contract version: `0.1-candidate`  
Scope: Core-owned machine-readable input boundary for external ecosystem integrations  
Parent architecture issue: #227  
Design issue: #228  
Release dependency: #224

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

---

## 2. Architectural constraints

The Integration Input Contract must preserve these existing OrbitFabric rules:

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

OrbitFabric already exposes multiple machine-readable surfaces.

Stable Core-owned surfaces include:

```text
model_summary.json
entity_index.json
relationship_manifest.json
lint JSON report
```

Current `main` additionally exposes the candidate:

```text
mission_snapshot.json
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

## 4. Canonical input-set roles

### 4.1 Required projection surfaces

A projection-capable loaded input set requires:

```text
mission_snapshot.json
entity_index.json
relationship_manifest.json
lint_report.json
```

Their roles are distinct.

### `mission_snapshot.json`

Role:

```text
complete loaded Mission Model semantics
```

The adapter consumes Mission Model fields from this surface instead of reading Mission Model YAML.

This role is conditional on the release/compatibility decision in #224.

Until #224 resolves Mission Snapshot classification sufficiently for production integration, this contract remains an architecture candidate.

### `entity_index.json`

Role:

```text
canonical indexed entity identity/domain inventory
```

The adapter must use Core-owned entity identity rather than inventing entity records or deriving identities from target naming conventions.

### `relationship_manifest.json`

Role:

```text
canonical admitted Core relationship records
```

The adapter must not reconstruct missing Core relationship semantics from Mission Snapshot fields, naming conventions or generated artifacts unless a future Core contract explicitly changes this boundary.

Unknown additive relationship families must follow the Relationship Manifest compatibility rules. Their semantics must never be guessed.

### `lint_report.json`

Role:

```text
Core-owned semantic lint result and findings
```

Loadability and semantic lint remain different questions.

An Integration Adapter may use lint state as a generation gate, but it must not rewrite Core findings as integration diagnostics.

---

### 4.2 Canonical companion surface

The coherent set should also include:

```text
model_summary.json
```

Role:

```text
domain-level introspection and consistency information
```

`model_summary.json` is useful to downstream inspection and orchestration, but it is not the complete semantic input and must not be used to reconstruct entity semantics.

An adapter implementation must not require model-summary-only information that cannot be obtained through documented Core-owned semantics.

---

## 5. Integration Input Manifest

The input set is described by a small Core-owned manifest:

```text
integration_input_manifest.json
```

The manifest is metadata/provenance only.

It must not duplicate Mission Model semantic payloads.

Conceptual shape:

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
      "role": "mission_snapshot",
      "kind": "orbitfabric.mission_snapshot",
      "format_version": "0.1-candidate",
      "path": "mission_snapshot.json",
      "sha256": "..."
    },
    {
      "role": "entity_index",
      "kind": "orbitfabric.entity_index",
      "format_version": "0.1",
      "path": "entity_index.json",
      "sha256": "..."
    },
    {
      "role": "relationship_manifest",
      "kind": "orbitfabric.relationship_manifest",
      "format_version": "0.1-candidate",
      "path": "relationship_manifest.json",
      "sha256": "..."
    },
    {
      "role": "lint_report",
      "kind": "orbitfabric-lint",
      "format_version": "v1",
      "path": "lint_report.json",
      "sha256": "..."
    },
    {
      "role": "model_summary",
      "kind": "orbitfabric.model_summary",
      "format_version": "0.1",
      "path": "model_summary.json",
      "sha256": "..."
    }
  ],
  "input_set_sha256": "..."
}
```

The exact JSON schema remains candidate until #228 is accepted.

---

## 6. Surface-version normalization

Different Core surfaces currently expose different version-field names.

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

It records the Core-declared compatibility identifier that an Integration Adapter must negotiate for that role.

For stable report families that do not currently expose an independent report-format version field, such as the lint JSON report, the manifest may expose a Core-governed compatibility label such as:

```text
v1
```

This label is part of the Integration Input Contract, not a reinterpretation of the lint report's top-level package `version` field.

---

## 7. Compatibility negotiation

An Integration Adapter must negotiate compatibility using:

```text
input-set kind
input-set version
surface role
surface kind / report identity
surface format version
supported typed records where applicable
```

`orbitfabric_version` is provenance and support information.

It must not be treated as the only compatibility key.

A compatible consumer should:

- tolerate unknown additive fields where the underlying Core surface contract permits additive evolution;
- reject missing fields that are required by the supported contract;
- consume only relationship families whose semantics it understands;
- safely ignore or preserve unknown additive relationship families according to the Relationship Manifest contract;
- reject incompatible required surface versions;
- never guess unknown semantic meaning.

No raw-YAML fallback is permitted when a required Core surface is incompatible.

---

## 8. Coherent generation invariant

The canonical Integration Input Set must be produced from one logical Core load/lint operation.

Conceptually:

```text
load Mission Model once
        ↓
structural validation
        ↓
semantic lint
        ↓
Mission Snapshot
        ↓
Entity Index
        ↓
Relationship Manifest
        ↓
Lint Report
        ↓
Model Summary
        ↓
compute surface digests
        ↓
write Integration Input Manifest LAST
```

The manifest is written last deliberately.

Consumer invariant:

> A directory containing some integration-input files but no valid Integration Input Manifest is not a coherent Integration Input Set.

This prevents a partially written export from being treated as complete merely because some expected file names exist.

Implementation may use temporary files/directories and atomic replacement where practical, but the public contract is the manifest-last completeness rule.

---

## 9. Proposed CLI boundary

A future implementation may expose a command conceptually equivalent to:

```bash
orbitfabric export integration-input-set <mission_dir> \
  --output-dir <dir>
```

The exact command name and options remain subject to review under the v1 CLI compatibility contract.

The command would produce the coherent set as one Core-owned operation.

An external Integration Adapter may invoke this CLI before projection.

The adapter must not depend on OrbitFabric internal Python module APIs as a substitute for this public boundary.

---

## 10. Load and lint state model

The input contract preserves separate machine-readable states.

```text
process exit status
!=
manifest availability
!=
load_result
!=
lint_result
!=
adapter compatibility result
```

### 10.1 Successful load

```text
load_result = loaded
```

The Mission Snapshot contains the complete loaded `MissionModel`.

Entity Index, Relationship Manifest and Model Summary may be produced from that loaded model.

Semantic lint is then represented separately.

### 10.2 Structural load failure

```text
load_result = failed
```

The Mission Snapshot follows its existing failure contract:

```text
mission = null
model = null
structured diagnostics present
```

Core must not expose a partial semantic Mission Model.

The Integration Input Manifest should still be written when technically possible so a downstream caller can inspect the failure state.

Loaded-model-dependent surfaces must not be synthesized from partial YAML.

An Integration Adapter must not proceed with semantic projection.

### 10.3 Loaded model with lint errors

A valid loaded model may coexist with:

```text
lint_result = failed
```

This is not structural load failure.

The default production projection/generation posture should remain consistent with existing Core generation commands: Core lint errors block generation.

A future adapter may offer an inspection-only mode, but such a mode must preserve the Core lint result and must not claim production-ready projection.

---

## 11. Diagnostic ownership

Diagnostic authority remains explicit.

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

but the diagnostic must reference the Core result rather than copying or rewriting Core findings into a new authority domain.

Adapter diagnostics must never be injected into Core lint output.

---

## 12. Provenance and digests

Each surface record contains a SHA-256 digest of the exact serialized surface bytes referenced by the manifest.

This provides:

```text
exact input reproducibility
artifact-to-input provenance
later staleness comparison
corruption/change detection
```

The input set additionally contains an `input_set_sha256` derived deterministically from the manifest's compatibility/provenance fields and ordered surface records, excluding the `input_set_sha256` field itself.

The exact canonical JSON encoding used for that calculation must be specified before implementation.

Timestamps are not required for identity and must never be the primary staleness mechanism.

`mission_dir` may remain useful provenance, but an absolute path is not semantic identity and must not participate in portable equivalence decisions.

Surface paths recorded by the Integration Input Manifest should be relative to the manifest location unless a later contract explicitly requires another URI scheme.

---

## 13. No semantic Mission fingerprint in v0

The v0 contract deliberately does **not** define a canonical Mission semantic fingerprint independent of serialization.

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

The first production contract therefore uses:

```text
exact per-surface SHA-256
+
input-set SHA-256
```

This safely answers:

```text
Were these exact Core integration inputs used?
```

A future canonical semantic fingerprint may be introduced through a separate reviewed compatibility decision if experience proves that semantic-equivalence detection is required.

---

## 14. Missing or incompatible surfaces

The canonical manifest must make surface availability explicit.

A required surface that is missing, unreadable, digest-invalid or version-incompatible blocks projection.

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

## 15. Inputs deliberately excluded from the projection contract

The first Core Integration Input Set does not require:

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

## 16. Consumer algorithm

A projection-capable Integration Adapter should conceptually perform:

```text
1. Load integration_input_manifest.json.
2. Verify kind and input_set_version.
3. Verify required surface roles exist.
4. Verify each required surface SHA-256.
5. Verify supported role/kind/format_version combinations.
6. Verify Mission identity consistency exposed by Core.
7. Inspect load_result.
8. Stop if load_result != loaded.
9. Inspect lint_result.
10. Apply the adapter's documented generation gate without rewriting Core findings.
11. Load Mission Snapshot semantics.
12. Resolve authored Profile references against Entity Index identities.
13. Consume admitted Core relationships from Relationship Manifest.
14. Perform projection-specific validation.
15. Produce extension-owned Integration Result and target artifacts.
```

At no point does the adapter reconstruct OrbitFabric semantics from raw YAML.

---

## 17. Relationship to Projection Profiles

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

---

## 18. Relationship to Studio

Studio may orchestrate generation of the Core Integration Input Set or inspect it through a future integration plugin.

Studio must not:

```text
parse Mission Model YAML to fill missing integration inputs
invent entity identities
infer missing Core relationships
replace Core lint findings
calculate integration provenance from timestamps alone
```

The same input contract should be usable from CLI-only workflows and Studio workflows.

---

## 19. Relationship to ecosystem-specific tools

The Core Integration Input Contract contains no OpenOBSW, OpenSVF, YAMCS, PUS, SRDB or other ecosystem-specific semantics.

Target-specific mapping belongs to the Projection Profile and Integration Adapter.

The OpenOBSW/OpenSVF PoC is evidence used to derive this architecture; it is not encoded into the Core contract.

---

## 20. Compatibility and release gate

This document is an architecture candidate.

It must not be described as a stable production contract until #224 resolves Mission Snapshot classification sufficiently for the role defined here.

Before implementation/freeze, #228 must resolve:

```text
exact manifest schema
exact surface required/optional rules
exact lint format-version label
exact failure-surface availability rules
exact input_set_sha256 canonical encoding
exact CLI command/options
required regression/golden protection
release classification
```

---

## 21. Test requirements for implementation

A future implementation should cover at least:

```text
valid loaded mission + lint passed
valid loaded mission + lint warnings
valid loaded mission + lint failed
structural load failure with machine-readable manifest
missing required surface detection
surface digest mismatch detection
unsupported input-set version
unsupported Mission Snapshot version
unsupported Entity Index version
unknown additive Relationship Manifest family behavior
manifest written last / incomplete-set rejection
relative-path portability
repeat generation determinism
no raw-YAML fallback in the reference adapter
```

Golden protection should be considered for the manifest envelope and required role records once the candidate contract is accepted.

---

## 22. Non-goals

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
```

---

## 23. Final position

The intended production boundary is:

```text
OrbitFabric Core owns mission semantics.

Core emits one coherent, versioned, digest-addressable Integration Input Set.

External adapters consume that set and never reconstruct OrbitFabric semantics from raw source files.

Projection Profiles own ecosystem-specific authored mapping choices.

Integration Adapters own target projection, integration diagnostics and extension-owned outputs.

Studio may visualize and orchestrate the same contracts without becoming a semantic authority.
```
