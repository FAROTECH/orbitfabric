# Golden Output and Regression Confidence Policy

Status: Active v1.x policy through v1.2.0  
Scope: regression confidence and selected golden-signature protection  
Applies to: stable and candidate structured surfaces, reports and generated artifacts after v1.0.0

OrbitFabric protects contract meaning selectively. Not every reproducible output should become a committed golden file.

## 1. Purpose

This policy separates:

```text
CI-generated evidence
committed golden signatures
candidate future golden targets
human-reviewable generated artifacts
disposable generated artifacts
internal test assets
```

A golden baseline is useful only when it protects a meaningful public compatibility surface.

A golden baseline is harmful when it freezes incidental formatting, ordering, prose or implementation detail that is not part of the contract.

## 2. Current CI confidence baseline

The Core CI pipeline includes representative checks such as:

```text
ruff check .
pytest
orbitfabric lint examples/demo-3u/mission/
orbitfabric gen docs examples/demo-3u/mission/
orbitfabric gen data-flow examples/demo-3u/mission/
orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml
orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml
mkdocs build --strict
```

CI also regenerates and uploads representative reports, logs and generated documentation.

These checks provide regression confidence. They do not make every generated artifact a golden compatibility baseline.

## 3. Terminology

### Generated evidence

Output produced during CI or local validation to demonstrate that the toolchain still behaves correctly.

Examples:

```text
generated/reports/*.json
generated/logs/*
generated/docs/*
```

### Golden output

A deliberately preserved expected output used for regression comparison because the output represents a meaningful public contract.

### Golden signature

A reduced selection of contract-significant fields from a larger output.

This is OrbitFabric's preferred strategy when full-file equality would freeze unrelated formatting or additive data.

### Confidence anchor

A command, test or output that raises release confidence without necessarily being a committed golden baseline.

`mkdocs build --strict` is a confidence anchor, not a golden output.

## 4. v1.0 golden signatures

The original v1.0 stable Core surfaces are protected by selected golden signatures:

```text
tests/golden/demo_3u_core_surfaces/model_summary_contract_signature.json
tests/golden/demo_3u_core_surfaces/entity_index_contract_signature.json
tests/golden/demo_3u_core_surfaces/relationship_manifest_contract_signature.json
```

Regression tests:

```text
tests/test_v1_golden_core_surfaces.py
```

These signatures protect selected meaning such as surface identity, mission identity, boundary flags, domain counts, entity IDs, relationship families and selected records.

They intentionally do not freeze full JSON files, absolute paths, terminal wording, Markdown prose, generated C++ formatting or generated ground dictionary formatting.

## 5. v1.2 Mission Snapshot golden signature

v1.2.0 adds a selected Mission Snapshot contract signature:

```text
tests/golden/demo_3u_core_surfaces/mission_snapshot_contract_signature.json
```

Regression test:

```text
tests/test_v12_mission_snapshot_golden.py
```

The Snapshot golden protects contract-significant semantics such as:

```text
snapshot identity and format token
result and mission identity
boundary flags
required top-level Mission Model domains
selected serialization invariants
representative telemetry identities
```

It deliberately does not freeze the entire serialized `model` payload byte-for-byte.

That distinction is essential. Mission Snapshot is stable for its documented envelope, boundary semantics and faithful complete-loaded-model role, while the nested Mission Model may evolve additively where the Mission Model Stability Contract permits it.

## 6. Relationship Manifest regression strategy

The original v1 Relationship Manifest golden remains unchanged.

The seven FDIR relationship families admitted in v1.2 are protected by dedicated tests rather than by rewriting the historical original-v1 golden signature.

This preserves two independent guarantees:

```text
original v1 relationship contract remains unchanged
v1.2 additive relationship families remain tested explicitly
```

This is preferable to silently changing the historical golden and losing visibility into which compatibility layer changed.

## 7. Core Integration Input Set regression protection

The coherent Integration Input Set is protected primarily through behavioral tests rather than one committed full-directory golden.

High-value properties include:

```text
one Core load and one lint operation
required and companion roles
availability and failure-state representation
per-surface kind/version records
per-surface SHA-256
RFC 8785/JCS input_set_sha256
manifest-last publication
path portability through relative records
no raw-YAML semantic fallback in the reference integration
```

A full generated input-set directory is not committed as a byte-for-byte golden because producer provenance and complete surface payloads can contain more detail than should be frozen by one release signature.

## 8. Future golden candidates

Potential future golden targets include:

| Family | Current posture | Suitability |
|---|---|---|
| lint JSON report | Stable | Strong selective candidate. |
| simulation JSON report | Stable | Strong selective candidate. |
| candidate dashboard summary | Candidate | Review only after a clearer promotion decision. |
| candidate scenario run index | Candidate | Review only after a clearer promotion decision. |
| candidate coverage summary | Candidate | Review only after a clearer promotion decision. |
| runtime contract manifest | Public preview | Possible selective candidate. |
| ground contract manifest | Public preview | Possible selective candidate. |
| generated Markdown | Human-oriented | Weak candidate. |
| plain-text logs | Human-oriented | Weak candidate. |
| generated C++17 bindings | Public preview | Selective fragments only. |
| generated CSV dictionaries | Public preview | Selective fragments only. |

A future PR should add a golden baseline only when the protected compatibility promise is clear.

## 9. What deserves protection

High-value targets include:

```text
surface kind and format identity
stable result tokens
mission identity
boundary flags
entity identities
relationship identities and narrow semantics
required role classification
failure-state distinctions
manifest compatibility records
stable provenance algorithms
scenario evidence meaning
```

Low-value targets include:

```text
human prose
incidental whitespace
undocumented ordering
absolute paths
terminal formatting
plain-text logs
example narrative wording
```

Protect meaning first.

## 10. Golden acceptance criteria

Before adding or changing a committed golden, a PR should answer:

```text
Which compatibility surface is protected?
Which command produces the source output?
Which fixture or mission is used?
Which fields are contract-significant?
Which fields are intentionally ignored?
Is ordering contract-significant?
Is formatting contract-significant?
Is the selection stable across supported Python versions?
What compatibility class applies if the signature changes?
```

A golden change must explain whether it is corrective, clarifying, additive, compatibility-sensitive or breaking.

## 11. Downstream consumer rule

Downstream tools should rely on documented Core-owned structured surfaces, not on CI artifact locations or test fixture filenames.

For general inspection the preferred chain is:

```text
mission_snapshot.json
entity_index.json
relationship_manifest.json
```

For external integration the preferred boundary is:

```text
Core Integration Input Set
```

Golden signatures protect selected meaning inside those contracts. They do not become a runtime API or source of mission truth.

## 12. Non-goals

This policy does not introduce:

```text
new Mission Model semantics
new JSON report fields
new generated surfaces
plugin execution
runtime behavior
ground behavior
schema migration tooling
Studio-specific semantic authority
```

## 13. Final statement

OrbitFabric uses selective golden signatures when a narrow stable compatibility promise deserves explicit regression protection.

v1.2.0 extends that strategy to Mission Snapshot while retaining the original v1 Core surface goldens unchanged and using dedicated tests for additive FDIR relationship families and Integration Input Set behavior.
