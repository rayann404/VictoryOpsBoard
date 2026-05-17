from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from modules.tasks.repo.task_repository import TaskRepository
from modules.tasks.repo.task_activity_repository import TaskActivityRepository
from modules.tasks.service.task_service import TaskService
from modules.tasks.depends.task_activity_depends import get_task_activity_repository


def get_task_repository(session: AsyncSession = Depends(get_db)) -> TaskRepository:
    return TaskRepository(session)


def get_task_service(
    task_repo: TaskRepository = Depends(get_task_repository),
    activity_repo: TaskActivityRepository = Depends(get_task_activity_repository),
) -> TaskService:
    return TaskService(task_repo, activity_repo)
