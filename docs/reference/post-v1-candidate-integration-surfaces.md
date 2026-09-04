# Post-v1 Integration Surface Classification

Status: Active compatibility inventory through v1.3.0  
Scope: Core-owned structured and integration lifecycle surfaces introduced after `v1.0.0 - Stable Mission Data Contract`

This page preserves the classification history of post-v1 Core-owned surfaces, records the v1.2 promotion decision and classifies the candidate Adapter Management foundation added in v1.3.0.

Candidate surfaces are not automatically stable. Promotion requires an explicit reviewed compatibility decision and appropriate regression protection.

---

## 1. Original v1.0 stable Core-owned surfaces

```text
model_summary.json
entity_index.json
relationship_manifest.json for original admitted families
```

These remain stable. The Mission Model remains the source of truth.

---

## 2. v1.1.0 candidate surfaces

The following were consolidated as candidate Core-owned surfaces in v1.1.0 and remain candidate after v1.3.0:

```text
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
simulation JSON structured expectation accounting
```

They support downstream inspection but are not silently promoted by either the v1.2 Core Integration Input decision or the v1.3 Adapter Management release.

---

## 3. v1.2.0 stable additions

### Mission Snapshot

`mission_snapshot.json` is stable from v1.2.0 for its documented envelope, load-failure behavior, boundary semantics and complete-loaded-model role.

Its format identifier remains `0.1-candidate` to preserve compatibility with the reference-proven producer/consumer chain.

The complete `model` payload follows Mission Model compatibility rules rather than a byte-for-byte Snapshot freeze.

### Core Integration Input Set

The coherent Core Integration Input Set is the stable Core input boundary for external ecosystem integrations from v1.2.0.

It combines one logical Core load/lint operation into explicit required/companion surface records with exact digests, compatibility identities, load/lint state and deterministic set fingerprinting.

Its `input_set_version` remains `0.1-candidate`; stability and format-version text are independent.

### Additive FDIR Relationship Manifest families

The following are admitted as additive stable-compatible relationship families:

```text
autonomous_action_triggered_by_fault
autonomous_action_uses_command_source
fault_observes_telemetry
fault_recovery_dispatches_command
fault_recovery_targets_mode
recovery_intent_includes_command
recovery_intent_targets_mode
```

Each is derived deterministically from an explicit loaded Mission Model field. They do not rename/remove/redefine original v1 families and do not introduce inferred graph semantics.

The original v1 Relationship Manifest golden remains fixed; dedicated regression tests protect these additive families.

---

## 4. v1.3.0 candidate Adapter Management foundation

v1.3.0 adds product capabilities without expanding the stable Mission Data Contract.

Candidate integration and lifecycle additions include:

```text
operation-input v1 integration contract lane
Adapter Manager lifecycle
Adapter Release Descriptor 0.1-candidate
Adapter Project Lock 0.1-candidate
explicit-source install-from-lock
source-neutral ResolvedAdapterRelease attachment seam
Adapter Catalog 0.1-candidate
Adapter Catalog CLI
```

The provider-neutral lifecycle is:

```text
Adapter Source Coordinate
    -> exact Catalog release selection
    -> provider-specific Release Source outside Core
    -> exact descriptor + artifact verification
    -> ResolvedAdapterRelease
    -> Core Project Lock / Adapter Manager lifecycle
    -> Installed Adapter State
```

Core owns exact release identity, candidate lifecycle contracts and installed-state orchestration. Provider-specific network acquisition, provider authentication and provider dispatch remain outside Core.

The first provider-specific implementation does not define a universal provider plugin protocol.

---

## 5. Current classification inventory

| Surface | Classification after v1.3.0 | Purpose |
|---|---|---|
| `model_summary.json` | Stable | Domain/count summary |
| `entity_index.json` | Stable | Canonical entity inventory |
| `relationship_manifest.json` original families | Stable | Original admitted explicit relationships |
| Relationship Manifest FDIR families | Additive stable-compatible | Additional explicit FDIR relationships |
| `mission_snapshot.json` | Stable | Complete loaded Mission Model inspection |
| Core Integration Input Set | Stable | Coherent Core input boundary for external integrations |
| `dashboard_summary.json` | Candidate | Dashboard-ready Core aggregation |
| `scenario_run_index.json` | Candidate | Index of simulation JSON report runs |
| `coverage_summary.json` | Candidate | Limited coverage derived from Core outputs |
| simulation JSON structured `expectations` | Candidate additive extension | Structured expectation accounting |
| operation-input v1 lane | Candidate | File-backed external adapter operation input |
| Adapter Release Descriptor | Candidate | Exact adapter release and artifact membership |
| Adapter Project Lock | Candidate | Project-scoped exact desired adapter state |
| Adapter Manager lifecycle | Candidate | Installed adapter lifecycle and verification |
| `ResolvedAdapterRelease` handoff | Candidate Core seam | Source-neutral exact resolved-release attachment |
| Adapter Catalog | Candidate | Provider-neutral exact release availability and source binding references |
| Adapter Catalog CLI | Candidate | Local validation/list/exact selection |

---

## 6. Extension-owned integration contracts

The Integration Framework additionally defines separately versioned extension contracts:

```text
Projection Profile
Integration Result
Integration Package / Adapter Execution
```

The original v0 lane remains independently versioned candidate material. The v1.3 operation-input lane uses the candidate Manifest `0.2-candidate`, `orbitfabric.adapter_cli.v1` and Result `0.2-candidate` contract family.

These are not stable Core Mission Data Contract surfaces and do not move target-specific semantics into Core.

---

## 7. Compatibility posture

The v1.3 release does not change Mission Model semantics.

Compatible Mission Data Contract consumers must:

- check Core surface kind/version identifiers;
- tolerate unknown additive fields where the relevant contract permits them;
- tolerate unknown additive Relationship Manifest types without assigning guessed semantics;
- reject missing/incompatible required Integration Input Set surfaces;
- distinguish Core load/lint diagnostics from integration diagnostics;
- never use raw YAML, filenames, timestamps or UI state as semantic fallbacks.

Adapter lifecycle consumers must additionally:

- keep Source Coordinate, exact release version and exact digest anchors explicit;
- resolve one exact Catalog release before acquisition;
- keep provider locators separate from Project Lock identity;
- fail closed on missing or ambiguous exact selection;
- distinguish provider acquisition evidence from Core trust/acceptance semantics;
- keep installed local state separate from project desired state.

---

## 8. Ownership boundary

```text
Core defines Mission Data Contract semantics.
Core emits stable and candidate structured surfaces.
Core owns provider-neutral exact adapter lifecycle contracts.
Projection Profiles own authored target-specific projection intent.
External adapters own target-specific validation and generation.
Provider-specific Release Sources own remote acquisition outside Core.
Studio and other downstream tools consume and compose explicit records.
```

Core is not a dashboard backend, flight software framework, ground segment, target-specific integration implementation, graph engine, in-process plugin execution platform or provider-specific registry client.

---

## 9. Explicit non-goals

The post-v1 integration and Adapter Management surfaces do not introduce:

```text
OpenOBSW/OpenSVF/YAMCS/F Prime-specific Core semantics
CCSDS/PUS/CFDP implementation
runtime telemetry behavior
ground execution behavior
relationship graph behavior
dependency graph behavior
third-party adapter import/execution inside the Core Python process
provider-specific acquisition inside Core
universal provider plugin protocol
latest/channel/version-range solving
Studio-specific semantic authority
```

Adapter Manager may execute an installed external adapter through its documented out-of-process execution contract. That lifecycle capability does not make target-specific code part of Core semantic authority.

---

## 10. Final statement

The post-v1 history is deliberately cumulative but maturity remains explicit:

```text
v1.0.0  stable narrow Mission Data Contract
v1.1.0  candidate inspection additions
v1.2.0  stable Mission Snapshot + Core Integration Input boundary
v1.3.0  candidate provider-neutral Adapter Management foundation
```

A stable Core package release does not automatically promote candidate product surfaces. Every promotion remains an explicit architectural and compatibility decision.
