from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    company_id: int
    position: Optional[str] = None
    department: Optional[str] = None
    notes: Optional[str] = None
    status: str = "ACTIVE"  # ACTIVE, INACTIVE, PENDING
    success_manager_id: Optional[int] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    department: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None
    success_manager_id: Optional[int] = None

class CustomerInDB(CustomerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CustomerResponse(CustomerInDB):
    pass 