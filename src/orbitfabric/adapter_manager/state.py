from __future__ import annotations

import os
import sys
from pathlib import Path

STATE_DIR_ENV = "ORBITFABRIC_STATE_DIR"


def default_state_root(override: str | Path | None = None) -> Path:
    if override is not None:
        return Path(override).expanduser().resolve()

    env_value = os.environ.get(STATE_DIR_ENV)
    if env_value:
        return Path(env_value).expanduser().resolve()

    home = Path.home()
    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA")
        if base:
            return Path(base).expanduser().resolve() / "OrbitFabric"
        return home / "AppData" / "Local" / "OrbitFabric"

    if sys.platform == "darwin":
        return home / "Library" / "Application Support" / "OrbitFabric"

    xdg_state_home = os.environ.get("XDG_STATE_HOME")
    if xdg_state_home:
        return Path(xdg_state_home).expanduser().resolve() / "orbitfabric"
    return home / ".local" / "state" / "orbitfabric"
