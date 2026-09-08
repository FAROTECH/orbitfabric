# Evidence Set Manifest Contract

Status: **Candidate generic contract**  
Format: `orbitfabric.evidence_set_manifest` / `0.1-candidate`  
Scope: retained evidence identity, byte integrity and typed correlation

## Purpose

The Evidence Set Manifest is a portable generic index for retained evidence objects.

It answers questions such as:

```text
Which retained evidence objects exist?
Who curated the set?
Who produced each content object?
Which exact bytes are retained?
Which exact Scenario, declared atom, Integration Result, mapping or artifact is correlated?
```

It does not interpret the evidence content.

## Ownership boundary

```text
contract vocabulary / JSON Schema / generic conformance
    OrbitFabric Core

manifest instance and inclusion decisions
    evidence-set curator

subject correlation claims
    evidence-set curator

evidence content and producer-specific meaning
    evidence producer
```

The curator and producer may be the same product, but the contract does not require that.

## Wire identity

```json
{
  "kind": "orbitfabric.evidence_set_manifest",
  "manifest_version": "0.1-candidate"
}
```

The format is candidate. Compatible consumers must not treat it as a stable Mission Data Contract surface until a separate promotion decision exists.

## Minimum manifest shape

```json
{
  "kind": "orbitfabric.evidence_set_manifest",
  "manifest_version": "0.1-candidate",
  "evidence_set": {
    "id": "r1-retained-evidence"
  },
  "curator": {
    "id": "orbitfabric-reference-mission"
  },
  "records": []
}
```

`evidence_set.id` is a curator-owned logical identity. It does not replace exact manifest bytes or evidence content digests.

`curator.id` is required. `version` and `revision` are optional when meaningful to the curator.

## Evidence record

Each record has a set-scoped logical id, a content descriptor and one or more typed subject correlations.

```json
{
  "id": "cosmos-native-runtime",
  "content": {
    "kind": "native_runtime_evidence",
    "producer": {
      "id": "orbitfabric-openc3-cosmos-adapter"
    },
    "reference": {
      "path": "evidence/cosmos-runtime.json",
      "media_type": "application/json",
      "sha256": "<64 lowercase hex characters>"
    }
  },
  "subjects": []
}
```

`content.kind` is producer-owned vocabulary. Core does not assign target-specific semantics to it.

`format_version`, producer `version` / `revision`, and `media_type` are optional.

## Content reference

The initial contract is local and bundle-oriented.

A content reference requires:

```text
bundle-relative path
exact SHA-256 of retained bytes
```

Generic conformance requires normalized forward-slash paths and rejects absolute paths, `.` / `..`, empty path segments and backslash paths.

Bundle verification resolves the path under the declared bundle root and rejects:

```text
path escape
missing/non-file content
SHA-256 mismatch
```

The path is a locator, not identity. Exact content identity is the SHA-256.

## Subject vocabulary

The initial generic subject vocabulary is intentionally narrow.

### Scenario source

```json
{
  "type": "scenario_source",
  "scenario_id": "payload_stop_acquisition_verification",
  "scenario_sha256": "<sha256>"
}
```

### Declared Scenario atom

```json
{
  "type": "scenario_atom",
  "scenario_sha256": "<sha256>",
  "atom_id": "atom-0007"
}
```

Atom correlation scope is:

```text
scenario_sha256 + atom_id
```

This composes directly with the Core Scenario Declaration candidate surface.

### Integration Result

```json
{
  "type": "integration_result",
  "result_sha256": "<sha256>"
}
```

### Integration mapping

```json
{
  "type": "integration_mapping",
  "result_sha256": "<sha256>",
  "mapping_id": "mapping-id"
}
```

### Integration artifact

```json
{
  "type": "integration_artifact",
  "result_sha256": "<sha256>",
  "artifact_id": "artifact-id"
}
```

One evidence record may correlate to several subjects.

## Identity and freshness

The contract intentionally avoids timestamp freshness.

Generic correlation uses exact identities:

```text
Scenario source       scenario id + exact Scenario SHA-256
Scenario atom         Scenario SHA-256 + atom id
Integration Result    exact Result SHA-256
mapping               Result SHA-256 + mapping id
artifact              Result SHA-256 + artifact id
retained content      exact content SHA-256
```

A changed upstream object produces an identity mismatch. Consumers do not need to guess freshness from modification time.

## Failure semantics

A malformed manifest, invalid subject identity, duplicate record id, unsafe path, missing retained file or SHA mismatch is an **Evidence Set conformance/integrity failure**.

That is distinct from any producer-specific evidence payload that happens to contain fields such as:

```text
status
result
passed
failed
warning
```

Core does not interpret those fields generically.

## Explicit non-goals

The manifest does not define:

```text
universal PASS / FAIL
normalized target verdicts
missing / unsupported evidence state machine
timestamp freshness
remote evidence provider protocol
target-specific fields
mutation of Integration Result
Studio-local correlation authority
```

A retained directory may also contain generated artifacts, projection plans, integrity inventories and human documentation. Those files are not evidence merely because they are present. Only records explicitly included by the curator are evidence records.

## Conformance

Core provides reusable conformance in:

```text
orbitfabric.conformance.evidence_set
```

The module separates:

```text
validate_manifest()
    wire schema, unique set-scoped record ids, normalized relative paths

verify_bundle()
    bundle containment, retained file existence, exact SHA-256
```

It can also be invoked as a module:

```bash
python -m orbitfabric.conformance.evidence_set manifest evidence-set.json
python -m orbitfabric.conformance.evidence_set bundle evidence-set.json <bundle-root>
```

## Relationship to Integration Result

Evidence Set Manifest is a separate post-operation artifact.

```text
Integration Result
    immutable operation result/projection provenance

Evidence Set Manifest
    retained evidence correlation and integrity index
```

`Integration Result.evidence[]` may continue to contain integration-owned attestations available when the adapter operation completes. It is not redefined as a future mutable evidence registry.
