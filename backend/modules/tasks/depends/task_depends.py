from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.modules.tasks.repo.task_repository import TaskRepository
from backend.modules.tasks.service.task_service import TaskService


def get_task_repository(session: AsyncSession = Depends(get_db)) -> TaskRepository:
    return TaskRepository(session)


def get_task_service(
    task_repo: TaskRepository = Depends(get_task_repository),
) -> TaskService:
    return TaskService(task_repo)
