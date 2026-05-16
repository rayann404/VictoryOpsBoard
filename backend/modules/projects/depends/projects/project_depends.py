from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.modules.projects.repo.projects.project_repository import ProjectRepository
from backend.modules.projects.service.projects.project_service import ProjectService


def get_project_repository(session: AsyncSession = Depends(get_db)) -> ProjectRepository:
    return ProjectRepository(session)


def get_project_service(
    project_repo: ProjectRepository = Depends(get_project_repository),
) -> ProjectService:
    return ProjectService(project_repo)
