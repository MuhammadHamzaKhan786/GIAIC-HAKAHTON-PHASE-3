from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from typing import List
from backend.src.database import engine
from backend.src.models.task import Task, TaskCreate, TaskRead, TaskUpdate, TaskUpdateOwner
from backend.src.models.user import User
from backend.src.auth.auth_bearer import get_current_user_from_token

router = APIRouter()

@router.get("/", response_model=List[TaskRead])
def get_tasks(current_user: dict = Depends(get_current_user_from_token)):
    user_id = current_user.get("sub")

    with Session(engine) as session:
        # Only return tasks for the authenticated user
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()

        return tasks

@router.get("/{task_id}", response_model=TaskRead)
def get_task_by_id(task_id: str, current_user: dict = Depends(get_current_user_from_token)):
    user_id = current_user.get("sub")

    with Session(engine) as session:
        # Find the task and verify it belongs to the authenticated user
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or access denied"
            )

        return task

@router.post("/", response_model=TaskRead)
def create_task(task: TaskCreate, current_user: dict = Depends(get_current_user_from_token)):
    user_id = current_user.get("sub")

    with Session(engine) as session:
        # Create task with the authenticated user's ID
        task_dict = task.model_dump()
        task_dict['user_id'] = user_id
        db_task = Task(**task_dict)

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return db_task

@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: str, task_update: TaskUpdate, current_user: dict = Depends(get_current_user_from_token)):
    user_id = current_user.get("sub")

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
            if field != 'user_id':  # Prevent changing user_id
                setattr(db_task, field, value)

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return db_task

@router.delete("/{task_id}")
def delete_task(task_id: str, current_user: dict = Depends(get_current_user_from_token)):
    user_id = current_user.get("sub")

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

@router.patch("/{task_id}/complete")
def toggle_task_completion(task_id: str, current_user: dict = Depends(get_current_user_from_token)):
    user_id = current_user.get("sub")

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