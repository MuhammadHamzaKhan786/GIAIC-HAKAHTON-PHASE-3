# Data Model: Spec-2 — Secure Backend Task Management API

## Entity Definitions

### Task Entity
Represents a task owned by a specific user in the system.

**Fields:**
- `id`: UUID (Primary Key)
  - Purpose: Unique identifier for the task
  - Constraints: Auto-generated, immutable, indexed
- `user_id`: UUID (Foreign Key)
  - Purpose: Reference to the owning user (derived from JWT)
  - Constraints: Required, references user ID from JWT claims, indexed
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
- Many-to-One: Task → User (task belongs to one user via JWT claims)

**Validation Rules:**
- Task must belong to the authenticated user (verified via JWT)
- Title cannot be empty
- Title has maximum length constraint
- Only the owner (via JWT) can modify the task
- Completion status can only be changed by the owner (via JWT)

### User (Referenced from JWT)
Represents the authenticated user whose identity is derived from JWT claims.

**Fields (from JWT claims):**
- `id`: UUID (Subject claim - "sub")
  - Purpose: Unique identifier for the user
  - Constraints: Derived from JWT "sub" claim, immutable
- `email`: String (optional, from JWT)
  - Purpose: User's email address
  - Constraints: From JWT claims if available

**Validation Rules:**
- User must have a valid JWT token
- User identity is derived exclusively from verified JWT claims
- No trust of user_id from request body or URL parameters
- All operations are validated against the authenticated user's identity

## State Transitions

### Task States
- **Active**: New task created, `completed` = false
- **Completed**: Task marked as done, `completed` = true
- **Deleted**: Task removed from active list (deleted from database)

### Allowed Transitions
- Active → Completed: When user toggles completion status via PATCH /api/tasks/{id}/complete
- Active → Deleted: When user deletes task via DELETE /api/tasks/{id}
- Completed → Active: When user toggles completion status via PATCH /api/tasks/{id}/complete
- Completed → Deleted: When user deletes completed task via DELETE /api/tasks/{id}

## Indexes and Performance

### Required Indexes
1. `tasks.user_id` - For efficient user-specific task retrieval
2. `tasks.completed` - For filtering completed vs active tasks
3. `tasks.created_at` - For chronological sorting
4. `tasks.updated_at` - For tracking modification times

### Query Patterns
1. Retrieve all tasks for a specific user (authenticated via JWT)
2. Retrieve completed or active tasks for a specific user
3. Find specific task by ID and user ID (for updates/deletes)
4. Count tasks by completion status for a specific user

## Data Integrity Constraints

### Referential Integrity
- Tasks are associated with users via JWT claims verification
- No traditional foreign key constraint (user identity from JWT, not database user table)
- All operations must validate user ownership via JWT

### Business Rules Enforcement
- Users can only access their own tasks (verified via JWT)
- Task ownership cannot be transferred
- Users cannot modify tasks they don't own (verified via JWT)
- Duplicate tasks are allowed (same title for different users)

## Schema Evolution Considerations

### Future Extensibility
- Additional task properties (priority, due date, category) can be added
- Task sharing functionality could be introduced (with proper authorization)
- Task comments or attachments could be added
- Subtasks or hierarchical structures could be implemented

### Migration Strategy
- Use SQLModel's migration capabilities
- Plan backward compatibility for API consumers
- Maintain data during schema evolution
- Test migrations on copy of production data

## Security Considerations

### Data Isolation
- User data isolation enforced at the application level
- All queries must filter by user_id derived from JWT
- Cross-user access prevented by design
- No direct access to other users' data possible

### Access Control
- Authentication required for all operations
- Authorization validated on every request
- User identity derived exclusively from JWT claims
- No bypass of authentication/authorization checks