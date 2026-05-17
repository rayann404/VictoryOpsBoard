from typing import List
from modules.tasks.models.task import Task, Comment
from modules.tasks.repo.task_repository import TaskRepository
from modules.tasks.repo.comment_repository import CommentRepository
from modules.projects.repo.board_repository import BoardRepository


CATCHUP_PROMPT_TEMPLATE = """
Ты — старший операционный менеджер (PM) в элитном digital-агентстве. Твоя специализация — декомпозиция хаотичных обсуждений в четкие, понятные инструкции для исполнителей.

Твоя цель: проанализировать контекст задачи и историю последних комментариев, чтобы выдать исполнителю (Assignee) максимально сжатый и конкретный "курс дела".

КОНТЕКСТ ЗАДАЧИ:
---
Название: {task_title}
Описание: {task_description}
Приоритет: {task_priority}
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

class AICatchUpService:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def _prepare_comments_context(self, comments: List[Comment]) -> str:
        """Сборка текста комментариев для промпта"""
        if not comments:
            return "Комментарии отсутствуют."

        context_lines = []
        for c in comments:
            author_info = f"Пользователь {c.user_id}"
            line = f"[{c.created_at}] {author_info}: {c.content}"
            context_lines.append(line)

        return "\n".join(context_lines)

    async def get_task_catchup(self, task: Task, comments: List[Comment]) -> str:
        """Сборка промпта для задачи"""
        comments_text = self._prepare_comments_context(comments)

        prompt = CATCHUP_PROMPT_TEMPLATE.format(
            task_title=task.title,
            task_description=task.description or "Описание отсутствует",
            task_priority=task.priority,
            comments_text=comments_text
        )

        return prompt

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
