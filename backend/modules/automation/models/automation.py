from typing import Any, Optional
from sqlalchemy import String, ForeignKey, JSON, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from core.models.base import Base

class AutomationRule(Base):
    __tablename__ = "automation_rules"
    
    name: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # IF-THEN Logic
    trigger_type: Mapped[str] = mapped_column(String(100)) # e.g., TASK_MOVED
    condition_data: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON)
    action_data: Mapped[dict[str, Any]] = mapped_column(JSON)
    
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))

class AutomationExecution(Base):
    __tablename__ = "automation_executions"
    
    rule_id: Mapped[int] = mapped_column(ForeignKey("automation_rules.id"))
    status: Mapped[str] = mapped_column(String(50)) # success, failed
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    execution_context: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON)
