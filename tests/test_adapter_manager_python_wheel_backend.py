from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

import pytest

from orbitfabric.adapter_manager import AdapterManager
from orbitfabric.adapter_manager.backends.python_wheel import PythonWheelManagedEnvironmentBackend
from orbitfabric.adapter_manager.errors import InstallationError
from orbitfabric.adapter_manager.hashing import sha256_file

ROOT = Path(__file__).resolve().parents[1]
VALID = ROOT / "conformance" / "fixtures" / "integration-v1" / "valid"
MANIFEST_ZERO = VALID / "manifest-zero-input.json"
RESULT_ZERO = VALID / "result-zero-input.json"


def _record_bytes(paths: list[str], record_path: str) -> bytes:
    rows = [[path, "", ""] for path in paths]
    rows.append([record_path, "", ""])
    output: list[str] = []
    for row in rows:
        output.append(",".join(row))
    return ("\n".join(output) + "\n").encode()


def _build_namespaced_wheel(tmp_path: Path) -> Path:
    distribution_stem = "namespaced_dummy_adapter"
    version = "1.0.0"
    dist_info = f"{distribution_stem}-{version}.dist-info"
    wheel = tmp_path / f"{distribution_stem}-{version}-py3-none-any.whl"
    result_payload = json.loads(RESULT_ZERO.read_text(encoding="utf-8"))

    cli_source = (
        "import json\n"
        "import sys\n"
        "from pathlib import Path\n\n"
        f"RESULT = {result_payload!r}\n\n"
        "def main():\n"
        "    args = sys.argv[1:]\n"
        "    if not args or args[0] != 'run':\n"
        "        return\n"
        "    output = Path(args[args.index('--output-dir') + 1])\n"
        "    output.mkdir(parents=True, exist_ok=True)\n"
        "    (output / 'integration_result.json').write_text(\n"
        "        json.dumps(RESULT, indent=2) + '\\n', encoding='utf-8'\n"
        "    )\n"
    ).encode()

    files = {
        f"{distribution_stem}/__init__.py": b"",
        f"{distribution_stem}/cli.py": cli_source,
        f"{distribution_stem}/integration_package.json": MANIFEST_ZERO.read_bytes(),
        f"{dist_info}/METADATA": (
            "Metadata-Version: 2.1\n"
            "Name: namespaced-dummy-adapter\n"
            f"Version: {version}\n"
            "\n"
        ).encode(),
        f"{dist_info}/WHEEL": (
            "Wheel-Version: 1.0\n"
            "Generator: orbitfabric-test\n"
            "Root-Is-Purelib: true\n"
            "Tag: py3-none-any\n"
            "\n"
        ).encode(),
        f"{dist_info}/entry_points.txt": (
            "[console_scripts]\n"
            "fixture-adapter = namespaced_dummy_adapter.cli:main\n"
        ).encode(),
    }
    record_path = f"{dist_info}/RECORD"
    files[record_path] = _record_bytes(list(files), record_path)

    with zipfile.ZipFile(wheel, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path, payload in files.items():
            archive.writestr(path, payload)
    return wheel


def _write_release(tmp_path: Path, wheel: Path) -> Path:
    descriptor = {
        "kind": "orbitfabric.adapter_release",
        "descriptor_version": "0.1-candidate",
        "source_coordinate": {
            "authority": "test.local",
            "publisher": "fixture",
            "name": "namespaced-wheel",
        },
        "release_version": "1.0.0",
        "source_provenance": {"commit": "fixture"},
        "artifacts": [
            {
                "id": "python-wheel",
                "artifact_type": "python-wheel",
                "filename": wheel.name,
                "sha256": sha256_file(wheel),
                "size": wheel.stat().st_size,
                "selectors": {"python": ">=3.11"},
            }
        ],
        "integration_package": {"sha256": sha256_file(MANIFEST_ZERO)},
    }
    descriptor_path = tmp_path / "adapter-release.json"
    descriptor_path.write_text(json.dumps(descriptor, indent=2) + "\n", encoding="utf-8")
    return descriptor_path


def test_python_backend_discovers_namespaced_manifest_from_distribution(tmp_path: Path) -> None:
    wheel = _build_namespaced_wheel(tmp_path)
    descriptor = _write_release(tmp_path, wheel)
    manager = AdapterManager(state_root=tmp_path / "state")

    record = manager.install(descriptor, wheel)

    manifest_path = Path(record.manifest_path)
    assert manifest_path.name == "integration_package.json"
    assert manifest_path.parent.name == "namespaced_dummy_adapter"
    assert manager.verify(record.instance_id).passed

    input_manifest = tmp_path / "input-set.json"
    profile = tmp_path / "profile.json"
    input_manifest.write_text("{}\n", encoding="utf-8")
    profile.write_text("{}\n", encoding="utf-8")
    execution = manager.execute(
        record.instance_id,
        operation="project",
        input_set_manifest=input_manifest,
        profile=profile,
        output_dir=tmp_path / "output",
    )
    assert execution.returncode == 0
    assert execution.result["result"] == "succeeded"

    manager.remove(record.instance_id)
    assert manager.list() == []


@pytest.mark.parametrize("stdout", ["", "/tmp/one/integration_package.json\n/tmp/two/integration_package.json\n"])
def test_python_backend_rejects_non_unique_distribution_manifest(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    stdout: str,
) -> None:
    backend = PythonWheelManagedEnvironmentBackend()

    def fake_run(argv: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(argv, 0, stdout=stdout, stderr="")

    monkeypatch.setattr(backend, "_run", fake_run)

    with pytest.raises(InstallationError, match="must contain exactly one integration_package.json"):
        backend._installed_manifest_path(
            tmp_path / "python",
            tmp_path,
            "namespaced-dummy-adapter",
        )


def test_wheel_distribution_name_comes_from_metadata(tmp_path: Path) -> None:
    wheel = _build_namespaced_wheel(tmp_path)
    backend = PythonWheelManagedEnvironmentBackend()

    assert backend._wheel_distribution_name(wheel) == "namespaced-dummy-adapter"
