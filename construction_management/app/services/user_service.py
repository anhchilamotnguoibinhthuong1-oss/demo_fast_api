from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.core.security import hash_password


class UserService:
    """
    Service layer cho User entity
    - Xử lý business logic liên quan đến user
    - Gọi database thông qua db session
    - Validate dữ liệu và raise exception khi cần
    """

    @staticmethod
    def create_user(db: Session, payload: UserCreate) -> User:
        """
        Tạo user mới
        - Kiểm tra email đã tồn tại
        - Hash password
        - Lưu vào database
        """
        existing = db.query(User).filter(User.email == payload.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email đã được sử dụng"
            )

        user = User(
            email=payload.email,
            full_name=payload.full_name,
            password_hash=hash_password(payload.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """Lấy user theo ID"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """Lấy user theo email"""
        user = db.query(User).filter(User.email == email).first()
        return user

    @staticmethod
    def list_all_users(db: Session) -> list[User]:
        """Lấy danh sách tất cả users"""
        return db.query(User).all()

    @staticmethod
    def update_user(db: Session, user_id: int, payload: UserUpdate) -> User:
        """Cập nhật thông tin user"""
        user = UserService.get_user_by_id(db, user_id)
        
        if payload.full_name is not None:
            user.full_name = payload.full_name
        if payload.is_active is not None:
            user.is_active = payload.is_active
        
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
