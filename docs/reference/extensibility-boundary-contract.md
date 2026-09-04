# Extensibility Boundary Contract

Status: Active v1.x governance contract through v1.3.0  
Scope: extensibility ownership, semantic boundary and provider-neutral adapter lifecycle boundary  
Applies to: downstream consumers, extension-owned integration contracts and external Release Sources from v1.0.0 onward

OrbitFabric Core is a Mission Data Contract framework. Extensibility must preserve that identity.

The central rule is:

```text
Mission Model is the semantic source of truth.
Core owns Mission Data Contract interpretation.
Extensions add value at the edges.
Extensions must not redefine Core semantics.
Provider-specific acquisition stays outside Core.
```

## 1. Stable Core-owned boundary

Stable Core-owned machine-readable surfaces include:

```text
model_summary.json
entity_index.json
relationship_manifest.json for admitted families
mission_snapshot.json
Core Integration Input Set
lint JSON report
simulation JSON report
```

The first three provide normalized inspection. Mission Snapshot provides the complete loaded-model view. The coherent Integration Input Set is the stable Core input boundary for external integrations from v1.2.0.

All remain derived, read-only Core outputs. The Mission Model remains the source of truth.

## 2. Candidate Core inspection surfaces

The following v1.1 Core-owned outputs remain candidate:

```text
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
simulation JSON structured expectation accounting
```

They may be consumed by downstream tools but are not silently promoted into the stable Core surface by v1.3.

## 3. Candidate extension integration contracts

The generic Integration Framework defines separately owned extension contracts:

```text
Projection Profile
Integration Package / Adapter Execution
Integration Result
```

The original candidate execution/result lane remains available, and v1.3.0 also includes the candidate operation-input lane:

```text
Integration Package Manifest 0.2-candidate
orbitfabric.adapter_cli.v1
Integration Result 0.2-candidate
```

These contracts are reference-proven, but they are not stable Core Mission Data Contract surfaces.

Their ownership model is:

```text
Projection Profile
  authored target-specific projection intent

Integration Package / Adapter
  target-specific validation, defaults, allocation and generation

Integration Result
  explicit mappings, artifacts, diagnostics, coverage, evidence references and provenance
```

Core governance defines the generic boundary. The integration package owns target-specific semantics.

## 4. Candidate Adapter Management boundary

v1.3.0 adds candidate Core-owned lifecycle contracts for exact external adapter releases:

```text
Adapter Release Descriptor 0.1-candidate
Adapter Project Lock 0.1-candidate
Adapter Manager lifecycle
source-neutral ResolvedAdapterRelease handoff
Adapter Catalog 0.1-candidate
Adapter Catalog CLI
```

This does not transfer target-specific adapter semantics or provider-specific acquisition into Core.

The ownership model is:

```text
Core
  exact Source Coordinate semantics
  Release Descriptor conformance
  Project Lock desired state
  Installed Adapter State
  installation / verification / execution / removal lifecycle
  provider-neutral Catalog model and exact selection

provider-specific Release Source
  provider lookup/authentication where applicable
  acquisition of exact descriptor/artifact bytes
  provider facts
  ResolvedAdapterRelease materialization
```

Project Lock identity must not be rewritten from provider URLs, tags, cache locations or machine-local installation state.

## 5. Core-owned semantics

Core owns:

```text
Mission Model loading
structural validation
semantic linting
scenario validation and evidence semantics
runtime-facing contract-binding semantics
ground-facing artifact semantics
model_summary.json semantics
entity_index.json semantics
relationship_manifest.json semantics
mission_snapshot.json semantics
Core Integration Input Set semantics
candidate Core inspection-surface semantics
generic integration invocation/result contract boundaries
candidate adapter identity / desired-state / installed-state semantics
provider-neutral Catalog exact-selection semantics
stability and compatibility classification
release compatibility policy
```

An extension or provider must not override, replace, mutate or privately reinterpret these semantics.

## 6. No raw-YAML semantic fallback

The stable v1.2 Core Integration Input boundary exists specifically so external integration adapters do not need a second Mission Model parser.

For semantic projection, an adapter must consume the documented Core Integration Input Set and validate required surface compatibility.

If a required Core surface is missing, failed or incompatible, the adapter must stop semantic projection. It must not reparse raw Mission Model YAML to reconstruct the missing semantics.

This rule prevents the integration ecosystem from developing parallel interpretations of the Mission Data Contract.

## 7. Extension-owned outputs

Extension-owned outputs must remain distinguishable from Core outputs.

Relevant categories include:

```text
Core output
Core diagnostic
Core generated artifact
Core-owned structured surface
extension metadata
extension diagnostic
extension-generated artifact
extension compatibility declaration
Integration Result record
external verification evidence
provider acquisition fact
```

An extension output must not be presented as Core output unless OrbitFabric Core itself produces and documents that surface.

Provider facts must not be presented as stronger Core trust evidence than they actually support.

## 8. Provenance

Extension-owned outputs should record enough provenance to answer:

```text
which extension produced this?
which extension version produced it?
which Core input set was consumed?
which Profile was consumed?
which operation was performed?
which artifacts were generated?
which values came from Core, Profile, defaults or adapter resolution?
which external tools contributed evidence?
```

The Integration Result Contract defines the current candidate machine-readable boundary for this information.

Adapter release lifecycle evidence should separately preserve exact release identity and artifact digests without conflating them with mutable provider transport metadata.

## 9. Semantic override ban

Forbidden extension/provider behaviors include:

```text
changing Mission Model meaning after Core loading
reinterpreting raw YAML as an alternate semantic authority
mutating Core-owned structured surfaces
rewriting Core validation findings as authoritative replacements
injecting extension relationships into Core relationship manifests
changing Core runtime-facing or ground-facing contract meaning
presenting extension output as Core output
inventing missing relationship or causal semantics
rewriting Project Lock identity from mutable provider metadata
promoting provider actor/uploader metadata to OrbitFabric publisher identity without evidence
```

If an extension disagrees with Core output, it may emit an extension diagnostic. It must not replace the Core result.

## 10. Integration execution boundary

Core does not import ecosystem-specific adapter implementation code in-process.

The generic integration contract remains external:

```text
OrbitFabric Core
    -> coherent Core Integration Input Set

external Integration Package
    -> static integration_package.json
    -> package-owned Profile schema
    -> external adapter executable

adapter invocation
    -> documented orbitfabric.adapter_cli contract
    -> Integration Result
    -> native target artifacts
```

v1.3 Adapter Manager may install and launch that external entrypoint from a managed adapter environment. This is host-side out-of-process Integration Package execution, not third-party implementation loading into the Core process.

The candidate `orbitfabric.adapter_cli.v1` operation-input lane permits zero or one required file-backed operation input, initially including the generic `scenario` role. Target-specific scenario projection remains adapter-owned.

## 11. Release Source attachment boundary

Provider-specific acquisition occurs outside Core:

```text
Core exact Catalog selection
    -> provider-specific Release Source
    -> exact verified descriptor/artifact bytes
    -> ResolvedAdapterRelease
    -> Core Project Lock lifecycle
```

Core must not depend on GitHub REST, registry APIs or provider authentication merely to preserve this boundary.

A satisfied exact Project Lock state remains satisfied without recontacting a provider.

A future universal provider registration/dispatch mechanism requires separate evidence and architecture. It must not be inferred from the first provider product.

## 12. Downstream consumers and Studio

Downstream tools, including OrbitFabric Studio, consume explicit Core and integration records.

They may:

```text
index
filter
group
navigate
visualize
lay out
present
orchestrate gated actions
```

They must not:

```text
reconstruct Mission Model semantics privately
invent relationships
parse raw YAML as a replacement for Core
turn target-specific integration rules into Core rules
rewrite diagnostics
infer provenance from timestamps alone
```

Studio-specific presentation requirements must not become Core semantic requirements.

## 13. In-process plugin boundary

The Core extensibility contract does not introduce:

```text
in-process third-party plugin discovery
in-process third-party plugin loading
custom lint plugin execution
custom generator plugin execution
remote plugin registry
plugin marketplace
generic extension dependency resolution
```

Adapter Manager's documented out-of-process execution of an installed Integration Package does not change this rule.

Any future in-process Core extension model requires a separate architecture decision.

The existence of a target-aware Studio Integration Plugin API does not alter this Core rule. Studio plugin presentation and Core semantic authority remain separate concerns.

## 14. Relationship semantics

Extensions and downstream consumers must not silently add relationships to a Core-owned Relationship Manifest.

A Core relationship family is admitted only when Core documents narrow semantics and derives records deterministically from explicit loaded Mission Model fields.

An extension may emit extension-owned relationship-like information only when ownership is explicit and it does not masquerade as Core data.

## 15. Compatibility-sensitive governance changes

The following are compatibility-sensitive:

- weakening Core semantic ownership;
- allowing raw-YAML semantic fallback where the stable Core input boundary applies;
- allowing extension output to masquerade as Core output;
- changing extension ownership rules;
- weakening provenance requirements;
- changing the out-of-process adapter boundary;
- introducing third-party implementation loading into the Core process without a separate accepted architecture decision;
- moving provider-specific acquisition into Core;
- changing Project Lock or Source Coordinate identity ownership;
- introducing provider dispatch/version-solving semantics without separate evidence and review;
- treating extension diagnostics or provider facts as Core diagnostics/trust evidence.

## 16. Explicit non-goals

This contract does not introduce:

```text
new Mission Model semantics
new YAML fields
relationship graph execution
dependency graph execution
flight runtime behavior
ground runtime behavior
in-process third-party Core plugin execution
provider-specific acquisition inside Core
provider-neutral provider dispatch/version solving
Studio-specific semantic authority
downstream-specific Core semantics
```

## 17. Final statement

v1.2.0 strengthened the extensibility boundary by stabilizing the coherent Core Integration Input Set while leaving target-specific Profile, Package and Result contracts external.

v1.3.0 preserves that semantic boundary and adds a candidate provider-neutral Adapter Management lifecycle. Core may manage exact external adapter release identity and execute installed Integration Packages out-of-process, while provider-specific acquisition and target-specific semantics remain external.

Core remains the semantic authority. Extensions and providers remain explicit consumers/producers at the edges. No extension or provider gets permission to create a second OrbitFabric semantic model.
