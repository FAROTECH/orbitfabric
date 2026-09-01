# Integration Operation-Input Contract Lane

Status: Candidate extension contract, promoted for conformance  
Manifest version: `0.2-candidate`  
Execution protocol: `orbitfabric.adapter_cli.v1`  
Result version: `0.2-candidate`

## Purpose

This contract extends the external Integration Package boundary with one
explicit operation-specific semantic input while preserving IISS and
Projection Profile as common context.

It does not change Mission Model, Scenario, IISS, Profile, Plugin API, target
projection, downstream execution, or native evidence ownership.

## Manifest

Every operation includes `input_requirements`.

```json
{
  "id": "project",
  "capabilities": ["projection"],
  "input_requirements": []
}
```

```json
{
  "id": "verification_projection",
  "capabilities": ["projection"],
  "input_requirements": [
    {"role": "scenario"}
  ]
}
```

The field is required. Empty means no additional input. The initial revision
allows at most one requirement. A declared role is required exactly once.
Unknown roles are incompatible. Operation ids remain opaque and
integration-owned.

## Execution

Canonical direct-argv form:

```text
<argv-prefix> run
    --operation <operation-id>
    --input-set-manifest <path>
    --profile <path>
    [--operation-input <role> <path>]
    --output-dir <path>
```

The generic consumer and adapter both reject missing, unexpected, or
duplicate roles. File paths are locators and are not semantic identity. No
shell, environment binding, inline JSON, or binding envelope is defined.

## Result provenance

Result `0.2-candidate` always contains `inputs.operation_inputs`.

Zero-input success:

```json
"operation_inputs": []
```

Consumed Scenario:

```json
{
  "role": "scenario",
  "status": "available",
  "id": "scenario-id",
  "sha256": "<exact consumed bytes>",
  "reason": null
}
```

Unavailable required Scenario on failure:

```json
{
  "role": "scenario",
  "status": "unavailable",
  "id": null,
  "sha256": null,
  "reason": "<diagnostic>"
}
```

Successful Results require available provenance for every declared role.

## Freshness

Positive currentness requires exact reliable matches for IISS, Profile, and
every declared operation input.

```text
all required dimensions equal -> fresh
available mismatch             -> stale
required dimension unavailable -> unknown
```

For an empty requirement list, operation-input freshness is satisfied without
inventing a resource.

## Published resources

Core publishes:

```text
orbitfabric/contracts/integration/
  integration-package-manifest-0.2-candidate.schema.json
  integration-result-0.2-candidate.schema.json
```

Reusable validation:

```bash
python -m orbitfabric.conformance.integration_contracts manifest MANIFEST
python -m orbitfabric.conformance.integration_contracts bindings MANIFEST OPERATION --role scenario
python -m orbitfabric.conformance.integration_contracts result MANIFEST RESULT
```

Install the `conformance` optional dependency when using the checker.

