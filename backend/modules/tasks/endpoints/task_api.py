from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from backend.modules.tasks.depends.task_depends import get_task_service
from backend.modules.tasks.schemas.task_schemas import TaskCreate, TaskResponse, TaskUpdate
from backend.modules.tasks.service.task_service import TaskService


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    data: TaskCreate,
    service: TaskService = Depends(get_task_service),
):
    return await service.create_task(data)


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    service: TaskService = Depends(get_task_service),
):
    return await service.get_tasks(skip=skip, limit=limit)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
):
    task = await service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    data: TaskUpdate,
    service: TaskService = Depends(get_task_service),
):
    task = await service.update_task(task_id, data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
):
    success = await service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
