from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.repository import BaseRepository
from backend.modules.projects.models.project import Board


class BoardRepository(BaseRepository[Board]):
    def __init__(self, session: AsyncSession):
        super().__init__(Board, session)
