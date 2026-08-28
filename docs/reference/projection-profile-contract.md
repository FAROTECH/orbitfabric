# Projection Profile Contract

Status: Candidate extension contract, design-frozen and reference-proven  
Contract version: `0.1-candidate`  
Scope: Generic authored projection-profile envelope for external ecosystem integrations  
Parent architecture issue: #227  
Design issue: #231  
Concept RFC: #213  
Core input dependency: #228

## 1. Purpose

The Projection Profile Contract defines how an engineer records ecosystem-specific projection intent without duplicating or redefining the OrbitFabric Mission Model.

It answers:

```text
What target-specific choices are authored by the integration user,
and how are those choices anchored to Core-owned mission entities?
```

The intended architecture is:

```text
Core Integration Input Set
    -> Projection Profile
    -> Integration Adapter
    -> Integration Result
```

The Mission Model remains the semantic source of truth.

The Profile is authored target-specific configuration. The Integration Result records the resolved/generated outcome.

The generic contract is design-frozen and has been exercised by the OpenOBSW/OpenSVF reference integration. It remains `0.1-candidate` and is not promoted to a stable Core Mission Data Contract surface by v1.2.0.

## 2. Ownership boundary

The contract deliberately separates generic governance from integration-specific semantics.

OrbitFabric governance owns:

```text
generic envelope identity and versioning
Profile instance identity and versioning
integration schema identity and versioning
Core source-reference shape
binding identity and authored intent
settings/config placement rules
authority and precedence rules
validation ownership boundaries
```

The Integration Package owns:

```text
target-specific settings keys
target-specific binding config keys
numeric allocation rules
protocol mappings
target naming rules
target type projection rules
adapter defaults and overrides
target-specific validation
```

Core must not learn OpenOBSW, OpenSVF, YAMCS, PUS, SRDB, cFS, F Prime or other ecosystem-specific semantics merely to define the Profile envelope.

## 3. Authoring format

The v0 Profile is one human-reviewable YAML document with a JSON-compatible loaded data model.

Requirements:

```text
YAML 1.2-compatible authoring
UTF-8 text
mapping keys are strings
no custom YAML tags
no duplicate mapping keys
no opaque binary state
no Studio-only authoritative database
```

The generic v0 contract defines no include, inheritance, overlay chain or remote import mechanism.

A future composition mechanism requires a separate reviewed contract.

## 4. Generic envelope

The candidate envelope is:

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

## 5. Version identities

Three version concepts remain distinct.

### `profile_version`

Identifies the generic OrbitFabric Projection Profile envelope.

Current value:

```text
0.1-candidate
```

### `profile.version`

Identifies the mission/project-authored revision of one Profile instance.

It is controlled by the Profile author and is not a substitute for an exact content digest.

### `integration.schema_version`

Identifies the integration-specific schema required to interpret `settings` and `bindings[].config` together with `integration.id`.

The adapter package/software version remains separate implementation and provenance information.

## 6. Profile identity

`profile.id` identifies the authored Profile lineage.

It must be:

```text
non-empty
stable across ordinary edits to the same Profile lineage
version-controlled
independent from filesystem path
```

It is not a Mission Model entity ID and must not be inserted into Core Entity Index or Relationship Manifest.

`profile.description` is optional human-readable metadata and carries no machine semantic authority.

## 7. Integration identity

`integration.id` identifies the integration and schema family expected to consume the Profile.

An adapter must reject a Profile whose `integration.id` or `integration.schema_version` it does not support.

It must not guess compatibility from package names, repository names or string similarity.

## 8. Integration-owned settings

`settings` is a JSON-compatible mapping owned by the integration-specific schema.

It is intended for target-wide authored configuration that is not naturally attached to one Core entity.

Reference examples may include:

```text
target naming prefix
allocation namespace
protocol defaults
SRDB-generation policy
target-tool compatibility selection
```

These examples do not become Core semantics.

The generic contract treats `settings` as opaque after generic envelope validation. Detailed validation remains integration-owned.

## 9. Core source reference

Every semantic source reference uses the domain-qualified Core identity:

```yaml
domain: telemetry
id: eps.obc.bus_voltage_mv
```

Both fields are required.

The pair must resolve to exactly one Entity Index record in the Core Integration Input Set.

Forbidden substitutes for Core semantic identity include:

```text
Mission YAML path
source filename or line
C symbol
numeric target ID
SRDB name
XTCE name
YAMCS path
artifact filename
Studio internal ID
```

Those values may appear as target-specific configuration or result data, but never as replacements for Core identity.

## 10. Binding contract

A binding records one stable Profile-local projection decision.

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
config    optional integration-owned mapping, default {}
reason    conditionally required for do_not_project
```

## 11. Binding identity

`bindings[].id` is:

```text
unique within the Profile
authored and version-controlled
case-sensitive
an identifier for the Profile mapping record
not a Mission Model entity
not a target artifact identity
```

Core and generic consumers must not infer semantics from binding-ID prefixes.

## 12. Source cardinality

A binding contains one or more Core source references.

The envelope supports:

```text
one source -> one binding
one Core entity -> multiple bindings
multiple Core entities -> one binding
```

Pure target-wide configuration with no Core semantic anchor belongs in `settings`.

The generic v0 contract does not permit a source-less semantic binding.

## 13. Source ordering

The generic contract assigns no semantic meaning to the order of `bindings[].sources`.

If a target requires packing order, field position or another ordered target concept, the integration-specific schema must represent that explicitly inside `config`.

Incidental YAML array order must not become hidden target semantics.

## 14. Authored intent

Allowed values are:

```text
project
do_not_project
```

`project` means the Profile explicitly requests or configures projection of the referenced Core semantics.

`do_not_project` means the Profile explicitly records intentional non-projection.

For `do_not_project`:

```text
reason is required and non-empty
config should be empty
```

The distinction is mandatory:

```text
no binding exists
!=
explicit do_not_project
```

## 15. Absence semantics

If a Core entity is not referenced by any binding, the generic meaning is only:

```text
no authored Profile decision exists for that entity
```

Absence does not mean unsupported, invalid, automatically projected or intentionally excluded.

The adapter may apply its documented default projection policy. The resolved outcome belongs in the Integration Result.

## 16. Binding config

`bindings[].config` is interpreted by the integration-specific schema.

Depending on the integration, it may contain:

```text
numeric allocations
protocol service and subtype mappings
target symbol overrides
target database names
target encoding or type overrides
housekeeping grouping or SID allocation
materialization choices
verification-facing protocol expectations
```

These examples remain target-specific and do not become generic Profile fields.

Studio and other tooling must obtain target-specific schema information from the Integration Package, not from a second hard-coded copy.

## 17. Semantic authority and precedence

The authority chain is:

```text
1. Core semantic value
2. Adapter deterministic target projection/default
3. Profile-authored target choice or override where explicitly allowed
4. Integration Result records the resolved value and origin
```

A Profile may override target representation where the integration schema permits it.

A Profile may not override Core semantic meaning.

Allowed examples:

```text
explicit target numeric ID
target symbol override
target encoding override where supported
protocol mapping
```

Forbidden semantic replacements include:

```text
redefining OrbitFabric unit
redefining command arguments
redefining event or fault trigger semantics
redefining Core severity meaning
redefining Core relationship meaning
```

If the target cannot faithfully represent Core semantics, the adapter must report an integration diagnostic rather than silently changing Core meaning.

## 18. Deterministic defaults

Profiles should not repeat values that can be derived deterministically and safely by the adapter.

Examples may include target symbols or types derived from Core identity and semantic type.

Preferred behavior:

```text
adapter deterministic default
Profile override only when required
Integration Result records the resolved value and origin
```

## 19. Stable external allocations

Externally persistent numeric IDs or other ABI-significant values require stronger discipline.

If an allocation must remain stable across builds or releases, the preferred production posture is explicit version-controlled Profile state.

An adapter may offer deterministic allocation assistance, but a production-significant value must not live only in hidden mutable adapter state.

## 20. Validation ownership

Validation layers remain distinct:

```text
Core Integration Input validation
  Core-owned

Generic Profile envelope validation
  generic contract helper and/or Integration Package

Integration-specific schema validation
  Integration Package / Adapter

Projection validation
  Integration Package / Adapter
```

Profile and adapter diagnostics are not injected into Core lint output.

Representative integration diagnostics include:

```text
unknown Core source entity
source domain mismatch
duplicate binding ID
unsupported integration schema version
missing required allocation
allocation collision
invalid protocol mapping
unsupported target encoding
invalid target name
```

## 21. Schema publication

The Integration Package publishes the detailed schema for `settings` and binding `config`.

The current supporting contract uses JSON Schema Draft 2020-12 and identifies the schema through:

```text
integration.id
integration.schema_version
```

The same schema authority is intended for adapter CLI validation, CI, Studio-assisted editing and human-facing schema documentation.

Core does not embed target-specific Profile keys.

## 22. Storage and lifecycle

A Profile instance is authored source configuration.

It should normally live with the mission/project source configuration or in another explicit version-controlled integration configuration repository.

The generic contract does not require one filesystem discovery convention.

An opaque Studio-private database must not become the authoritative Profile store.

## 23. Provenance and digest

The Profile contains no self-digest.

The Integration Result records at least:

```text
profile.id
profile.version
integration.id
integration.schema_version
exact consumed Profile content SHA-256
```

`profile.version` is authored lifecycle metadata. The digest records the exact bytes consumed.

The v0 contract does not define semantic-equivalence fingerprinting for Profiles.

## 24. Reference extraction principles

The original PoC mapping model was useful evidence but is not the production schema.

Production extraction follows these rules:

```text
local copied semantic entity names
  -> Core {domain,id} references

Core semantic unit/type/command arguments/severity
  -> remain Core-derived

stable target numeric allocation
  -> Profile-authored where external persistence requires it

deterministic target symbol/name/type
  -> adapter default where safe

target protocol mapping and target grouping
  -> integration-owned Profile config

resolved target values
  -> Integration Result with provenance
```

This authority split has been exercised by the OpenOBSW/OpenSVF reference package and remains the reference behavior for the generic candidate contract.

## 25. Example

Illustrative target-specific keys remain integration-owned:

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
```

The example does not make `numeric_id`, `pus`, `c_prefix` or any OpenOBSW/OpenSVF concept generic Core semantics.

## 26. Consumer rules

A consumer of a Projection Profile must:

1. validate the generic envelope;
2. validate `integration.id` and `integration.schema_version` against the selected Integration Package;
3. resolve every source through the Core Integration Input Set;
4. validate integration-owned settings and config through the package-published schema;
5. preserve the authority precedence described above;
6. keep Core diagnostics and integration diagnostics distinct;
7. produce resolved outcomes through the Integration Result rather than mutating the Profile silently.

A consumer must not use raw Mission Model YAML as a semantic fallback when the stable Core Integration Input Set is required.

## 27. Non-goals

The Projection Profile Contract does not introduce:

```text
new Mission Model semantics
new Core YAML fields
target-specific semantics inside Core
Profile execution inside Core
plugin discovery or loading
relationship inference
runtime behavior
ground behavior
Studio-specific semantic authority
```

## 28. Current maturity

The generic Profile envelope and authority rules are design-frozen and reference-proven.

The OpenOBSW/OpenSVF reference Integration Package has exercised the contract end to end with a real Core Integration Input Set and downstream Studio acceptance path.

The contract nevertheless remains:

```text
0.1-candidate
```

It is an extension contract with its own maturity lifecycle. v1.2.0 stabilizes the Core input boundary, not every extension contract that consumes it.

## 29. Final statement

The Projection Profile records authored target-specific intent without becoming a second Mission Model.

Core identity is always domain-qualified. Target-specific semantics remain integration-owned. Deterministic defaults are preferred over duplicated state. Stable external allocations are version-controlled when required. Resolved values and provenance belong in the Integration Result.
