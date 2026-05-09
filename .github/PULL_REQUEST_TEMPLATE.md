## Summary

Describe the purpose of this pull request.

State the milestone or project area when relevant, for example:

`v0.7 — Generated Runtime Skeletons`

## Changes

List the concrete changes introduced by this PR.

- 
- 
- 

## Affected Area

Select all that apply:

- [ ] Mission Model
- [ ] Model loading / validation
- [ ] Semantic lint rules
- [ ] Scenario loading / validation
- [ ] Scenario simulation
- [ ] JSON reports
- [ ] Documentation generation
- [ ] Generated artifacts
- [ ] Example missions
- [ ] CI / tooling
- [ ] Public documentation
- [ ] Release alignment
- [ ] Other

## Mission Data Contract Impact

Does this PR change Mission Data Contract semantics?

- [ ] No
- [ ] Yes

If yes, describe the impact clearly.

Examples:

- new model field
- new reference rule
- new lint diagnostic
- new generated artifact
- changed JSON report structure
- changed scenario expectation semantics

## Architectural Boundary

State what this PR intentionally does **not** implement.

This section is required for any non-trivial change.

Examples:

- real flight runtime
- real onboard storage runtime
- real downlink queue execution
- real contact scheduling
- RF/link-budget behavior
- CCSDS/PUS/CFDP runtime behavior
- ground segment implementation
- operator console
- command authentication/authorization
- runtime skeleton generation
- flight-ready software

## Clean-Room Confirmation

By opening this PR, I confirm that this contribution does not include:

- [ ] proprietary mission data
- [ ] private spacecraft architecture
- [ ] private packet formats
- [ ] real operational logs
- [ ] non-public payload details
- [ ] real bus maps or pinouts
- [ ] employer-owned or customer-owned code
- [ ] export-controlled or NDA-protected material

All examples are synthetic or derived only from public information.

## Validation

Select the checks that were run.

- [ ] `ruff check .`
- [ ] `pytest`
- [ ] `mkdocs build --strict`
- [ ] `orbitfabric lint examples/demo-3u/mission/ --json generated/reports/lint_report.json`
- [ ] `orbitfabric gen docs examples/demo-3u/mission/`
- [ ] `orbitfabric gen data-flow examples/demo-3u/mission/ --output-file generated/docs/data_flow.md`
- [ ] `orbitfabric sim examples/demo-3u/scenarios/battery_low_during_payload.yaml --json generated/reports/battery_low_during_payload_report.json --log generated/logs/battery_low_during_payload.log`
- [ ] `orbitfabric sim examples/demo-3u/scenarios/payload_data_flow_evidence.yaml --json generated/reports/payload_data_flow_evidence_report.json --log generated/logs/payload_data_flow_evidence.log`

If some checks were not run, explain why.

## Generated Artifacts

- [ ] This PR does not commit generated artifacts.
- [ ] This PR intentionally updates generated artifacts.

If generated artifacts are committed, explain why.

## Notes for Review

Add anything the reviewer should pay attention to.
