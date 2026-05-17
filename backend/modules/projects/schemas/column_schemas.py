from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ColumnBase(BaseModel):
    name: str = Field(..., max_length=100)
    position: int = 0
    wip_limit: Optional[int] = None
    board_id: int


class ColumnCreate(ColumnBase):
    pass


class ColumnUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    position: Optional[int] = None
    wip_limit: Optional[int] = None


class ColumnResponse(ColumnBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
