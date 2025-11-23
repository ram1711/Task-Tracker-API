from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from app.models.task import Priority
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.services.task import TaskService, get_task_service

router = APIRouter()


@router.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(
    payload: TaskCreate,
    service: TaskService = Depends(get_task_service),
):
    return service.create_task(payload)


@router.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
):
    return service.get_task(task_id)


@router.get("/tasks", response_model=List[TaskOut])
def list_tasks(
    include_done: bool = Query(False),
    search: Optional[str] = Query(None),
    priority: Optional[Priority] = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: TaskService = Depends(get_task_service),
):
    return service.list_tasks(
        include_done=include_done,
        search=search,
        priority=priority,
        offset=offset,
        limit=limit,
    )


@router.patch("/tasks/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    service: TaskService = Depends(get_task_service),
):
    return service.update_task(task_id, payload)


@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
):
    service.delete_task(task_id)
    return {"detail": "Task deleted successfully"}
