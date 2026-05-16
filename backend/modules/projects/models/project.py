from typing import List, Optional
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.core.models.base import Base

class Project(Base):
    __tablename__ = "projects"
    
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String(1000))
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"))
    
    # Relationships
    organization: Mapped["Organization"] = relationship(back_populates="projects")
    boards: Mapped[List["Board"]] = relationship(back_populates="project")

class Board(Base):
    __tablename__ = "boards"
    
    name: Mapped[str] = mapped_column(String(255))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    
    # Relationships
    project: Mapped["Project"] = relationship(back_populates="boards")
    columns: Mapped[List["Column"]] = relationship(back_populates="board")

class Column(Base):
    __tablename__ = "columns"
    
    name: Mapped[str] = mapped_column(String(100))
    position: Mapped[int] = mapped_column(Integer, default=0)
    wip_limit: Mapped[Optional[int]] = mapped_column(Integer)
    board_id: Mapped[int] = mapped_column(ForeignKey("boards.id", ondelete="CASCADE"))
    
    # Relationships
    board: Mapped["Board"] = relationship(back_populates="columns")
    tasks: Mapped[List["Task"]] = relationship(back_populates="column")

class Tag(Base):
    __tablename__ = "tags"
    
    name: Mapped[str] = mapped_column(String(50))
    color: Mapped[str] = mapped_column(String(20), default="#000000")
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"))
