from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from modules.tasks.depends.task_activity_depends import get_task_activity_service
from modules.tasks.schemas.task_activity_schemas import (
    TaskActivityCreate,
    TaskActivityResponse,
)
from modules.tasks.service.task_activity_service import TaskActivityService


router = APIRouter(prefix="/activities", tags=["Task Activities"])


@router.post("/", response_model=TaskActivityResponse, status_code=status.HTTP_201_CREATED)
async def create_activity(
    data: TaskActivityCreate,
    service: TaskActivityService = Depends(get_task_activity_service),
):
    return await service.create_activity(data)


@router.get("/", response_model=List[TaskActivityResponse])
async def get_activities(
    skip: int = 0,
    limit: int = 100,
    service: TaskActivityService = Depends(get_task_activity_service),
):
    return await service.get_activities(skip=skip, limit=limit)


@router.get("/{activity_id}", response_model=TaskActivityResponse)
async def get_activity(
    activity_id: int,
    service: TaskActivityService = Depends(get_task_activity_service),
):
    activity = await service.get_activity(activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Task activity not found")
    return activity
