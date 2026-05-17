from pydantic import BaseModel
from typing import Literal


class TaskCreatedEvent(BaseModel):
    type: Literal["task.created"]

    task_id: int
    project_id: int
    organization_id: int

    title: str
    column_id: int