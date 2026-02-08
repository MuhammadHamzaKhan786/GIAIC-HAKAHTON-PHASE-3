"""
Proper MCP Tool Registration Module
"""
from mcp.server import FastMCP
from mcp import Tool
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
import asyncio
from backend.mcp.db import get_session, Task
from sqlmodel import select
from datetime import datetime
from backend.mcp.errors import TaskNotFoundError, ValidationError, UnauthorizedError


# Define enums and models
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


def get_current_user_id_mock():
    """
    Mock function to get user_id until we properly integrate with request context.
    In a real implementation, this would extract user_id from the JWT in the request headers.
    """
    import os
    return os.getenv("MOCK_USER_ID", "test_user_123")


# Create the MCP server instance using FastMCP
server = FastMCP(
    name="mcp-task-server",
    instructions="MCP server for task management"
)


# Define the tool handler functions
async def add_task_handler(params: dict) -> dict:
    """
    Add a new task.
    """
    # Parse the params into the request object
    request = AddTaskRequest(**params)

    # Validate inputs
    if not request.title or len(request.title.strip()) == 0:
        raise ValidationError(message="Title is required and cannot be empty", field="title")

    if request.description and len(request.description) > 1000:
        raise ValidationError(message="Description exceeds maximum length of 1000 characters", field="description")

    # Get current user from JWT (will be implemented in auth phase)
    user_id = get_current_user_id_mock()

    # Create a new task record
    new_task = Task(
        user_id=user_id,
        title=request.title.strip(),
        description=request.description,
        completed=False
    )

    with next(get_session()) as session:
        session.add(new_task)
        session.commit()
        session.refresh(new_task)

    response = AddTaskResponse(
        task_id=new_task.id,
        title=new_task.title,
        completed=new_task.completed,
        created_at=new_task.created_at.isoformat()
    )

    return response.dict()


async def list_tasks_handler(params: dict) -> dict:
    """
    List tasks for the authenticated user.
    """
    # Parse the params into the request object
    request = ListTasksRequest(**params)

    # Get current user from JWT (will be implemented in auth phase)
    user_id = get_current_user_id_mock()

    with next(get_session()) as session:
        # Build query based on status filter
        query = select(Task).where(Task.user_id == user_id)

        if request.status != "all":
            if request.status == "pending":
                query = query.where(Task.completed == False)
            elif request.status == "completed":
                query = query.where(Task.completed == True)

        tasks = session.exec(query).all()

        task_items = [
            TaskItem(id=task.id, title=task.title, completed=task.completed)
            for task in tasks
        ]

        response = ListTasksResponse(tasks=task_items)

    return response.dict()


async def complete_task_handler(params: dict) -> dict:
    """
    Mark a task as completed.
    """
    # Parse the params into the request object
    request = CompleteTaskRequest(**params)

    # Get current user from JWT (will be implemented in auth phase)
    user_id = get_current_user_id_mock()

    with next(get_session()) as session:
        # Find the task by ID and user_id to ensure ownership
        statement = select(Task).where(Task.id == request.task_id, Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            raise TaskNotFoundError(task_id=request.task_id)

        # Update the task completion status
        task.completed = True
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)

    response = CompleteTaskResponse(
        task_id=task.id,
        title=task.title,
        completed=task.completed
    )

    return response.dict()


async def update_task_handler(params: dict) -> dict:
    """
    Update a task's properties.
    """
    # Parse the params into the request object
    request = UpdateTaskRequest(**params)

    # Get current user from JWT (will be implemented in auth phase)
    user_id = get_current_user_id_mock()

    # Validate that at least one field is provided for update
    if request.title is None and request.description is None:
        raise ValidationError(message="At least one field (title or description) must be provided for update")

    with next(get_session()) as session:
        # Find the task by ID and user_id to ensure ownership
        statement = select(Task).where(Task.id == request.task_id, Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            raise TaskNotFoundError(task_id=request.task_id)

        # Update task properties if provided
        if request.title is not None:
            if len(request.title.strip()) == 0:
                raise ValidationError(message="Title cannot be empty", field="title")
            task.title = request.title
        if request.description is not None:
            task.description = request.description

        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)

    response = UpdateTaskResponse(
        task_id=task.id,
        title=task.title,
        completed=task.completed
    )

    return response.dict()


async def delete_task_handler(params: dict) -> dict:
    """
    Delete a task.
    """
    # Parse the params into the request object
    request = DeleteTaskRequest(**params)

    # Get current user from JWT (will be implemented in auth phase)
    user_id = get_current_user_id_mock()

    with next(get_session()) as session:
        # Find the task by ID and user_id to ensure ownership
        statement = select(Task).where(Task.id == request.task_id, Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            raise TaskNotFoundError(task_id=request.task_id)

        # Delete the task
        session.delete(task)
        session.commit()

    response = DeleteTaskResponse(
        task_id=request.task_id,
        status="deleted"
    )

    return response.dict()


# Define tools using the proper decorator approach for FastMCP
# We need to wrap the async handlers to match FastMCP expectations

# For FastMCP, the tools need to be registered with their schema information
# Since FastMCP.add_tool doesn't directly accept inputSchema and outputSchema as parameters,
# we'll create wrapper functions with proper annotations and use the FastMCP approach

# The right way to do this is to use a different approach where we create a Tool object
# and register it with FastMCP. Let me fix this:

import functools

# Register the tools with the server using FastMCP's add_tool method
# The function is the first parameter, and then the optional parameters
server.add_tool(
    add_task_handler,
    name="add_task",
    title="Add Task",
    description="Create a new task for the user"
)

server.add_tool(
    list_tasks_handler,
    name="list_tasks",
    title="List Tasks",
    description="Get list of tasks for the user"
)

server.add_tool(
    complete_task_handler,
    name="complete_task",
    title="Complete Task",
    description="Mark a task as completed"
)

server.add_tool(
    update_task_handler,
    name="update_task",
    title="Update Task",
    description="Update task properties"
)

server.add_tool(
    delete_task_handler,
    name="delete_task",
    title="Delete Task",
    description="Delete a task"
)