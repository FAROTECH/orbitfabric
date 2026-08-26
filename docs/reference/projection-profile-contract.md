# Projection Profile Contract

Status: Architecture candidate — Phase B.2 generic envelope design-frozen; reference integration schema review pending  
Contract version: `0.1-candidate`  
Scope: Generic authored projection-profile envelope for external ecosystem integrations  
Parent architecture issue: #227  
Design issue: #231  
Concept RFC: #213  
Core input dependency: #228

---

## 1. Purpose

The Projection Profile Contract defines how an engineer records **ecosystem-specific projection intent** without duplicating or redefining the OrbitFabric Mission Model.

It answers:

```text
What target-specific choices are authored by the integration user,
and how are those choices anchored to Core-owned mission entities?
```

The intended architecture is:

```text
Core Integration Input Set
        ↓
Projection Profile
        ↓
Integration Adapter
        ↓
Integration Result
```

The Mission Model remains the semantic source of truth.

The Profile is authored configuration.

The Integration Result is resolved/generated output.

---

## 2. Architectural boundary

The generic Profile contract is deliberately split into two ownership layers.

### OrbitFabric Core governance owns

```text
generic envelope identity/versioning
Profile instance identity/versioning
integration-schema identity/versioning
Core source-reference shape
binding identity and authored intent
settings/config placement rules
authority/precedence rules
validation ownership boundaries
```

### Integration package owns

```text
target-specific settings keys
target-specific binding config keys
numeric-allocation rules
protocol mappings
target naming rules
target type projection rules
adapter-specific defaults/overrides
target-specific validation
```

Core must not learn OpenOBSW, OpenSVF, YAMCS, PUS, SRDB, cFS or other target-specific semantics merely to define the Profile envelope.

---

## 3. v0 authoring format

The v0 Profile is a single human-reviewable YAML document with a JSON-compatible data model.

Requirements:

```text
YAML 1.2-compatible authoring
UTF-8 text
mapping keys are strings
no custom YAML tags
no duplicate mapping keys
no opaque binary state
no Studio-only database
```

Standard YAML anchors/aliases may be used as authoring syntax if the parser supports them, but they create no additional Profile semantics.

The loaded Profile data must remain representable as ordinary JSON-compatible objects, arrays, strings, numbers, booleans and null values.

### No generic include/inheritance in v0

The generic v0 contract defines no:

```text
include
extends
inheritance
overlay chain
remote import
```

A Profile is one explicit document.

This keeps provenance, review and exact-byte digesting unambiguous.

A future composition mechanism requires a separate reviewed contract.

---

## 4. Frozen generic envelope

The v0 candidate envelope is:

```yaml
kind: orbitfabric.projection_profile
profile_version: 0.1-candidate

profile:
  id: openobsw-opensvf-demo
  version: 0.1.0
  description: Optional human-readable description

integration:
  id: orbitfabric-openobsw-opensvf
  schema_version: 0.1-candidate

settings: {}

bindings: []
```

Generic fields are limited to:

```text
kind
profile_version
profile.id
profile.version
profile.description
integration.id
integration.schema_version
settings
bindings
bindings[].id
bindings[].intent
bindings[].sources
bindings[].sources[].domain
bindings[].sources[].id
bindings[].config
bindings[].reason
```

No target-specific key is admitted into the generic envelope outside `settings` and `bindings[].config`.

---

## 5. Version identities

The Profile contract keeps three version concepts distinct.

### `profile_version`

Meaning:

```text
OrbitFabric generic Projection Profile envelope version
```

Current candidate:

```text
0.1-candidate
```

### `profile.version`

Meaning:

```text
mission/project-authored Profile instance revision
```

This value is controlled by the Profile author/project.

It is not a substitute for an exact content digest.

### `integration.schema_version`

Meaning:

```text
integration-specific settings/config schema version
```

The pair:

```text
integration.id
integration.schema_version
```

identifies the target-specific schema required to interpret `settings` and binding `config` objects.

The adapter package/software version remains separate implementation/provenance information.

---

## 6. Profile identity

`profile.id` identifies the authored Profile instance family.

It must be:

```text
non-empty
stable across ordinary edits to the same Profile lineage
version-controlled
independent from filesystem path
```

`profile.id` is not a Mission Model entity ID and must not be inserted into Core Entity Index or Relationship Manifest.

`profile.description` is optional human-readable metadata and carries no machine semantic authority.

---

## 7. Integration identity

`integration.id` identifies the integration/schema family expected to consume the Profile.

Examples are integration-package identifiers, not external runtime names.

The generic contract does not prescribe a repository/package naming convention.

An adapter must reject a Profile whose `integration.id` or `integration.schema_version` it does not support.

An adapter must not guess compatibility from package name similarity.

---

## 8. Integration-owned `settings`

`settings` is a mapping owned by the integration-specific schema.

It is intended for target-wide authored configuration that is not naturally attached to one Core semantic entity.

Examples in a reference integration may include concepts such as:

```text
target naming prefix
allocation namespace
protocol defaults
SRDB-generation policy
target-tool compatibility selection
```

Those examples do not become generic Core semantics.

The generic contract treats `settings` as an opaque JSON-compatible object after envelope validation.

Integration-specific schema validation remains adapter-owned.

---

## 9. Core source reference

Every semantic source reference in a binding uses:

```yaml
domain: telemetry
id: eps.obc.bus_voltage_mv
```

Both `domain` and `id` are required.

The pair must resolve to exactly one entity in the Core Integration Input Set Entity Index.

This prevents a Profile from replacing Core identity with target conventions.

Forbidden substitutes include:

```text
Mission YAML path
source filename/line
C symbol
numeric target ID
SRDB name
XTCE name
YAMCS path
artifact filename
Studio internal ID
```

Those may appear as target-specific configuration/result data, but they are never Core semantic references.

---

## 10. Binding contract

A binding is one stable, profile-local authored projection decision.

Generic shape:

```yaml
bindings:
  - id: tm.bus_voltage
    intent: project
    sources:
      - domain: telemetry
        id: eps.obc.bus_voltage_mv
    config: {}
```

Each binding contains:

```text
id        required
intent    required
sources   required, at least one source
config    optional integration-owned mapping; defaults to {}
reason    conditionally required for do_not_project
```

---

## 11. Binding identity

`bindings[].id`:

```text
is unique within the Profile
is authored and version-controlled
identifies the Profile mapping record
is case-sensitive
is not a Mission Model semantic entity
is not an Integration Result target identity
```

Downstream tools should treat a binding ID as opaque unless the integration-specific schema explicitly adds conventions.

Core does not infer semantics from binding-ID prefixes.

---

## 12. Source cardinality

A v0 binding requires one or more Core source references.

This supports:

```text
one source -> one binding
one Core entity -> multiple bindings
multiple Core entities -> one binding
```

Therefore the generic envelope can represent both one-to-many and many-to-one authored projection intent.

### No source-less semantic binding

Pure target-wide configuration with no Core semantic anchor belongs in `settings`.

The v0 generic contract does not permit `sources: []` for a binding.

This prevents target-only infrastructure from masquerading as a mission-semantic mapping.

---

## 13. Source ordering is not generic semantics

The generic contract does **not** assign semantic meaning to the order of `bindings[].sources`.

If a target construct requires physical ordering, field position or packing order, the integration-specific schema must represent that requirement explicitly inside `config`.

For example, a housekeeping packet schema may define explicit target-order metadata rather than relying on the incidental order in `sources`.

This avoids hidden target semantics in a generic Core-governed array.

---

## 14. Authored projection intent

Allowed v0 `intent` values are:

```text
project
do_not_project
```

### `project`

Means:

```text
the Profile explicitly requests/configures projection of the referenced Core semantics
```

`config` may be empty when adapter defaults are sufficient.

### `do_not_project`

Means:

```text
the Profile explicitly records intentional non-projection
```

For `do_not_project`:

```text
reason is required and non-empty
config should be empty
```

This distinction is required because:

```text
no binding exists
!=
explicit do_not_project
```

---

## 15. Absence semantics

If a Core entity is not referenced by any Profile binding, the generic meaning is:

```text
no authored Profile decision exists for that entity
```

Absence does **not** mean:

```text
do not project
unsupported
project automatically
invalid
```

The Integration Adapter may apply its documented default projection policy to unmentioned entities.

The resolved outcome belongs in the Integration Result.

This rule preserves the distinction between authored state and adapter behavior.

---

## 16. Integration-owned binding `config`

`bindings[].config` is a JSON-compatible mapping interpreted by the integration-specific schema.

It may contain target-specific authored values such as, depending on the integration:

```text
numeric allocations
protocol service/subservice mapping
target symbol override
target database name override
target type/encoding override
housekeeping SID/allocation
target grouping/materialization choices
verification-facing protocol expectations
```

These examples are not generic Profile fields.

Core does not parse their meaning.

Studio obtains their schema/meaning from the installed integration package rather than from hard-coded Studio logic.

---

## 17. Semantic-authority precedence

The following precedence is frozen:

```text
1. Core semantic value
       ↓ authoritative mission meaning

2. Adapter deterministic projection/default
       ↓ target representation derived from Core

3. Profile-authored target choice/override
       ↓ only where the integration schema explicitly allows it

4. Integration Result
       ↓ records resolved output and provenance
```

A Profile may override **target representation**.

A Profile may not override **Core semantic meaning**.

Examples:

```text
allowed:
  explicit target numeric ID
  target symbol override
  target encoding override where schema permits
  protocol mapping

not allowed as semantic replacement:
  redefining OrbitFabric unit
  redefining command arguments
  redefining event/fault trigger condition
  redefining semantic severity
  redefining Core relationship meaning
```

If target representation cannot faithfully express Core semantics, the adapter reports an integration diagnostic instead of silently changing Core meaning.

---

## 18. Deterministic defaults

Profiles should not repeat values that can be derived deterministically and safely by the adapter.

Reference examples include:

```text
C symbol derived from Core ID + configured prefix
SRDB name derived from Core ID
C type derived from Core semantic type
```

Preferred behavior:

```text
adapter default when deterministic
profile override only when required
Integration Result records resolved value and origin
```

This reduces duplicate authored state and drift.

---

## 19. Stable external allocations

Identifiers with external persistence, compatibility or ABI significance require stronger discipline.

If a numeric allocation must remain stable across builds/releases, the preferred production posture is:

```text
explicit Profile-authored allocation
```

An integration may support deterministic allocation assistance, but production-significant allocation must not live only in hidden mutable adapter state.

If an adapter auto-allocates and the value becomes externally significant, the value should be materialized into version-controlled Profile state before relying on it as a stable contract.

---

## 20. Validation ownership

Validation layers remain distinct.

```text
Core Integration Input validation
    -> Core-owned

Generic Profile envelope validation
    -> shared contract helper and/or integration package

Integration-specific schema validation
    -> Integration Adapter/package

Projection validation
    -> Integration Adapter/package
```

No Profile/integration diagnostic is injected into Core lint output.

Examples of integration-owned diagnostics:

```text
unknown Core source entity
source domain mismatch
duplicate binding ID
unsupported integration schema version
missing required numeric allocation
numeric allocation collision
invalid protocol mapping
unsupported target encoding override
invalid target name
```

---

## 21. Profile storage and lifecycle

A concrete Profile instance is authored source configuration.

It should normally live:

```text
with the mission/project source configuration
or
in another explicitly version-controlled integration configuration repository
```

The generic v0 contract does not mandate one filesystem layout.

A future discovery convention may be defined separately.

Studio must not make an opaque private database the authoritative Profile store.

---

## 22. Profile provenance and digest

The Profile does not contain a self-digest.

The Integration Result later records at least:

```text
profile.id
profile.version
integration.id
integration.schema_version
exact consumed Profile content/file SHA-256
```

An exact-byte Profile digest intentionally changes for formatting/comments when the source bytes change.

The v0 contract does not define semantic-equivalence fingerprinting for Profiles.

`profile.version` remains authored lifecycle metadata; the exact digest records what bytes were actually consumed.

---

## 23. PoC extraction disposition

The current `orbitfabric_models/poc_slice.yaml` is a useful precursor but must not be copied as the production schema.

Initial production disposition is frozen as follows.

| Current PoC field/concept | v0 disposition |
|---|---|
| `contract.name` | `profile.id` |
| `contract.version` | `profile.version` |
| `c_prefix` | integration-owned `settings` |
| local entity `name` | replace with Core `{domain,id}` source reference |
| `of_id` / `OF_*` symbol | deterministic adapter default where possible; explicit target-symbol override only when required |
| `of_id_value` | Profile-authored target allocation when stable external identity is required |
| `srdb_name` | deterministic Core-ID-derived default where valid; optional target override |
| `c_type` | adapter-derived from Core type by default; explicit target override only where justified |
| `unit` | remove; Core-derived semantic value |
| `pus_service` / `pus_subtype` | integration-specific binding `config` |
| `hk_set` / `sid` | integration-specific Profile mapping/allocation; multi-source binding where appropriate |
| `sample_rate_hz` | remove when duplicating Core timing; allow only explicitly target-specific override |
| `collection_interval_s` | Core-derived unless integration schema defines it as a distinct target scheduling choice |
| command `arguments` | remove; Core-derived command signature |
| `expected_responses` | integration/verification config only when required; not Core command semantics |
| event `severity` | remove when duplicating Core semantic severity |
| trigger parameter/condition/threshold | remove; Core-owned event/fault semantics |

The OpenOBSW/OpenSVF reference schema may refine target-specific key names after PoC PR #30 review, but it must preserve this authority split.

---

## 24. Example reference extraction

Illustrative only; target-specific keys remain owned by the future reference integration schema.

```yaml
kind: orbitfabric.projection_profile
profile_version: 0.1-candidate

profile:
  id: poc-openobsw-opensvf
  version: 0.1.0

integration:
  id: orbitfabric-openobsw-opensvf
  schema_version: 0.1-candidate

settings:
  c_prefix: OF_

bindings:
  - id: tm.obc_bus_voltage
    intent: project
    sources:
      - domain: telemetry
        id: eps.obc.bus_voltage_mv
    config:
      numeric_id: 0x4001
      pus:
        service: 3
        subtype: 25

  - id: cmd.ping
    intent: project
    sources:
      - domain: commands
        id: dhs.obc.ping
    config:
      numeric_id: 0x1701
      pus:
        service: 17
        subtype: 1

  - id: hk.obc
    intent: project
    sources:
      - domain: telemetry
        id: eps.obc.bus_voltage_mv
    config:
      target_kind: housekeeping_set
      sid: 1
```

Notice what is deliberately absent:

```text
unit
command argument list
event trigger semantics
semantic severity
Core source YAML path
```

Those remain Core-owned.

---

## 25. Representativeness review

The generic envelope has been reviewed against the architecture cases required by #227/#231.

| Case | Representation |
|---|---|
| one-to-one projection | one binding, one source |
| one Core entity -> multiple targets | multiple bindings referencing same Core source |
| multiple Core entities -> one target construct | one binding with multiple sources |
| explicit non-projection | `intent: do_not_project` + required reason |
| no authored decision | no binding; adapter policy decides resolved outcome |
| adapter deterministic default | `intent: project` with empty/partial `config` |
| explicit target override | integration-owned key in `config` |
| stable numeric allocation | explicit integration-owned value in `config` |
| multi-parameter HK/group mapping | multi-source binding + explicit target ordering/config when needed |
| command mapping | command Core source + integration-owned config |
| telemetry mapping | telemetry Core source + integration-owned config |
| event mapping | event Core source + integration-owned config |
| fault-related mapping | fault Core source + integration-owned config |
| target-wide policy | `settings` |
| target does not support entity | adapter emits unsupported result; Profile may additionally record `do_not_project` only when intentionally authored |

No OpenOBSW/OpenSVF/YAMCS-specific field is required by the generic envelope to represent these cases.

---

## 26. Relationship to Integration Result

The Profile records **authored intent**.

It must not contain:

```text
resolved generated target nodes
generated artifact paths/digests
projection coverage result
integration diagnostics
runtime evidence
verification evidence
staleness state
```

Those belong to the Integration Result.

The later Integration Result contract should preserve resolution provenance conceptually such as:

```text
core
adapter_default
profile
```

so downstream tools can explain why a resolved projection value exists.

---

## 27. Relationship to Studio

Studio may expose a visual Profile editor, but the data authority remains the Profile file.

Studio must:

```text
edit the same version-controlled Profile document
resolve Core entity selectors from the Core Integration Input Set
obtain target-specific settings/config schema from the integration package
preserve generic Profile semantics
```

Studio must not:

```text
create a second hidden mapping database
invent Core source IDs
hard-code OpenOBSW/OpenSVF schema into generic Studio code
infer target mappings from generated artifacts
```

The same Profile must remain usable in CLI-only, CI and Studio workflows.

---

## 28. Relationship to integration package execution

The Profile contract does not require Core to load or execute integration code.

The first production execution boundary remains:

```text
OrbitFabric Core CLI
    -> produces Core Integration Input Set

external Integration Adapter/package
    -> loads Input Set + Profile
    -> validates generic/integration-specific Profile contract
    -> produces Integration Result + target artifacts
```

This remains consistent with ADR-0015.

---

## 29. Relationship to PoC PR #30

The generic envelope is design-frozen independently of the remaining OpenOBSW/OpenSVF ownership review.

Gonçalo's feedback remains important for the **reference integration-specific schema**, especially:

```text
SRDB -> XTCE ownership
OpenOBSW contract-only boundary
OpenSVF long-term integration surfaces
YamcsBridge reuse
external compatibility markers
verification/campaign evidence interfaces
```

Those decisions may refine reference `settings`/`config` keys and adapter capabilities.

They must not move OpenOBSW/OpenSVF semantics into the generic Profile envelope unless a genuinely ecosystem-independent requirement emerges.

---

## 30. Design-freeze position

The following Phase B.2 generic decisions are frozen for `0.1-candidate`:

```text
single YAML/JSON-compatible document
no generic include/inheritance
small generic envelope
independent generic/Profile-instance/integration-schema versions
settings as target-wide integration-owned config
bindings as profile-local authored decisions
Core source reference = {domain,id}
minimum one source per binding
source order has no generic semantic meaning
binding intent = project | do_not_project
reason required for do_not_project
absence = no authored decision
integration-owned binding config
Core > adapter default > Profile target override authority precedence
no duplication/redefinition of Core semantic fields
no self-digest; exact Profile digest recorded by Integration Result
no semantic Profile fingerprint in v0
no Studio-private authoritative state
```

The remaining work under #231 is primarily:

```text
reference OpenOBSW/OpenSVF integration schema review
adapter-provided schema publication mechanism
implementation/schema-validation choice
```

Those items do not reopen the generic authored-state boundary unless review exposes a genuinely generic gap.

---

## 31. Non-goals

The v0 generic Profile contract does not define:

```text
Integration Result schema
artifact manifest schema
runtime orchestration
verification execution
Studio plugin lifecycle
Core plugin discovery/loading/execution
OpenOBSW/OpenSVF implementation changes
integration-specific settings/config keys
Profile inheritance/composition
semantic-equivalence fingerprinting
new Mission Model fields
new Mission Model semantics
```

---

## 32. Final position

The design-frozen generic candidate is:

```text
Core owns mission semantics and Core entity identity.

Projection Profile owns only authored ecosystem-specific projection intent.

Generic Profile bindings reference Core entities through {domain,id}.

Integration-specific settings/config remain independently schema-versioned and adapter-owned.

Adapter defaults may derive target representation without forcing duplicate Profile state.

Profile overrides may alter target representation but never Core semantic meaning.

Integration Result records what was actually resolved/generated and why.

Studio edits the same version-controlled Profile rather than becoming another semantic authority.
```
