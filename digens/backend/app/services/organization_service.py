from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional, List
from ..models.organization import Organization
from ..schemas.organization import OrganizationCreate, OrganizationUpdate

def get_organization(db: Session, org_id: int) -> Optional[Organization]:
    return db.query(Organization).filter(Organization.id == org_id).first()

def get_organization_by_slug(db: Session, slug: str) -> Optional[Organization]:
    return db.query(Organization).filter(Organization.slug == slug).first()

def get_organizations(db: Session, skip: int = 0, limit: int = 100) -> List[Organization]:
    return db.query(Organization).offset(skip).limit(limit).all()

def create_organization(db: Session, org: OrganizationCreate) -> Organization:
    # Slug kontrolü
    db_org = get_organization_by_slug(db, slug=org.slug)
    if db_org:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization with this slug already exists"
        )
    
    # Yeni organizasyon oluştur
    db_org = Organization(**org.dict())
    
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org

def update_organization(db: Session, org_id: int, org_update: OrganizationUpdate) -> Organization:
    db_org = get_organization(db, org_id)
    if not db_org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    update_data = org_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_org, field, value)
    
    db.commit()
    db.refresh(db_org)
    return db_org

def delete_organization(db: Session, org_id: int) -> bool:
    db_org = get_organization(db, org_id)
    if not db_org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    db.delete(db_org)
    db.commit()
    return True 