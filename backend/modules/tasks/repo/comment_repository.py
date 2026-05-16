from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.repository import BaseRepository
from backend.modules.tasks.models.task import Comment


class CommentRepository(BaseRepository[Comment]):
    def __init__(self, session: AsyncSession):
        super().__init__(Comment, session)
