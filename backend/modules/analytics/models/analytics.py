from typing import Any, Optional
from sqlalchemy import String, ForeignKey, JSON, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from backend.core.models.base import Base

class ProjectSummary(Base):
    __tablename__ = "project_summaries"
    
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    summary_text: Mapped[str] = mapped_column(Text)
    bottlenecks: Mapped[Optional[str]] = mapped_column(Text)
    ai_metadata: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON)

class AnalyticsSnapshot(Base):
    __tablename__ = "analytics_snapshots"
    
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    metric_name: Mapped[str] = mapped_column(String(100))
    metric_value: Mapped[float] = mapped_column()
    dimensions: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON)

class SlaMonitor(Base):
    __tablename__ = "sla_monitors"
    
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    column_id: Mapped[int] = mapped_column(ForeignKey("columns.id"))
    entry_time: Mapped[Any] = mapped_column(DateTime(timezone=True))
    exit_time: Mapped[Optional[Any]] = mapped_column(DateTime(timezone=True))
    is_breached: Mapped[bool] = mapped_column(default=False)
