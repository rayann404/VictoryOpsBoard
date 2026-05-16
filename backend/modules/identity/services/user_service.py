from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.modules.identity.repository import UserRepository, RoleRepository
from backend.modules.identity.schemas import UserCreate, UserUpdate, RoleCreate, RoleUpdate
from backend.modules.identity.models.user import User, Role

class IdentityService:
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session)
        self.role_repo = RoleRepository(session)
        self.session = session
        
    def _hash_password(self, password: str) -> str:
        # Placeholder for password hashing (e.g. using passlib bcrypt)
        # For a real application, you must hash the password properly here.
        return f"hashed_{password}"
        
    # --- Role Methods ---
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
        
    # --- User Methods ---
    async def get_user(self, user_id: int) -> Optional[User]:
        return await self.user_repo.get_by_id(user_id)
        
    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return await self.user_repo.get_all(skip=skip, limit=limit)
        
    async def create_user(self, data: UserCreate) -> User:
        user_data = data.model_dump(exclude={"password"})
        user_data["hashed_password"] = self._hash_password(data.password)
        
        user = await self.user_repo.create(**user_data)
        
        # EDA: Emit event
        # await event_bus.publish("USER_CREATED", user_id=user.id)
        
        return user
        
    async def update_user(self, user_id: int, data: UserUpdate) -> Optional[User]:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            return None
            
        update_data = data.model_dump(exclude_unset=True, exclude={"password"})
        if data.password:
            update_data["hashed_password"] = self._hash_password(data.password)
            
        updated_user = await self.user_repo.update(user, **update_data)
        
        # EDA: Emit event
        # await event_bus.publish("USER_UPDATED", user_id=updated_user.id)
        
        return updated_user
        
    async def delete_user(self, user_id: int) -> bool:
        success = await self.user_repo.delete(user_id)
        if success:
            # EDA: Emit event
            # await event_bus.publish("USER_DELETED", user_id=user_id)
            pass
        return success
