# Research: MCP Server & Task Tooling

## Technical Decisions

### 1. MCP SDK Selection

**Decision**: Use the official `mcp` Python SDK for implementing the Model Context Protocol server

**Rationale**: The official SDK provides standardized tool registration, request/response handling, and integration with OpenAI Agents. It's maintained by the protocol creators and ensures compatibility with the broader MCP ecosystem.

**Alternatives considered**:
- Custom MCP implementation: Too complex and error-prone
- Third-party MCP libraries: Would add unnecessary dependencies and potential compatibility issues
- Direct HTTP endpoints: Would not follow MCP standards

### 2. Database Connection Management

**Decision**: Use SQLModel with asyncpg for asynchronous database operations

**Rationale**: SQLModel provides the perfect combination of SQLAlchemy features with Pydantic validation. Combined with asyncpg, it offers high-performance async database operations that won't block the event loop during I/O operations.

**Alternatives considered**:
- Traditional synchronous SQLAlchemy: Would block the event loop during DB operations
- Peewee ORM: Less mature async support
- Raw asyncpg: Missing ORM conveniences and validation features

### 3. Authentication Approach

**Decision**: JWT token extraction from headers with server-side verification

**Rationale**: Following the constitution's requirement to never trust client-provided user_id, JWT tokens will be extracted from headers and validated server-side. This ensures that only authenticated users can access their own data.

**Alternatives considered**:
- Session cookies: Not ideal for API/tool-based access
- API keys: Would require additional management layer
- OAuth tokens: More complex than necessary for this use case

### 4. Error Handling Strategy

**Decision**: Structured error responses following MCP standards with specific error types

**Rationale**: MCP tools require standardized error responses that agents can parse reliably. Using structured errors with specific codes (NOT_FOUND, BAD_REQUEST, FORBIDDEN, INTERNAL_ERROR) enables the agent to handle errors appropriately.

**Alternatives considered**:
- Generic error responses: Would make it difficult for agents to react appropriately
- HTTP status codes only: Doesn't work well with MCP protocol
- Custom error formats: Would break compatibility with standard MCP clients

### 5. Tool Registration Pattern

**Decision**: Centralized tool registry with individual tool modules

**Rationale**: Separating each tool into its own module maintains clean code organization while allowing centralized registration. This approach makes it easy to add new tools or modify existing ones without affecting other parts of the system.

**Alternatives considered**:
- All tools in one file: Would become unwieldy as more tools are added
- Automatic discovery: Would make it harder to control tool registration order and configuration
- Decorator-based registration: Would spread tool definitions across multiple places

## Implementation Patterns

### 1. Request Flow Pattern

```
Agent -> MCP Server -> JWT Validation -> Tool Handler -> Database -> Response
```

This ensures all requests are authenticated and routed through the proper channels as required by the constitution.

### 2. Tool Schema Definition

Each tool follows a consistent pattern with:
- Input validation using Pydantic models
- Error handling with standardized responses
- Ownership verification before database operations
- Consistent response formatting

### 3. Database Transaction Management

All tool operations use proper transaction handling:
- Individual operations wrapped in transactions
- Rollbacks on validation or authorization failures
- Connection pooling for efficiency

## Security Considerations

### 1. User Isolation

- User ID always extracted from JWT token, never trusted from request
- All database queries filtered by authenticated user ID
- Ownership checks before performing operations on resources

### 2. Input Validation

- Comprehensive Pydantic models for all tool inputs
- Validation at the tool boundary before database operations
- Sanitized outputs to prevent injection attacks

### 3. Token Handling

- Proper JWT validation with correct signing algorithms
- Expiration time checks
- Secure storage and transmission of tokens