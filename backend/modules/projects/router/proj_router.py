from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.modules.projects.schemas.proj_schemas import ProjectResponse, ProjectCreate, ProjectUpdate
from backend.modules.projects.service.proj_service import ProjectService

async def get_db_session() -> AsyncSession:
    pass

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(data: ProjectCreate, session: AsyncSession = Depends(get_db_session)):
    service = ProjectService(session)
    return await service.create_project(data)

@router.get("/", response_model=List[ProjectResponse])
async def get_projects(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_db_session)):
    service = ProjectService(session)
    return await service.get_projects(skip=skip, limit=limit)

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, session: AsyncSession = Depends(get_db_session)):
    service = ProjectService(session)
    project = await service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, data: ProjectUpdate, session: AsyncSession = Depends(get_db_session)):
    service = ProjectService(session)
    project = await service.update_project(project_id, data)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int, session: AsyncSession = Depends(get_db_session)):
    service = ProjectService(session)
    success = await service.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
