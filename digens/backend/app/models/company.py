from sqlalchemy import Column, String, Boolean, JSON, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .base import BaseModel

class Company(BaseModel):
    __tablename__ = "companies"

    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    settings = Column(JSON, nullable=True)
    logo_url = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    
    # Organization ilişkisi
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    organization = relationship("Organization", back_populates="companies")
    
    # Diğer ilişkiler
    users = relationship("User", secondary="company_users", back_populates="companies")
    departments = relationship("Department", back_populates="company")
    customers = relationship("Customer", back_populates="company") 