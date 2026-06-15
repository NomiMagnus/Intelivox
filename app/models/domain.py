from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from uuid import uuid4

class ResidentType(str, Enum):
    INDIVIDUAL = "individual"
    ORGANIZATION = "organization"
    INSTITUTION = "institution"

class ResidentStatus(str, Enum):
    NEW = "new"
    ACTIVE = "active"
    PENDING = "pending"
    INACTIVE = "inactive"

class Resident:
    def __init__(
        self,
        resident_type: ResidentType = ResidentType.INDIVIDUAL,
        status: ResidentStatus = ResidentStatus.NEW,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        organization_name: Optional[str] = None,
        mobile_phone: Optional[str] = None,
        home_phone: Optional[str] = None,
        work_phone: Optional[str] = None,
        email: Optional[str] = None,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id or str(uuid4())
        self.type = resident_type
        self.status = status
        self.first_name = first_name
        self.last_name = last_name
        self.organization_name = organization_name
        self.mobile_phone = mobile_phone
        self.home_phone = home_phone
        self.work_phone = work_phone
        self.email = email
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "status": self.status.value,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "organization_name": self.organization_name,
            "mobile_phone": self.mobile_phone,
            "home_phone": self.home_phone,
            "work_phone": self.work_phone,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Resident":
        return cls(
            id=data.get("id"),
            resident_type=ResidentType(data.get("type", ResidentType.INDIVIDUAL.value)),
            status=ResidentStatus(data.get("status", ResidentStatus.NEW.value)),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            organization_name=data.get("organization_name"),
            mobile_phone=data.get("mobile_phone"),
            home_phone=data.get("home_phone"),
            work_phone=data.get("work_phone"),
            email=data.get("email"),
            created_at=datetime.fromisoformat(data.get("created_at")) if data.get("created_at") else None,
        )
