from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any
from ..core.database import get_db
from ..services.user_service import (
    create_user,
    get_user,
    get_users,
    update_user,
    delete_user
)
from ..schemas.user import UserCreate, UserResponse, UserUpdate
from ..core.security import oauth2_scheme

router = APIRouter()

@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)) -> Any:
    return create_user(db=db, user=user)

@router.get("/users/", response_model=List[UserResponse])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Any:
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Any:
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user_info(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Any:
    return update_user(db=db, user_id=user_id, user_update=user_update)

@router.delete("/users/{user_id}")
def delete_user_account(
    user_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Any:
    return {"success": delete_user(db=db, user_id=user_id)} 