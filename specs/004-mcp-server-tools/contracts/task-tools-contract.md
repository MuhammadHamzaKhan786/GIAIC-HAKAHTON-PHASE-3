# MCP Tool Contracts: Task Management

## Overview

This document defines the contract for MCP tools that provide task management functionality to OpenAI Agents.

## add_task Tool

**Purpose**: Creates a new task for the authenticated user

**Request Schema**:
```json
{
  "type": "add_task",
  "input": {
    "type": "object",
    "properties": {
      "title": {
        "type": "string",
        "description": "Task title (required)",
        "minLength": 1,
        "maxLength": 255
      },
      "description": {
        "type": "string",
        "description": "Task description (optional)",
        "maxLength": 1000
      }
    },
    "required": ["title"]
  }
}
```

**Response Schema**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "description": "Unique identifier for the created task"
    },
    "title": {
      "type": "string",
      "description": "Task title"
    },
    "completed": {
      "type": "boolean",
      "description": "Whether the task is completed (default: false)"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "Timestamp of task creation"
    }
  },
  "required": ["task_id", "title", "completed", "created_at"]
}
```

**Error Responses**:
- `BAD_REQUEST`: Invalid input parameters
- `FORBIDDEN`: Unauthorized access
- `INTERNAL_ERROR`: Database or system error

---

## list_tasks Tool

**Purpose**: Fetches tasks for the authenticated user

**Request Schema**:
```json
{
  "type": "list_tasks",
  "input": {
    "type": "object",
    "properties": {
      "status": {
        "type": "string",
        "enum": ["all", "pending", "completed"],
        "default": "all",
        "description": "Filter by completion status (optional)"
      }
    }
  }
}
```

**Response Schema**:
```json
{
  "type": "object",
  "properties": {
    "tasks": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "type": "integer",
            "description": "Task identifier"
          },
          "title": {
            "type": "string",
            "description": "Task title"
          },
          "completed": {
            "type": "boolean",
            "description": "Whether the task is completed"
          }
        },
        "required": ["id", "title", "completed"]
      }
    }
  },
  "required": ["tasks"]
}
```

**Error Responses**:
- `FORBIDDEN`: Unauthorized access
- `INTERNAL_ERROR`: Database or system error

---

## complete_task Tool

**Purpose**: Marks a task as completed

**Request Schema**:
```json
{
  "type": "complete_task",
  "input": {
    "type": "object",
    "properties": {
      "task_id": {
        "type": "integer",
        "description": "ID of the task to complete"
      }
    },
    "required": ["task_id"]
  }
}
```

**Response Schema**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "description": "Task identifier"
    },
    "title": {
      "type": "string",
      "description": "Task title"
    },
    "completed": {
      "type": "boolean",
      "description": "Whether the task is completed (true)"
    }
  },
  "required": ["task_id", "title", "completed"]
}
```

**Error Responses**:
- `BAD_REQUEST`: Invalid task_id
- `NOT_FOUND`: Task not found
- `FORBIDDEN`: Unauthorized access (task doesn't belong to user)
- `INTERNAL_ERROR`: Database or system error

---

## update_task Tool

**Purpose**: Updates task properties

**Request Schema**:
```json
{
  "type": "update_task",
  "input": {
    "type": "object",
    "properties": {
      "task_id": {
        "type": "integer",
        "description": "ID of the task to update"
      },
      "title": {
        "type": "string",
        "description": "New task title (optional)",
        "minLength": 1,
        "maxLength": 255
      },
      "description": {
        "type": "string",
        "description": "New task description (optional)",
        "maxLength": 1000
      }
    },
    "required": ["task_id"]
  }
}
```

**Response Schema**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "description": "Task identifier"
    },
    "title": {
      "type": "string",
      "description": "Updated task title"
    },
    "completed": {
      "type": "boolean",
      "description": "Whether the task is completed"
    }
  },
  "required": ["task_id", "title", "completed"]
}
```

**Error Responses**:
- `BAD_REQUEST`: Invalid input parameters
- `NOT_FOUND`: Task not found
- `FORBIDDEN`: Unauthorized access (task doesn't belong to user)
- `INTERNAL_ERROR`: Database or system error

---

## delete_task Tool

**Purpose**: Deletes a task

**Request Schema**:
```json
{
  "type": "delete_task",
  "input": {
    "type": "object",
    "properties": {
      "task_id": {
        "type": "integer",
        "description": "ID of the task to delete"
      }
    },
    "required": ["task_id"]
  }
}
```

**Response Schema**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "description": "Task identifier that was deleted"
    },
    "status": {
      "type": "string",
      "description": "Deletion status"
    }
  },
  "required": ["task_id", "status"]
}
```

**Error Responses**:
- `BAD_REQUEST`: Invalid task_id
- `NOT_FOUND`: Task not found
- `FORBIDDEN`: Unauthorized access (task doesn't belong to user)
- `INTERNAL_ERROR`: Database or system error

---

## Authentication

All tools require a valid JWT token to be provided in the request header. The user_id is extracted from the JWT payload and used to enforce ownership validation. The system does not accept user_id as an input parameter to prevent spoofing.