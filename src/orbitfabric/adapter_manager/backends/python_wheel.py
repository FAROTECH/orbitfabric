from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import venv

from orbitfabric.conformance.integration_contracts import ContractError, validate_manifest

from ..errors import InstallationError
from ..hashing import sha256_file
from ..models import (
    BackendInstallReceipt,
    InstalledAdapterRecord,
    ResolvedAdapterRelease,
    VerificationDimension,
)


class PythonWheelManagedEnvironmentBackend:
    backend_id = "python-wheel-managed-env"
    artifact_type = "python-wheel"

    def supports(self, release: ResolvedAdapterRelease) -> bool:
        return release.artifact.artifact_type == self.artifact_type

    def install(
        self,
        release: ResolvedAdapterRelease,
        instance_id: str,
        instances_root: Path,
    ) -> BackendInstallReceipt:
        if not self.supports(release):
            raise InstallationError(
                f"Backend {self.backend_id} does not support artifact type "
                f"{release.artifact.artifact_type!r}"
            )

        instance_root = instances_root / instance_id
        if instance_root.exists():
            raise InstallationError(f"Adapter instance root already exists: {instance_root}")

        venv_dir = instance_root / "venv"
        try:
            instance_root.mkdir(parents=True)
            venv.EnvBuilder(with_pip=True).create(venv_dir)
            python = self._python_path(venv_dir)
            self._run(
                [
                    str(python),
                    "-m",
                    "pip",
                    "install",
                    "--disable-pip-version-check",
                    str(release.artifact_path),
                ],
                cwd=instance_root,
            )

            manifest_path = self._installed_manifest_path(python, instance_root)
            manifest_digest = sha256_file(manifest_path)
            expected_manifest_digest = release.descriptor.integration_package.sha256
            if manifest_digest != expected_manifest_digest:
                raise InstallationError(
                    "Installed Integration Package Manifest SHA-256 does not match "
                    "the Adapter Release Descriptor"
                )

            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                validate_manifest(manifest)
            except (OSError, json.JSONDecodeError, ContractError) as exc:
                raise InstallationError(
                    f"Installed Integration Package Manifest is not conformant: {exc}"
                ) from exc

            declared_prefix = manifest["execution"]["argv_prefix"]
            execution_prefix = self._resolve_execution_prefix(venv_dir, declared_prefix)
            return BackendInstallReceipt(
                backend_id=self.backend_id,
                install_root=instance_root,
                manifest_path=manifest_path,
                manifest_sha256=manifest_digest,
                execution_argv_prefix=execution_prefix,
            )
        except Exception:
            shutil.rmtree(instance_root, ignore_errors=True)
            raise

    def verify(self, record: InstalledAdapterRecord) -> VerificationDimension:
        install_root = Path(record.install_root)
        if not install_root.is_dir():
            return VerificationDimension(
                status="FAIL",
                detail=f"Installation root is missing: {install_root}",
            )
        venv_dir = install_root / "venv"
        python = self._python_path(venv_dir)
        if not python.is_file():
            return VerificationDimension(
                status="FAIL",
                detail=f"Managed Python executable is missing: {python}",
            )
        return VerificationDimension(status="PASS")

    def remove(self, record: InstalledAdapterRecord) -> None:
        install_root = Path(record.install_root)
        try:
            shutil.rmtree(install_root)
        except FileNotFoundError:
            return
        except OSError as exc:
            raise InstallationError(
                f"Cannot remove adapter installation root {install_root}: {exc}"
            ) from exc

    @staticmethod
    def _python_path(venv_dir: Path) -> Path:
        if sys.platform == "win32":
            return venv_dir / "Scripts" / "python.exe"
        return venv_dir / "bin" / "python"

    def _installed_manifest_path(self, python: Path, cwd: Path) -> Path:
        script = (
            "from importlib.resources import files; "
            "print(files('integration_package').joinpath('integration_package.json'))"
        )
        completed = self._run([str(python), "-I", "-c", script], cwd=cwd)
        manifest_path = Path(completed.stdout.strip()).resolve()
        if not manifest_path.is_file():
            raise InstallationError(
                f"Installed adapter does not expose integration_package.json: {manifest_path}"
            )
        return manifest_path

    @staticmethod
    def _resolve_execution_prefix(venv_dir: Path, declared_prefix: list[str]) -> list[str]:
        command = declared_prefix[0]
        if Path(command).name != command:
            raise InstallationError(
                "Python wheel backend requires a bare console-script name in execution.argv_prefix"
            )

        scripts_dir = venv_dir / ("Scripts" if sys.platform == "win32" else "bin")
        candidates = [scripts_dir / command]
        if sys.platform == "win32":
            candidates.extend(
                [
                    scripts_dir / f"{command}.exe",
                    scripts_dir / f"{command}.cmd",
                ]
            )
        executable = next((path for path in candidates if path.is_file()), None)
        if executable is None:
            raise InstallationError(
                f"Installed adapter console endpoint cannot be resolved: {command}"
            )
        return [str(executable.resolve()), *declared_prefix[1:]]

    @staticmethod
    def _run(argv: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment.pop("PYTHONPATH", None)
        environment.pop("PYTHONHOME", None)
        try:
            return subprocess.run(
                argv,
                cwd=cwd,
                env=environment,
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as exc:
            detail = (exc.stderr or exc.stdout or "").strip()
            if len(detail) > 2000:
                detail = detail[-2000:]
            raise InstallationError(
                f"Python wheel backend command failed ({exc.returncode}): "
                f"{' '.join(argv)}"
                + (f"\n{detail}" if detail else "")
            ) from exc
