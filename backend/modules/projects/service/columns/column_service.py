from typing import List, Optional

from backend.modules.projects.models.project import Column
from backend.modules.projects.repo.columns.column_repository import ColumnRepository
from backend.modules.projects.schemas.columns.column_schemas import ColumnCreate, ColumnUpdate


class ColumnService:
    def __init__(self, column_repo: ColumnRepository):
        self.column_repo = column_repo

    async def get_column(self, column_id: int) -> Optional[Column]:
        return await self.column_repo.get_by_id(column_id)

    async def get_columns(self, skip: int = 0, limit: int = 100) -> List[Column]:
        return await self.column_repo.get_all(skip=skip, limit=limit)

    async def create_column(self, data: ColumnCreate) -> Column:
        column = await self.column_repo.create(**data.model_dump())
        # EDA: Emit event COLUMN_CREATED
        return column

    async def update_column(self, column_id: int, data: ColumnUpdate) -> Optional[Column]:
        column = await self.column_repo.get_by_id(column_id)
        if not column:
            return None
        updated_column = await self.column_repo.update(column, **data.model_dump(exclude_unset=True))
        # EDA: Emit event COLUMN_UPDATED
        return updated_column

    async def delete_column(self, column_id: int) -> bool:
        success = await self.column_repo.delete(column_id)
        if success:
            # EDA: Emit event COLUMN_DELETED
            pass
        return success
