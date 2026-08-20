from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.permission import require_admin
from app.models.user import User
from app.schemas.user import UserResponse
from app.services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


# =========================================================
# USER + ADMIN
# =========================================================

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_current_user_profile(
    current_user: User = Depends(get_current_user),
):
    """
    USER và ADMIN đều có thể xem thông tin
    tài khoản của chính mình.
    """

    return current_user


# =========================================================
# ADMIN ONLY
# =========================================================

@router.get(
    "/",
    response_model=list[UserResponse],
)
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Chỉ ADMIN được xem danh sách tất cả user.
    """

    users = UserService.list_all_users(db)

    return users


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Chỉ ADMIN được xem thông tin user khác.
    """

    user = UserService.get_user_by_id(db, user_id)

    return user
