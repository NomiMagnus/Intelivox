from fastapi import APIRouter, HTTPException
from typing import List

from app.models.schemas import (
    ResidentCreatePayload,
    ResidentRead,
    ResidentStatus,
    ResidentUpdatePayload,
)
from app.services.resident_service import resident_service

router = APIRouter(prefix="/api")

@router.post("/residents", response_model=ResidentRead)
def create_resident(payload: ResidentCreatePayload):
    resident = resident_service.create_resident(payload.dict(exclude_none=True))
    return ResidentRead(**resident.to_dict())

@router.get("/residents", response_model=List[ResidentRead])
def list_residents():
    residents = resident_service.list_residents()
    return [ResidentRead(**resident.to_dict()) for resident in residents]

@router.get("/residents/{resident_id}", response_model=ResidentRead)
def get_resident(resident_id: str):
    resident = resident_service.get_resident(resident_id)
    if not resident:
        raise HTTPException(status_code=404, detail="Resident not found")
    return ResidentRead(**resident.to_dict())

@router.patch("/residents/{resident_id}", response_model=ResidentRead)
def patch_resident(resident_id: str, update: ResidentUpdatePayload):
    resident = resident_service.update_resident(resident_id, update.dict(exclude_unset=True))
    if not resident:
        raise HTTPException(status_code=404, detail="Resident not found")
    return ResidentRead(**resident.to_dict())
