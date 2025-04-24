from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional, List
from ..models.company import Company
from ..schemas.company import CompanyCreate, CompanyUpdate

def get_company(db: Session, company_id: int) -> Optional[Company]:
    return db.query(Company).filter(Company.id == company_id).first()

def get_company_by_slug(db: Session, slug: str) -> Optional[Company]:
    return db.query(Company).filter(Company.slug == slug).first()

def get_companies(
    db: Session,
    organization_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Company]:
    query = db.query(Company)
    if organization_id:
        query = query.filter(Company.organization_id == organization_id)
    return query.offset(skip).limit(limit).all()

def create_company(db: Session, company: CompanyCreate) -> Company:
    # Slug kontrolü
    db_company = get_company_by_slug(db, slug=company.slug)
    if db_company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Company with this slug already exists"
        )
    
    # Yeni şirket oluştur
    db_company = Company(**company.dict())
    
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def update_company(db: Session, company_id: int, company_update: CompanyUpdate) -> Company:
    db_company = get_company(db, company_id)
    if not db_company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    update_data = company_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_company, field, value)
    
    db.commit()
    db.refresh(db_company)
    return db_company

def delete_company(db: Session, company_id: int) -> bool:
    db_company = get_company(db, company_id)
    if not db_company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    db.delete(db_company)
    db.commit()
    return True 