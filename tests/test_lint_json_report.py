from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from orbitfabric.cli import app
from orbitfabric.lint.engine import LintEngine
from orbitfabric.lint.json_report import lint_report_to_dict
from orbitfabric.model.loader import MissionModelLoader

DEMO_MISSION = Path("examples/demo-3u/mission")
runner = CliRunner()


def test_lint_report_to_dict_for_clean_demo_mission() -> None:
    model = MissionModelLoader().load(DEMO_MISSION)
    report = LintEngine().run(model)

    payload = lint_report_to_dict(model, report)

    assert payload["tool"] == "orbitfabric-lint"
    assert payload["version"] == "0.1.0"
    assert payload["mission"] == "demo-3u"
    assert payload["model_version"] == "0.1.0"
    assert payload["result"] == "passed"
    assert payload["summary"] == {"errors": 0, "warnings": 0, "info": 0}
    assert payload["findings"] == []
    assert payload["loaded"]["subsystems"] == 4
    assert payload["loaded"]["telemetry"] == 5


def test_lint_command_writes_json_report(tmp_path: Path) -> None:
    output_path = tmp_path / "lint_report.json"

    result = runner.invoke(
        app,
        [
            "lint",
            "examples/demo-3u/mission",
            "--json",
            str(output_path),
        ],
    )

    assert result.exit_code == 0
    assert output_path.exists()
    assert "JSON report written to" in result.output

    payload = json.loads(output_path.read_text(encoding="utf-8"))

    assert payload["tool"] == "orbitfabric-lint"
    assert payload["mission"] == "demo-3u"
    assert payload["result"] == "passed"
    assert payload["summary"]["errors"] == 0