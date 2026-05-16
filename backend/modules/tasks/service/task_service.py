from typing import List, Optional
from fastapi import HTTPException
from modules.tasks.models.task import Task
from modules.tasks.repo.task_repository import TaskRepository
from modules.tasks.schemas.task_schemas import TaskCreate, TaskUpdate
from modules.tasks.repo.task_activity_repository import TaskActivityRepository

class TaskService:
    def __init__(self, task_repo: TaskRepository, activity_repo: TaskActivityRepository):
        self.task_repo = task_repo
        self.activity_repo = activity_repo

    async def get_tasks(self, skip: int = 0, limit: int = 100) -> List[Task]:
        return await self.task_repo.get_all(skip=skip, limit=limit)

    async def create_task(self, data: TaskCreate) -> Task:
        task = await self.task_repo.create(**data.model_dump())
        return task

    async def update_task(self, task_id: int, data: TaskUpdate) -> Optional[Task]:
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            return None
        updated_task = await self.task_repo.update(task, **data.model_dump(exclude_unset=True))
        return updated_task

    async def delete_task(self, task_id: int) -> bool:
        success = await self.task_repo.delete(task_id)
        if success:
            pass
        return success
    
    async def move_task(self, task_id: int, new_column_id: int, user_id: int) -> Optional[Task]:
        task = await self.task_repo.get_by_id(task_id)
        if not task:
             return None
        old_column_id = task.column_id
        if old_column_id == new_column_id:
            return task
        

        new_column = await self.column_repo.get_by_id(new_column_id)
        if new_column and new_column.wip_limit:
            current_count = await self.task_repo.count_in_column(new_column_id)
            if current_count >= new_column.wip_limit:
                raise HTTPException(status_code=400, detail="WIP Limit reached for this column")


        updated_task = await self.task_repo.update(task, column_id=new_column_id)

        await self.activity_repo.create(
            task_id=task_id,
            user_id=user_id,
            activity_type="moved",
            old_value=str(old_column_id),
            new_value=str(new_column_id)
        )
   
        # 5. TODO: Отправить событие в NATS для Real-time и Automation

        return updated_task

