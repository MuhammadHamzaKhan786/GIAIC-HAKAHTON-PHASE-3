# Data Model: MCP Server & Task Tooling

## Primary Entity: Task

**Description**: Represents a user's task item that can be managed through MCP tools

**Fields**:
- `id`: int (primary key, auto-generated)
- `user_id`: str (foreign key reference to user, indexed for performance)
- `title`: str (required, max 255 characters)
- `description`: str | None (optional, can be null, max 1000 characters)
- `completed`: bool (default False)
- `created_at`: datetime (auto-set on creation)
- `updated_at`: datetime (auto-updated on modification)

**Relationships**:
- Belongs to one user (via user_id foreign key)
- No direct relationships to other entities (standalone)

**Validation Rules**:
- `title` must be between 1 and 255 characters
- `description` can be null or between 1 and 1000 characters
- `completed` defaults to False when creating new tasks
- `user_id` must be a valid user identifier from authentication system
- `created_at` and `updated_at` are automatically managed by the system

**State Transitions**:
- New Task: `completed` = False
- Complete Task: `completed` = True
- Update Task: `updated_at` gets updated to current timestamp

## Secondary Entity: User Session (Implicit)

**Description**: Represents the authenticated user context derived from JWT token (not stored in database)

**Fields**:
- `user_id`: str (extracted from JWT payload)
- `expires_at`: datetime (token expiration time)
- `permissions`: List[str] (user permissions if needed)

**Note**: This is not a database entity but rather an authentication concept used to validate user ownership of tasks.

## Constraints

1. **Ownership Constraint**: All operations must be scoped to the authenticated user's tasks
2. **Timestamp Constraints**: `created_at` must be before or equal to `updated_at`
3. **Indexing**: `user_id` field should be indexed for efficient querying by user
4. **Nullability**: Only `description` field allows NULL values

## Access Patterns

1. **By User**: Query tasks for a specific user (filtered by user_id)
2. **By Completion Status**: Query pending or completed tasks
3. **By User and Status**: Combined filter for user and completion status
4. **Individual Task**: Query specific task by ID with user validation

## Index Recommendations

- Composite index on (user_id, completed) for efficient filtering
- Individual index on user_id for user-specific queries
- Individual index on completed for status-based queries