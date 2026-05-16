from sqlalchemy.ext.asyncio import AsyncSession
from core.repository import BaseRepository
from modules.organizations.models.organization import Organization

class OrganizationRepository(BaseRepository[Organization]):
    def __init__(self, session: AsyncSession):
        super().__init__(Organization, session)
