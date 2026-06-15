from typing import Optional
from pydantic import BaseModel, EmailStr, root_validator, constr
from enum import Enum


class ResidentType(str, Enum):
    individual = "individual"
    organization = "organization"
    institution = "institution"


class ResidentStatus(str, Enum):
    new = "new"
    active = "active"
    pending = "pending"
    inactive = "inactive"


PhoneStr = constr(min_length=7, max_length=32, regex=r'^[+0-9()\-\s]{7,32}$')


class ResidentCreate(BaseModel):
    type: ResidentType = ResidentType.individual
    status: ResidentStatus = ResidentStatus.new
    first_name: Optional[constr(max_length=128)] = None
    last_name: Optional[constr(max_length=128)] = None
    organization_name: Optional[constr(max_length=256)] = None
    mobile_phone: Optional[PhoneStr] = None
    home_phone: Optional[PhoneStr] = None
    work_phone: Optional[PhoneStr] = None
    email: Optional[EmailStr] = None

    class Config:
        extra = 'forbid'

    @root_validator
    def check_names_or_organization(cls, values):
        t = values.get('type')
        fn = values.get('first_name')
        ln = values.get('last_name')
        org = values.get('organization_name')
        if t == ResidentType.individual:
            if not fn or not ln:
                raise ValueError('first_name and last_name are required for individual residents')
        else:
            if not org:
                raise ValueError('organization_name is required for organization or institution residents')
        return values


class ResidentUpdate(BaseModel):
    type: Optional[ResidentType] = None
    status: Optional[ResidentStatus] = None
    first_name: Optional[constr(max_length=128)] = None
    last_name: Optional[constr(max_length=128)] = None
    organization_name: Optional[constr(max_length=256)] = None
    mobile_phone: Optional[PhoneStr] = None
    home_phone: Optional[PhoneStr] = None
    work_phone: Optional[PhoneStr] = None
    email: Optional[EmailStr] = None

    class Config:
        extra = 'forbid'


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
    email: Optional[EmailStr] = None
    created_at: str

    class Config:
        orm_mode = True
