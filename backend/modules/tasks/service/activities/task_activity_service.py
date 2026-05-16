from typing import List, Optional

from backend.modules.tasks.models.task import TaskActivity
from backend.modules.tasks.repo.activities.task_activity_repository import TaskActivityRepository
from backend.modules.tasks.schemas.activities.task_activity_schemas import TaskActivityCreate


class TaskActivityService:
    def __init__(self, activity_repo: TaskActivityRepository):
        self.activity_repo = activity_repo

    async def get_activity(self, activity_id: int) -> Optional[TaskActivity]:
        return await self.activity_repo.get_by_id(activity_id)

    async def get_activities(self, skip: int = 0, limit: int = 100) -> List[TaskActivity]:
        return await self.activity_repo.get_all(skip=skip, limit=limit)

    async def create_activity(self, data: TaskActivityCreate) -> TaskActivity:
        activity = await self.activity_repo.create(**data.model_dump())
        # EDA: Emit event TASK_ACTIVITY_CREATED
        return activity
