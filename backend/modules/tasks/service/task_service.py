from typing import List, Optional

from modules.tasks.models.task import Task
from modules.tasks.repo.task_repository import TaskRepository
from modules.tasks.schemas.task_schemas import TaskCreate, TaskUpdate
from modules.tasks.repo.task_activity_repository import TaskActivityRepository
from core.realtime.services.event_bus import EventBus

class TaskService:
    def __init__(
            self,
            task_repo: TaskRepository,
            activity_repo: TaskActivityRepository,
            event_bus: EventBus,
    ):
        self.task_repo = task_repo
        self.activity_repo = activity_repo
        self.event_bus = event_bus

    async def get_task(self, task_id: int) -> Optional[Task]:
        return await self.task_repo.get_by_id(task_id)

    async def get_tasks(self, skip: int = 0, limit: int = 100) -> List[Task]:
        return await self.task_repo.get_all(skip=skip, limit=limit)

    async def create_task(self, data: TaskCreate) -> Task:
        task = await self.task_repo.create(**data.model_dump())
        event = TaskCreatedEvent(
            type="task.created",

            task_id=str(task.id),

            project_id=str(task.project_id),

            organization_id=str(
                task.organization_id
            ),

            title=task.title,
            status=task.status,
        )

        await self.event_bus.publish(
            channel=project_channel(
                str(task.project_id)
            ),

            event=event.model_dump(),
        )

        await self.activity_repo.create(
            activity_type="created",
            old_value=None,
            new_value=str(task.id),
            task_id=task.id,
            user_id=task.creator_id,
        )

        return task

    async def update_task(self, task_id: int, data: TaskUpdate) -> Optional[Task]:
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            return None
        updated_task = await self.task_repo.update(task, **data.model_dump(exclude_unset=True))
        # EDA: Emit event TASK_UPDATED

        update_data = data.model_dump(exclude_unset=True)
        activity_types = {
            "title": "title_changed",
            "description": "description_changed",
            "priority": "priority_changed",
            "assignee_id": "assigned",
            "metadata_json": "metadata_updated",
        }
        changes = []

        for field, activity_type in activity_types.items():
            if field not in update_data:
                continue

            old_value = getattr(task, field)
            new_value = update_data[field]
            if old_value == new_value:
                continue

            changes.append((activity_type, old_value, new_value))

        updated_task = await self.task_repo.update(task, **update_data)

        for activity_type, old_value, new_value in changes:
            await self.activity_repo.create(
                task_id=task_id,
                user_id=updated_task.creator_id,
                activity_type=activity_type,
                old_value=str(old_value) if old_value is not None else None,
                new_value=str(new_value) if new_value is not None else None,
            )

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
