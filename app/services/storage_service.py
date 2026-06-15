import json
from pathlib import Path
from threading import Lock
from typing import Any, Dict, List, Optional

from app.config import settings
from app.models.domain import Resident

_lock = Lock()

class JsonStorageService:
    def __init__(self, residents_file: Path):
        self.residents_file = residents_file

    def _load_all(self) -> List[Dict[str, Any]]:
        with _lock:
            with self.residents_file.open("r", encoding="utf-8") as handle:
                try:
                    data = json.load(handle)
                except json.JSONDecodeError:
                    data = []
                return data

    def _write_all(self, data: List[Dict[str, Any]]) -> None:
        with _lock:
            with self.residents_file.open("w", encoding="utf-8") as handle:
                json.dump(data, handle, indent=2, ensure_ascii=False)

    def list_residents(self) -> List[Resident]:
        return [Resident.from_dict(item) for item in self._load_all()]

    def get_resident(self, resident_id: str) -> Optional[Resident]:
        for item in self._load_all():
            if item.get("id") == resident_id:
                return Resident.from_dict(item)
        return None

    def save_resident(self, resident: Resident) -> Resident:
        data = self._load_all()
        existing_index = next((index for index, item in enumerate(data) if item.get("id") == resident.id), None)
        if existing_index is not None:
            data[existing_index] = resident.to_dict()
        else:
            data.append(resident.to_dict())
        self._write_all(data)
        return resident

    def update_resident(self, resident_id: str, patch: Dict[str, Any]) -> Optional[Resident]:
        data = self._load_all()
        for index, item in enumerate(data):
            if item.get("id") == resident_id:
                item.update(patch)
                data[index] = item
                self._write_all(data)
                return Resident.from_dict(item)
        return None

storage_service = JsonStorageService(settings.residents_file)
