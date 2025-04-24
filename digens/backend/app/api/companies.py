from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Any, Optional
from ..core.database import get_db
from ..services.company_service import (
    create_company,
    get_company,
    get_companies,
    update_company,
    delete_company
)
from ..schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate
from ..core.security import oauth2_scheme

router = APIRouter()

@router.post("/companies/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_new_company(
    company: CompanyCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Any:
    return create_company(db=db, company=company)

@router.get("/companies/", response_model=List[CompanyResponse])
def read_companies(
    organization_id: Optional[int] = Query(None, description="Filter companies by organization ID"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Any:
    companies = get_companies(db, organization_id=organization_id, skip=skip, limit=limit)
    return companies

@router.get("/companies/{company_id}", response_model=CompanyResponse)
def read_company(
    company_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Any:
    db_company = get_company(db, company_id=company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company

@router.put("/companies/{company_id}", response_model=CompanyResponse)
def update_company_info(
    company_id: int,
    company_update: CompanyUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Any:
    return update_company(db=db, company_id=company_id, company_update=company_update)

@router.delete("/companies/{company_id}")
def delete_company_by_id(
    company_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Any:
    return {"success": delete_company(db=db, company_id=company_id)} 