from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TaskActivityBase(BaseModel):
    activity_type: str = Field(..., max_length=50)
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    task_id: int
    user_id: int


class TaskActivityCreate(TaskActivityBase):
    pass


class TaskActivityResponse(TaskActivityBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
