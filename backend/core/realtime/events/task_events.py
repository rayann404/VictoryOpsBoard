from pydantic import BaseModel
from typing import Literal


class TaskCreatedEvent(BaseModel):
    type: Literal["task.created"]

    task_id: str
    project_id: str
    organization_id: str

    title: str
    status: str