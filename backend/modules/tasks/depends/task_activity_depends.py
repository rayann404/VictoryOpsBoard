from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from modules.tasks.repo.task_activity_repository import TaskActivityRepository
from modules.tasks.service.task_activity_service import TaskActivityService


def get_task_activity_repository(
    session: AsyncSession = Depends(get_db),
) -> TaskActivityRepository:
    return TaskActivityRepository(session)


def get_task_activity_service(
    activity_repo: TaskActivityRepository = Depends(get_task_activity_repository),
) -> TaskActivityService:
    return TaskActivityService(activity_repo)
