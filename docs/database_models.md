# Database Models Documentation

## Overview

The application uses SQLModel for database modeling with Neon PostgreSQL as the database backend. The system includes four main models: User, Task, Conversation, and Message, with proper relationships and foreign key constraints.

## Models

### User Model

Represents the authenticated user in the system.

#### Fields
- **id** (UUID, Primary Key): Unique identifier for the user
- **email** (String, unique, not null): User's email address
- **password_hash** (String, not null): BCrypt hash of the user's password
- **created_at** (DateTime, not null): Timestamp when the user was created
- **updated_at** (DateTime, not null): Timestamp when the user was last updated

#### Relationships
- `tasks`: List of Task objects (one-to-many)
- `conversations`: List of Conversation objects (one-to-many)
- `messages`: List of Message objects (one-to-many)

#### Constraints
- Email must be unique across all users

### Task Model

Represents individual tasks owned by users.

#### Fields
- **id** (UUID, Primary Key): Unique identifier for the task
- **title** (String, 1-500 characters, not null): Task title/description
- **completed** (Boolean, default: false): Whether the task is completed
- **user_id** (UUID, Foreign Key to user.id, not null): Owner of the task
- **created_at** (DateTime, not null): Timestamp when the task was created
- **updated_at** (DateTime, not null): Timestamp when the task was last updated

#### Relationships
- `user`: Reference to the owning User object (many-to-one)

#### Constraints
- Title must be 1-500 characters
- User ID must reference a valid user

### Conversation Model

Represents a conversation thread between a user and the AI assistant.

#### Fields
- **id** (UUID, Primary Key): Unique identifier for the conversation
- **title** (String, 0-200 characters, default: "New Conversation"): Conversation title
- **user_id** (UUID, Foreign Key to user.id, not null): Owner of the conversation
- **created_at** (DateTime, not null): Timestamp when the conversation was started
- **updated_at** (DateTime, not null): Timestamp when the conversation was last updated

#### Relationships
- `user`: Reference to the owning User object (many-to-one)
- `messages`: List of Message objects in this conversation (one-to-many)

#### Constraints
- User ID must reference a valid user

### Message Model

Represents individual messages within a conversation.

#### Fields
- **id** (UUID, Primary Key): Unique identifier for the message
- **role** (String, regex: "^(user|assistant)$", not null): Who sent the message ("user" or "assistant")
- **content** (String, 1-10000 characters, not null): The message content
- **conversation_id** (UUID, Foreign Key to conversation.id, not null): Which conversation this message belongs to
- **user_id** (UUID, Foreign Key to user.id, not null): User who owns this message
- **created_at** (DateTime, not null): Timestamp when the message was sent

#### Relationships
- `conversation`: Reference to the Conversation object (many-to-one)
- `user`: Reference to the owning User object (many-to-one)

#### Constraints
- Role must be either "user" or "assistant"
- Content must be 1-10000 characters
- Conversation ID must reference a valid conversation
- User ID must reference a valid user

## Relationships

### User Relationships
- **One-to-Many**: A User can have multiple Tasks, Conversations, and Messages
- Foreign Key: `user_id` in Task, Conversation, and Message tables

### Conversation Relationships
- **One-to-Many**: A Conversation can have multiple Messages
- **Many-to-One**: A Conversation belongs to one User
- Foreign Keys: `conversation_id` in Message table, `user_id` in Conversation table

### Message Relationships
- **Many-to-One**: A Message belongs to one Conversation and one User
- Foreign Keys: `conversation_id` and `user_id` in Message table

## Security Considerations

All database operations enforce user isolation through foreign key constraints and user ID verification:

1. **Row-Level Security**: Users can only access their own data
   - Tasks are filtered by `user_id`
   - Conversations are filtered by `user_id`
   - Messages are filtered by `user_id`

2. **Foreign Key Integrity**: Database constraints prevent orphaned records
   - All Tasks must belong to a valid User
   - All Conversations must belong to a valid User
   - All Messages must belong to a valid Conversation and User

3. **Ownership Verification**: API endpoints verify user ownership before allowing operations
   - Each request validates that the authenticated user matches the resource owner
   - Cross-user access is prevented through both database constraints and application logic

## Indexes

Automatic indexes are created for:
- Primary key fields (id)
- Foreign key fields (user_id, conversation_id)
- Unique constraints (email in User table)

Additional indexes may be added based on query patterns for performance optimization.

## Migrations

Database schema changes are managed through Alembic migrations:
- Initial schema includes all four models
- Migrations ensure backward compatibility
- Database connections use proper connection pooling