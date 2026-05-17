from sqlalchemy.ext.asyncio import AsyncSession

from core.repository import BaseRepository
from modules.tasks.models.task import TaskActivity


class TaskActivityRepository(BaseRepository[TaskActivity]):
    def __init__(self, session: AsyncSession):
        super().__init__(TaskActivity, session)
