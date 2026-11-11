from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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
