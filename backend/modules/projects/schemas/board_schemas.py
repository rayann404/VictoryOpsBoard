from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class BoardBase(BaseModel):
    name: str = Field(..., max_length=255)
    project_id: int


class BoardCreate(BoardBase):
    pass


class BoardUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)


class BoardResponse(BoardBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
