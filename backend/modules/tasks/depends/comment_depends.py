from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from modules.tasks.repo.comment_repository import CommentRepository
from modules.tasks.service.comment_service import CommentService


def get_comment_repository(session: AsyncSession = Depends(get_db)) -> CommentRepository:
    return CommentRepository(session)


def get_comment_service(
    comment_repo: CommentRepository = Depends(get_comment_repository),
) -> CommentService:
    return CommentService(comment_repo)
