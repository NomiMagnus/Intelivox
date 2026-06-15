import uuid
from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db import Base
import enum


class ResidentType(enum.Enum):
    individual = "individual"
    organization = "organization"
    institution = "institution"


class ResidentStatus(enum.Enum):
    new = "new"
    active = "active"
    pending = "pending"
    inactive = "inactive"


class Resident(Base):
    __tablename__ = "resident"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    type = Column(Enum(ResidentType, name="resident_type"), nullable=False, default=ResidentType.individual)
    status = Column(Enum(ResidentStatus, name="resident_status"), nullable=False, default=ResidentStatus.new)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    organization_name = Column(String(256), nullable=True)
    mobile_phone = Column(String(32), nullable=True)
    home_phone = Column(String(32), nullable=True)
    work_phone = Column(String(32), nullable=True)
    email = Column(String(254), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
