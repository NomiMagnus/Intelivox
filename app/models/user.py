import uuid
import enum
from typing import Any, Dict
from sqlalchemy import Column, String, Boolean, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base


class UserStatus(enum.Enum):
    active = "active"
    inactive = "inactive"


class User(Base):
    __tablename__ = "tbl_user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    id_number = Column(String(32), unique=True, nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(254), unique=True, nullable=False)
    phone = Column(String(32), nullable=True)
    password = Column(String(256), nullable=False)
    salt = Column(String(64), nullable=False)
    department = Column(String(128), nullable=True)
    status = Column(Enum(UserStatus, name="user_status"), nullable=False, default=UserStatus.active)
    must_change_password = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user_roles = relationship("UserRole", back_populates="user", lazy="selectin")

    def to_dict(self) -> Dict[str, Any]:
        # NOTE: password and salt are intentionally never exposed.
        return {
            "id": str(self.id),
            "id_number": self.id_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "department": self.department,
            "status": self.status.value if isinstance(self.status, enum.Enum) else self.status,
            "must_change_password": self.must_change_password,
            "created_at": self.created_at.isoformat() if self.created_at is not None else None,
        }
