from typing import Optional
from sqlmodel import Field, SQLModel

# This class defines your Python code validation schema AND your PostgreSQL table layout
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    descp: str
    priority: str
    status: str