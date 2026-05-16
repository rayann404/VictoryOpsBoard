from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.repository import BaseRepository
from backend.modules.projects.models.project import Column


class ColumnRepository(BaseRepository[Column]):
    def __init__(self, session: AsyncSession):
        super().__init__(Column, session)
