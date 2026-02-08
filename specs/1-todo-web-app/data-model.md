# Data Model: Todo Full-Stack Web Application (Hackathon Phase-2)

## Entity Definitions

### User Entity
Represents a registered user in the system with authentication capabilities.

**Fields:**
- `id`: UUID (Primary Key)
  - Purpose: Unique identifier for the user
  - Constraints: Auto-generated, immutable, indexed
- `email`: String (Unique, Indexed)
  - Purpose: User's email address for login
  - Constraints: Valid email format, unique, required
- `password_hash`: String
  - Purpose: BCrypt or similar hash of user's password
  - Constraints: Required, stored securely, never plaintext
- `created_at`: DateTime
  - Purpose: Timestamp when user account was created
  - Constraints: Auto-populated, immutable
- `updated_at`: DateTime
  - Purpose: Timestamp when user record was last updated
  - Constraints: Auto-updated on modification

**Relationships:**
- One-to-Many: User → Tasks (user owns multiple tasks)

**Validation Rules:**
- Email must be unique across all users
- Email must conform to standard email format
- Password must meet security requirements (length, complexity)
- All timestamps are stored in UTC

### Task Entity
Represents a todo item owned by a specific user.

**Fields:**
- `id`: UUID (Primary Key)
  - Purpose: Unique identifier for the task
  - Constraints: Auto-generated, immutable, indexed
- `user_id`: UUID (Foreign Key)
  - Purpose: Reference to the owning user
  - Constraints: Required, references User.id, indexed
- `title`: String
  - Purpose: Content/description of the task
  - Constraints: Required, max length 500 characters
- `completed`: Boolean
  - Purpose: Completion status of the task
  - Constraints: Default false, required
- `created_at`: DateTime
  - Purpose: Timestamp when task was created
  - Constraints: Auto-populated, immutable
- `updated_at`: DateTime
  - Purpose: Timestamp when task was last updated
  - Constraints: Auto-updated on modification

**Relationships:**
- Many-to-One: Task → User (task belongs to one user)

**Validation Rules:**
- Task must belong to an existing user
- Title cannot be empty
- Title has maximum length constraint
- Only the owner can modify the task
- Completion status can only be changed by the owner

## State Transitions

### Task States
- **Active**: New task created, `completed` = false
- **Completed**: Task marked as done, `completed` = true
- **Deleted**: Task removed from active list (soft delete)

### Allowed Transitions
- Active → Completed: When user marks task as complete
- Active → Deleted: When user deletes task
- Completed → Active: When user unmarks task as complete
- Completed → Deleted: When user deletes completed task

## Indexes and Performance

### Required Indexes
1. `users.email` - For efficient user lookup during authentication
2. `users.created_at` - For time-based queries
3. `tasks.user_id` - For efficient user-specific task retrieval
4. `tasks.completed` - For filtering completed vs active tasks
5. `tasks.created_at` - For chronological sorting

### Query Patterns
1. Retrieve all tasks for a specific user
2. Retrieve completed or active tasks for a specific user
3. Find specific task by ID and user ID (for updates/deletes)
4. Count tasks by completion status for a specific user

## Data Integrity Constraints

### Referential Integrity
- Foreign key constraint ensures tasks reference valid users
- Cascade delete behavior: deleting a user removes all their tasks

### Business Rules Enforcement
- Users can only access their own tasks
- Task ownership cannot be transferred
- Users cannot modify tasks they don't own
- Duplicate email addresses are not allowed

## Schema Evolution Considerations

### Future Extensibility
- Additional user properties (profile picture, preferences) can be added
- Task categorization could be added via tags or categories
- Task priority levels could be introduced
- Due dates could be added to tasks

### Migration Strategy
- Use SQLModel's migration capabilities
- Plan backward compatibility for API consumers
- Maintain data during schema evolution
- Test migrations on copy of production data