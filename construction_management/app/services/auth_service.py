from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from app.services.user_service import UserService


class AuthService:
    """
    Service layer cho authentication
    - Xử lý logic đăng nhập, đăng ký
    - Quản lý token
    """

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        """
        Xác thực user với email và password
        - Tìm user theo email
        - So sánh password
        - Kiểm tra trạng thái active
        """
        user = UserService.get_user_by_email(db, email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email hoặc mật khẩu không đúng"
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tài khoản đã bị vô hiệu hóa"
            )
        return user

    @staticmethod
    def create_tokens(user: User) -> dict:
        """
        Tạo access token và refresh token
        """
        access_token = create_access_token({"sub": str(user.id), "role": user.role})
        refresh_token = create_refresh_token({"sub": str(user.id), "role": user.role})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "refresh_token": refresh_token
        }

    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str) -> dict:
        """
        Cập nhật access token từ refresh token
        """
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="refresh_token is required"
            )

        data = decode_token(refresh_token)
        if not data or data.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        user_id = data.get("sub")
        user = UserService.get_user_by_id(db, int(user_id))
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not active"
            )

        return AuthService.create_tokens(user)
