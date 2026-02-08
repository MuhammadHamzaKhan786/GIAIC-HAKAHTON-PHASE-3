from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class TaskStatus(str, Enum):
    ALL = "all"
    PENDING = "pending"
    COMPLETED = "completed"


class AddTaskRequest(BaseModel):
    title: str
    description: Optional[str] = None


class AddTaskResponse(BaseModel):
    task_id: int
    title: str
    completed: bool
    created_at: str


class ListTasksRequest(BaseModel):
    status: TaskStatus = TaskStatus.ALL


class TaskItem(BaseModel):
    id: int
    title: str
    completed: bool


class ListTasksResponse(BaseModel):
    tasks: List[TaskItem]


class CompleteTaskRequest(BaseModel):
    task_id: int


class CompleteTaskResponse(BaseModel):
    task_id: int
    title: str
    completed: bool


class UpdateTaskRequest(BaseModel):
    task_id: int
    title: Optional[str] = None
    description: Optional[str] = None


class UpdateTaskResponse(BaseModel):
    task_id: int
    title: str
    completed: bool


class DeleteTaskRequest(BaseModel):
    task_id: int


class DeleteTaskResponse(BaseModel):
    task_id: int
    status: str