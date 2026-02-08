# Chat API Documentation

## Endpoint: POST /api/{user_id}/chat

### Description
The main chat endpoint that handles conversation between authenticated users and the AI assistant. The system maintains stateless operations by loading full conversation history from the database for each request and saving both user and assistant messages to persistent storage.

### Authentication
- **Required**: JWT Bearer token in Authorization header
- **Header**: `Authorization: Bearer <token>`
- **Verification**: Token is validated and user_id in token must match the path parameter

### Parameters

#### Path Parameters
- **user_id** (string, required): The UUID of the authenticated user making the request

#### Request Body
- **message** (string, required): The message content from the user (min length: 1, max length: 10000)
- **conversation_id** (string, optional): The UUID of an existing conversation; if not provided, a new conversation will be created

### Request Examples

```json
{
  "message": "Hello, how can you help me with my tasks?",
  "conversation_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
}
```

Or without conversation_id to start a new conversation:

```json
{
  "message": "Hello, how can you help me with my tasks?"
}
```

### Response

#### Success Response (200 OK)
```json
{
  "conversation_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "response": "Hello! I can help you manage your tasks. You can ask me to create, update, or list your tasks."
}
```

#### Error Responses

**400 Bad Request** - When message is empty or invalid
```json
{
  "detail": "Message cannot be empty"
}
```

**401 Unauthorized** - When authentication is missing or invalid
```json
{
  "detail": "Not authenticated"
}
```

Or when user ID in token doesn't match the path parameter:
```json
{
  "detail": "Invalid user ID in token"
}
```

**404 Not Found** - When conversation is not found for the user (though this shouldn't happen with the current implementation as it creates a new conversation)

**500 Internal Server Error** - For server-side errors
```json
{
  "detail": "An unexpected error occurred"
}
```

### Implementation Details

1. **Authentication Verification**: The endpoint extracts the user_id from the JWT token and verifies it matches the path parameter to prevent unauthorized access.

2. **Conversation Management**:
   - If conversation_id is provided, the system attempts to load an existing conversation for the user
   - If no valid conversation is found, a new conversation is automatically created

3. **Message Persistence**: Both user and assistant messages are saved to the database with proper ownership.

4. **Stateless Operation**: Each request loads the full conversation history from the database to provide context to the AI agent.

5. **Response Generation**: The system generates an AI response (currently using a placeholder) and saves it to the database.

### Security Considerations

- All operations are scoped to the authenticated user's data
- Conversation and message tables enforce foreign key relationships to user_id
- JWT tokens are validated for authenticity and expiration
- User ID in token is verified against the path parameter to prevent IDOR attacks

### Rate Limiting

This endpoint does not include rate limiting by default. Consider implementing rate limiting in production deployments to prevent abuse.