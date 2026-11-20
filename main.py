import json
import logging
import time

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log = {
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        log.update(getattr(record, "fields", {}))
        return json.dumps(log)


handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger = logging.getLogger("todo-api")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False

app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    done: bool = False


tasks: list[Task] = []


@app.get("/")
def root():
    return {"message": "Todo API is running"}


@app.get("/tasks")
def list_tasks():
    return tasks


@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task)
    return task


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for t in tasks:
        if t.id == task_id:
            return t


raise HTTPException(status_code=404, detail="Task not found")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    logger.info(
        "request",
        extra={
            "fields": {
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "duration_ms": round((time.perf_counter() - start) * 1000, 1),
            }
        },
    )
    return response


@app.get("/health")
def health():
    return {"status": "ok"}
