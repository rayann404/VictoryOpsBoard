from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from modules.tasks.repo.task_repository import TaskRepository
from modules.tasks.repo.task_activity_repository import TaskActivityRepository
from modules.tasks.service.task_service import TaskService
from modules.tasks.depends.task_activity_depends import get_task_activity_repository
from modules.projects.depends.board_depends import get_board_repository
from modules.projects.depends.column_depends import get_column_repository
from modules.projects.depends.project_depends import get_project_repository
from core.realtime.services.event_bus import EventBus
from core.realtime.dependencies import get_event_bus


def get_task_repository(session: AsyncSession = Depends(get_db)) -> TaskRepository:
    return TaskRepository(session)


def get_task_service(
    task_repo: TaskRepository = Depends(get_task_repository),
    activity_repo: TaskActivityRepository = Depends(get_task_activity_repository),
    column_repo: TaskActivityRepository = Depends(get_column_repository),
    board_repo: TaskActivityRepository = Depends(get_board_repository),
    project_repo: TaskActivityRepository = Depends(get_project_repository),
    event_bus: EventBus = Depends(get_event_bus)
) -> TaskService:
    return TaskService(
        task_repo,
        activity_repo,
        column_repo,
        board_repo,
        project_repo,
        event_bus
    )
