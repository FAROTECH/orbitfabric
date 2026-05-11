# Diagnostics and Lint Rules

This page documents the diagnostics and lint rules currently implemented by OrbitFabric.

Current documented baseline:

```text
v0.8.0 - Ground Integration Artifacts
```

OrbitFabric diagnostics are intentionally actionable. A diagnostic should tell the user:

- what is wrong;
- where it was found;
- which Mission Model domain is affected;
- how to fix it.

Diagnostics may be produced by different layers:

- the Mission Model loader;
- the semantic lint engine;
- the scenario loader;
- scenario reference validation.

Not every diagnostic listed here is produced by the same command.

---

## Severity levels

| Severity | Meaning |
|---|---|
| `ERROR` | The model, scenario or operation is invalid and the command must fail. |
| `WARNING` | The model is structurally valid, but an engineering concern was found. |
| `INFO` | Informational diagnostic. Currently reserved for future use. |

Default lint behavior:

```text
ERROR   -> lint fails
WARNING -> lint passes with warnings
INFO    -> lint passes
```

With:

```bash
orbitfabric lint <mission-dir> --warnings-as-errors
```

warning-level findings also make lint fail.

---

## Diagnostic shape

OrbitFabric diagnostics expose a common diagnostic shape across Mission Model loading, scenario loading, scenario reference validation and semantic lint findings.

| Field | Meaning |
|---|---|
| `severity` | Diagnostic severity. |
| `code` | Stable diagnostic or rule identifier. |
| `file` | File where the issue was found, when known. |
| `domain` | Mission Model or scenario domain. |
| `object_id` | Object affected by the diagnostic, when known. |
| `message` | Human-readable explanation. |
| `suggestion` | Suggested fix, when available. |

---

## Rule families

| Prefix | Family |
|---|---|
| `OF-SYN-*` | YAML syntax, file loading and file shape diagnostics. |
| `OF-STR-*` | Structural Mission Model diagnostics. |
| `OF-ID-*` | Identifier uniqueness diagnostics. |
| `OF-REF-*` | Cross-reference diagnostics. |
| `OF-TLM-*` | Telemetry engineering lint rules. |
| `OF-CMD-*` | Command engineering lint rules. |
| `OF-EVT-*` | Event engineering lint rules. |
| `OF-FLT-*` | Fault engineering lint rules. |
| `OF-MODE-*` | Mode and mode-transition diagnostics. |
| `OF-PKT-*` | Packet engineering lint rules. |
| `OF-PAY-*` | Payload Contract lint rules. |
| `OF-DP-*` | Data Product Contract lint rules. |
| `OF-CON-*` | Contact assumption rules. |
| `OF-DL-*` | Downlink flow assumption rules. |
| `OF-CAB-*` | Commandability rule diagnostics. |
| `OF-AUT-*` | Autonomous action diagnostics. |
| `OF-REC-*` | Recovery intent diagnostics. |
| `OF-SCN-*` | Scenario loading and scenario reference diagnostics. |

---

## Current required Mission Model files

```text
spacecraft.yaml
subsystems.yaml
modes.yaml
telemetry.yaml
commands.yaml
events.yaml
faults.yaml
packets.yaml
policies.yaml
```

Current optional Mission Model files:

```text
payloads.yaml
data_products.yaml
contacts.yaml
commandability.yaml
```

---

## Current command coverage

Current behavior:

| Command | Diagnostics produced |
|---|---|
| `orbitfabric lint <mission-dir>` | Mission Model loading diagnostics, structural diagnostics, semantic lint findings. |
| `orbitfabric gen docs <mission-dir>` | Mission Model loading diagnostics; generation aborts if lint errors exist. |
| `orbitfabric gen data-flow <mission-dir>` | Mission Model loading diagnostics; generation aborts if lint errors exist. |
| `orbitfabric gen runtime <mission-dir>` | Mission Model loading diagnostics; generation aborts if lint errors exist. |
| `orbitfabric gen ground <mission-dir>` | Mission Model loading diagnostics; generation aborts if lint errors exist. |
| `orbitfabric sim <scenario-file>` | Scenario loading diagnostics, Mission Model loading diagnostics, scenario reference diagnostics and scenario execution failures. |

---

## Ground generation note

v0.8.0 does not add a dedicated ground-specific diagnostic family.

Ground artifact generation consumes the already validated Mission Model and aborts when lint errors exist.

This is intentional.

Ground-facing generated artifacts must not reinterpret raw YAML, bypass validation or invent new semantics outside the Mission Data Contract.

---

## Notes for contributors

When adding a new diagnostic or lint rule:

1. assign a stable `OF-*` code;
2. choose the correct family prefix;
3. use `ERROR` only when the model or scenario is invalid;
4. use `WARNING` for engineering concerns that are valid but risky or incomplete;
5. provide an actionable message;
6. provide a suggested fix where possible;
7. add or update tests;
8. update this rule catalog.

Do not document a rule as implemented until it exists in code and is covered by tests.

The full rule tables are intentionally kept in the source history and tests as the implementation evolves toward v1.0. This page documents the current family coverage and command behavior for the v0.8.0 development preview.
