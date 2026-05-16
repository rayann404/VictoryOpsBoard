from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from backend.modules.identity.dependies.role_depends import get_role_service
from backend.modules.identity.schemas.user_schemas import RoleCreate, RoleResponse, RoleUpdate
from backend.modules.identity.services.role_service import RoleService


router = APIRouter(prefix="/identity/roles", tags=["Roles"])


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    data: RoleCreate,
    service: RoleService = Depends(get_role_service),
):
    return await service.create_role(data)


@router.get("/", response_model=List[RoleResponse])
async def get_roles(
    skip: int = 0,
    limit: int = 100,
    service: RoleService = Depends(get_role_service),
):
    return await service.get_roles(skip=skip, limit=limit)


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: int,
    service: RoleService = Depends(get_role_service),
):
    role = await service.get_role(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.patch("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    data: RoleUpdate,
    service: RoleService = Depends(get_role_service),
):
    role = await service.update_role(role_id, data)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: int,
    service: RoleService = Depends(get_role_service),
):
    success = await service.delete_role(role_id)
    if not success:
        raise HTTPException(status_code=404, detail="Role not found")
