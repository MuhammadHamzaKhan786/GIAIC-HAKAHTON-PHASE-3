from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING
import uuid


class MessageBase(SQLModel):
    role: str = Field(regex="^(user|assistant)$", nullable=False)  # Either 'user' or 'assistant'
    content: str = Field(min_length=1, max_length=10000, nullable=False)


class Message(MessageBase, table=True):
    __tablename__ = "src_message"  # Renamed to avoid conflict with backend/models/message.py
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="src_conversation.id", nullable=False)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")
    user: Optional["User"] = Relationship(back_populates="messages")


class MessageRead(MessageBase):
    id: uuid.UUID
    conversation_id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime


class MessageCreate(MessageBase):
    pass


class MessageUpdate(SQLModel):
    content: Optional[str] = Field(default=None, min_length=1, max_length=10000)