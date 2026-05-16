from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
# from backend.core.database import get_db_session  # Placeholder for DB dependency
from backend.modules.identity.schemas import (
    UserResponse, UserCreate, UserUpdate,
    RoleResponse, RoleCreate, RoleUpdate
)
from backend.modules.identity.service import IdentityService

async def get_db_session() -> AsyncSession:
    # Placeholder
    pass

router = APIRouter(prefix="/identity", tags=["Identity"])

# --- Roles ---
@router.post("/roles", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(data: RoleCreate, session: AsyncSession = Depends(get_db_session)):
    service = IdentityService(session)
    return await service.create_role(data)

@router.get("/roles", response_model=List[RoleResponse])
async def get_roles(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_db_session)):
    service = IdentityService(session)
    return await service.get_roles(skip=skip, limit=limit)

@router.get("/roles/{role_id}", response_model=RoleResponse)
async def get_role(role_id: int, session: AsyncSession = Depends(get_db_session)):
    service = IdentityService(session)
    role = await service.get_role(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.patch("/roles/{role_id}", response_model=RoleResponse)
async def update_role(role_id: int, data: RoleUpdate, session: AsyncSession = Depends(get_db_session)):
    service = IdentityService(session)
    role = await service.update_role(role_id, data)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(role_id: int, session: AsyncSession = Depends(get_db_session)):
    service = IdentityService(session)
    success = await service.delete_role(role_id)
    if not success:
        raise HTTPException(status_code=404, detail="Role not found")

# --- Users ---
@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, session: AsyncSession = Depends(get_db_session)):
    service = IdentityService(session)
    return await service.create_user(data)

@router.get("/users", response_model=List[UserResponse])
async def get_users(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_db_session)):
    service = IdentityService(session)
    return await service.get_users(skip=skip, limit=limit)

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(get_db_session)):
    service = IdentityService(session)
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, data: UserUpdate, session: AsyncSession = Depends(get_db_session)):
    service = IdentityService(session)
    user = await service.update_user(user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_db_session)):
    service = IdentityService(session)
    success = await service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
