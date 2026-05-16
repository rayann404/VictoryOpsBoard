from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.repository import BaseRepository
from backend.modules.identity.models.user import User, Role

class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

class RoleRepository(BaseRepository[Role]):
    def __init__(self, session: AsyncSession):
        super().__init__(Role, session)
