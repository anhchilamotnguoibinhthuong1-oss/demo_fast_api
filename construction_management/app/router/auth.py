from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Dict
from fastapi.security import OAuth2PasswordRequestForm

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import RegisterRequest, LoginRequest, Token
from app.services.user_service import UserService
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    """
    Đăng ký tài khoản mới
    - Kiểm tra email đã tồn tại
    - Hash mật khẩu
    - Lưu vào database
    """
    return UserService.create_user(db, payload)


@router.post("/login", response_model=Token)
def login(payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Đăng nhập và cấp JWT token
    - Xác thực email & password
    - Tạo access token và refresh token
    """
    user = AuthService.authenticate_user(db, payload.username, payload.password)
    return AuthService.create_tokens(user)


@router.post("/refresh", response_model=Token)
def refresh_token_endpoint(payload: Dict[str, str], db: Session = Depends(get_db)):
    """
    Cập nhật access token bằng refresh token
    - Xác thực refresh token
    - Cấp access token mới
    """
    refresh_token = payload.get("refresh_token")
    return AuthService.refresh_access_token(db, refresh_token)
