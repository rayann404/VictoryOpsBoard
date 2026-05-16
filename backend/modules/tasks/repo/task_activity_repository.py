from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.repository import BaseRepository
from backend.modules.tasks.models.task import TaskActivity


class TaskActivityRepository(BaseRepository[TaskActivity]):
    def __init__(self, session: AsyncSession):
        super().__init__(TaskActivity, session)
