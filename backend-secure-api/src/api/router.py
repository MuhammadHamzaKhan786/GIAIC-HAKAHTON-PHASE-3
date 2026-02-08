from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from typing import List
from ..database import engine
from ..models.task import Task, TaskCreate, TaskRead, TaskUpdate
from ..auth.auth_bearer import get_current_user_id

router = APIRouter()

@router.get("/tasks", response_model=List[TaskRead])
def get_tasks(user_id: str = Depends(get_current_user_id)):
    with Session(engine) as session:
        # Only return tasks for the authenticated user
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()

        return tasks

@router.post("/tasks", response_model=TaskRead)
def create_task(task: TaskCreate, user_id: str = Depends(get_current_user_id)):
    with Session(engine) as session:
        # Create task with the authenticated user's ID
        db_task = Task.model_validate(task)
        db_task.user_id = user_id

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return db_task

@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task_by_id(task_id: str, user_id: str = Depends(get_current_user_id)):
    with Session(engine) as session:
        # Find the task and verify it belongs to the authenticated user
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        db_task = session.exec(statement).first()

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or access denied"
            )

        return db_task

@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: str, task_update: TaskUpdate, user_id: str = Depends(get_current_user_id)):
    with Session(engine) as session:
        # Find the task and verify it belongs to the authenticated user
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        db_task = session.exec(statement).first()

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or access denied"
            )

        # Update the task with provided fields
        for field, value in task_update.model_dump(exclude_unset=True).items():
            setattr(db_task, field, value)

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return db_task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: str, user_id: str = Depends(get_current_user_id)):
    with Session(engine) as session:
        # Find the task and verify it belongs to the authenticated user
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        db_task = session.exec(statement).first()

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or access denied"
            )

        session.delete(db_task)
        session.commit()

        return {"success": True}

@router.patch("/tasks/{task_id}/complete")
def toggle_task_completion(task_id: str, user_id: str = Depends(get_current_user_id)):
    with Session(engine) as session:
        # Find the task and verify it belongs to the authenticated user
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        db_task = session.exec(statement).first()

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or access denied"
            )

        # Toggle the completion status
        db_task.completed = not db_task.completed

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return {"success": True, "completed": db_task.completed}