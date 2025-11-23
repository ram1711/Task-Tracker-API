from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.task import TaskORM, Priority


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data) -> TaskORM:
        obj = TaskORM(
            title=data.title,
            description=data.description,
            priority=data.priority,
            due_at=data.due_at,
        )
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, task_id: int) -> Optional[TaskORM]:
        return (
            self.db.query(TaskORM)
            .filter(TaskORM.id == task_id, TaskORM.is_deleted.is_(False))
            .first()
        )

    def list(
        self,
        *,
        include_done: bool,
        search: Optional[str],
        priority: Optional[Priority],
        offset: int,
        limit: int,
    ) -> List[TaskORM]:
        q = self.db.query(TaskORM).filter(TaskORM.is_deleted.is_(False))

        if not include_done:
            q = q.filter(TaskORM.is_done.is_(False))
        if search:
            like = f"%{search.lower()}%"
            q = q.filter(func.lower(TaskORM.title).like(like))
        if priority:
            q = q.filter(TaskORM.priority == priority)

        return (
            q.order_by(TaskORM.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    def update(self, obj: TaskORM, data) -> TaskORM:
        for field, value in data.dict(exclude_unset=True).items():
            setattr(obj, field, value)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def soft_delete(self, obj: TaskORM) -> None:
        obj.is_deleted = True
        self.db.add(obj)
        self.db.commit()
