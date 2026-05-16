from typing import List, Optional

from backend.modules.projects.models.project import Board
from backend.modules.projects.repo.board_repository import BoardRepository
from backend.modules.projects.schemas.board_schemas import BoardCreate, BoardUpdate


class BoardService:
    def __init__(self, board_repo: BoardRepository):
        self.board_repo = board_repo

    async def get_board(self, board_id: int) -> Optional[Board]:
        return await self.board_repo.get_by_id(board_id)

    async def get_boards(self, skip: int = 0, limit: int = 100) -> List[Board]:
        return await self.board_repo.get_all(skip=skip, limit=limit)

    async def create_board(self, data: BoardCreate) -> Board:
        board = await self.board_repo.create(**data.model_dump())
        # EDA: Emit event BOARD_CREATED
        return board

    async def update_board(self, board_id: int, data: BoardUpdate) -> Optional[Board]:
        board = await self.board_repo.get_by_id(board_id)
        if not board:
            return None
        updated_board = await self.board_repo.update(board, **data.model_dump(exclude_unset=True))
        # EDA: Emit event BOARD_UPDATED
        return updated_board

    async def delete_board(self, board_id: int) -> bool:
        success = await self.board_repo.delete(board_id)
        if success:
            # EDA: Emit event BOARD_DELETED
            pass
        return success
