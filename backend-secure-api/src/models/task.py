from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=500)
    completed: bool = False

class Task(TaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(nullable=False)  # Derived from JWT claims
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskRead(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    completed: Optional[bool] = None