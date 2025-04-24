from sqlalchemy import Column, String, Boolean, JSON
from .base import BaseModel

class Organization(BaseModel):
    __tablename__ = "organizations"

    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    settings = Column(JSON, nullable=True)
    logo_url = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    address = Column(String, nullable=True) 