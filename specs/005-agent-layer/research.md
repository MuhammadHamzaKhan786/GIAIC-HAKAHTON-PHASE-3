# Research: Agent Layer & Conversational Memory

## Technology Decisions & Patterns

### 1. OpenAI Agents SDK Integration

**Decision**: Use OpenAI Agents SDK to power the conversational AI assistant.

**Rationale**: The OpenAI Agents SDK provides the most mature and well-documented approach for creating AI assistants that can call tools based on natural language input. It allows us to define tools (our MCP tools) and let the AI decide which ones to call based on user input.

**Alternatives considered**:
- LangChain Agents: More complex setup and vendor lock-in with less direct control
- Custom LLM orchestration: Requires building tool selection logic from scratch
- Anthropic Claude Functions: Vendor-specific approach, not suitable for multi-vendor strategy

### 2. MCP SDK Integration Pattern

**Decision**: Implement MCP client wrapper to connect OpenAI Agent to backend tools.

**Rationale**: The MCP SDK provides a standardized way to expose backend functionality as tools for AI agents. This ensures proper separation of concerns between AI logic and business logic, allowing the agent to focus on natural language understanding while backend tools handle the actual business operations.

**Alternatives considered**:
- Direct database calls from agent: Violates constitution's "Tool-Based Execution" principle
- REST API integration: Would require more complex authentication and state management
- GraphQL mutations: Overkill for simple tool invocations

### 3. Database Storage for Conversations

**Decision**: Use Neon PostgreSQL via SQLModel to store conversation and message history.

**Rationale**:
- Aligns with constitution's "Stateless Backend Design" principle
- Ensures conversations persist across server restarts
- Provides audit trail for conversation history
- Neon PostgreSQL offers serverless scaling benefits
- SQLModel provides Python-native ORM with SQLAlchemy backing

**Alternatives considered**:
- In-memory storage: Violates stateless design principle
- File-based storage: Difficult to scale and synchronize across instances
- Redis: Additional infrastructure complexity for simple persistence needs

### 4. Authentication & User Isolation

**Decision**: Implement Better Auth with JWT token validation for user isolation.

**Rationale**:
- Complies with constitution's "User Isolation & Security" principle
- Ensures each user only accesses their own conversations and tasks
- JWT tokens can be validated serverlessly without session state
- Better Auth provides modern, secure authentication patterns

**Alternatives considered**:
- Session-based authentication: Requires server-side session storage
- API Keys: Less user-friendly and harder to manage for end users
- OAuth only: Limits user registration options

### 5. API Design for Chat Endpoint

**Decision**: Create stateless POST /api/chat endpoint that reconstructs conversation context.

**Rationale**:
- Maintains statelessness as required by constitution
- Supports horizontal scaling without shared session state
- Each request contains all necessary context (user identity, conversation ID)
- Allows for proper authentication and authorization on each call

**Pattern**:
```
Client → POST /api/chat {conversation_id?, message} → JWT Auth → Load/Init Conversation → Fetch Message History → Store User Message → Run Agent → Agent → MCP Tools → Store Assistant Response → Return {conversation_id, response, tool_calls}
```

### 6. Error Handling Strategy

**Decision**: Implement graceful error handling with user-friendly messages.

**Rationale**:
- Aligns with constitution's "Natural Language Reliability" and "Transparency" principles
- Ensures system is robust against malformed inputs and tool failures
- Maintains positive user experience even when operations fail
- Provides clear feedback without exposing system internals

**Pattern**:
- Task not found: "I couldn't find that task. Would you like to see your current tasks?"
- MCP failure: "Sorry, I encountered an issue processing your request. Please try again."
- Authentication failure: Standard HTTP 401 responses

### 7. Response Transparency

**Decision**: Return tool calls and execution results in API response.

**Rationale**:
- Supports constitution's "Transparency" principle
- Allows frontend to display what actions were taken
- Enables debugging and monitoring of AI behavior
- Provides user confidence in system operations

**Response Format**:
```json
{
  "conversation_id": "uuid",
  "response": "AI-generated response",
  "tool_calls": [
    {
      "name": "add_task",
      "arguments": {"task": "buy groceries"},
      "result": {"success": true, "task_id": "123"}
    }
  ]
}
```