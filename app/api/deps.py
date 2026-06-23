from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db
from app.models.user import User, UserStatus
from app.services import security
from app.services.user_service import user_service


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get(settings.auth_cookie_name)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        user_id = security.verify_token(token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    user = user_service.get_user(db, user_id)
    if not user or user.status != UserStatus.active:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    if not user_service.is_admin(user):
        raise HTTPException(status_code=403, detail="Administrator role required")
    return user
