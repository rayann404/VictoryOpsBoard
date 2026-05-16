from typing import List, Optional, Any
from sqlalchemy import String, ForeignKey, Integer, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.core.models.base import Base

class Task(Base):
    __tablename__ = "tasks"
    
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    priority: Mapped[int] = mapped_column(Integer, default=1) # 1: Low, 2: Medium, 3: High
    metadata_json: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON)
    
    column_id: Mapped[int] = mapped_column(ForeignKey("columns.id"))
    assignee_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    # Relationships
    column: Mapped["Column"] = relationship(back_populates="tasks")
    comments: Mapped[List["Comment"]] = relationship(back_populates="task")
    activities: Mapped[List["TaskActivity"]] = relationship(back_populates="task")

class Comment(Base):
    __tablename__ = "comments"
    
    content: Mapped[str] = mapped_column(Text)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    task: Mapped["Task"] = relationship(back_populates="comments")

class TaskActivity(Base):
    __tablename__ = "task_activities"
    
    activity_type: Mapped[str] = mapped_column(String(50)) # e.g., 'moved', 'assigned', 'status_change'
    old_value: Mapped[Optional[str]] = mapped_column(Text)
    new_value: Mapped[Optional[str]] = mapped_column(Text)
    
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    task: Mapped["Task"] = relationship(back_populates="activities")

class TaskTag(Base):
    __tablename__ = "task_tags"
    
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
