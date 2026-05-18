# v1.0 Candidate Surface Inventory

Status: Development preview  
Scope: v0.12.0 release candidate hardening  
Applies to: OrbitFabric Core surfaces being reviewed before v1.0.0

This page inventories OrbitFabric Core surfaces that need review before any future `v1.0.0 - Stable Mission Data Contract` claim.

It is an inventory and classification document only.

It does not introduce new Mission Model semantics, new YAML fields, new CLI behavior, new JSON report fields, new generated surfaces, new lint diagnostics, new scenario behavior, schema migration tooling, JSON Schema publication, runtime behavior, ground behavior, plugin discovery, plugin loading, plugin execution, metadata schema, metadata parser, metadata loader, metadata validator or Studio-specific APIs.

---

## 1. Purpose

v0.12.0 is a release candidate hardening milestone.

Its purpose is not to broaden OrbitFabric.

Its purpose is to make the path toward v1.0.0 explicit by identifying which existing surfaces are candidates for stabilization, which remain preview, which remain generated and disposable, and which remain internal.

The guiding rule remains:

```text
Mission Model is the source of truth.
Core owns Mission Data Contract semantics.
Generated and exported surfaces are derived from the validated Mission Model.
Downstream tools consume Core-owned structured surfaces.
Extensions must not redefine Core semantics.
```

No surface listed here becomes stable only because it appears in this inventory.

A stable v1.0 commitment requires a future explicit v1.0 release decision.

---

## 2. Classification labels

This inventory uses the same pre-v1.0 language already defined by the Stability and Compatibility Contract and Generated Surfaces Stability references.

### 2.1 Candidate for v1.0 stabilization

A candidate for v1.0 stabilization is already public enough and central enough to require focused review before v1.0.0.

It is not yet stable.

Changes remain possible before v1.0.0, but compatibility-sensitive changes should be explicit and documented.

### 2.2 Public preview

A public preview surface is documented and usable, but is not currently proposed as a guaranteed v1.0 stable surface without further review.

### 2.3 Generated disposable artifact

A generated disposable artifact is reproducible from the Mission Model.

It may be useful for integration or inspection, but user-owned implementation code must not live inside it.

### 2.4 Internal implementation detail

An internal implementation detail is not a public compatibility surface.

It may change as long as documented behavior and public surfaces remain valid.

---

## 3. Candidate v1.0 stabilization inventory

The following existing surfaces are candidates for v1.0 stabilization review.

| Surface | Current classification | v1.0 candidate posture | Stabilization question |
|---|---|---|---|
| Mission Model YAML | Candidate contract | Candidate for stable source-of-truth contract | Are all documented domains, fields, identifiers and controlled values ready to be frozen or versioned? |
| Core structural validation | Public preview behavior | Candidate for stable validation baseline | Are validation responsibilities and failure modes clearly documented? |
| Core semantic lint diagnostics | Public preview behavior | Candidate for stable diagnostic policy | Are lint rule codes, severities and meanings stable enough for CI users? |
| Scenario YAML | Public preview | Candidate for stable host-side evidence input | Are scenario fields and expectation semantics ready for compatibility commitment? |
| Scenario JSON report | Public preview | Candidate for stable evidence report family | Are top-level fields, result values and evidence records ready for compatibility commitment? |
| Lint JSON report | Public preview | Candidate for stable validation report family | Are top-level fields, diagnostic records and result values ready for compatibility commitment? |
| `model_summary.json` | Candidate contract | Candidate for stable Core-owned inspection surface | Is the domain-level contract summary sufficiently narrow and complete? |
| `entity_index.json` | Candidate contract | Candidate for stable Core-owned inspection surface | Are entity records, kinds and identifiers sufficiently narrow and complete? |
| `relationship_manifest.json` | Candidate contract | Candidate for stable Core-owned inspection surface | Are relationship records, families and boundary flags sufficiently narrow and complete? |
| Release compatibility policy | Documentation contract | Candidate for stable release governance reference | Are compatibility classes and review rules clear enough for v1.0 maintenance? |
| Extensibility boundary contract | Documentation contract | Candidate for stable extensibility boundary reference | Are Core ownership, extension ownership and semantic override rules ready to remain stable? |

These candidates should be reviewed before v1.0.0.

They should not be silently changed in unrelated PRs.

---

## 4. Public preview surfaces not yet selected as stable contracts

The following surfaces remain public preview and useful, but should not automatically become stable v1.0 contracts without separate review.

| Surface | Current posture | v1.0 decision needed |
|---|---|---|
| CLI textual output | Human-oriented public preview | Confirm that terminal text remains non-machine-contract. |
| `orbitfabric inspect mission` output | Human-oriented inspection output | Decide whether only behavior, not exact formatting, is stable. |
| `orbitfabric validate scenario` output | Human-oriented validation output | Decide whether only pass or fail behavior, not exact wording, is stable. |
| Generated Markdown mission docs | Public preview generated docs | Decide whether format remains disposable and human-reviewable only. |
| Demo mission content | Public example | Decide whether examples remain illustrative rather than compatibility fixtures. |
| Plain-text simulation logs | Human-oriented evidence output | Confirm logs are not machine-readable compatibility contracts. |

These surfaces should remain clearly separated from machine-readable JSON reports and Core-owned structured surfaces.

---

## 5. Generated disposable artifact inventory

The following generated artifacts should remain disposable unless a future architectural decision says otherwise.

| Surface | Current posture | Required boundary before v1.0 |
|---|---|---|
| Generated C++17 runtime-facing bindings | Public preview disposable generated artifact | Must remain contract-facing bindings, not flight software. |
| `runtime_contract_manifest.json` | Public preview generated artifact | Must remain generated from the Mission Model and not become a runtime authority. |
| Generated C++17 host-build smoke files | Generated validation artifact | Must remain build confidence support, not user-owned implementation. |
| Generated JSON ground dictionaries | Public preview disposable generated artifact | Must remain ground-facing contract dictionaries, not live decoders. |
| Generated CSV ground dictionaries | Public preview disposable generated artifact | Must remain review artifacts, not source of truth. |
| Generated ground Markdown artifacts | Public preview disposable generated artifact | Must remain human-reviewable generated documentation. |
| `ground_contract_manifest.json` | Public preview generated artifact | Must remain a generated manifest, not ground runtime behavior. |

Generated artifacts should remain reproducible from the validated Mission Model.

User-owned implementation code must stay outside generated output directories.

---

## 6. Internal implementation inventory

The following areas are internal implementation details unless explicitly promoted by a future reviewed design.

```text
Python module layout
private helper functions
internal builder object identities
Pydantic model internals not documented as public contracts
internal lint implementation structure
internal generator implementation structure
internal exporter implementation structure
test helper layout
CI job implementation details
local development scripts
```

Internal does not mean unimportant.

It means these areas should not be treated as public compatibility surfaces.

---

## 7. Explicit non-candidates for v1.0 Core stability

The following are not candidates for the v1.0 Core stable surface in the current path.

```text
flight runtime
ground runtime
mission control system
operator console
telemetry archive
telemetry database
command uplink service
hardware abstraction layer
RTOS integration
CCSDS/PUS/CFDP implementation
Yamcs integration
OpenC3 integration
XTCE-compliant mission database
relationship graph
dependency graph
visual modeling backend
Studio-specific API
plugin discovery
plugin loading
plugin execution
metadata schema
metadata parser
metadata loader
metadata validator
schema migration tooling
JSON Schema publication
```

These topics may be valid future work, but they are outside the v0.12.0 hardening path and outside the current v1.0 Core stable Mission Data Contract target.

---

## 8. Required review before v1.0.0

Before v1.0.0, OrbitFabric should explicitly review:

```text
which Mission Model domains become stable
which optional domains remain preview
which JSON report fields become stable
which Core-owned structured surface fields become stable
which generated artifact paths remain documented
which CLI commands and options become stable
which lint diagnostic policies become stable
which scenario evidence semantics become stable
which extensibility boundary rules become stable
which generated artifacts remain disposable
which surfaces remain internal
```

The review should produce compatibility notes or migration notes where necessary.

It should not produce migration tooling unless a separate architectural decision explicitly accepts that scope.

---

## 9. Downstream consumer rule

Downstream tools should consume documented Core-owned structured surfaces when they need Mission Data Contract inspection.

They must not reconstruct Core semantics from:

```text
raw YAML
generated Markdown
generated runtime files
generated ground files
stdout or stderr text
file names
ID naming conventions
UI state
extension-owned assumptions
```

The intended downstream inspection chain remains:

```text
model_summary.json
entity_index.json
relationship_manifest.json
```

This inventory does not add a new downstream API.

It only clarifies which existing surfaces need v1.0 stabilization review.

---

## 10. v0.12.0 boundary

This inventory supports v0.12.0 release candidate hardening.

It must not be read as permission to add new functional scope.

v0.12.0 should make OrbitFabric more stable, more explicit and less ambiguous.

It should not make OrbitFabric broader.

It should not turn OrbitFabric into flight software, ground software, a simulator runtime, a visual modeling tool, a plugin execution platform or a schema migration system.
