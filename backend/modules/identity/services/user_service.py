from typing import List, Optional

from modules.identity.repos.user_repository import UserRepository
from modules.identity.schemas.user_schemas import UserCreate, UserUpdate
from modules.identity.models.user import User


class InvalidCredentialsError(Exception):
    pass


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        
    def _hash_password(self, password: str) -> str:
        return hash(password)

        
    # User Methods
    async def get_user(self, user_id: int) -> Optional[User]:
        return await self.user_repo.get_by_id(user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await self.user_repo.get_by_email(email)

    async def authenticate_user(self, email: str, password: str) -> User:
        user = await self.get_user_by_email(email)
        if not user or user.hashed_password != self._hash_password(password):
            raise InvalidCredentialsError()
        return user
        
    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return await self.user_repo.get_all(skip=skip, limit=limit)
        
    async def create_user(self, data: UserCreate) -> User:
        user_data = data.model_dump(exclude={"password"})
        user_data["hashed_password"] = self._hash_password(data.password)
        
        user = await self.user_repo.create(**user_data)

        
        return user
        
    async def update_user(self, user_id: int, data: UserUpdate) -> Optional[User]:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            return None
            
        update_data = data.model_dump(exclude_unset=True, exclude={"password"})
        if data.password:
            update_data["hashed_password"] = self._hash_password(data.password)
            
        updated_user = await self.user_repo.update(user, **update_data)
        
        return updated_user
        
    async def delete_user(self, user_id: int) -> bool:
        success = await self.user_repo.delete(user_id)
        if success:
            pass
        return success
