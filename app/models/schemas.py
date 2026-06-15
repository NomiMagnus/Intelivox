from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class ResidentType(str, Enum):
    individual = "individual"
    organization = "organization"
    institution = "institution"

class ResidentStatus(str, Enum):
    new = "new"
    active = "active"
    pending = "pending"
    inactive = "inactive"

class ResidentCreatePayload(BaseModel):
    type: ResidentType = Field(default=ResidentType.individual)
    status: ResidentStatus = Field(default=ResidentStatus.new)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    organization_name: Optional[str] = None
    mobile_phone: Optional[str] = None
    home_phone: Optional[str] = None
    work_phone: Optional[str] = None
    email: Optional[str] = None

class ResidentUpdatePayload(BaseModel):
    type: Optional[ResidentType] = None
    status: Optional[ResidentStatus] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    organization_name: Optional[str] = None
    mobile_phone: Optional[str] = None
    home_phone: Optional[str] = None
    work_phone: Optional[str] = None
    email: Optional[str] = None

class ResidentRead(BaseModel):
    id: str
    type: ResidentType
    status: ResidentStatus
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    organization_name: Optional[str] = None
    mobile_phone: Optional[str] = None
    home_phone: Optional[str] = None
    work_phone: Optional[str] = None
    email: Optional[str] = None
    created_at: str
