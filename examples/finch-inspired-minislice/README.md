# FINCH-inspired Minislice

This example is a small FINCH-inspired public conceptual demo for OrbitFabric.

It is derived from the generic:

    examples/university-cubesat-minislice/

and follows the controlled-specialization pattern used by:

    examples/oresat-inspired-minislice/

The example is inspired by publicly available UTAT Space Systems / FINCH material.

## Status and scope

This example is:

- public-material-derived;
- conceptual;
- intentionally small;
- intended for OrbitFabric validation, simulation and documentation generation;
- an external open-source example;
- not an official FINCH model.

This example is not:

- an official FINCH configuration;
- endorsed by UTAT Space Systems, the University of Toronto Aerospace Team, or the University of Toronto;
- a statement that UTAT uses OrbitFabric;
- a conversion of FINCH architecture diagrams into OrbitFabric;
- a replacement for FINCH firmware, system architecture diagrams, data-processing tools, or systems-engineering tools;
- a real mission operations model.

The correct description is:

    FINCH-inspired public demo

or:

    publicly derived conceptual example

Avoid describing it as:

    official FINCH model
    FINCH OrbitFabric model
    UTAT uses OrbitFabric
    conversion of FINCH architecture
    replacement for FINCH firmware / diagrams / data-processing tools

## Why this example exists

OrbitFabric is a model-first mission data fabric for small spacecraft. It is not flight software, not an OBC firmware, not a dynamic simulator and not a ground segment.

This minislice demonstrates a narrow mission-data contract:

    acquisition parameters loaded
    -> OBC schedules imaging and enters ACQUISITION_PREP
    -> ADCS readiness and camera readiness are checked
    -> OBC verifies acquisition conditions
    -> IMAGE_ACQUISITION generates hyperspectral image data
    -> compressed image data is retained onboard
    -> contact capacity prioritizes critical summaries first
    -> compressed image data remains partially pending
    -> events, faults and scenario evidence explain the outcome

The point is not to reproduce FINCH. The point is to test OrbitFabric's contract-layer approach against a recognizable public university CubeSat imaging-payload pattern.

## Directory layout

    examples/finch-inspired-minislice/
    ├── README.md
    ├── mission
    │   ├── spacecraft.yaml
    │   ├── subsystems.yaml
    │   ├── modes.yaml
    │   ├── telemetry.yaml
    │   ├── commands.yaml
    │   ├── events.yaml
    │   ├── faults.yaml
    │   ├── packets.yaml
    │   ├── payloads.yaml
    │   ├── policies.yaml
    │   ├── data_products.yaml
    │   └── contacts.yaml
    └── scenarios
        └── image_acquisition_downlink_constraint.yaml

There is deliberately no `mission/downlink.yaml`.

In OrbitFabric v0.4.0-style examples, downlink flows are modeled inside:

    mission/contacts.yaml

through:

    contacts:
      contact_profiles:
      link_profiles:
      contact_windows:
      downlink_flows:

## Main scenario

The main scenario is:

    scenarios/image_acquisition_downlink_constraint.yaml

Scenario id:

    image_acquisition_downlink_constraint

Conceptual sequence:

1. The spacecraft starts in `NOMINAL`.
2. Acquisition parameters are loaded during a contact-oriented operation.
3. The OBC schedules an image acquisition and enters `ACQUISITION_PREP`.
4. ADCS is marked ready for acquisition pointing.
5. The payload camera is prepared and marked ready.
6. The OBC emits `obc.acquisition_conditions_met`.
7. The spacecraft enters `IMAGE_ACQUISITION` and the hyperspectral image acquisition completes.
8. The spacecraft enters `DATA_COMPRESSION` and creates a downlink-eligible bundle.
9. A constrained contact starts.
10. Critical housekeeping, acquisition summary and evidence products are prioritized.
11. The compressed hyperspectral bundle is only partially downlinked.
12. Remaining compressed image data remains pending onboard.
