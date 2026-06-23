from enum import Enum
from typing import List, Optional
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


# ---------------------------------------------------------------------------
# Users, roles & auth
# ---------------------------------------------------------------------------

class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"


class RoleRead(BaseModel):
    id: str
    code: str
    name: Optional[str] = None
    status: str


class UserRoleRead(BaseModel):
    id: str
    role_id: str
    code: Optional[str] = None
    name: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: str


class UserCreatePayload(BaseModel):
    id_number: str
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    # Optional list of role codes to assign on creation (defaults to ["user"]).
    role_codes: Optional[List[str]] = None


class UserUpdatePayload(BaseModel):
    id_number: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    status: Optional[UserStatus] = None


class UserRead(BaseModel):
    id: str
    id_number: str
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    status: str
    must_change_password: bool
    created_at: str
    roles: List[UserRoleRead] = Field(default_factory=list)


class LoginPayload(BaseModel):
    username_or_email: str
    password: str


class ChangePasswordPayload(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8)


class MeResponse(BaseModel):
    user: UserRead
    is_admin: bool


class RoleAssignPayload(BaseModel):
    role_code: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
