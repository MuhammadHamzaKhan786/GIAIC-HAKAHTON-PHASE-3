from mcp.server import Server
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from backend.mcp.tools import (
    AddTaskRequest, AddTaskResponse, ListTasksRequest, TaskItem,
    ListTasksResponse, CompleteTaskRequest, CompleteTaskResponse,
    UpdateTaskRequest, UpdateTaskResponse, DeleteTaskRequest,
    DeleteTaskResponse
)
from backend.mcp.db import get_session, Task
from sqlmodel import select
from datetime import datetime
from backend.mcp.errors import TaskNotFoundError, ValidationError, UnauthorizedError

# Create the MCP server instance
server = Server("mcp-task-server")


def get_current_user_id_mock():
    """
    Mock function to get user_id until we properly integrate with request context.
    In a real implementation, this would extract user_id from the JWT in the request headers.
    """
    # For now, we'll return a fixed user ID as a placeholder.
    # In a real system, this would be extracted from the Authorization header.
    import os
    return os.getenv("MOCK_USER_ID", "test_user_123")

# Register the MCP tools
@server.tool()
async def add_task(request: AddTaskRequest) -> AddTaskResponse:
    """
    Add a new task.
    """
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

    return AddTaskResponse(
        task_id=new_task.id,
        title=new_task.title,
        completed=new_task.completed,
        created_at=new_task.created_at.isoformat()
    )


@server.tool()
async def list_tasks(request: ListTasksRequest) -> ListTasksResponse:
    """
    List tasks for the authenticated user.
    """
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

    return ListTasksResponse(tasks=task_items)


@server.tool()
async def complete_task(request: CompleteTaskRequest) -> CompleteTaskResponse:
    """
    Mark a task as completed.
    """
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

    return CompleteTaskResponse(
        task_id=task.id,
        title=task.title,
        completed=task.completed
    )


@server.tool()
async def update_task(request: UpdateTaskRequest) -> UpdateTaskResponse:
    """
    Update a task's properties.
    """
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

    return UpdateTaskResponse(
        task_id=task.id,
        title=task.title,
        completed=task.completed
    )


@server.tool()
async def delete_task(request: DeleteTaskRequest) -> DeleteTaskResponse:
    """
    Delete a task.
    """
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

    return DeleteTaskResponse(
        task_id=request.task_id,
        status="deleted"
    )

# Export the server instance
__all__ = ['server']