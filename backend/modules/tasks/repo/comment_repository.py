from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.repository import BaseRepository
from modules.tasks.models.task import Comment


class CommentRepository(BaseRepository[Comment]):
    def __init__(self, session: AsyncSession):
        super().__init__(Comment, session)


    async def get_by_task_id(self, task_id: int, limit: int = 20) -> list[Comment]:
        comments = await self.session.execute(
            select(Comment)
            .where(Comment.task_id == task_id)
            .order_by(Comment.created_at.desc())
            .limit(limit)
        )
        # TODO: решить проблему с пагинацией

        return comments.scalars().all()
