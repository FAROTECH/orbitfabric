from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from .errors import InventoryError
from .models import InstalledAdapterRecord

INVENTORY_KIND = "orbitfabric.adapter_inventory"
INVENTORY_VERSION = "0.1-internal"


class InstalledAdapterInventory:
    """Core-owned user-scoped actual installed adapter state."""

    def __init__(self, state_root: Path) -> None:
        self.state_root = state_root
        self.path = state_root / "inventory.json"

    def list(self) -> list[InstalledAdapterRecord]:
        payload = self._load_payload()
        records: list[InstalledAdapterRecord] = []
        try:
            for item in payload["instances"]:
                records.append(InstalledAdapterRecord.model_validate(item))
        except (KeyError, TypeError, ValidationError) as exc:
            raise InventoryError(f"Installed Adapter Inventory is invalid: {exc}") from exc
        return sorted(records, key=lambda record: record.instance_id)

    def get(self, instance_id: str) -> InstalledAdapterRecord:
        for record in self.list():
            if record.instance_id == instance_id:
                return record
        raise InventoryError(f"Installed adapter instance not found: {instance_id}")

    def add(self, record: InstalledAdapterRecord) -> None:
        records = self.list()
        if any(item.instance_id == record.instance_id for item in records):
            raise InventoryError(f"Installed adapter instance already exists: {record.instance_id}")
        records.append(record)
        self._write_records(records)

    def remove(self, instance_id: str) -> InstalledAdapterRecord:
        records = self.list()
        removed: InstalledAdapterRecord | None = None
        retained: list[InstalledAdapterRecord] = []
        for record in records:
            if record.instance_id == instance_id:
                removed = record
            else:
                retained.append(record)
        if removed is None:
            raise InventoryError(f"Installed adapter instance not found: {instance_id}")
        self._write_records(retained)
        return removed

    def _load_payload(self) -> dict[str, Any]:
        if not self.path.exists():
            return {
                "kind": INVENTORY_KIND,
                "inventory_version": INVENTORY_VERSION,
                "instances": [],
            }
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise InventoryError(f"Cannot read Installed Adapter Inventory: {exc}") from exc
        if not isinstance(payload, dict):
            raise InventoryError("Installed Adapter Inventory must be a JSON object")
        if payload.get("kind") != INVENTORY_KIND:
            raise InventoryError("Installed Adapter Inventory kind is invalid")
        if payload.get("inventory_version") != INVENTORY_VERSION:
            raise InventoryError("Installed Adapter Inventory version is unsupported")
        return payload

    def _write_records(self, records: list[InstalledAdapterRecord]) -> None:
        self.state_root.mkdir(parents=True, exist_ok=True)
        payload = {
            "kind": INVENTORY_KIND,
            "inventory_version": INVENTORY_VERSION,
            "instances": [record.model_dump(mode="json") for record in records],
        }
        encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        temporary = self.path.with_suffix(".json.tmp")
        try:
            temporary.write_text(encoded, encoding="utf-8")
            os.replace(temporary, self.path)
        except OSError as exc:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass
            raise InventoryError(f"Cannot update Installed Adapter Inventory: {exc}") from exc
