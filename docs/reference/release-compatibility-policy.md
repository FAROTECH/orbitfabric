# Release Compatibility Policy

Status: Active v1.0 policy  
Scope: release compatibility classification and maintenance discipline  
Applies to: OrbitFabric releases from `v1.0.0 - Stable Mission Data Contract` onward

This page defines how OrbitFabric classifies compatibility impact across releases after v1.0.0.

It is a documentation contract. It does not introduce new version numbers, new release tags, new package metadata, new CLI behavior, new Mission Model semantics, new generated surfaces, plugin execution, runtime behavior, ground behavior or Studio-specific APIs.

---

## 1. Purpose

OrbitFabric v1.0.0 establishes the first stable narrow Mission Data Contract surface.

Compatibility-sensitive changes must be explicit, reviewed and documented.

This policy defines how release changes should be classified after v1.0.0.

It covers:

- release compatibility classes;
- what counts as compatibility-sensitive;
- what counts as additive;
- what counts as internal;
- what patch releases should and should not do;
- how release notes should describe compatibility impact;
- how stable v1.0 surfaces evolve.

---

## 2. Stable v1.0 release status

The v1.0.0 stable surface includes:

```text
Mission Model documented contract semantics
Core structural validation
Core semantic lint diagnostic policy
scenario YAML evidence inputs
lint JSON report
simulation JSON report
model_summary.json
entity_index.json
relationship_manifest.json for admitted families
CLI command interface for documented workflows
release compatibility policy
extensibility boundary contract
```

The following remain preview, disposable or out of scope unless explicitly promoted later:

```text
CLI textual output
generated Markdown mission documentation
plain-text simulation logs
generated C++17 runtime-facing bindings
generated ground-facing dictionaries
runtime_contract_manifest.json
ground_contract_manifest.json
plugin execution
relationship graph behavior
schema migration tooling
JSON Schema publication
security enforcement semantics
Studio-specific API
```

Compatibility review protects users and downstream tools from silent changes.

---

## 3. Release compatibility classes

OrbitFabric uses the following release compatibility classes.

| Class | Meaning | Example |
|---|---|---|
| additive | Adds documented capability without changing existing meaning. | New optional field, new optional report metadata, new documentation page. |
| corrective | Fixes a mistake while preserving intended meaning. | Correcting documentation wording or generated path text. |
| clarifying | Makes existing meaning more explicit. | Boundary clarification or non-goal clarification. |
| compatibility-sensitive | Changes a documented stable, public preview or machine-readable surface. | Rename field, change result token, change diagnostic severity. |
| breaking preview change | Intentionally changes a non-stable preview surface in an incompatible way. | Remove a preview field with explicit note. |
| breaking stable change | Intentionally changes a stable v1.0 surface in an incompatible way. | Remove or rename a stable JSON field. |
| internal-only | Changes internals without changing public behavior or documented surfaces. | Refactor private Python helper structure. |

These classes are not version numbers.

They are review labels for assessing release impact.

---

## 4. Compatibility-sensitive surfaces

A change is compatibility-sensitive when it affects a documented user-facing or machine-readable surface.

Compatibility-sensitive surfaces include:

```text
Mission Model directory layout
Mission Model top-level keys
Mission Model documented field names
Mission Model documented field meanings
controlled values
identifier rules
scenario YAML structure
scenario expectation semantics
CLI command names
CLI command groups
CLI documented options
JSON report top-level fields
JSON report result values
JSON report kind/tool values
lint diagnostic codes
lint diagnostic severities
Core-owned surface kind values
Core-owned surface version fields
generated manifest profile names
generated artifact default paths
boundary flags
release documentation claims
```

Changing any of these must be explicit and documented.

---

## 5. Additive changes

Additive changes are usually acceptable when they do not silently change existing meaning.

Examples include:

```text
adding a new optional documentation page
adding a new optional report field
adding a new optional Mission Model field
adding a new diagnostic code
adding a new generated artifact file while preserving existing files
adding a new boundary flag while preserving existing boundary meanings
```

Additive does not automatically mean harmless.

For example, adding a new diagnostic can affect CI if it changes pass/fail behavior.

Additive changes should still be reviewed when they affect validation, reports or downstream tooling.

---

## 6. Corrective and clarifying changes

Corrective and clarifying changes should preserve intended behavior.

Examples include:

```text
correcting documentation typos
making a non-goal explicit
clarifying that a generated artifact is disposable
clarifying that a JSON report is derived output
clarifying that terminal text is not a machine contract
```

A correction becomes compatibility-sensitive if it changes the documented meaning of a public surface.

---

## 7. Breaking stable changes

Breaking changes to stable v1.0 surfaces are not routine maintenance.

They require explicit release notes, compatibility impact, migration guidance and architectural justification.

Examples include:

```text
removing a stable documented field
renaming a stable documented field
renaming a stable CLI command
changing a stable result token
changing a stable diagnostic severity
changing the meaning of a stable Core-owned surface field
```

Breaking stable changes must not be hidden inside unrelated PRs.

---

## 8. Breaking preview changes

Preview surfaces may still change, but incompatible changes must be deliberate, reviewed and documented.

Examples include:

```text
renaming a preview generated manifest field
changing disposable generated artifact formatting
changing human-oriented terminal wording
changing preview generated dictionary formatting
```

Preview changes should not be described as stable-surface changes unless they affect a selected stable surface.

---

## 9. Patch release rule

Patch releases should be conservative.

Patch releases should normally be limited to:

```text
bug fixes
documentation corrections
release note corrections
CI or packaging fixes
non-semantic refactors
small compatibility clarifications
```

Patch releases should not normally introduce:

```text
new Mission Model domains
new required YAML fields
new generated surfaces
new CLI command groups
new report families
new plugin behavior
new runtime behavior
new ground behavior
```

If a patch release must include a compatibility-sensitive change, that impact must be explicitly documented.

---

## 10. Minor release rule after v1.0.0

After v1.0.0, minor releases may introduce new preview capabilities and additive stable-surface extensions.

However, every minor release should clearly state whether it changes:

```text
Mission Model semantics
CLI surface
JSON report structure
lint diagnostic behavior
generated artifact structure
Core-owned structured surfaces
scenario evidence behavior
public documentation claims
```

A minor release should keep architectural boundaries explicit.

It should not blur OrbitFabric into flight software, ground software, simulator runtime, plugin execution platform or Studio-specific backend.

---

## 11. Release note expectations

Release notes should identify compatibility impact clearly.

For every release after v1.0.0, release notes should preferably include:

```text
Summary
Compatibility impact
Mission Data Contract impact
CLI impact
JSON report impact
Generated artifact impact
Lint diagnostic impact
Scenario evidence impact
Architectural boundary
Migration notes, if needed
```

If there is no impact in an area, release notes should say so clearly.

This reduces ambiguity for users and downstream tooling.

---

## 12. PR review rule

PRs that affect compatibility-sensitive surfaces should say so explicitly.

A PR should not claim to be internal-only if it changes:

```text
Mission Model documented fields
CLI documented commands or options
JSON report structures
lint diagnostic codes or severities
scenario expectation semantics
generated artifact paths
Core-owned surface fields
public documentation compatibility claims
```

The PR template remains the operational review checkpoint.

This policy clarifies what reviewers should look for.

---

## 13. Deprecation rule after v1.0.0

When practical, a compatibility-sensitive replacement should be documented with:

```text
old surface
new surface
reason for change
migration note
expected removal timing, if known
```

Diagnostic codes, result tokens and public field names should not be silently recycled.

---

## 14. Current non-goals

This release compatibility policy does not introduce:

```text
new version numbers
new release tags
new package metadata
new release automation
new changelog generator
new schema migration tooling
new JSON Schema publication
new Mission Model semantics
new CLI behavior
new JSON report fields
new generated surfaces
plugin execution
plugin discovery
plugin loader
relationship graph
dependency graph
runtime behavior
ground behavior
Studio-specific API
```

---

## 15. Relationship to existing references

This page complements, but does not replace:

```text
Versioning Model
Stability and Compatibility Contract
Mission Model Stability Contract
CLI Contract v1 Preview
Generated Surfaces Stability
Lint Rule Code Stability
JSON Report Compatibility
Scenario Evidence Stability
```

`Versioning Model` explains what version fields mean.

This page explains how release changes should be classified for compatibility review after v1.0.0.

---

## 16. Stable v1.0 direction

OrbitFabric v1.0.0 stabilizes the Mission Data Contract core.

Future releases should preserve that narrowness.

The stable contract protects Mission Data Contract workflows without turning OrbitFabric into flight software, a ground segment, a simulator runtime, a visual modeling database or a plugin execution platform.
