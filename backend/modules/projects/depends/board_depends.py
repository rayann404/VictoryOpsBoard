from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from modules.projects.repo.board_repository import BoardRepository
from modules.projects.service.board_service import BoardService


def get_board_repository(session: AsyncSession = Depends(get_db)) -> BoardRepository:
    return BoardRepository(session)


def get_board_service(
    board_repo: BoardRepository = Depends(get_board_repository),
) -> BoardService:
    return BoardService(board_repo)
