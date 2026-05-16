# Lint Rule Code Stability

Status: Development preview  
Scope: v0.10.0 lint diagnostic compatibility classification  
Applies to: OrbitFabric diagnostic and lint rule codes before v1.0.0

This page classifies OrbitFabric diagnostic and lint rule codes on the path toward v1.0.0.

It is a documentation contract. It does not introduce new lint rules, new diagnostics, new severities, new Mission Model semantics, new report fields, plugin execution, runtime behavior, ground behavior or Studio-specific APIs.

---

## 1. Purpose

OrbitFabric diagnostics are part of the user-facing and machine-readable validation experience.

Diagnostic codes appear in lint output, JSON reports and user workflows. They are therefore compatibility-sensitive before v1.0.0.

This document defines how diagnostic and lint rule codes should evolve before v1.0.0.

It covers:

- diagnostic code stability;
- rule family naming;
- severity changes;
- message and suggestion changes;
- JSON report compatibility;
- downstream tooling expectations;
- non-goals.

The detailed list of current diagnostics remains documented in `Diagnostics and Lint Rules`.

---

## 2. Current classification

Current diagnostic and lint rule surfaces are classified as follows:

| Surface | Classification | Notes |
|---|---|---|
| diagnostic code prefixes | Public preview | Examples: `OF-SYN-*`, `OF-STR-*`, `OF-REF-*`. |
| documented diagnostic codes | Public preview | Examples: `OF-SYN-001`, `OF-REF-001`, `OF-CMD-009`. |
| diagnostic severity values | Public preview | Current values: `ERROR`, `WARNING`, `INFO`. |
| diagnostic JSON fields | Public preview | Current common fields include `severity`, `code`, `file`, `domain`, `object_id`, `message`, `suggestion`. |
| human-readable diagnostic messages | Human-oriented public preview | Useful for users. Not a strict machine contract. |
| diagnostic suggestions | Human-oriented public preview | May improve over time. Not a strict machine contract. |
| lint engine internals | Internal implementation detail | Not a public compatibility surface. |
| test helper structure | Internal validation asset | Not a public compatibility surface. |

No diagnostic or lint rule surface is classified as a stable v1.0 contract yet.

---

## 3. Diagnostic code rule

A diagnostic code identifies a class of issue.

Before v1.0.0, documented diagnostic codes should be treated as compatibility-sensitive.

The same code should keep the same broad meaning across releases.

For example, if a code identifies an unknown telemetry reference, it should not later be reused to identify an unrelated command argument issue.

Diagnostic codes should not be recycled for unrelated checks.

---

## 4. Rule family prefixes

Current rule families are documented with `OF-*` prefixes.

Examples include:

```text
OF-SYN-*  syntax, loading and file shape diagnostics
OF-STR-*  structural Mission Model diagnostics
OF-ID-*   identifier uniqueness diagnostics
OF-REF-*  cross-reference diagnostics
OF-TLM-*  telemetry engineering rules
OF-CMD-*  command engineering rules
OF-SCN-*  scenario diagnostics
```

Rule family prefixes are compatibility-sensitive.

Adding a new family is allowed before v1.0.0, but it should be documented explicitly.

Renaming an existing family is compatibility-sensitive and should be avoided unless the old family was clearly wrong.

---

## 5. Compatibility-sensitive changes

The following changes are compatibility-sensitive before v1.0.0:

- removing a documented diagnostic code;
- renaming a documented diagnostic code;
- reusing a diagnostic code for a different issue class;
- changing a diagnostic from one rule family to another;
- changing the severity of a documented diagnostic;
- changing whether a diagnostic causes a command to fail;
- changing the diagnostic JSON field names;
- removing a documented diagnostic JSON field;
- changing the meaning of `severity`, `code`, `file`, `domain`, `object_id`, `message` or `suggestion`;
- changing `--warnings-as-errors` behavior;
- changing whether a loader, lint or scenario diagnostic is emitted for the same invalid input class.

Compatibility-sensitive does not mean forbidden.

It means the change must be explicit, reviewed and documented.

---

## 6. Severity evolution rule

Severity values are part of the diagnostic contract.

Current severity values are:

```text
ERROR
WARNING
INFO
```

Severity changes should be treated carefully.

Changing a diagnostic from `WARNING` to `ERROR` can make previously passing workflows fail.

Changing a diagnostic from `ERROR` to `WARNING` can make previously rejected models pass.

Both directions are compatibility-sensitive.

---

## 7. Message and suggestion evolution

Human-readable messages and suggestions may improve over time.

The exact wording of `message` and `suggestion` is not a strict machine compatibility contract.

However, message changes should preserve the same diagnostic meaning when the code remains unchanged.

Downstream tools must not rely on parsing human-readable diagnostic text.

They should use structured fields such as:

```text
severity
code
file
domain
object_id
```

---

## 8. JSON report relationship

Lint JSON reports expose diagnostic information for machine use.

The diagnostic code and severity fields are public preview report fields.

Downstream tools may use diagnostic codes and severity values for automation, but must treat the current pre-v1.0 surface as public preview rather than stable v1.0 compatibility.

If a future release changes diagnostic JSON structure, that change should be documented in the JSON report reference and the stability contract.

---

## 9. Adding new diagnostics

Adding a new diagnostic is allowed before v1.0.0.

A new diagnostic should:

- use an appropriate existing family prefix, when possible;
- use a new code number within that family;
- have a clear severity;
- have a specific domain;
- have an actionable message;
- include a suggestion when practical;
- be documented in `Diagnostics and Lint Rules`;
- include tests when implementation is changed.

Adding a new diagnostic can be compatibility-sensitive if it makes existing missions fail or changes CI behavior.

---

## 10. Removing or deprecating diagnostics

Before v1.0.0, diagnostics may still evolve.

However, removal should be deliberate.

A removed diagnostic should not leave a validation gap in the Mission Data Contract unless the rule itself has been explicitly reconsidered.

If a diagnostic is replaced, the replacement code should be documented.

Diagnostic codes should not be silently recycled.

---

## 11. Downstream tool rule

Downstream tools should use diagnostic codes and structured fields, not message text.

Recommended machine-facing fields are:

```text
severity
code
file
domain
object_id
```

Downstream tools must not infer hidden semantics from:

```text
message wording
suggestion wording
terminal formatting
finding order
source code implementation details
private test helper names
```

---

## 12. Current non-goals

This lint rule code stability classification does not introduce:

```text
new lint rules
new diagnostic codes
new diagnostic severities
new JSON report fields
new CLI behavior
new Mission Model semantics
schema migration tooling
SARIF export
JSON Schema publication
plugin lint rules
custom lint plugin support
stable v1.0 diagnostic guarantee
```

---

## 13. Relationship to existing references

This page complements, but does not replace:

```text
Diagnostics and Lint Rules
JSON Reports v0.1
CLI Contract v1 Preview
Stability and Compatibility Contract
```

`Diagnostics and Lint Rules` remains the source for the current list of diagnostic families and implemented rules.

This page defines how those codes should be treated as compatibility-sensitive surfaces before v1.0.0.

---

## 14. v1.0 direction

Before v1.0.0, OrbitFabric should decide which diagnostic families and codes become stable.

Likely v1.0 candidates include:

```text
core syntax diagnostics
core structural diagnostics
core identifier diagnostics
core reference diagnostics
core telemetry, command, event, fault, mode and packet diagnostics
core payload, data product, contact/downlink and commandability diagnostics
core scenario diagnostics
```

v1.0.0 should stabilize diagnostic meaning enough for users and CI workflows to rely on codes, without freezing implementation internals or human-readable wording permanently.
