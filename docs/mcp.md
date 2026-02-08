# MCP Task Server Documentation

## Overview

The MCP Task Server provides a standardized interface for managing tasks through Model Context Protocol (MCP) tools. This server enables AI agents to perform task operations (create, read, update, delete, complete) through well-defined tools.

## Architecture

The server follows the Agent-First Architecture pattern:
- Frontend → FastAPI → Agent → MCP → Database
- All operations are mediated by AI agents through MCP tools
- Stateless backend design with no in-memory session storage
- JWT-based authentication and user isolation

## Available Tools

### add_task
Creates a new task for the authenticated user.

**Input Schema**:
```json
{
  "title": "string (required, min 1 char, max 255 chars)",
  "description": "string (optional, max 1000 chars)"
}
```

**Output Schema**:
```json
{
  "task_id": "integer",
  "title": "string",
  "completed": "boolean",
  "created_at": "ISO 8601 datetime string"
}
```

**Example Call**:
```json
{
  "tool": "add_task",
  "params": {
    "title": "Buy groceries",
    "description": "Milk, bread, eggs"
  }
}
```

### list_tasks
Fetches tasks for the authenticated user.

**Input Schema**:
```json
{
  "status": "'all' | 'pending' | 'completed' (optional, default: 'all')"
}
```

**Output Schema**:
```json
{
  "tasks": [
    {
      "id": "integer",
      "title": "string",
      "completed": "boolean"
    }
  ]
}
```

**Example Call**:
```json
{
  "tool": "list_tasks",
  "params": {
    "status": "pending"
  }
}
```

### complete_task
Marks a task as completed.

**Input Schema**:
```json
{
  "task_id": "integer (required)"
}
```

**Output Schema**:
```json
{
  "task_id": "integer",
  "title": "string",
  "completed": "boolean"
}
```

**Example Call**:
```json
{
  "tool": "complete_task",
  "params": {
    "task_id": 123
  }
}
```

### update_task
Updates task properties.

**Input Schema**:
```json
{
  "task_id": "integer (required)",
  "title": "string (optional)",
  "description": "string (optional)"
}
```

**Output Schema**:
```json
{
  "task_id": "integer",
  "title": "string",
  "completed": "boolean"
}
```

**Example Call**:
```json
{
  "tool": "update_task",
  "params": {
    "task_id": 123,
    "title": "Updated task title"
  }
}
```

### delete_task
Deletes a task.

**Input Schema**:
```json
{
  "task_id": "integer (required)"
}
```

**Output Schema**:
```json
{
  "task_id": "integer",
  "status": "string"
}
```

**Example Call**:
```json
{
  "tool": "delete_task",
  "params": {
    "task_id": 123
  }
}
```

## Error Handling

The server returns standardized error responses:

- `NOT_FOUND`: Resource not found (e.g., task doesn't exist)
- `BAD_REQUEST`: Invalid input parameters
- `FORBIDDEN`: Unauthorized access (e.g., accessing another user's task)
- `INTERNAL_ERROR`: Server-side error

## Environment Configuration

Create a `.env` file with the following variables:

```env
# Database configuration
DATABASE_URL=postgresql://username:password@localhost:5432/task_db

# JWT configuration
JWT_SECRET_KEY=your-super-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Mock user ID for development (remove in production)
MOCK_USER_ID=development_user
```

## Authentication

The server extracts user identity from JWT tokens passed in the Authorization header. All operations are scoped to the authenticated user's tasks to prevent unauthorized access.

## Running the Server

1. Install dependencies:
   ```bash
   pip install mcp fastapi sqlmodel asyncpg python-dotenv uvicorn python-jose[cryptography] passlib[bcrypt]
   ```

2. Set up environment variables (see Environment Configuration above)

3. Start the server:
   ```bash
   cd backend/mcp
   uvicorn main:app --reload --port 8000
   ```

The server will be available at `http://localhost:8000`.