from sqlalchemy.ext.asyncio import AsyncSession

from core.repository import BaseRepository
from modules.tasks.models.task import Task


class TaskRepository(BaseRepository[Task]):
    def __init__(self, session: AsyncSession):
        super().__init__(Task, session)
