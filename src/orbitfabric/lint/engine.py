from __future__ import annotations

from orbitfabric.lint.finding import LintReport
from orbitfabric.lint.rules_commands import check_commands
from orbitfabric.lint.rules_contacts import check_contacts
from orbitfabric.lint.rules_data_products import check_data_products
from orbitfabric.lint.rules_events import check_events
from orbitfabric.lint.rules_faults import check_faults
from orbitfabric.lint.rules_modes import check_modes
from orbitfabric.lint.rules_packets import check_packets
from orbitfabric.lint.rules_payloads import check_payloads
from orbitfabric.lint.rules_references import check_references
from orbitfabric.lint.rules_telemetry import check_telemetry
from orbitfabric.model.mission import MissionModel


class LintEngine:
    """Runs semantic lint rules against a validated Mission Model."""

    def run(self, model: MissionModel) -> LintReport:
        findings = []
        findings.extend(check_references(model))
        findings.extend(check_modes(model))
        findings.extend(check_payloads(model))
        findings.extend(check_data_products(model))
        findings.extend(check_contacts(model))
        findings.extend(check_telemetry(model))
        findings.extend(check_commands(model))
        findings.extend(check_events(model))
        findings.extend(check_faults(model))
        findings.extend(check_packets(model))

        return LintReport(
            mission_id=model.spacecraft.id,
            model_version=model.spacecraft.model_version,
            findings=findings,
        )