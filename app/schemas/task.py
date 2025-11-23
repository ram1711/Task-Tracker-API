from datetime import datetime, timedelta, timezone
from typing import Optional

from pydantic import BaseModel, Field, validator

from app.models.task import Priority


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Priority = Priority.medium
    due_at: Optional[datetime] = None

    @validator("due_at")
    def validate_due_date(cls, v):
        if v is not None:
            now = datetime.now(timezone.utc)  # timezone-aware current datetime
            if v < now or v > now + timedelta(days=365):
                raise ValueError("due_at must be a future date within one year")
        return v


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[Priority] = None
    is_done: Optional[bool] = None
    due_at: Optional[datetime] = None

    @validator("due_at")
    def validate_due_date(cls, v):
        if v is not None:
            now = datetime.now(timezone.utc)  # timezone-aware current datetime
            if v < now or v > now + timedelta(days=365):
                raise ValueError("due_at must be a future date within one year")
        return v


class TaskOut(TaskBase):
    id: int
    is_done: bool
    created_at: datetime
    due_at: Optional[datetime]
    completed_at: Optional[datetime]

    class Config:
        orm_mode = True

    @validator("due_at")
    def validate_due_date(cls, v):
        if v is not None:
            now = datetime.now(timezone.utc)  # timezone-aware current datetime
            if v < now or v > now + timedelta(days=365):
                raise ValueError("due_at must be a future date within one year")
        return v
