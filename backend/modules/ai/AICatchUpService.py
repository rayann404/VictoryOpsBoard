from modules.tasks.repo.comment_repository import CommentRepository
from modules.tasks.repo.task_repository import TaskRepository
from modules.projects.repo.board_repository import BoardRepository


class AIService:
    def __init__(self, task_repo: TaskRepository, comment_repo: CommentRepository, board_repo: BoardRepository):
        self.task_repo = task_repo
        self.comment_repo = comment_repo
        self.board_repo = board_repo
