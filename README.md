OrbitFabric is a model-first Mission Data Fabric for small spacecraft.

It lets small spacecraft teams define telemetry, commands, events, faults, operational modes, packets and operational scenarios once, in a single Mission Data Contract, and then use that contract to validate consistency, generate documentation, run simulations and prepare future onboard and ground integration artifacts.

OrbitFabric is not a flight software framework, not a ground segment and not a spacecraft dynamics simulator.

It is the contract layer between mission design, onboard software, simulation, testing, documentation and ground integration.

> Define once. Validate. Simulate. Test. Document. Integrate.

---

## Current Status

OrbitFabric is in early MVP development.

The current v0.1 vertical slice is already functional:

- Mission Model YAML loading;
- structural validation;
- semantic linting;
- engineering lint rules;
- JSON lint report generation;
- generated Markdown documentation;
- scenario YAML loading;
- scenario reference validation;
- deterministic scenario execution;
- simulation JSON report generation;
- simulation plain-text log generation;
- synthetic demo mission: `demo-3u`.

Current quality baseline:

```text
ruff check .  -> passing
pytest        -> 34 tests passing