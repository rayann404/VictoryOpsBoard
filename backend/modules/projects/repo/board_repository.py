from sqlalchemy.ext.asyncio import AsyncSession

from core.repository import BaseRepository
from modules.projects.models.project import Board


class BoardRepository(BaseRepository[Board]):
    def __init__(self, session: AsyncSession):
        super().__init__(Board, session)
