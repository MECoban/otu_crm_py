from sqlalchemy import Column, String, Boolean, JSON, Enum
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum

class UserRole(str, enum.Enum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    DEVELOPER = "DEVELOPER"
    LEADER = "LEADER"
    SUCCESS_MANAGER = "SUCCESS_MANAGER"
    CUSTOMER = "CUSTOMER"

class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.CUSTOMER)
    profile_image = Column(String, nullable=True)
    settings = Column(JSON, nullable=True)
    
    # İlişkiler
    companies = relationship("Company", secondary="company_users", back_populates="users")
    managed_customers = relationship("Customer", back_populates="success_manager") 