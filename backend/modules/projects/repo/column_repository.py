from sqlalchemy.ext.asyncio import AsyncSession

from core.repository import BaseRepository
from modules.projects.models.project import Column


class ColumnRepository(BaseRepository[Column]):
    def __init__(self, session: AsyncSession):
        super().__init__(Column, session)
