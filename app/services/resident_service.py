from typing import Dict, List, Optional

from app.models.domain import Resident, ResidentStatus, ResidentType
from app.services.storage_service import storage_service

class ResidentService:
    def create_resident(self, payload: Dict[str, Optional[str]]) -> Resident:
        resident = Resident(
            resident_type=ResidentType(payload.get("type", ResidentType.INDIVIDUAL.value)),
            status=ResidentStatus(payload.get("status", ResidentStatus.NEW.value)),
            first_name=payload.get("first_name"),
            last_name=payload.get("last_name"),
            organization_name=payload.get("organization_name"),
            mobile_phone=payload.get("mobile_phone"),
            home_phone=payload.get("home_phone"),
            work_phone=payload.get("work_phone"),
            email=payload.get("email"),
        )
        return storage_service.save_resident(resident)

    def list_residents(self) -> List[Resident]:
        return storage_service.list_residents()

    def get_resident(self, resident_id: str) -> Optional[Resident]:
        return storage_service.get_resident(resident_id)

    def update_resident(self, resident_id: str, patch_data: Dict[str, Optional[str]]) -> Optional[Resident]:
        current = self.get_resident(resident_id)
        if not current:
            return None

        if patch_data.get("type") is not None:
            current.type = ResidentType(patch_data["type"])
        if patch_data.get("status") is not None:
            current.status = ResidentStatus(patch_data["status"])
        if patch_data.get("first_name") is not None:
            current.first_name = patch_data["first_name"]
        if patch_data.get("last_name") is not None:
            current.last_name = patch_data["last_name"]
        if patch_data.get("organization_name") is not None:
            current.organization_name = patch_data["organization_name"]
        if patch_data.get("mobile_phone") is not None:
            current.mobile_phone = patch_data["mobile_phone"]
        if patch_data.get("home_phone") is not None:
            current.home_phone = patch_data["home_phone"]
        if patch_data.get("work_phone") is not None:
            current.work_phone = patch_data["work_phone"]
        if patch_data.get("email") is not None:
            current.email = patch_data["email"]

        return storage_service.update_resident(resident_id, current.to_dict())

resident_service = ResidentService()
