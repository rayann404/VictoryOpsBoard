from pydantic import BaseModel
from typing import Literal


class TaskCreatedEvent(BaseModel):
    type: Literal["task.created"]

    task_id: int
    title: str
    column_id: int
    creator_id: int
    description: str
    priority: int
    project_id: int
    organization_id: int

