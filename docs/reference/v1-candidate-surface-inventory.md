# v1.0 Candidate Surface Inventory

Status: Historical pre-v1.0 review inventory  
Scope: v0.12.0 release candidate hardening  
Applies to: OrbitFabric Core surfaces reviewed before `v1.0.0 - Stable Mission Data Contract`

This page records the pre-v1.0 inventory used during `v0.12.0 - v1.0 Release Candidate Hardening`.

It is kept as historical release-governance evidence.

It is no longer the current stability decision.

The current v1.0 stable surface is defined by:

```text
v1.0 Stable Surface Decision
v1.0 Compatibility and Migration Notes
v1.0.0 release notes
```

This inventory does not introduce new Mission Model semantics, new YAML fields, new CLI behavior, new JSON report fields, new generated surfaces, new lint diagnostics, new scenario behavior, schema migration tooling, JSON Schema publication, runtime behavior, ground behavior, plugin discovery, plugin loading, plugin execution, metadata schema, metadata parser, metadata loader, metadata validator or Studio-specific APIs.

---

## 1. Purpose

This inventory supported the pre-v1.0 review phase.

Its purpose was to identify which existing surfaces were candidates for stabilization, which remained preview, which remained generated and disposable, and which remained internal before the v1.0.0 release decision.

The guiding rule remains valid:

```text
Mission Model is the source of truth.
Core owns Mission Data Contract semantics.
Generated and exported surfaces are derived from the validated Mission Model.
Downstream tools consume Core-owned structured surfaces.
Extensions must not redefine Core semantics.
```

No surface is stable merely because it appears in this historical inventory.

A surface is stable in v1.0.0 only if it is listed in the accepted v1.0 Stable Surface Decision or a later reviewed release decision.

---

## 2. Historical candidate inventory

The following existing surfaces were reviewed as candidates before v1.0.0.

| Surface | Historical classification | v1.0 outcome |
|---|---|---|
| Mission Model YAML | Candidate contract | Stable selected surface for documented contract semantics. |
| Core structural validation | Public preview behavior | Stable selected surface. |
| Core semantic lint diagnostics | Public preview behavior | Stable selected diagnostic policy. |
| Scenario YAML | Public preview | Stable selected host-side evidence input. |
| Scenario JSON report | Public preview | Stable selected evidence report family. |
| Lint JSON report | Public preview | Stable selected validation report family. |
| `model_summary.json` | Candidate contract | Stable selected Core-owned structured surface. |
| `entity_index.json` | Candidate contract | Stable selected Core-owned structured surface. |
| `relationship_manifest.json` | Candidate contract | Stable selected Core-owned structured surface for admitted families. |
| Release compatibility policy | Documentation contract | Stable selected governance surface. |
| Extensibility boundary contract | Documentation contract | Stable selected governance surface. |

---

## 3. Surfaces that remain preview or disposable

The following surfaces remain useful but are not part of the narrow v1.0 stable surface unless explicitly promoted later.

| Surface | v1.0 posture |
|---|---|
| CLI textual output | Public preview, human-oriented. |
| `orbitfabric inspect mission` terminal output | Public preview, human-oriented. |
| `orbitfabric validate scenario` terminal output | Public preview, human-oriented. |
| Generated Markdown mission docs | Public preview generated documentation. |
| Demo mission content | Public example. |
| Plain-text simulation logs | Public preview, human-oriented. |
| Generated C++17 runtime-facing bindings | Public preview disposable generated artifact. |
| `runtime_contract_manifest.json` | Public preview generated artifact. |
| Generated ground dictionaries | Public preview disposable generated artifact. |
| `ground_contract_manifest.json` | Public preview generated artifact. |

Generated artifacts should remain reproducible from the validated Mission Model.

User-owned implementation code must stay outside generated output directories.

---

## 4. Internal implementation inventory

The following areas remain internal implementation details unless explicitly promoted by a future reviewed design.

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

## 5. Explicit non-candidates for v1.0 Core stability

The following are not part of the v1.0 Core stable surface.

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

These topics may be valid future work, but they are outside the v1.0.0 stable Core surface.

---

## 6. Downstream consumer rule

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

It only records the historical pre-v1.0 review inventory and points to the accepted v1.0 decision.
