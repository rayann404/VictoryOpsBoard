from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from backend.modules.projects.depends.board_depends import get_board_service
from backend.modules.projects.schemas.board_schemas import (
    BoardCreate,
    BoardResponse,
    BoardUpdate,
)
from backend.modules.projects.service.board_service import BoardService


router = APIRouter(prefix="/boards", tags=["Boards"])


@router.post("/", response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
async def create_board(
    data: BoardCreate,
    service: BoardService = Depends(get_board_service),
):
    return await service.create_board(data)


@router.get("/", response_model=List[BoardResponse])
async def get_boards(
    skip: int = 0,
    limit: int = 100,
    service: BoardService = Depends(get_board_service),
):
    return await service.get_boards(skip=skip, limit=limit)


@router.get("/{board_id}", response_model=BoardResponse)
async def get_board(
    board_id: int,
    service: BoardService = Depends(get_board_service),
):
    board = await service.get_board(board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board


@router.patch("/{board_id}", response_model=BoardResponse)
async def update_board(
    board_id: int,
    data: BoardUpdate,
    service: BoardService = Depends(get_board_service),
):
    board = await service.update_board(board_id, data)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board


@router.delete("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_board(
    board_id: int,
    service: BoardService = Depends(get_board_service),
):
    success = await service.delete_board(board_id)
    if not success:
        raise HTTPException(status_code=404, detail="Board not found")
