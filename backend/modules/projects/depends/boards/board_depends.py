from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.modules.projects.repo.boards.board_repository import BoardRepository
from backend.modules.projects.service.boards.board_service import BoardService


def get_board_repository(session: AsyncSession = Depends(get_db)) -> BoardRepository:
    return BoardRepository(session)


def get_board_service(
    board_repo: BoardRepository = Depends(get_board_repository),
) -> BoardService:
    return BoardService(board_repo)
