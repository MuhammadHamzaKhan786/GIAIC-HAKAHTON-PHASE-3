from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid


class ConversationBase(SQLModel):
    user_id: str = Field(index=True)


class Conversation(ConversationBase, table=True):
    """
    Represents a unique conversation thread between a user and the AI assistant.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationRead(ConversationBase):
    id: str
    created_at: datetime
    updated_at: datetime


class ConversationCreate(ConversationBase):
    pass