from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from modules.projects.repo.column_repository import ColumnRepository
from modules.projects.service.column_service import ColumnService


def get_column_repository(session: AsyncSession = Depends(get_db)) -> ColumnRepository:
    return ColumnRepository(session)


def get_column_service(
    column_repo: ColumnRepository = Depends(get_column_repository),
) -> ColumnService:
    return ColumnService(column_repo)
