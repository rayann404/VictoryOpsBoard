from typing import Any, Optional
from sqlalchemy import String, ForeignKey, JSON, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from core.models.base import Base

class EventStore(Base):
    __tablename__ = "events"
    
    event_type: Mapped[str] = mapped_column(String(100), index=True)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))

class Notification(Base):
    __tablename__ = "notifications"
    
    title: Mapped[str] = mapped_column(String(255))
    message: Mapped[str] = mapped_column(Text)
    is_read: Mapped[bool] = mapped_column(default=False)
    channel: Mapped[str] = mapped_column(String(50)) # web, email, telegram
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
