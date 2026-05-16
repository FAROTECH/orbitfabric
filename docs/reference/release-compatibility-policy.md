# Release Compatibility Policy

Status: Development preview  
Scope: v0.10.0 release compatibility classification  
Applies to: OrbitFabric releases before v1.0.0

This page defines how OrbitFabric should classify compatibility impact across releases on the path toward v1.0.0.

It is a documentation contract. It does not introduce new version numbers, new release tags, new package metadata, new CLI behavior, new Mission Model semantics, new generated surfaces, plugin execution, runtime behavior, ground behavior or Studio-specific APIs.

---

## 1. Purpose

OrbitFabric is still before v1.0.0.

That means its public surfaces may still evolve, but compatibility-sensitive changes must be explicit, reviewed and documented.

This policy defines how release changes should be classified before v1.0.0.

It covers:

- release compatibility classes;
- what counts as compatibility-sensitive;
- what counts as additive;
- what counts as internal;
- what patch releases should and should not do;
- how release notes should describe compatibility impact;
- what v1.0.0 should eventually stabilize.

---

## 2. Current release status

Current OrbitFabric releases are development-preview releases.

No current release before v1.0.0 should be interpreted as a full stable compatibility guarantee.

However, the following surfaces are already public enough to require explicit compatibility review:

```text
Mission Model YAML
scenario YAML
CLI commands and documented options
lint diagnostic codes
JSON report fields
generated manifest fields
Core-owned structured surfaces
generated artifact paths
reference documentation claims
```

Compatibility review protects users and downstream tools from silent changes.

---

## 3. Release compatibility classes

OrbitFabric uses the following release compatibility classes before v1.0.0.

| Class | Meaning | Example |
|---|---|---|
| additive | Adds documented capability without changing existing meaning. | New optional field, new optional report metadata, new documentation page. |
| corrective | Fixes a mistake while preserving intended meaning. | Correcting documentation wording or generated path text. |
| clarifying | Makes existing meaning more explicit. | Boundary clarification or non-goal clarification. |
| compatibility-sensitive | Changes a documented public or preview surface. | Rename field, change result token, change diagnostic severity. |
| breaking preview change | Intentionally changes a development-preview surface in an incompatible way. | Remove documented field before v1.0 with explicit note. |
| internal-only | Changes internals without changing public behavior or documented surfaces. | Refactor private Python helper structure. |

These classes are not version numbers.

They are review labels for assessing release impact.

---

## 4. Compatibility-sensitive surfaces

A change is compatibility-sensitive when it affects a documented user-facing or machine-readable surface.

Current compatibility-sensitive surfaces include:

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

Additive changes are usually acceptable before v1.0.0 when they do not silently change existing meaning.

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

## 7. Breaking preview changes

Before v1.0.0, OrbitFabric may still make breaking preview changes.

Breaking preview changes are allowed only when they are deliberate, reviewed and documented.

Examples include:

```text
removing a documented field
renaming a documented field
renaming a CLI command
changing a result token
changing a diagnostic severity
changing a generated manifest profile name
changing the meaning of a Core-owned surface
changing whether a domain is required or optional
```

Breaking preview changes should not be hidden inside unrelated PRs.

They should have a clear PR title, release note and migration explanation when practical.

---

## 8. Patch release rule

Before v1.0.0, patch releases should be conservative.

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

## 9. Minor release rule before v1.0.0

Before v1.0.0, minor releases may introduce new preview capabilities.

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

## 10. Release note expectations

Release notes should identify compatibility impact clearly.

For any release after v0.10.0, release notes should preferably include:

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

## 11. PR review rule

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

## 12. Deprecation rule before v1.0.0

Before v1.0.0, OrbitFabric does not need a heavy deprecation framework.

However, when practical, a compatibility-sensitive replacement should be documented with:

```text
old surface
new surface
reason for change
migration note
expected removal timing, if known
```

Diagnostic codes, result tokens and public field names should not be silently recycled.

---

## 13. Current non-goals

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
stable v1.0 compatibility guarantee
```

---

## 14. Relationship to existing references

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

This page explains how release changes should be classified for compatibility review before v1.0.0.

---

## 15. v1.0 direction

Before v1.0.0, OrbitFabric should converge on a stable compatibility promise for the Mission Data Contract.

v1.0.0 should define which of the following become stable:

```text
Mission Model schema
scenario input semantics
CLI core workflow commands
lint diagnostic code meanings
JSON report families
Core-owned structured surfaces
generated manifest boundaries
release note compatibility sections
```

The stable v1.0 contract should remain narrow.

It should protect Mission Data Contract workflows without turning OrbitFabric into flight software, a ground segment, a simulator runtime, a visual modeling database or a plugin execution platform.
