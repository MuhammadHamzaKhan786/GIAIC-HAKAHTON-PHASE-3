# Quickstart: Agent Layer & Conversational Memory

## Overview
Quick validation steps to verify the Agent Layer & Conversational Memory feature works as expected.

## Prerequisites
- Running MCP server with task management tools
- OpenAI API key configured
- Better Auth integration active
- Neon PostgreSQL connection available

## Step-by-Step Validation

### 1. Environment Setup
```bash
# Ensure MCP server is running
# Verify OPENAI_API_KEY is set in environment
# Confirm database connection works
# Check Better Auth JWT validation
```

### 2. Basic Conversation Flow
```bash
# Start a new conversation
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hi, I want to add a task to buy groceries"}'

# Expected response: New conversation created, task added, confirmation returned
```

### 3. Conversation Persistence
```bash
# Resume same conversation with task listing
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": "PREVIOUS_CONVERSATION_ID", "message": "What tasks do I have?"}'

# Expected response: Same conversation context, lists previously added task
```

### 4. Tool Integration
```bash
# Test different task operations
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": "SAME_CONVERSATION_ID", "message": "Complete the grocery task"}'

# Expected response: Task marked as complete, confirmation returned
# Tool calls should include complete_task operation
```

### 5. Multi-user Isolation
```bash
# User A conversation
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer USER_A_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "I am User A, add task X"}'

# User B conversation (should be isolated)
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer USER_B_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "I am User B, add task Y"}'

# Verify User B cannot access User A's conversation
```

### 6. Natural Language Processing
Test these variations:
- "Add a task to walk the dog"
- "Show me my tasks"
- "Mark the dog walking task as done"
- "Remove the grocery shopping task"
- "Change the deadline for the report task to Friday"

Expected: Agent correctly maps language to appropriate MCP tools

### 7. Error Handling
```bash
# Test invalid JWT
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer INVALID_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task"}'

# Expected: 401 Unauthorized

# Test non-existent task
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer VALID_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": "VALID_CONVO_ID", "message": "Complete the fake task"}'

# Expected: Friendly error message like "I couldn't find that task."
```

### 8. Server Restart Recovery
```bash
# 1. Start conversation and add tasks
# 2. Restart the server
# 3. Resume conversation with same ID
# 4. Verify conversation history is preserved
# 5. Verify tasks are still accessible
```

### 9. MCP Tool Transparency
Verify that API responses include the `tool_calls` array showing:
- Which tools were called
- What arguments were passed
- What results were returned

Example:
```json
{
  "response": "I've added the task to buy groceries.",
  "tool_calls": [
    {
      "name": "add_task",
      "arguments": {"task": "buy groceries"},
      "result": {"success": true, "task_id": "abc123"}
    }
  ]
}
```

## Success Criteria

✅ New conversations created when no conversation_id provided
✅ Existing conversations resumed when conversation_id provided
✅ Natural language mapped to correct MCP tool calls
✅ Messages persist across server restarts
✅ User isolation maintained (cannot access other users' data)
✅ Error handling returns user-friendly messages
✅ Tool calls are transparent in API responses
✅ Authentication validates JWT and enforces user scoping

## Troubleshooting

**Issue**: Agent doesn't recognize certain language patterns
**Solution**: Review prompt engineering in prompts.py and add more examples

**Issue**: Conversations don't persist
**Solution**: Check database connection and migration status

**Issue**: Unauthorized access to other users' data
**Solution**: Verify JWT validation and user_id scoping logic

**Issue**: MCP tools not being called
**Solution**: Check agent configuration and tool availability