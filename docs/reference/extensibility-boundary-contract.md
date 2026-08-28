# Extensibility Boundary Contract

Status: Active v1.x governance contract through v1.2.0  
Scope: extensibility ownership and semantic boundary  
Applies to: downstream consumers and extension-owned integration contracts from v1.0.0 onward

OrbitFabric Core is a Mission Data Contract framework. Extensibility must preserve that identity.

The central rule is:

```text
Mission Model is the semantic source of truth.
Core owns Mission Data Contract interpretation.
Extensions add value at the edges.
Extensions must not redefine Core semantics.
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

They may be consumed by downstream tools but are not silently promoted into the stable Core surface by v1.2.

## 3. Candidate extension integration contracts

The generic Integration Framework defines three separately owned extension contracts:

```text
Projection Profile
Integration Result
Integration Package / Adapter Execution
```

They remain `0.1-candidate` after v1.2.0.

They are design-frozen and reference-proven, but they are not stable Core Mission Data Contract surfaces.

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

## 4. Core-owned semantics

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
stability and compatibility classification
release compatibility policy
```

An extension must not override, replace, mutate or privately reinterpret these semantics.

## 5. No raw-YAML semantic fallback

The stable v1.2 Core Integration Input boundary exists specifically so external integration adapters do not need a second Mission Model parser.

For semantic projection, an adapter must consume the documented Core Integration Input Set and validate required surface compatibility.

If a required Core surface is missing, failed or incompatible, the adapter must stop semantic projection. It must not reparse raw Mission Model YAML to reconstruct the missing semantics.

This rule prevents the integration ecosystem from developing parallel interpretations of the Mission Data Contract.

## 6. Extension-owned outputs

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
```

An extension output must not be presented as Core output unless OrbitFabric Core itself produces and documents that surface.

## 7. Provenance

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

## 8. Semantic override ban

Forbidden extension behaviors include:

```text
changing Mission Model meaning after Core loading
reinterpreting raw YAML as an alternate semantic authority
mutating Core-owned structured surfaces
rewriting Core validation findings as authoritative replacements
injecting extension relationships into Core relationship manifests
changing Core runtime-facing or ground-facing contract meaning
presenting extension output as Core output
inventing missing relationship or causal semantics
```

If an extension disagrees with Core output, it may emit an extension diagnostic. It must not replace the Core result.

## 9. Integration execution boundary

Core does not dynamically discover, load or execute ecosystem-specific adapters in-process.

The generic execution model is:

```text
OrbitFabric Core CLI
    -> coherent Core Integration Input Set

external Integration Package
    -> static integration_package.json
    -> package-owned Profile schema
    -> external adapter executable

adapter invocation
    -> orbitfabric.adapter_cli.v0
    -> Integration Result
    -> native target artifacts
```

This preserves trust separation and keeps third-party integration dependencies out of Core.

## 10. Downstream consumers and Studio

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

## 11. Plugin execution

The Core extensibility contract does not introduce:

```text
plugin discovery
plugin loading
plugin execution
custom lint plugin execution
custom generator plugin execution
third-party code execution inside Core
remote plugin registry
plugin marketplace
extension dependency resolution
```

Any future Core execution model requires a separate architecture decision.

The existence of a target-aware Studio Integration Plugin API does not alter this Core rule. Studio plugin presentation and Core semantic authority remain separate concerns.

## 12. Relationship semantics

Extensions and downstream consumers must not silently add relationships to a Core-owned Relationship Manifest.

A Core relationship family is admitted only when Core documents narrow semantics and derives records deterministically from explicit loaded Mission Model fields.

An extension may emit extension-owned relationship-like information only when ownership is explicit and it does not masquerade as Core data.

## 13. Compatibility-sensitive governance changes

The following are compatibility-sensitive:

- weakening Core semantic ownership;
- allowing raw-YAML semantic fallback where the stable Core input boundary applies;
- allowing extension output to masquerade as Core output;
- changing extension ownership rules;
- weakening provenance requirements;
- changing the out-of-process adapter boundary;
- introducing execution into Core without a separate accepted architecture decision;
- treating extension diagnostics as Core diagnostics.

## 14. Explicit non-goals

This contract does not introduce:

```text
new Mission Model semantics
new YAML fields
relationship graph execution
dependency graph execution
runtime behavior
ground behavior
Core plugin execution
Studio-specific semantic authority
OpenOBSW/OpenSVF/YAMCS-specific Core semantics
```

## 15. Final statement

v1.2.0 strengthens the extensibility boundary by stabilizing the coherent Core Integration Input Set while leaving target-specific Profile, Package and Result contracts external and candidate.

Core remains the semantic authority. Extensions remain explicit consumers and producers at the edges. No extension gets permission to create a second OrbitFabric semantic model.
