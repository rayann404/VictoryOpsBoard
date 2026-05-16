from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.core.repository import BaseRepository
from backend.modules.identity.models.user import User, Role

class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

class RoleRepository(BaseRepository[Role]):
    def __init__(self, session: AsyncSession):
        super().__init__(Role, session)
