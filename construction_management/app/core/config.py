import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

# Chọn file .env nếu có, không thì dùng .env.example
_env_file = ".env" if os.path.exists(".env") else ".env.example"


class Settings(BaseSettings):
    """
    Cấu hình ứng dụng được đọc từ file .env
    """

    # =========================================================
    # DATABASE
    # =========================================================
    
    # Chuỗi kết nối database (SQLite, PostgreSQL, MySQL,...)
    # Ví dụ: sqlite:///./test.db
    DATABASE_URL: str

    # =========================================================
    # JWT & AUTHENTICATION
    # =========================================================
    
    # Khóa bí mật dùng để ký JWT token (phải giữ bí mật)
    SECRET_KEY: str
    
    # Thuật toán hash JWT (mặc định: HS256)
    ALGORITHM: str = "HS256"
    
    # Access token hết hạn sau bao lâu (mặc định: 30 phút)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Refresh token hết hạn sau bao lâu (mặc định: 7 ngày)
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # =========================================================
    # APPLICATION
    # =========================================================
    
    # Môi trường chạy app (development / production)
    APP_ENV: str = "development"
    
    # Bật/tắt debug mode (True = chi tiết lỗi, False = ẩn chi tiết)
    DEBUG: bool = False

    # Cấu hình cách BaseSettings đọc file .env
    model_config = SettingsConfigDict(
        env_file=_env_file,
        env_file_encoding="utf-8",
        extra="ignore",  # Bỏ qua biến môi trường không khai báo
    )


# Cache settings để không tạo lại nhiều lần
@lru_cache
def get_settings() -> Settings:
    """Lấy settings cached"""
    return Settings()


# Tạo settings dùng chung trong toàn project
settings = get_settings()
