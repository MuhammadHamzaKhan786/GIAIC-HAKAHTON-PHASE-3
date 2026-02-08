---
id: 1
title: "AI Todo Chatbot Constitution"
stage: constitution
date_iso: 2026-02-04
surface: agent
model: claude-opus-4-5-20251101
feature: todo-chatbot
branch: main
user: user
command: /sp.constitution
labels: ["constitution", "todo-chatbot", "mcp", "agents-sdk"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
  - "history/prompts/constitution/1-ai-todo-chatbot-constitution.constitution.prompt.md"
tests_yaml: []
---

# AI Todo Chatbot Constitution

## Original Prompt

```
/sp.constitution

Project: Phase III – AI-Powered Todo Chatbot with MCP + OpenAI Agents SDK

Objective:
Build an AI-native conversational task manager that enables users to create, update, complete, delete, and list todos using natural language, powered by OpenAI Agents SDK and MCP (Model Context Protocol) tools, implemented via Claude Code and Spec-Kit Plus with zero manual coding.

Core Principles:

- Agent-First Architecture
  All task operations must be mediated by an AI agent invoking MCP tools.

- Stateless Backend Design
  FastAPI server holds no runtime memory. Conversation context is reconstructed from database on every request.

- Tool-Based Execution
  The agent may not directly mutate database state; all mutations must occur through MCP tools.

- Deterministic Behavior
  Identical user inputs with identical database state should produce consistent outcomes.

- User Isolation & Security
  Every operation must be scoped to authenticated user_id via JWT verification.

- Natural Language Reliability
  Common task intents (add, list, update, complete, delete) must be correctly inferred from conversational input.

- Transparency
  Every agent action must return confirmation and expose invoked MCP tools in API response.

---

Key Standards:

- All chat requests must flow:
  Frontend → FastAPI → Agent → MCP → Database → Agent → Client

- MCP tools must be:
  - Stateless
  - Idempotent where possible
  - Validated for user ownership

- AI Agent must:
  - Select correct tool based on intent
  - Fill parameters programmatically
  - Handle ambiguity via clarification or tool chaining

- Conversation state must be persisted:
  - Conversations table
  - Messages table
  - Server reconstructs history per request

- Authentication:
  - JWT verified on every API call
  - user_id extracted from token, never trusted from client input

---

Architectural Constraints:

- Backend: Python FastAPI
- Agent Framework: OpenAI Agents SDK
- MCP Server: Official MCP SDK
- ORM: SQLModel
- Database: Neon PostgreSQL
- Frontend: OpenAI ChatKit
- Authentication: Better Auth + JWT

---

System Constraints:

- No in-memory session storage
- No direct DB access by agent
- No frontend bypass of MCP tools
- No manual coding (Claude Code only)
- No vendor-specific LLM logic outside OpenAI Agents SDK

---

Behavioral Rules:

- Task creation → add_task
- Task listing → list_tasks
- Task completion → complete_task
- Task deletion → delete_task
- Task update → update_task

- Ambiguous delete/update:
  Agent must call list_tasks before mutating.

- Every mutation requires friendly confirmation.

- Errors must be user-readable:
  e.g. "I couldn't find that task."

---

Quality Requirements:

- Chat UI responsive on all devices
- Tool calls returned in API response
- Conversations resumable after server restart
- All endpoints protected
- Database ownership enforced

---

Deliverables:

- ChatKit frontend
- FastAPI chat endpoint
- MCP server with task tools
- Agent configuration
- Database models + migrations
- Spec files
- README setup instructions

---

Success Criteria:

- Users can manage todos entirely via natural language
- Agent reliably invokes correct MCP tools
- Conversation history persists across requests
- Server remains stateless
- All operations scoped to authenticated user
- Tool invocations visible
- Deployment succeeds on Vercel + Neon
- System recovers cleanly after restart
```

## Response Summary

Updated the project constitution to reflect the AI-Powered Todo Chatbot with MCP + OpenAI Agents SDK requirements. The new constitution establishes core principles around agent-first architecture, stateless backend design, tool-based execution, deterministic behavior, user isolation & security, natural language reliability, and transparency. The technology stack now includes OpenAI ChatKit frontend, Python FastAPI backend, OpenAI Agents SDK, MCP SDK, SQLModel ORM, Neon PostgreSQL database, and Better Auth + JWT authentication. System constraints prohibit in-memory session storage, direct DB access by agents, frontend bypass of MCP tools, manual coding, vendor-specific LLM logic outside OpenAI Agents SDK, and stateful backend services. Behavioral rules establish the mapping between natural language commands and specific MCP tools (add_task, list_tasks, complete_task, delete_task, update_task). Quality requirements emphasize transparency of tool calls, persistence of conversation state, and robust authentication.

## Outcome

Successfully updated the constitution file at `.specify/memory/constitution.md` with the new AI-powered todo chatbot requirements and principles, advancing the project to version 2.0.0 of the constitution.

## Evaluation

- ✅ Constitution updated with all specified core principles
- ✅ Technology stack aligned with requirements
- ✅ System constraints properly documented
- ✅ Behavioral rules established for MCP tool mapping
- ✅ Quality requirements captured
- ✅ Version updated from 1.0.0 to 2.0.0
- ✅ Proper date and governance information included