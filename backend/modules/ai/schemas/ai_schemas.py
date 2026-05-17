from pydantic import BaseModel, Field
from typing import List

class CatchUpResponse(BaseModel):
    summary: str = Field(
        ..., 
        description="Краткая выжимка текущего состояния задачи и обсуждения."
    )
    blockers: List[str] = Field(
        default_factory=list, 
        description="Список факторов, блокирующих выполнение задачи."
    )
    next_steps: List[str] = Field(
        ..., 
        description="Конкретные шаги, которые должен предпринять исполнитель."
    )
