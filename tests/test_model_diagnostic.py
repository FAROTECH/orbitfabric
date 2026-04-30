from __future__ import annotations

from orbitfabric.model.errors import ModelDiagnostic


def test_model_diagnostic_format_includes_suggestion() -> None:
    diagnostic = ModelDiagnostic(
        severity="ERROR",
        code="OF-SCN-001",
        file="scenario.yaml",
        domain="scenario",
        object_id="battery_low_during_payload",
        message="scenario command references unknown command 'payload.unknown_command'",
        suggestion="Use a command defined in commands.yaml.",
    )

    assert diagnostic.format() == (
        "ERROR OF-SCN-001 scenario.yaml battery_low_during_payload "
        "scenario command references unknown command 'payload.unknown_command' "
        "Suggestion: Use a command defined in commands.yaml."
    )