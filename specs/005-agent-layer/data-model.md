# Data Model: Agent Layer & Conversational Memory

## Entities

### Conversation
Represents a unique conversation thread between a user and the AI assistant.

**Fields**:
- `id`: UUID (primary key) - Unique identifier for the conversation
- `user_id`: UUID (foreign key) - Links conversation to authenticated user
- `created_at`: DateTime (timestamp) - When conversation was initiated
- `updated_at`: DateTime (timestamp) - Last activity in conversation

**Relationships**:
- One Conversation → Many Messages (one-to-many)
- One User → Many Conversations (one-to-many)

**Validation**:
- `user_id` must exist in users table (foreign key constraint)
- `created_at` set automatically on creation
- `updated_at` updated automatically on modification

### Message
Represents an individual message in a conversation thread.

**Fields**:
- `id`: UUID (primary key) - Unique identifier for the message
- `conversation_id`: UUID (foreign key) - Links message to conversation
- `user_id`: UUID (foreign key) - Links message to user who sent it
- `role`: String (enum: "user", "assistant", "system") - Who sent the message
- `content`: Text - The actual message content
- `created_at`: DateTime (timestamp) - When message was created

**Relationships**:
- Many Messages → One Conversation (many-to-one)
- Many Messages → One User (many-to-one)

**Validation**:
- `conversation_id` must exist in conversations table
- `user_id` must exist in users table
- `role` must be one of "user", "assistant", or "system"
- `content` cannot be empty
- `created_at` set automatically on creation

## Entity States

### Conversation States
- Active: New messages can be added
- Archived: Read-only, no new messages allowed (future extension)

### Message States
- Stored: Message has been saved to database
- Transient: Message exists in agent memory but not yet persisted (rare, should be stored immediately)

## Relationships & Constraints

### Ownership Validation
- All operations must verify that requesting user owns the conversation
- Message.user_id must match the authenticated user for "user" role messages
- Access to conversation history restricted to owning user

### Indexes
- Conversation: Index on (user_id, created_at) for efficient user conversation lookup
- Message: Index on (conversation_id, created_at) for chronological message retrieval
- Message: Index on (user_id, conversation_id) for user message validation

## Data Lifecycle

### Creation
1. When conversation_id is not provided in API request → new Conversation created
2. User message received → Message created with role="user"
3. Agent response generated → Message created with role="assistant"

### Retrieval
1. Messages for conversation retrieved in chronological order (created_at ASC)
2. Conversation history reconstructed from Message records

### Updates
- Conversation.updated_at updated when new messages are added
- No direct updates to Message records (append-only pattern)

### Deletion
- Future extension: Ability to delete conversations (and associated messages)
- Soft delete pattern preferred to maintain audit trail