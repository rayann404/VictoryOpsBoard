from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
# from backend.core.database import get_db_session  # Placeholder for real DB dependency
from backend.modules.organizations.schemas.org_schemas import OrganizationResponse, OrganizationCreate, OrganizationUpdate
from backend.modules.organizations.service.org_service import OrganizationService

# Mock dependency for session, replace with actual import later
async def get_db_session() -> AsyncSession:
    pass

router = APIRouter(prefix="/organizations", tags=["Organizations"])

@router.post("/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    data: OrganizationCreate,
    session: AsyncSession = Depends(get_db_session)
):
    service = OrganizationService(session)
    return await service.create_organization(data)

@router.get("/", response_model=List[OrganizationResponse])
async def get_organizations(
    skip: int = 0, 
    limit: int = 100,
    session: AsyncSession = Depends(get_db_session)
):
    service = OrganizationService(session)
    return await service.get_organizations(skip=skip, limit=limit)

@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(
    org_id: int,
    session: AsyncSession = Depends(get_db_session)
):
    service = OrganizationService(session)
    org = await service.get_organization(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@router.patch("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: int,
    data: OrganizationUpdate,
    session: AsyncSession = Depends(get_db_session)
):
    service = OrganizationService(session)
    org = await service.update_organization(org_id, data)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    org_id: int,
    session: AsyncSession = Depends(get_db_session)
):
    service = OrganizationService(session)
    success = await service.delete_organization(org_id)
    if not success:
        raise HTTPException(status_code=404, detail="Organization not found")
