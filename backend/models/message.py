from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid
from typing import Optional


class MessageBase(SQLModel):
    conversation_id: str = Field(index=True)
    user_id: str = Field(index=True)
    role: str = Field(regex="^(user|assistant|system)$")  # Role must be user, assistant, or system
    content: str = Field(min_length=1)  # Content cannot be empty


class Message(MessageBase, table=True):
    """
    Represents an individual message in a conversation thread.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    conversation_id: str = Field(index=True, foreign_key="conversation.id")
    user_id: str = Field(index=True)
    role: str = Field(regex="^(user|assistant|system)$")
    content: str = Field(sa_column_kwargs={"nullable": False})
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MessageRead(MessageBase):
    id: str
    created_at: datetime


class MessageCreate(MessageBase):
    pass