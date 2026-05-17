from typing import List, Optional

from modules.tasks.models.task import Comment
from modules.tasks.repo.comment_repository import CommentRepository
from modules.tasks.schemas.comment_schemas import CommentCreate, CommentUpdate


class CommentService:
    def __init__(self, comment_repo: CommentRepository):
        self.comment_repo = comment_repo

    async def get_comment(self, comment_id: int) -> Optional[Comment]:
        return await self.comment_repo.get_by_id(comment_id)

    async def get_comments(self, skip: int = 0, limit: int = 100) -> List[Comment]:
        return await self.comment_repo.get_all(skip=skip, limit=limit)

    async def create_comment(self, data: CommentCreate) -> Comment:
        comment = await self.comment_repo.create(**data.model_dump())
        # EDA: Emit event COMMENT_CREATED
        return comment

    async def update_comment(self, comment_id: int, data: CommentUpdate) -> Optional[Comment]:
        comment = await self.comment_repo.get_by_id(comment_id)
        if not comment:
            return None
        updated_comment = await self.comment_repo.update(comment, **data.model_dump(exclude_unset=True))
        # EDA: Emit event COMMENT_UPDATED
        return updated_comment

    async def delete_comment(self, comment_id: int) -> bool:
        success = await self.comment_repo.delete(comment_id)
        if success:
            # EDA: Emit event COMMENT_DELETED
            pass
        return success
