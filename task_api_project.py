from fastapi import FastAPI, HTTPException, status,Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session,select
from database import get_session
import time
from pydantic import BaseModel, Field
from typing import Literal, Optional
from database import init_db
from models import Task
from contextlib import asynccontextmanager
task_list = {
    1 : {
        "descp" : "Work out",
        "priority" : "Low",
        "status" : "To-do"
    }
}
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Task Management API",lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TaskCreate(BaseModel):
    descp : str = Field(..., max_length=30)
    priority : Literal["Low", "Medium", "High"] = "Medium"
    status : Literal["To-do", "In-progress", "Done"] = "To-do"

class TaskUpdate(BaseModel):
    descp : Optional[str] = Field(None, max_length=30)
    priority : Optional[Literal["Low", "Medium", "High"]] = None
    status : Optional[Literal["To-do", "In-progress", "Done"]] = None

@app.get("/")
def welcome():
    print(f"[{time.ctime()}] Welcome endpoint hit!")
    return {
        "message": "WELCOME to Task API",
        "developer": "Vedant Limbasiya",
        "timestamp": time.ctime()
    }

@app.get("/task/get-tasks",response_model = list[Task])
def get_all_tasks(priority : str | None = None, session: Session = Depends(get_session)):
    statement = select(Task)
    if priority:
        statement = statement.where(Task.priority == priority)
        
    tasks  = session.exec(statement).all()
    return tasks

@app.get("/task/get-task/{task_id}", response_model =Task)
def get_task(task_id : int,session : Session = Depends(get_session)):
    statement = select(Task).where(Task.id == task_id)
    task = session.exec(statement).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task

@app.post("/task/create-task", response_model = Task)
def create_task(task: Task, session: Session = Depends(get_session)):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.patch("/task/update-task/{task_id}", response_model = Task)
def update_task(task_id: int, task: TaskUpdate, session: Session = Depends(get_session)):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    
    update_task = task.model_dump(exclude_unset=True)
    for key, value in update_task.items():
        setattr(db_task, key, value)
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@app.delete("/task/delete-task/{task_id}")
def delete_task(task_id : int,session:Session = Depends(get_session)):
    task = session.get(Task,task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        
    session.delete(task)
    session.commit()
    return {"message" : f"Task {task_id} deleted successfully"}