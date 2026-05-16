from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.modules.projects.repo.columns.column_repository import ColumnRepository
from backend.modules.projects.service.columns.column_service import ColumnService


def get_column_repository(session: AsyncSession = Depends(get_db)) -> ColumnRepository:
    return ColumnRepository(session)


def get_column_service(
    column_repo: ColumnRepository = Depends(get_column_repository),
) -> ColumnService:
    return ColumnService(column_repo)
