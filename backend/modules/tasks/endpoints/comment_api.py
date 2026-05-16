from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from modules.tasks.depends.comment_depends import get_comment_service
from modules.tasks.schemas.comment_schemas import (
    CommentCreate,
    CommentResponse,
    CommentUpdate,
)
from modules.tasks.service.comment_service import CommentService


router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    data: CommentCreate,
    service: CommentService = Depends(get_comment_service),
):
    return await service.create_comment(data)


@router.get("/", response_model=List[CommentResponse])
async def get_comments(
    skip: int = 0,
    limit: int = 100,
    service: CommentService = Depends(get_comment_service),
):
    return await service.get_comments(skip=skip, limit=limit)


@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment(
    comment_id: int,
    service: CommentService = Depends(get_comment_service),
):
    comment = await service.get_comment(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.patch("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    data: CommentUpdate,
    service: CommentService = Depends(get_comment_service),
):
    comment = await service.update_comment(comment_id, data)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    service: CommentService = Depends(get_comment_service),
):
    success = await service.delete_comment(comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")
