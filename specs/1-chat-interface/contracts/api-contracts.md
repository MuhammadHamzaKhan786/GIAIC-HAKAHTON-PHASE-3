# API Contracts: AI Todo Chatbot (Spec 1: Chat Interface & Stateless Messaging)

**Feature**: 1-chat-interface
**Date**: 2026-02-04
**Version**: 1.0

## Overview
This document defines the API contracts for the conversational AI system, specifying the interfaces between frontend and backend components. These contracts extend the existing API architecture while ensuring consistent communication patterns and supporting the stateless design requirement.

## Authentication Contract

### JWT Token Format
Consistent with existing authentication system in `backend/src/auth/auth_bearer.py`
```
Header: Authorization: Bearer {jwt_token}
```

### Token Claims Expected (consistent with existing system)
- `user_id`: UUID string identifying the authenticated user (same format as existing User model)
- `exp`: Expiration timestamp (Unix epoch)
- `iat`: Issued at timestamp (Unix epoch)
- `sub`: Subject identifier (same as user_id)

### Authentication Response Codes (consistent with existing patterns)
- `200 OK`: Valid token, request processed
- `401 Unauthorized`: Invalid, expired, or missing token
- `403 Forbidden`: Token valid but insufficient permissions

## Extended API Contract

### Chat Endpoint (extends existing API router)
The chat functionality extends the existing API structure in `backend/src/api/router.py`

#### Endpoint: POST /api/{user_id}/chat

##### Request
**Method**: `POST`
**Path**: `/api/{user_id}/chat`
**Headers**:
```
Authorization: Bearer {jwt_token} (using existing auth middleware)
Content-Type: application/json
```

**Path Parameter**:
- `user_id` (string, required): UUID of the authenticated user (must match JWT claim, consistent with existing patterns)

**Body Parameters**:
```json
{
  "message": "string, required: the user's message content",
  "conversation_id": "string, optional: UUID of existing conversation"
}
```

##### Response
**Success Response (200 OK)**:
```json
{
  "response": "string: assistant's response to the user's message",
  "conversation_id": "string: UUID of the conversation (existing or newly created)",
  "timestamp": "string: ISO 8601 timestamp of response",
  "tool_calls": "array: list of MCP tools called during response (if applicable)"
}
```

**Error Responses** (consistent with existing patterns in `backend/src/api/router.py`):
- `400 Bad Request`:
```json
{
  "error": "string: reason for bad request",
  "code": "string: error code"
}
```
- `401 Unauthorized`:
```json
{
  "error": "Invalid or expired authentication token",
  "code": "UNAUTHORIZED"
}
```
- `403 Forbidden`:
```json
{
  "error": "Access denied to this conversation",
  "code": "FORBIDDEN_ACCESS"
}
```
- `404 Not Found`:
```json
{
  "error": "Conversation not found",
  "code": "CONVERSATION_NOT_FOUND"
}
```
- `422 Unprocessable Entity`:
```json
{
  "error": "Validation error in request body",
  "code": "VALIDATION_ERROR"
}
```
- `500 Internal Server Error`:
```json
{
  "error": "An unexpected error occurred",
  "code": "INTERNAL_ERROR"
}
```

#### Example Request/Response
**Request**:
```
POST /api/123e4567-e89b-12d3-a456-426614174000/chat
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (consistent with existing auth)
Content-Type: application/json

{
  "message": "What are my tasks for today?",
  "conversation_id": "abc123ef-456g-789h-123j-456k789l0123"
}
```

**Response**:
```
200 OK
Content-Type: application/json

{
  "response": "You have 3 tasks scheduled for today: Buy groceries, Call dentist, Team meeting at 2 PM",
  "conversation_id": "abc123ef-456g-789h-123j-456k789l0123",
  "timestamp": "2026-02-04T10:30:45.123Z",
  "tool_calls": [
    {
      "name": "list_tasks",
      "arguments": {
        "date": "2026-02-04"
      }
    }
  ]
}
```

## Conversation Management Contracts

### Create New Conversation (Implicit)
The system creates a new conversation automatically when:
- A request includes no conversation_id
- A request references a non-existent conversation_id
- A user initiates a "New Conversation" action via frontend

### Get Conversation History (consistent with existing patterns)
**Endpoint**: `GET /api/{user_id}/conversations/{conversation_id}/messages`

**Response** (200 OK):
```json
{
  "conversation_id": "string: UUID of the conversation",
  "messages": [
    {
      "id": "string: message UUID",
      "role": "string: 'user' or 'assistant'",
      "content": "string: message content",
      "created_at": "string: ISO 8601 timestamp"
    }
  ],
  "total_count": "number: total messages in conversation"
}
```

## Data Contracts (consistent with existing SQLModel patterns)

### Conversation Object
Following the same patterns as existing models in `backend/src/models/`:
```json
{
  "id": "string: UUID of the conversation",
  "user_id": "string: UUID of the owning user (consistent with existing User model)",
  "created_at": "string: ISO 8601 timestamp of creation",
  "updated_at": "string: ISO 8601 timestamp of last update"
}
```

### Message Object
Following the same patterns as existing models in `backend/src/models/`:
```json
{
  "id": "string: UUID of the message",
  "user_id": "string: UUID of the message author (consistent with existing patterns)",
  "conversation_id": "string: UUID of parent conversation",
  "role": "string: 'user' or 'assistant'",
  "content": "string: message text content",
  "created_at": "string: ISO 8601 timestamp of creation"
}
```

## Error Contract Patterns (consistent with existing patterns)

### Standard Error Response Format
Following the same patterns as existing API endpoints in `backend/src/api/router.py`:
```json
{
  "error": "Human-readable error message",
  "code": "MACHINE_READABLE_ERROR_CODE",
  "timestamp": "ISO 8601 timestamp",
  "request_id": "Unique identifier for the request (for debugging)"
}
```

### Common Error Codes (consistent with existing system)
- `UNAUTHORIZED`: Authentication token invalid or missing
- `FORBIDDEN_ACCESS`: User attempting to access another user's data
- `CONVERSATION_NOT_FOUND`: Referenced conversation doesn't exist
- `MESSAGE_TOO_LONG`: Message exceeds maximum allowed length
- `VALIDATION_ERROR`: Request body doesn't match expected schema
- `AGENT_TIMEOUT`: AI agent didn't respond within allowed time
- `DATABASE_ERROR`: Database operation failed
- `INTERNAL_ERROR`: Unexpected error occurred

## Security Requirements (consistent with existing patterns)

### Input Validation
- All string inputs must be sanitized against injection attacks
- UUIDs must be properly formatted (consistent with existing validation)
- Message content length limited to 4000 characters
- All inputs validated against expected schema (using existing Pydantic patterns)

### Access Controls
- User ID in JWT must match the user_id in the path parameter (consistent with existing patterns in task endpoints)
- Conversation ownership verified for all operations using existing validation
- No access to other users' conversations or messages (following existing access patterns)

### Privacy (consistent with existing patterns)
- Message content treated as private user data
- No message content exposed in error messages
- All logs exclude sensitive message content (consistent with existing logging)

## Performance Requirements (maintaining consistency with existing app)

### Response Times
- Chat endpoint: < 5 seconds for 95% of requests
- Conversation history: < 2 seconds for 95% of requests
- New conversation creation: < 1 second
- Consistent with existing API performance expectations

### Concurrent Users
- System supports at least 100 concurrent chat sessions
- No degradation in response times up to capacity limits
- Shares connection pool with existing database operations

## Versioning Policy
- API version indicated in Accept header if needed
- Breaking changes require new endpoint version
- Backwards compatibility maintained for 90 days after announcement
- Follows same versioning patterns as existing API