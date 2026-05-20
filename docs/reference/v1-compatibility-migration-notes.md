# v1.0 Compatibility and Migration Notes

Status: Proposed for v1.0.0  
Scope: v1.0 compatibility posture and migration-note discipline  
Applies to: OrbitFabric Core after `v0.12.0 - v1.0 Release Candidate Hardening`

This page defines the compatibility and migration posture for the path toward `v1.0.0 - Stable Mission Data Contract`.

It records the current expected compatibility status after the v1.0 stable surface decision, the first golden signatures for Core-owned structured surfaces and the v1.0 demo evidence chain reference.

It is a documentation policy and release-governance reference only.

It does not introduce schema migration tooling, JSON Schema publication, migration commands, compatibility scanners, new Mission Model semantics, new YAML fields, new CLI behavior, new JSON report fields, new generated surfaces, runtime behavior, ground behavior, plugin discovery, plugin loading, plugin execution, metadata schema, metadata parser, metadata loader, metadata validator or Studio-specific APIs.

---

## 1. Purpose

The path toward v1.0.0 requires explicit answers to two questions:

```text
What will OrbitFabric keep compatible after v1.0.0?
What should pre-v1.0 users know if a preview surface changes before v1.0.0?
```

This page records how those answers should be written and what the current v1.0 compatibility posture is.

It does not introduce new compatibility tooling.

It does not make every existing public surface stable.

---

## 2. Relationship to existing references

This page complements these references:

```text
Stability and Compatibility Contract
Release Compatibility Policy
v1.0 Candidate Surface Inventory
v1.0 Stable Surface Decision
v1.0 Demo Evidence Chain
Golden Output and Regression Confidence Policy
Mission Model Stability Contract
CLI Contract v1 Preview
JSON Report Compatibility
Scenario Evidence Stability
Generated Surfaces Stability
Extensibility Boundary Contract
```

The Stable Surface Decision identifies the narrow proposed v1.0 stable surface.

The Demo Evidence Chain explains the selected end-to-end proof path for the existing `demo-3u` Mission Model.

The Golden Output and Regression Confidence Policy explains how selected outputs can be protected from accidental drift.

The committed v1.0 golden signatures now protect selected fields of:

```text
model_summary.json
entity_index.json
relationship_manifest.json
```

This page explains how to document compatibility decisions and migration notes around those surfaces.

---

## 3. Compatibility note versus migration note

### 3.1 Compatibility note

A compatibility note explains whether a surface remains compatible, changes compatibility class or requires careful review.

A compatibility note should be used when a public, candidate or stable surface changes or is being stabilized.

Examples:

```text
This field remains public preview and is not yet a stable v1.0 contract.
This report family is a v1.0 candidate and changes to top-level fields are compatibility-sensitive.
This generated artifact remains disposable and should not be treated as a stable ABI.
```

### 3.2 Migration note

A migration note explains what a user or downstream tool should do when a surface changes.

A migration note should be used when a change affects existing usage.

Examples:

```text
Use the new field name instead of the old field name.
Stop consuming terminal text and consume the JSON report instead.
Regenerate disposable artifacts from the Mission Model rather than editing generated files.
Update downstream tooling to consume `entity_index.json` instead of scanning raw YAML.
```

A migration note is not a migration tool.

---

## 4. When notes are required

Before v1.0.0, compatibility or migration notes should be required for changes that affect:

```text
Mission Model documented fields
Mission Model documented field meanings
Mission Model controlled values
Mission Model identifier rules
scenario YAML structure
scenario expectation semantics
CLI command names
CLI command groups
CLI documented options
lint diagnostic codes
lint diagnostic severities
JSON report top-level fields
JSON report result values
JSON report kind values
Core-owned structured surface fields
Core-owned structured surface kind values
Core-owned structured surface version fields
relationship family names
relationship endpoint meaning
generated manifest fields
generated artifact default paths
manifest profile names
boundary flags
public documentation compatibility claims
```

If a change only affects private implementation details, a migration note is usually not required.

If a change affects a human-oriented document or generated Markdown wording without changing contract meaning, a compatibility note may be enough.

---

## 5. Recommended note structure

A compatibility or migration note should be short, explicit and scoped.

Recommended structure:

```text
Surface:
Status:
Change type:
Compatibility impact:
Migration guidance:
Reason:
Scope boundary:
```

### 5.1 Surface

Name the affected surface.

Examples:

```text
Mission Model YAML
scenario YAML
lint JSON report
simulation JSON report
model_summary.json
entity_index.json
relationship_manifest.json
runtime_contract_manifest.json
ground_contract_manifest.json
CLI command: orbitfabric lint
```

### 5.2 Status

Use one of these statuses:

```text
stable v1.0 candidate
stable v1.0 selected surface
public preview
candidate contract
generated disposable artifact
internal implementation detail
out of v1.0 scope
```

### 5.3 Change type

Use the release compatibility classes already defined by the Release Compatibility Policy:

```text
additive
corrective
clarifying
compatibility-sensitive
breaking preview change
internal-only
```

### 5.4 Compatibility impact

State the actual impact.

Examples:

```text
No Mission Data Contract impact.
Compatibility-sensitive for downstream tools consuming JSON reports.
Breaking preview change for tools consuming the previous field name.
Internal-only change with no public surface impact.
```

### 5.5 Migration guidance

State what users or downstream tools should do.

Examples:

```text
No migration required.
Regenerate generated artifacts from the Mission Model.
Consume the JSON report instead of terminal output.
Update downstream tooling to use the new field name.
Treat this artifact as disposable and do not patch it manually.
```

### 5.6 Reason

Explain why the change exists.

Examples:

```text
Clarifies the existing boundary.
Aligns the generated surface with the documented contract.
Removes ambiguity before v1.0.0.
Prevents downstream tools from reconstructing semantics from raw YAML.
```

### 5.7 Scope boundary

State what the note does not imply.

Examples:

```text
This does not introduce runtime behavior.
This does not introduce ground behavior.
This does not introduce plugin discovery, loading or execution.
This does not make the surface stable v1.0 unless explicitly stated by the v1.0 release.
```

---

## 6. Current v1.0 compatibility posture

The current expected v1.0 compatibility posture is:

```text
Mission Model documented contract semantics: stable v1.0 selected surface
Core structural validation: stable v1.0 selected surface
Core semantic lint diagnostic policy: stable v1.0 selected surface
scenario YAML evidence inputs: stable v1.0 selected surface
lint JSON report: stable v1.0 selected surface
simulation JSON report: stable v1.0 selected surface
model_summary.json: stable v1.0 selected surface, golden signature protected
entity_index.json: stable v1.0 selected surface, golden signature protected
relationship_manifest.json: stable v1.0 selected surface, golden signature protected for admitted families
CLI command interface for documented workflows: stable v1.0 selected surface
release compatibility policy: stable v1.0 selected governance surface
extensibility boundary contract: stable v1.0 selected governance surface
CLI textual output: public preview, human-oriented
orbitfabric inspect mission terminal output: public preview, human-oriented
orbitfabric validate scenario terminal output: public preview, human-oriented
generated Markdown docs: public preview generated documentation
demo mission narrative text: public example
plain-text simulation logs: public preview, human-oriented
generated C++17 runtime-facing bindings: public preview disposable generated artifact
generated ground-facing dictionaries: public preview disposable generated artifact
runtime_contract_manifest.json: public preview generated manifest
ground_contract_manifest.json: public preview generated manifest
Python internals: internal implementation detail
plugin discovery/loading/execution: out of v1.0 Core scope
schema migration tooling: out of v1.0 Core scope
JSON Schema publication: out of v1.0 Core scope
security enforcement semantics: out of v1.0 Core scope
relationship graph behavior: out of v1.0 Core scope
Studio-specific API: out of v1.0 Core scope
```

This posture follows the v1.0 Stable Surface Decision.

It must not be silently changed by unrelated work.

Any later PR that changes one of the selected stable surfaces must include an explicit compatibility or migration note.

---

## 7. Migration posture from v0.12.0 to the current v1.0 candidate state

No migration is required from the v0.12.0 release candidate hardening baseline to the current v1.0 candidate documentation and regression-test state.

The changes introduced after v0.12.0 are governance, documentation and regression-confidence changes:

```text
v1.0 Stable Surface Decision
v1.0 golden signatures for Core-owned structured surfaces
v1.0 Demo Evidence Chain reference
```

These changes do not add, remove or rename:

```text
Mission Model fields
Mission Model domains
controlled values
reference rules
lint diagnostics
scenario expectations
JSON report fields
Core-owned structured surface fields
generated artifact families
CLI commands
CLI options
```

They do not require users to rewrite mission YAML files.

They do not require downstream tools to migrate field names.

They do not require regenerated artifacts for compatibility reasons.

Recommended user action:

```text
No migration required.
Continue treating the Mission Model as the source of truth.
Regenerate disposable artifacts from the Mission Model when needed.
Consume Core-owned structured JSON surfaces instead of terminal text, generated Markdown or raw YAML reconstruction.
```

---

## 8. Stable surface change discipline after v1.0.0

After v1.0.0, a change to a selected stable surface is compatibility-sensitive when it affects:

```text
field presence
field meaning
kind values
version fields
identifier rules
relationship family names
relationship endpoint meaning
boundary flags
result values
lint diagnostic codes
scenario evidence semantics
CLI command names
CLI documented options
```

Allowed additive changes must remain clearly additive.

Corrective changes must explain why the previous behavior was inconsistent with the documented contract.

Breaking changes to stable surfaces must not be hidden inside unrelated work.

---

## 9. Generated artifact migration principles

Migration guidance should follow these principles.

### 9.1 Prefer regeneration over manual patching

Generated artifacts should be regenerated from the Mission Model.

Users should not manually patch generated runtime-facing or ground-facing artifacts as a migration strategy.

### 9.2 Prefer Core-owned structured surfaces over derived text

Downstream tools should consume:

```text
model_summary.json
entity_index.json
relationship_manifest.json
```

They should not reconstruct Core semantics from:

```text
raw YAML
generated Markdown
generated runtime files
generated ground files
stdout or stderr text
plain-text logs
file names
ID naming conventions
UI state
private extension assumptions
```

### 9.3 Prefer compatibility notes over tooling before v1.0.0

Before v1.0.0, compatibility notes are enough.

OrbitFabric should not introduce schema migration tooling unless a separate architectural decision accepts that scope.

### 9.4 Prefer explicit deferral over vague stability

If a surface is not ready for v1.0, say so.

A deferred surface is safer than an ambiguous stable-sounding claim.

### 9.5 Keep v1.0 narrow

v1.0.0 should stabilize the Mission Data Contract core.

It should not stabilize flight runtime behavior, ground runtime behavior, plugin execution, Studio-specific APIs or graph engines.

---

## 10. Standard note outcomes before v1.0.0

Before v1.0.0, review outcomes should fall into one of these categories:

| Outcome | Meaning |
|---|---|
| Accepted for v1.0 stable contract | The surface is intended to become part of the stable v1.0 Mission Data Contract. |
| Remains candidate contract | The surface is important but needs more review before being declared stable. |
| Remains public preview | The surface remains documented and usable but not stable. |
| Remains generated disposable artifact | The output remains reproducible and useful but should not be patched or treated as source of truth. |
| Deferred beyond v1.0 | The decision is intentionally postponed and should not block v1.0.0. |
| Explicitly out of v1.0 scope | The surface or feature is outside the stable Core target. |
| Migration note required | Existing users or downstream tools need explicit guidance. |
| No migration required | The change is clarifying, additive or internal-only. |

A v1.0 release candidate should not leave central surfaces in an ambiguous state.

---

## 11. Release note expectations

Future release notes on the path to v1.0.0 should include a compatibility section when relevant.

Recommended release note fields:

```text
Compatibility impact
Migration notes
Mission Data Contract impact
CLI impact
JSON report impact
Generated artifact impact
Lint diagnostic impact
Scenario evidence impact
Core-owned structured surface impact
Architectural boundary
```

If there is no migration impact, release notes should say:

```text
No migration required.
```

If a surface remains preview, release notes should say so explicitly.

---

## 12. Non-goals

This page does not introduce:

```text
schema migration tooling
migration commands
compatibility scanners
JSON Schema publication
new Mission Model semantics
new YAML fields
new CLI behavior
new JSON report fields
new generated surfaces
new lint diagnostics
new scenario behavior
new golden files
new snapshot tests
new CI jobs
runtime behavior
ground behavior
plugin discovery
plugin loading
plugin execution
metadata schema
metadata parser
metadata loader
metadata validator
relationship graph
dependency graph
Studio-specific API
security enforcement semantics
```

This page only defines the current v1.0 compatibility posture and how compatibility and migration notes should be written before v1.0.0.
