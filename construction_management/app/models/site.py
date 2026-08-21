from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship

from app.db.database import Base


class ConstructionSite(Base):
    __tablename__ = "construction_sites"
    # Khóa chính
    id = Column(Integer, primary_key=True, index=True)

    # Tên công trình (không vượt 255 ký tự)
    name = Column(String(255), nullable=False)

    # Mô tả công trình
    description = Column(Text, nullable=True)

    # Một User có thể sở hữu nhiều công trình
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Thời gian tạo công trình
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Thời gian cập nhật công trình
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Soft delete - thời gian xóa
    deleted_at = Column(DateTime, nullable=True)

    # Soft delete - cờ xóa
    is_deleted = Column(Boolean, nullable=False, default=False)

    # Công trình thuộc về một User
    owner = relationship("User", back_populates="owned_sites", foreign_keys=[owner_id])

    # Một công trình có nhiều thành viên
    members = relationship(
        "SiteMember", back_populates="site", cascade="all, delete-orphan"
    )

    # Một công trình có nhiều hạng mục
    work_items = relationship(
        "WorkItem", back_populates="site", cascade="all, delete-orphan"
    )

    # Một công trình có nhiều log hoạt động
    activity_logs = relationship(
        "ActivityLog", back_populates="site", cascade="all, delete-orphan"
    )


class SiteMember(Base):
    __tablename__ = "site_members"
    # ID công trình
    site_id = Column(Integer, ForeignKey("construction_sites.id"), primary_key=True)
    # ID người dùng
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    # Vai trò của User trong công trình
    # OWNER / MEMBER
    role = Column(String(20), nullable=False)
    # Thời gian tham gia công trình
    joined_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    # SiteMember -> ConstructionSite
    site = relationship("ConstructionSite", back_populates="members")
    # SiteMember -> User
    user = relationship("User", back_populates="site_memberships")


class ActivityLog(Base):
    __tablename__ = "activity_logs"
    # Khóa chính
    id = Column(Integer, primary_key=True, index=True)

    # Công trình liên quan đến hoạt động
    site_id = Column(Integer, ForeignKey("construction_sites.id"), nullable=False)

    # Người thực hiện hoạt động
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Loại hoạt động: CREATE_SITE, UPDATE_SITE, DELETE_SITE, ADD_MEMBER, REMOVE_MEMBER
    action = Column(String(50), nullable=False)

    # Mô tả chi tiết hoạt động
    description = Column(Text, nullable=True)

    # Thời gian hoạt động
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Quan hệ
    site = relationship("ConstructionSite", back_populates="activity_logs")
    user = relationship("User")
