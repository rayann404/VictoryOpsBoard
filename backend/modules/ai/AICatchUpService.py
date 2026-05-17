from modules.tasks.repo.task_repository import TaskRepository
from modules.tasks.repo.comment_repository import CommentRepository
from modules.projects.repo.board_repository import BoardRepository
from google import genai
from google.genai import types
from .schemas.ai_schemas import CatchUpResponse
from config import settings


CATCHUP_PROMPT_TEMPLATE = """
Ты — старший операционный менеджер (PM) в элитном digital-агентстве. Твоя специализация — декомпозиция хаотичных обсуждений в четкие, понятные инструкции для исполнителей.

Твоя цель: проанализировать контекст задачи и историю последних комментариев, чтобы выдать исполнителю (Assignee) максимально сжатый и конкретный "курс дела".

КОНТЕКСТ ЗАДАЧИ:
---
ID задачи: {task_id}
Название: {task_title}
Описание: {task_description}
Приоритет: {task_priority}
ID исполнителя: {task_assignee_id}
Дата создания: {task_created_at}
Дата последнего обновления: {task_updated_at}
---

ИСТОРИЯ ОБСУЖДЕНИЯ (в хронологическом порядке):
{comments_text}

ИНСТРУКЦИЯ ПО ФОРМИРОВАНИЮ ОТВЕТА (JSON):
1. summary (Суть): В 2-3 предложениях объясни текущий статус. На чем остановились? Какое финальное решение принято? Игнорируй вежливость, пиши только факты.
2. blockers (Проблемы): Список факторов, которые мешают работе прямо сейчас (недостаток доступов, противоречивые требования, отсутствие контента). Если всё ок — верни пустой список [].
3. next_steps (План действий): Составь список из конкретных шагов для ИСПОЛНИТЕЛЯ прямо сейчас. Каждый шаг должен начинаться с глагола в повелительном наклонении (например: "Изменить", "Добавить", "Запросить"). Шаги должны быть атомарными.

ТРЕБОВАНИЯ:
- Язык: Русский.
- Тон: Профессиональный, лаконичный, директивный.
- Формат: Ты ДОЛЖЕН вернуть ТОЛЬКО валидный JSON. Не пиши никакой вводной информации, пояснений или markdown-разметки (типа ```json). Только сам объект.
"""

class AIService:
    def __init__(
        self,
        task_repo: TaskRepository,
        comment_repo: CommentRepository,
        board_repo: BoardRepository,
        client: genai.Client,
    ):
        self.task_repo = task_repo
        self.comment_repo = comment_repo
        self.board_repo = board_repo
        self.client = client

    async def get_task_context(self, task_id: int) -> dict:
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")

        comments = await self.comment_repo.get_by_task_id(task_id)
        comments = list(reversed(comments))

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
                    "user_id": comment.user_id,
                    "content": comment.content,
                    "created_at": comment.created_at
                }
                for comment in comments
            ]
        }

    async def get_task_catchup_payload(self, task_id: int) -> dict:
        context = await self.get_task_context(task_id)
        task = context["task"]

        comments_text = "\n".join(
            f"[{comment['created_at']}] Пользователь {comment['user_id']}: {comment['content']}"
            for comment in context["comments"]
        ) or "Комментарии отсутствуют."

        prompt = CATCHUP_PROMPT_TEMPLATE.format(
            task_id=task["id"],
            task_title=task["title"],
            task_description=task["description"] or "Описание отсутствует",
            task_priority=task["priority"],
            task_assignee_id=task["assignee_id"] or "Исполнитель не назначен",
            task_created_at=task["created_at"],
            task_updated_at=task["updated_at"],
            comments_text=comments_text,
        )

        return {
            "context": context,
            "prompt": prompt,
        }


    async def catchup_request(self, payload: dict) -> CatchUpResponse:
        response = await self.client.aio.models.generate_content(
            model=settings.AI_MODEL,
            contents=payload['prompt'],
            config=types.GenerateContentConfig(
                temperature=0.1,
                response_mime_type="application/json",
                response_schema=CatchUpResponse,
                max_output_tokens=2000,
            ),
        )

        return CatchUpResponse.model_validate_json(response.text)
