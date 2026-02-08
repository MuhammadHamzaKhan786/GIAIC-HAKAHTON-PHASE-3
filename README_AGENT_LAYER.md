# Agent Layer & Conversational Memory Implementation

## Overview
This implementation provides an OpenAI Agent powered chatbot that integrates with MCP tools for managing todo operations, with conversation persistence in Neon database. The system accepts natural language input, maintains conversation history, and executes todo operations through MCP tool integration.

## Architecture
- **Frontend**: ChatKit UI
- **Backend**: FastAPI
- **AI**: OpenAI Agents SDK
- **Tools**: Official MCP SDK
- **Database**: Neon PostgreSQL via SQLModel
- **Auth**: Better Auth

## Key Components

### 1. Data Models
- `Conversation`: Represents a conversation thread with user_id, timestamps
- `Message`: Individual messages in conversations with role (user/assistant/system)

### 2. Agent Layer
- `agent.py`: Initializes OpenAI Agent with MCP tools and system prompt
- `runner.py`: Executes agent with message history and captures tool calls
- `prompts.py`: Contains system prompts for the agent

### 3. API Layer
- `chat.py`: Main chat endpoint POST /api/{user_id}/chat
- `auth.py`: Authentication validation middleware

### 4. Services
- `mcp_client.py`: Wrapper for MCP server communication

## API Endpoint
`POST /api/{user_id}/chat`

Input:
```json
{
  "conversation_id": "optional UUID",
  "message": "required message text"
}
```

Process:
1. Validates JWT token
2. Creates conversation if missing
3. Loads previous messages
4. Saves user message
5. Builds agent message array
6. Calls run_agent()
7. Saves assistant message
8. Returns:
```json
{
  "conversation_id": "UUID",
  "response": "AI response text",
  "tool_calls": ["array of tool calls"]
}
```

## Features
- Stateless backend (all state stored in database)
- Conversation persistence across server restarts
- User isolation via JWT validation
- MCP tool integration for todo operations
- Natural language processing for task management
- Error handling with user-friendly messages

## Validation Checks Passed
- ✓ Chat resumes after restart
- ✓ Agent uses MCP tools
- ✓ Tasks persist
- ✓ Messages stored
- ✓ User isolated
- ✓ Natural language works