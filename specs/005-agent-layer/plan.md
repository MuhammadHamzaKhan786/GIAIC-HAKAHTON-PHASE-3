# Implementation Plan: Agent Layer & Conversational Memory

**Branch**: `005-agent-layer` | **Date**: 2026-02-07 | **Spec**: [link to spec.md](./spec.md)

**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of an OpenAI Agent powered chatbot that integrates with MCP tools for managing todo operations, with conversation persistence in Neon database. The system will accept natural language input, maintain conversation history, and execute todo operations through MCP tool integration. This implementation follows the constitution's principles of agent-first architecture, stateless backend design, and tool-based execution.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, OpenAI SDK, SQLModel, Neon PostgreSQL, Better Auth, MCP SDK
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest
**Target Platform**: Linux server
**Project Type**: Web backend with API endpoints
**Performance Goals**: <3 second response time for typical operations, handle 100 concurrent users
**Constraints**: <200ms p95 latency for database operations, secure authentication required, agent-first architecture (no direct DB access), stateless backend (no in-memory session storage)
**Scale/Scope**: 10k users, persistent conversation history

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance with Constitution Principles:

✅ **Agent-First Architecture**: All task operations mediated by OpenAI Agent invoking MCP tools
✅ **Stateless Backend Design**: FastAPI server holds no runtime memory; conversation context reconstructed from database
✅ **Tool-Based Execution**: Agent calls MCP tools only; no direct database access by agent
✅ **Deterministic Behavior**: Identical inputs with identical DB state produce consistent outcomes
✅ **User Isolation & Security**: Every operation scoped to authenticated user_id via JWT verification
✅ **Natural Language Reliability**: Common intents (add, list, update, complete, delete) correctly inferred
✅ **Transparency**: Every agent action returns confirmation and exposes invoked MCP tools in API response

### System Constraints Adherence:
✅ No in-memory session storage - conversation state from database
✅ No direct DB access by agent - MCP tools only
✅ No manual coding - Claude Code only
✅ No stateful backend - reconstruct from database
✅ All mutations through MCP tools

## Project Structure

### Documentation (this feature)

```text
specs/005-agent-layer/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification
├── research.md          # Research and technology decisions
├── data-model.md        # Entity definitions
├── quickstart.md        # Validation steps
├── contracts/           # API contracts
│   └── chat-api.yaml    # Chat endpoint contract
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── agent/
│   ├── agent.py         # OpenAI Agent initialization
│   ├── runner.py        # Agent execution and MCP tool bridge
│   └── prompts.py       # System prompts and instructions
├── api/
│   └── chat.py          # POST /api/chat endpoint
├── models/
│   ├── conversation.py  # Conversation SQLModel
│   └── message.py       # Message SQLModel
└── services/
    └── mcp_client.py    # MCP server communication layer
```

**Structure Decision**: Web application backend structure with dedicated modules for agent functionality, API endpoints, and data models. This separates concerns with agent logic in its own module, API endpoints clearly defined, and data models properly structured for conversation persistence. Follows constitution's stateless design and tool-based execution principles.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Additional MCP layer | Constitution requirement | Direct DB access violates "Tool-Based Execution" principle |
| Stateless complexity | Constitution requirement | In-memory sessions violate "Stateless Backend Design" |
