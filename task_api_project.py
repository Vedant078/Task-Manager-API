from fastapi import FastAPI, HTTPException, status
import time
from pydantic import BaseModel, Field
from typing import Literal, Optional

task_list = {
    1 : {
        "descp" : "Work out",
        "priority" : "Low",
        "status" : "To-do"
    }
}

app = FastAPI(title="Task Management API")

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

@app.get("/task/get-tasks")
def get_all_tasks():
    return task_list

@app.get("/task/get-task/{task_id}")
def get_task(task_id : int):
    if task_id not in task_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task_list[task_id]

@app.get("/task/filter/{task_status}")
def filterTasks(task_status: str):
    filtered_tasks = {}
    
    for task_id in task_list:
        current_task = task_list[task_id]
        if current_task["status"] == task_status:
            filtered_tasks[task_id] = current_task
            
    return filtered_tasks

@app.post("/task/create-task", status_code=status.HTTP_201_CREATED)
def create_task(task_id : int, task : TaskCreate):
    if task_id in task_list:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task ID already exists")
    
    task_list[task_id] = task.model_dump()
    return task_list[task_id]

@app.patch("/task/update-task/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    if task_id not in task_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    update_data = task.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        task_list[task_id][key] = value
        
    return task_list[task_id]

@app.delete("/task/delete-task/{task_id}")
def delete_task(task_id : int):
    if task_id not in task_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        
    del task_list[task_id]
    return {"message" : f"Task {task_id} deleted successfully"}