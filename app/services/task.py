from datetime import datetime, timezone
from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1 import tasks
from app.db.session import get_db
from app.models.task import TaskORM, Priority
from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate


def make_aware(dt):
    if dt and dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt

class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def create_task(self, data: TaskCreate) -> TaskORM:
        created_task = self.repo.create(data)
        created_task.due_at = make_aware(created_task.due_at)
        return created_task

    def get_task(self, task_id: int) -> TaskORM:
        task = self.repo.get(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        task.due_at = make_aware(task.due_at)
        return task

    def list_tasks(
        self,
        *,
        include_done: bool,
        search: Optional[str],
        priority: Optional[Priority],
        offset: int,
        limit: int,
    ) -> List[TaskORM]:
        tasks = self.repo.list(
            include_done=include_done,
            search=search,
            priority=priority,
            offset=offset,
            limit=limit,
        )
        for task in tasks:
            task.due_at = make_aware(task.due_at)
            # Similarly for other datetime fields if needed
        return tasks
        # return self.repo.list(
        #     include_done=include_done,
        #     search=search,
        #     priority=priority,
        #     offset=offset,
        #     limit=limit,
        # )

    def update_task(self, task_id: int, data: TaskUpdate) -> TaskORM:
        task = self.get_task(task_id)

        if data.is_done is not None:
            if data.is_done and not task.is_done:
                task.completed_at = datetime.utcnow()
            elif not data.is_done and task.is_done:
                task.completed_at = None
        updated_task = self.repo.update(task, data)
        updated_task.due_at = make_aware(updated_task.due_at)
        return updated_task

    def delete_task(self, task_id: int) -> None:
        task = self.get_task(task_id)
        self.repo.soft_delete(task)
        
def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    repo = TaskRepository(db)
    return TaskService(repo)
