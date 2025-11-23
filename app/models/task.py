import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, func
from app.db.session import Base


class Priority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskORM(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(String(1000), nullable=True)
    priority = Column(Enum(Priority), nullable=False, default=Priority.medium)
    is_done = Column(Boolean, default=False, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    due_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
