from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from modules.organizations.depends.org_depends import get_organization_service
from modules.organizations.schemas.org_schemas import OrganizationResponse, OrganizationCreate, OrganizationUpdate
from modules.organizations.service.org_service import OrganizationService

router = APIRouter(prefix="/organizations", tags=["Organizations"])

@router.post("/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    data: OrganizationCreate,
    service: OrganizationService = Depends(get_organization_service),
):
    return await service.create_organization(data)

@router.get("/", response_model=List[OrganizationResponse])
async def get_organizations(
    skip: int = 0, 
    limit: int = 100,
    service: OrganizationService = Depends(get_organization_service),
):
    return await service.get_organizations(skip=skip, limit=limit)

@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(
    org_id: int,
    service: OrganizationService = Depends(get_organization_service),
):
    org = await service.get_organization(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@router.patch("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: int,
    data: OrganizationUpdate,
    service: OrganizationService = Depends(get_organization_service),
):
    org = await service.update_organization(org_id, data)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    org_id: int,
    service: OrganizationService = Depends(get_organization_service),
):
    success = await service.delete_organization(org_id)
    if not success:
        raise HTTPException(status_code=404, detail="Organization not found")
