from fastapi import Request, Depends
from google import genai
from modules.tasks.repo.task_repository import TaskRepository
from modules.tasks.repo.comment_repository import CommentRepository
from modules.projects.repo.board_repository import BoardRepository
from modules.tasks.depends.comment_depends import get_comment_repository
from modules.tasks.depends.task_depends import get_task_repository
from modules.projects.depends.board_depends import get_board_repository
from modules.ai.AICatchUpService import AIService


async def get_ai_client(request: Request) -> genai.Client:
    client = getattr(request.app.state, 'gemini', None)

    if client is None:
        raise RuntimeError('No gemini client')

    return client


async def get_gemini(
        client: genai.Client = Depends(get_ai_client)
) -> genai.Client:
    return client


async def get_ai_service(
        task_repo: TaskRepository = Depends(get_task_repository),
        comment_repo: CommentRepository = Depends(get_comment_repository),
        boards_repo: BoardRepository = Depends(get_board_repository),
        client: genai.Client = Depends(get_ai_client),
) -> AIService:
    return AIService(
        task_repo=task_repo,
        comment_repo=comment_repo,
        board_repo=boards_repo,
        client=client,
    )
