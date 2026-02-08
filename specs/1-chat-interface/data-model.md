# Data Model: AI Todo Chatbot (Spec 1: Chat Interface & Stateless Messaging)

**Feature**: 1-chat-interface
**Date**: 2026-02-04
**Modeler**: Claude Code

## Overview
This document defines the data models for the conversational AI system, focusing on conversation and message persistence in Neon PostgreSQL. The models extend the existing architecture with User and Task models, maintaining consistency with the existing SQLModel patterns and authentication system.

## Entity Relationship Diagram

```
         User (existing)
            ▲
            │ user_id
            │
Conversation (new)      Message (new)
┌─────────────────┐    ┌─────────────────────────┐
│ id (UUID)       │    │ id (UUID)               │
│ user_id (UUID)  │◄───┤ user_id (UUID)          │
│ created_at      │    │ conversation_id (UUID)  │◄──┐
│ updated_at      │    │ role (String)           │   │
└─────────────────┘    │ content (Text)          │   │
                       │ created_at (DateTime)   │   │
                       └─────────────────────────┘   │
                                                    │
┌────────────────────────────────────────────────────┘
       Task (existing)
```

## Database Schema Integration

### Conversation Table
Extends the existing database schema to store top-level conversation containers, each associated with a single user using the existing user_id pattern.

**Table Name**: `conversations`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the conversation |
| user_id | UUID | NOT NULL, INDEX | Foreign key linking to authenticated user (consistent with existing User model) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Timestamp when conversation was created |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Timestamp when conversation was last updated |

**Indexes**:
- Primary key index on `id`
- Index on `user_id` for efficient user-based queries (consistent with existing patterns)
- Composite index on `(user_id, created_at)` for chronological ordering

**Relationships**:
- One-to-many with Message table via `conversation_id` foreign key
- Many-to-one with existing User table via `user_id` foreign key (following existing patterns from Task model)

### Message Table
Extends the existing database schema to store individual messages within conversations, differentiating between user and assistant roles.

**Table Name**: `messages`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the message |
| user_id | UUID | NOT NULL, INDEX | Foreign key linking to authenticated user (consistent with existing patterns) |
| conversation_id | UUID | NOT NULL, INDEX, FOREIGN KEY | Links message to its conversation |
| role | VARCHAR(20) | NOT NULL, CHECK | Role of the message sender ('user' or 'assistant') |
| content | TEXT | NOT NULL | The actual message content |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Timestamp when message was created |

**Indexes**:
- Primary key index on `id`
- Index on `conversation_id` for efficient conversation retrieval
- Index on `created_at` for chronological ordering
- Composite index on `(conversation_id, created_at)` for ordered message retrieval
- Index on `user_id` for consistency with existing patterns

**Foreign Keys**:
- `conversation_id` references `conversations.id`
- `user_id` follows the same pattern as existing User relationship (similar to Task.user_id)

**Constraints**:
- Check constraint on `role` field to ensure only 'user' or 'assistant' values
- Cascade delete on `conversation_id` to remove all messages when conversation deleted (following existing cascade patterns)

## SQLModel Class Extensions

### Conversation Model
Consistent with existing SQLModel patterns in backend/src/models/

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
import sqlalchemy.dialects.postgresql as pg

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(
        sa_column=pg.UUID(as_uuid=True),
        default_factory=uuid4,
        primary_key=True
    )
    user_id: UUID = Field(
        sa_column=pg.UUID(as_uuid=True),
        nullable=False,
        index=True
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )

    # Relationship to messages following existing patterns
    messages: list["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
```

### Message Model
Consistent with existing SQLModel patterns in backend/src/models/

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
import sqlalchemy.dialects.postgresql as pg
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: UUID = Field(
        sa_column=pg.UUID(as_uuid=True),
        default_factory=uuid4,
        primary_key=True
    )
    user_id: UUID = Field(
        sa_column=pg.UUID(as_uuid=True),
        nullable=False,
        index=True
    )
    conversation_id: UUID = Field(
        sa_column=pg.UUID(as_uuid=True),
        foreign_key="conversations.id",
        nullable=False,
        index=True
    )
    role: MessageRole = Field(
        sa_column=pg.VARCHAR(20),
        nullable=False,
        description="Role of the message sender"
    )
    content: str = Field(
        sa_column=pg.TEXT,
        nullable=False
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )

    # Relationship to conversation following existing patterns
    conversation: "Conversation" = Relationship(
        back_populates="messages"
    )
```

## API Contract Integration

### Send Message Request (extends existing API structure)
```
POST /api/{user_id}/chat
Headers: Authorization: Bearer {jwt_token} (consistent with existing auth)
Body: {
  "message": "Hello, assistant!",
  "conversation_id": "optional_conversation_uuid"
}
Response: 200 OK
Body: {
  "response": "Hello! How can I help you?",
  "conversation_id": "uuid"
}
```

### Get Conversation History Request (follows existing patterns)
```
GET /api/{user_id}/conversations/{conversation_id}/messages
Headers: Authorization: Bearer {jwt_token} (consistent with existing auth)
Response: 200 OK
Body: [
  {
    "id": "message_uuid",
    "role": "user",
    "content": "Hello, assistant!",
    "created_at": "2026-02-04T10:00:00Z"
  },
  {
    "id": "message_uuid",
    "role": "assistant",
    "content": "Hello! How can I help you?",
    "created_at": "2026-02-04T10:00:05Z"
  }
]
```

## Business Rules Integration

### Conversation Management (consistent with existing patterns)
- Each conversation belongs to exactly one user following existing ownership patterns
- Users can create multiple conversations
- Conversation creation timestamp reflects when first message is sent
- Last updated timestamp updates with each new message
- Uses same user_id validation as existing Task model

### Message Management (consistent with existing patterns)
- Each message belongs to exactly one conversation
- Messages must have a role of either 'user' or 'assistant'
- Message content cannot be empty
- Messages are ordered chronologically by creation time
- Assistant messages are automatically created by the system
- Uses same session patterns as existing database operations

### Data Integrity (consistent with existing patterns)
- All foreign key relationships are enforced by the database
- Conversation and message IDs use UUIDs to ensure global uniqueness
- User ownership is validated on all read/write operations using existing patterns
- Cascading deletes ensure data consistency following existing patterns

### Access Control (consistent with existing patterns)
- Users can only access their own conversations and messages using existing validation
- Authentication is required for all operations using existing middleware
- Invalid user_id/token combinations return 401 Unauthorized using existing patterns
- Cross-user access attempts are prevented by database constraints and existing validation

## Performance Considerations

### Indexing Strategy (consistent with existing patterns)
- Index on user_id enables efficient user-based queries using existing patterns
- Composite index on (conversation_id, created_at) optimizes message retrieval
- Additional indexes can be added based on query patterns

### Data Size Limits (consistent with existing patterns)
- Message content stored as TEXT (no practical size limit in PostgreSQL)
- Consider implementing application-level size limits for performance
- Large conversation histories may require pagination in future

### Query Optimization (consistent with existing patterns)
- Use JOIN queries to efficiently retrieve conversation history following existing patterns
- Leverage existing database session management from other models
- Connection pooling shares resources with existing models

## Migration Scripts

### Create Tables (extends existing database)
```sql
-- Create conversations table
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),  -- Assuming existing users table
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create indexes following existing patterns
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_created_at ON conversations(created_at);
CREATE INDEX idx_conversations_user_created ON conversations(user_id, created_at);

-- Create messages table
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create indexes following existing patterns
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_messages_conv_created ON messages(conversation_id, created_at);
CREATE INDEX idx_messages_user_id ON messages(user_id);
```

## Integration with Existing Models

The new Conversation and Message models follow the same patterns as the existing Task and User models in backend/src/models/:

- Same import structure and field definitions
- Consistent use of UUID primary keys
- Similar relationship patterns
- Matching session management in API endpoints
- Consistent authentication and authorization patterns
- Following the same database transaction patterns