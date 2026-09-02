from __future__ import annotations

from pathlib import Path
from typing import Protocol

from ..models import (
    BackendInstallReceipt,
    InstalledAdapterRecord,
    ResolvedAdapterRelease,
    VerificationDimension,
)


class InstallationBackend(Protocol):
    backend_id: str

    def supports(self, release: ResolvedAdapterRelease) -> bool: ...

    def install(
        self,
        release: ResolvedAdapterRelease,
        instance_id: str,
        instances_root: Path,
    ) -> BackendInstallReceipt: ...

    def verify(self, record: InstalledAdapterRecord) -> VerificationDimension: ...

    def remove(self, record: InstalledAdapterRecord) -> None: ...
