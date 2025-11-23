from fastapi import FastAPI
from app.db.session import engine, Base
from app.api.v1.tasks import router as tasks_router
from app.models import task

app = FastAPI(title="Task Tracker API", version="0.1.0")

Base.metadata.create_all(bind=engine)

app.include_router(tasks_router, prefix="/api/v1", tags=["tasks"])
