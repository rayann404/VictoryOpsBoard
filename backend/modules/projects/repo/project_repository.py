from sqlalchemy.ext.asyncio import AsyncSession

from core.repository import BaseRepository
from modules.projects.models.project import Project


class ProjectRepository(BaseRepository[Project]):
    def __init__(self, session: AsyncSession):
        super().__init__(Project, session)
