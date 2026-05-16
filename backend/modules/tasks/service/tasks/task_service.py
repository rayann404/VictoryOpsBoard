from typing import List, Optional

from backend.modules.tasks.models.task import Task
from backend.modules.tasks.repo.tasks.task_repository import TaskRepository
from backend.modules.tasks.schemas.tasks.task_schemas import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo

    async def get_task(self, task_id: int) -> Optional[Task]:
        return await self.task_repo.get_by_id(task_id)

    async def get_tasks(self, skip: int = 0, limit: int = 100) -> List[Task]:
        return await self.task_repo.get_all(skip=skip, limit=limit)

    async def create_task(self, data: TaskCreate) -> Task:
        task = await self.task_repo.create(**data.model_dump())
        # EDA: Emit event TASK_CREATED
        return task

    async def update_task(self, task_id: int, data: TaskUpdate) -> Optional[Task]:
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            return None
        updated_task = await self.task_repo.update(task, **data.model_dump(exclude_unset=True))
        # EDA: Emit event TASK_UPDATED
        return updated_task

    async def delete_task(self, task_id: int) -> bool:
        success = await self.task_repo.delete(task_id)
        if success:
            # EDA: Emit event TASK_DELETED
            pass
        return success
