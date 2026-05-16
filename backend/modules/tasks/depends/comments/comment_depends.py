from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.modules.tasks.repo.comments.comment_repository import CommentRepository
from backend.modules.tasks.service.comments.comment_service import CommentService


def get_comment_repository(session: AsyncSession = Depends(get_db)) -> CommentRepository:
    return CommentRepository(session)


def get_comment_service(
    comment_repo: CommentRepository = Depends(get_comment_repository),
) -> CommentService:
    return CommentService(comment_repo)
