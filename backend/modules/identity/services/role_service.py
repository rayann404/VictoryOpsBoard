from typing import List, Optional

from modules.identity.repos.user_repository import RoleRepository
from modules.identity.schemas.user_schemas import RoleCreate, RoleUpdate
from modules.identity.models.user import Role

class RoleService:
    def __init__(self, role_repo: RoleRepository):
        self.role_repo = role_repo      
    # Role Methods
    async def get_role(self, role_id: int) -> Optional[Role]:
        return await self.role_repo.get_by_id(role_id)
        
    async def get_roles(self, skip: int = 0, limit: int = 100) -> List[Role]:
        return await self.role_repo.get_all(skip=skip, limit=limit)
        
    async def create_role(self, data: RoleCreate) -> Role:
        return await self.role_repo.create(**data.model_dump())
        
    async def update_role(self, role_id: int, data: RoleUpdate) -> Optional[Role]:
        role = await self.role_repo.get_by_id(role_id)
        if not role:
            return None
        return await self.role_repo.update(role, **data.model_dump(exclude_unset=True))
        
    async def delete_role(self, role_id: int) -> bool:
        return await self.role_repo.delete(role_id)
     
