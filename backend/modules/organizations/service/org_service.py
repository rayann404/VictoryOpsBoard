from typing import List, Optional

from modules.organizations.repo.repository import OrganizationRepository
from modules.organizations.schemas.org_schemas import OrganizationCreate, OrganizationUpdate
from modules.organizations.models.organization import Organization

class OrganizationService:
    def __init__(self, repository: OrganizationRepository):
        self.repository = repository
    
    async def get_organization(self, org_id: int) -> Optional[Organization]:
        return await self.repository.get_by_id(org_id)
        
    async def get_organizations(self, skip: int = 0, limit: int = 100) -> List[Organization]:
        return await self.repository.get_all(skip=skip, limit=limit)
        
    async def create_organization(self, data: OrganizationCreate) -> Organization:
        # TODO: Business logic validation goes here

        
        org = await self.repository.create(**data.model_dump())
        
        
        return org
        
    async def update_organization(self, org_id: int, data: OrganizationUpdate) -> Optional[Organization]:
        org = await self.repository.get_by_id(org_id)
        if not org:
            return None
            
        update_data = data.model_dump(exclude_unset=True)
        updated_org = await self.repository.update(org, **update_data)
        

        
        return updated_org

    async def delete_organization(self, org_id: int) -> bool:
        success = await self.repository.delete(org_id)
        if success:
            pass
        return success
