import uuid
import enum
from typing import Any, Dict
from sqlalchemy import Column, String, Enum, DateTime, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base


class RoleStatus(enum.Enum):
    active = "active"
    inactive = "inactive"


class UserRoleStatus(enum.Enum):
    active = "active"
    inactive = "inactive"


class Role(Base):
    __tablename__ = "tbl_role"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    code = Column(String(32), unique=True, nullable=False)
    name = Column(String(128), nullable=True)
    status = Column(Enum(RoleStatus, name="role_status"), nullable=False, default=RoleStatus.active)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "code": self.code,
            "name": self.name,
            "status": self.status.value if isinstance(self.status, enum.Enum) else self.status,
            "created_at": self.created_at.isoformat() if self.created_at is not None else None,
        }


class UserRole(Base):
    __tablename__ = "tbl_user_role"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("tbl_user.id"), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("tbl_role.id"), nullable=False)
    start_date = Column(Date, nullable=False, server_default=func.current_date())
    end_date = Column(Date, nullable=True)
    status = Column(Enum(UserRoleStatus, name="user_role_status"), nullable=False, default=UserRoleStatus.active)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="user_roles")
    role = relationship("Role", lazy="selectin")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "role_id": str(self.role_id),
            "start_date": self.start_date.isoformat() if self.start_date is not None else None,
            "end_date": self.end_date.isoformat() if self.end_date is not None else None,
            "status": self.status.value if isinstance(self.status, enum.Enum) else self.status,
            "created_at": self.created_at.isoformat() if self.created_at is not None else None,
        }
