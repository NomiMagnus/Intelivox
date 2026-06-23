from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Response
from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db
from app.api.deps import get_current_user, require_admin
from app.models.user import User
from app.models.schemas import (
    ResidentCreatePayload,
    ResidentRead,
    ResidentUpdatePayload,
    UserCreatePayload,
    UserUpdatePayload,
    UserRead,
    RoleRead,
    LoginPayload,
    ChangePasswordPayload,
    MeResponse,
    RoleAssignPayload,
)
from app.services import security
from app.services.resident_service import resident_service
from app.services.user_service import user_service

router = APIRouter(prefix="/api")

@router.post("/residents", response_model=ResidentRead)
def create_resident(payload: ResidentCreatePayload, db: Session = Depends(get_db)):
    resident = resident_service.create_resident(db, payload.dict(exclude_none=True))
    return ResidentRead(**resident.to_dict())

@router.get("/residents", response_model=List[ResidentRead])
def list_residents(q: Optional[str] = None, db: Session = Depends(get_db)):
    residents = (
        resident_service.search_residents(db, q)
        if q and q.strip()
        else resident_service.list_residents(db)
    )
    return [ResidentRead(**resident.to_dict()) for resident in residents]

@router.get("/residents/{resident_id}", response_model=ResidentRead)
def get_resident(resident_id: str, db: Session = Depends(get_db)):
    resident = resident_service.get_resident(db, resident_id)
    if not resident:
        raise HTTPException(status_code=404, detail="Resident not found")
    return ResidentRead(**resident.to_dict())

@router.patch("/residents/{resident_id}", response_model=ResidentRead)
def patch_resident(resident_id: str, update: ResidentUpdatePayload, db: Session = Depends(get_db)):
    resident = resident_service.update_resident(db, resident_id, update.dict(exclude_unset=True))
    if not resident:
        raise HTTPException(status_code=404, detail="Resident not found")
    return ResidentRead(**resident.to_dict())


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _user_read(user: User) -> UserRead:
    data = user.to_dict()
    data["roles"] = user_service.get_user_roles(user)
    return UserRead(**data)


def _set_auth_cookie(response: Response, user_id: str) -> None:
    response.set_cookie(
        key=settings.auth_cookie_name,
        value=security.create_token(user_id),
        max_age=settings.token_ttl_minutes * 60,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        path="/",
    )


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

@router.post("/auth/login", response_model=MeResponse)
def login(payload: LoginPayload, response: Response, db: Session = Depends(get_db)):
    user = user_service.authenticate(db, payload.username_or_email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    _set_auth_cookie(response, str(user.id))
    return MeResponse(user=_user_read(user), is_admin=user_service.is_admin(user))


@router.post("/auth/logout")
def logout(response: Response):
    response.delete_cookie(key=settings.auth_cookie_name, path="/")
    return {"detail": "Logged out"}


@router.post("/auth/refresh", response_model=MeResponse)
def refresh(response: Response, user: User = Depends(get_current_user)):
    _set_auth_cookie(response, str(user.id))
    return MeResponse(user=_user_read(user), is_admin=user_service.is_admin(user))


@router.get("/auth/me", response_model=MeResponse)
def me(user: User = Depends(get_current_user)):
    return MeResponse(user=_user_read(user), is_admin=user_service.is_admin(user))


@router.post("/auth/change-password", response_model=MeResponse)
def change_password(
    payload: ChangePasswordPayload,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not user_service.change_password(db, user, payload.old_password, payload.new_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    return MeResponse(user=_user_read(user), is_admin=user_service.is_admin(user))


# ---------------------------------------------------------------------------
# Users (auth required; create/update/delete require admin)
# ---------------------------------------------------------------------------

@router.get("/users", response_model=List[UserRead])
def list_users(q: Optional[str] = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    users = user_service.search_users(db, q) if q and q.strip() else user_service.list_users(db)
    return [_user_read(u) for u in users]


@router.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return _user_read(user)


@router.post("/users", response_model=UserRead)
def create_user(payload: UserCreatePayload, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    try:
        user = user_service.create_user(
            db, payload.dict(exclude={"role_codes"}, exclude_none=True), payload.role_codes
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="ID number, username or email already exists")
    return _user_read(user)


@router.patch("/users/{user_id}", response_model=UserRead)
def patch_user(user_id: str, update: UserUpdatePayload, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    try:
        user = user_service.update_user(db, user_id, update.dict(exclude_unset=True))
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="ID number, username or email already exists")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return _user_read(user)


@router.delete("/users/{user_id}", response_model=UserRead)
def delete_user(user_id: str, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    """Soft delete: marks the user inactive, never removes the row."""
    user = user_service.soft_delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return _user_read(user)


@router.get("/roles", response_model=List[RoleRead])
def list_roles(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return [RoleRead(**role.to_dict()) for role in user_service.list_roles(db)]


@router.post("/users/{user_id}/roles", response_model=UserRead)
def assign_role(
    user_id: str,
    payload: RoleAssignPayload,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    start = date.fromisoformat(payload.start_date) if payload.start_date else None
    end = date.fromisoformat(payload.end_date) if payload.end_date else None
    link = user_service.assign_role(db, user_id, payload.role_code, start, end)
    if not link:
        raise HTTPException(status_code=404, detail="User or role not found")
    user = user_service.get_user(db, user_id)
    return _user_read(user)
