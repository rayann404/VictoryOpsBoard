from modules.tasks.repo.comment_repository import CommentRepository
from modules.tasks.repo.task_repository import TaskRepository
from modules.projects.repo.board_repository import BoardRepository


class AIService:
    def __init__(self, task_repo: TaskRepository, comment_repo: CommentRepository, board_repo: BoardRepository):
        self.task_repo = task_repo
        self.comment_repo = comment_repo
        self.board_repo = board_repo


    async def get_all_context(self, task_id: int) -> dict:
        task = await self.task_repo.get_by_id(task_id)

        comments = await self.comment_repo.get_by_task_id(task_id)

        return {
            "task": {
                "id": task_id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "assignee_id": task.assignee_id,
                "created_at": task.created_at,
                "updated_at": task.updated_at
            },
            "comments": [
                {
                    "user_id": comment.id,
                    "content": comment.content,
                    "created_at": comment.created_at
                }
                for comment in comments
            ]
        }
