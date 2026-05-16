from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.modules.organizations.repo.repository import OrganizationRepository
from backend.modules.organizations.schemas.org_schemas import OrganizationCreate, OrganizationUpdate
from backend.modules.organizations.models.organization import Organization

class OrganizationService:
    def __init__(self, session: AsyncSession):
        self.repository = OrganizationRepository(session)
        self.session = session
    
    async def get_organization(self, org_id: int) -> Optional[Organization]:
        return await self.repository.get_by_id(org_id)
        
    async def get_organizations(self, skip: int = 0, limit: int = 100) -> List[Organization]:
        return await self.repository.get_all(skip=skip, limit=limit)
        
    async def create_organization(self, data: OrganizationCreate) -> Organization:
        # TODO: Business logic validation goes here
        # For instance, ensuring unique slug can be done via try/except on IntegrityError in repository, 
        # or checking explicitly before creation.
        
        org = await self.repository.create(**data.model_dump())
        
        # EDA: Emit event
        # await event_bus.publish("ORGANIZATION_CREATED", org_id=org.id)
        
        return org
        
    async def update_organization(self, org_id: int, data: OrganizationUpdate) -> Optional[Organization]:
        org = await self.repository.get_by_id(org_id)
        if not org:
            return None
            
        update_data = data.model_dump(exclude_unset=True)
        updated_org = await self.repository.update(org, **update_data)
        
        # EDA: Emit event
        # await event_bus.publish("ORGANIZATION_UPDATED", org_id=updated_org.id)
        
        return updated_org

    async def delete_organization(self, org_id: int) -> bool:
        success = await self.repository.delete(org_id)
        if success:
            # EDA: Emit event
            # await event_bus.publish("ORGANIZATION_DELETED", org_id=org_id)
            pass
        return success
