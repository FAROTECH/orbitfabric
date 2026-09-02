from __future__ import annotations


class AdapterManagerError(RuntimeError):
    """Raised when an Adapter Manager lifecycle operation cannot complete."""


class ReleaseResolutionError(AdapterManagerError):
    """Raised when an exact adapter release cannot be resolved or verified."""


class AcceptanceError(AdapterManagerError):
    """Raised when release evidence does not satisfy the selected policy."""


class InstallationError(AdapterManagerError):
    """Raised when an installation backend cannot materialize a release."""


class InventoryError(AdapterManagerError):
    """Raised when installed inventory state is invalid or cannot be updated."""


class VerificationError(AdapterManagerError):
    """Raised when an installed adapter cannot be verified sufficiently."""


class ExecutionError(AdapterManagerError):
    """Raised when an installed adapter cannot be executed through the generic protocol."""


class ProjectLockError(AdapterManagerError):
    """Raised when an Adapter Project Lock cannot be loaded or evaluated."""
