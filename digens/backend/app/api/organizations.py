from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any
from ..core.database import get_db
from ..services.organization_service import (
    create_organization,
    get_organization,
    get_organizations,
    update_organization,
    delete_organization
)
from ..schemas.organization import OrganizationCreate, OrganizationResponse, OrganizationUpdate
from ..core.security import oauth2_scheme

router = APIRouter()

@router.post("/organizations/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
def create_new_organization(
    org: OrganizationCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Any:
    return create_organization(db=db, org=org)

@router.get("/organizations/", response_model=List[OrganizationResponse])
def read_organizations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Any:
    organizations = get_organizations(db, skip=skip, limit=limit)
    return organizations

@router.get("/organizations/{org_id}", response_model=OrganizationResponse)
def read_organization(
    org_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Any:
    db_org = get_organization(db, org_id=org_id)
    if db_org is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return db_org

@router.put("/organizations/{org_id}", response_model=OrganizationResponse)
def update_organization_info(
    org_id: int,
    org_update: OrganizationUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Any:
    return update_organization(db=db, org_id=org_id, org_update=org_update)

@router.delete("/organizations/{org_id}")
def delete_organization_by_id(
    org_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Any:
    return {"success": delete_organization(db=db, org_id=org_id)} 