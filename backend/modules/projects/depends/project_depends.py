from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from modules.projects.repo.project_repository import ProjectRepository
from modules.projects.service.project_service import ProjectService


def get_project_repository(session: AsyncSession = Depends(get_db)) -> ProjectRepository:
    return ProjectRepository(session)


def get_project_service(
    project_repo: ProjectRepository = Depends(get_project_repository),
) -> ProjectService:
    return ProjectService(project_repo)
