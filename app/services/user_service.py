from datetime import date
from typing import Dict, List, Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import settings
from app.models.role import Role, UserRole, UserRoleStatus
from app.models.user import User, UserStatus
from app.services import security


class UserService:
    def list_users(self, db: Session) -> List[User]:
        return db.query(User).from_statement(text("SELECT * FROM prc_get_users()")).all()

    def search_users(self, db: Session, q: Optional[str]) -> List[User]:
        if not q:
            return self.list_users(db)
        return (
            db.query(User)
            .from_statement(text("SELECT * FROM prc_search_users(CAST(:q AS text))"))
            .params(q=q)
            .all()
        )

    def get_user(self, db: Session, user_id: str) -> Optional[User]:
        return (
            db.query(User)
            .from_statement(text("SELECT * FROM prc_get_user(:user_id)"))
            .params(user_id=user_id)
            .first()
        )

    def list_roles(self, db: Session) -> List[Role]:
        return db.query(Role).from_statement(text("SELECT * FROM prc_get_roles()")).all()

    # ----- lookups -----
    def get_by_identifier(self, db: Session, identifier: str) -> Optional[User]:
        return (
            db.query(User)
            .filter((User.username == identifier) | (User.email == identifier))
            .first()
        )

    def get_user_roles(self, user: User) -> List[Dict[str, Optional[str]]]:
        roles: List[Dict[str, Optional[str]]] = []
        for ur in user.user_roles:
            roles.append(
                {
                    "id": str(ur.id),
                    "role_id": str(ur.role_id),
                    "code": ur.role.code if ur.role else None,
                    "name": ur.role.name if ur.role else None,
                    "start_date": ur.start_date.isoformat() if ur.start_date else None,
                    "end_date": ur.end_date.isoformat() if ur.end_date else None,
                    "status": ur.status.value if hasattr(ur.status, "value") else ur.status,
                }
            )
        return roles

    def is_admin(self, user: User) -> bool:
        today = date.today()
        for ur in user.user_roles:
            if not ur.role or ur.role.code != "admin":
                continue
            if ur.status != UserRoleStatus.active:
                continue
            if ur.start_date and ur.start_date > today:
                continue
            if ur.end_date and ur.end_date < today:
                continue
            return True
        return False

    # ----- writes (plain SQLAlchemy) -----
    def create_user(self, db: Session, payload: Dict, role_codes: Optional[List[str]] = None) -> User:
        salt = security.generate_salt()
        user = User(
            id_number=payload["id_number"],
            username=payload["username"],
            email=payload["email"],
            first_name=payload.get("first_name"),
            last_name=payload.get("last_name"),
            phone=payload.get("phone"),
            department=payload.get("department"),
            salt=salt,
            password=security.hash_password(settings.generic_password, salt),
            status=UserStatus.active,
            must_change_password=True,
        )
        db.add(user)
        db.flush()  # assign user.id before linking roles

        codes = role_codes or ["user"]
        for code in codes:
            role = db.query(Role).filter(Role.code == code).first()
            if role:
                db.add(UserRole(user_id=user.id, role_id=role.id, status=UserRoleStatus.active))

        db.commit()
        db.refresh(user)
        return user

    def update_user(self, db: Session, user_id: str, patch: Dict) -> Optional[User]:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        for field in ("id_number", "username", "email", "first_name", "last_name", "phone", "department"):
            if patch.get(field) is not None:
                setattr(user, field, patch[field])
        if patch.get("status") is not None:
            user.status = UserStatus(patch["status"])
        db.commit()
        db.refresh(user)
        return user

    def soft_delete_user(self, db: Session, user_id: str) -> Optional[User]:
        """No real deletion: flip the user to inactive status."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        user.status = UserStatus.inactive
        db.commit()
        db.refresh(user)
        return user

    def assign_role(
        self,
        db: Session,
        user_id: str,
        role_code: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Optional[UserRole]:
        user = db.query(User).filter(User.id == user_id).first()
        role = db.query(Role).filter(Role.code == role_code).first()
        if not user or not role:
            return None
        link = UserRole(
            user_id=user.id,
            role_id=role.id,
            status=UserRoleStatus.active,
        )
        if start_date is not None:
            link.start_date = start_date
        link.end_date = end_date
        db.add(link)
        db.commit()
        db.refresh(link)
        return link

    # ----- auth -----
    def authenticate(self, db: Session, identifier: str, password: str) -> Optional[User]:
        user = self.get_by_identifier(db, identifier)
        if not user or user.status != UserStatus.active:
            return None
        if not security.verify_password(password, user.salt, user.password):
            return None
        return user

    def change_password(self, db: Session, user: User, old_password: str, new_password: str) -> bool:
        if not security.verify_password(old_password, user.salt, user.password):
            return False
        salt = security.generate_salt()
        user.salt = salt
        user.password = security.hash_password(new_password, salt)
        user.must_change_password = False
        db.commit()
        db.refresh(user)
        return True


user_service = UserService()
