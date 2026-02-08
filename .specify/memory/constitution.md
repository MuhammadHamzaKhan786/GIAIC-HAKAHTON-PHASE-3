<!-- Sync Impact Report
Version change: 1.0.0 → 2.0.0
Modified principles: I-VI (renamed and updated to reflect new project focus)
Added sections: Agent-First Architecture, Stateless Backend Design, Tool-Based Execution, Natural Language Reliability, Transparency
Removed sections: Previous principles about Spec-Driven Development, Agentic Workflow Purity, etc.
Templates requiring updates: ⚠ plan-template.md, ⚠ spec-template.md, ⚠ tasks-template.md
Follow-up TODOs: None
-->

# AI-Powered Todo Chatbot with MCP + OpenAI Agents SDK Constitution

## Core Principles

### I. Agent-First Architecture
All task operations must be mediated by an AI agent invoking MCP tools. The system must route all user interactions through the OpenAI Agent which selects and executes appropriate MCP tools based on natural language input.

### II. Stateless Backend Design
FastAPI server holds no runtime memory. Conversation context is reconstructed from database on every request. No in-memory session storage is allowed - all state must persist in the database.

### III. Tool-Based Execution
The agent may not directly mutate database state; all mutations must occur through MCP tools. The flow must be: Frontend → FastAPI → Agent → MCP → Database → Agent → Client with no direct DB access by agent.

### IV. Deterministic Behavior
Identical user inputs with identical database state should produce consistent outcomes. State transitions must be predictable and reproducible regardless of server restarts.

### V. User Isolation & Security
Every operation must be scoped to authenticated user_id via JWT verification. Authentication must be enforced via Better Auth + JWT with user_id extracted from token, never trusted from client input.

### VI. Natural Language Reliability
Common task intents (add, list, update, complete, delete) must be correctly inferred from conversational input. The agent must select correct tools based on intent and handle ambiguity via clarification or tool chaining.

### VII. Transparency
Every agent action must return confirmation and expose invoked MCP tools in API response. Users must be able to see which MCP tools were called and what the results were.

## Technology Stack

**Frontend**: OpenAI ChatKit - Conversational UI for natural language todo management
**Backend**: Python FastAPI - Stateful conversation routing and JWT authentication middleware
**Agent Framework**: OpenAI Agents SDK - AI-powered natural language understanding and tool selection
**MCP Server**: Official MCP SDK - Standardized tool interface for database operations
**ORM**: SQLModel - Database schema management and object-relational mapping
**Database**: Neon PostgreSQL - Persistent conversation and task data storage
**Authentication**: Better Auth + JWT - User signup/signin and session management
**Development Framework**: Claude Code + Spec-Kit Plus - Agentic development workflow

## Development Workflow

1. **Specification**: Write comprehensive feature specifications following the spec template
2. **Planning**: Generate architectural plans using the plan template and /sp.plan command
3. **Task Breakdown**: Create testable tasks using the tasks template and /sp.tasks command
4. **Implementation**: Execute tasks using specialized agents (Auth, Frontend, Backend, DB, Agent)
5. **Validation**: Ensure all changes follow the AI → MCP → Database pattern and meet acceptance criteria

## System Constraints

- No in-memory session storage allowed
- No direct DB access by agent (must use MCP tools only)
- No frontend bypass of MCP tools
- No manual coding (Claude Code only)
- No vendor-specific LLM logic outside OpenAI Agents SDK
- No stateful backend services (must reconstruct from database)

## Behavioral Rules

- Task creation → add_task MCP tool
- Task listing → list_tasks MCP tool
- Task completion → complete_task MCP tool
- Task deletion → delete_task MCP tool
- Task update → update_task MCP tool
- Ambiguous delete/update: Agent must call list_tasks before mutating
- Every mutation requires friendly confirmation
- Errors must be user-readable: e.g. "I couldn't find that task."

## Quality Requirements

- Chat UI responsive on all devices
- Tool calls returned in API response for transparency
- Conversations resumable after server restart
- All endpoints protected with JWT verification
- Database ownership enforced on all operations
- Conversation state persists across requests

## Governance

This constitution supersedes all other development practices. Amendments require:
- Documentation of changes and rationale
- Approval through the /sp.constitution command
- Migration plan for existing implementations
- Version update following semantic versioning rules

All PRs and code reviews must verify compliance with these principles. All database mutations must go through MCP tools as specified.

**Version**: 2.0.0 | **Ratified**: 2026-02-04 | **Last Amended**: 2026-02-04