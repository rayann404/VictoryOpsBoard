from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.repository import BaseRepository
from backend.modules.projects.models.project import Project

class ProjectRepository(BaseRepository[Project]):
    def __init__(self, session: AsyncSession):
        super().__init__(Project, session)
