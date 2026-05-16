from typing import List, Optional

from backend.modules.projects.models.project import Project
from backend.modules.projects.repo.projects.project_repository import ProjectRepository
from backend.modules.projects.schemas.projects.project_schemas import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, project_repo: ProjectRepository):
        self.project_repo = project_repo

    async def get_project(self, project_id: int) -> Optional[Project]:
        return await self.project_repo.get_by_id(project_id)

    async def get_projects(self, skip: int = 0, limit: int = 100) -> List[Project]:
        return await self.project_repo.get_all(skip=skip, limit=limit)

    async def create_project(self, data: ProjectCreate) -> Project:
        project = await self.project_repo.create(**data.model_dump())
        # EDA: Emit event PROJECT_CREATED
        return project

    async def update_project(self, project_id: int, data: ProjectUpdate) -> Optional[Project]:
        project = await self.project_repo.get_by_id(project_id)
        if not project:
            return None
        updated_project = await self.project_repo.update(project, **data.model_dump(exclude_unset=True))
        # EDA: Emit event PROJECT_UPDATED
        return updated_project

    async def delete_project(self, project_id: int) -> bool:
        success = await self.project_repo.delete(project_id)
        if success:
            # EDA: Emit event PROJECT_DELETED
            pass
        return success
