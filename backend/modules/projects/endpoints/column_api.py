from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from modules.projects.depends.column_depends import get_column_service
from modules.projects.schemas.column_schemas import (
    ColumnCreate,
    ColumnResponse,
    ColumnUpdate,
)
from modules.projects.service.column_service import ColumnService


router = APIRouter(prefix="/columns", tags=["Columns"])


@router.post("/", response_model=ColumnResponse, status_code=status.HTTP_201_CREATED)
async def create_column(
    data: ColumnCreate,
    service: ColumnService = Depends(get_column_service),
):
    return await service.create_column(data)


@router.get("/", response_model=List[ColumnResponse])
async def get_columns(
    skip: int = 0,
    limit: int = 100,
    service: ColumnService = Depends(get_column_service),
):
    return await service.get_columns(skip=skip, limit=limit)


@router.get("/{column_id}", response_model=ColumnResponse)
async def get_column(
    column_id: int,
    service: ColumnService = Depends(get_column_service),
):
    column = await service.get_column(column_id)
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")
    return column


@router.patch("/{column_id}", response_model=ColumnResponse)
async def update_column(
    column_id: int,
    data: ColumnUpdate,
    service: ColumnService = Depends(get_column_service),
):
    column = await service.update_column(column_id, data)
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")
    return column


@router.delete("/{column_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_column(
    column_id: int,
    service: ColumnService = Depends(get_column_service),
):
    success = await service.delete_column(column_id)
    if not success:
        raise HTTPException(status_code=404, detail="Column not found")
