# Implementation Plan: MCP Server & Task Tooling

**Branch**: `004-mcp-server-tools` | **Date**: 2026-02-06 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/[004-mcp-server-tools]/spec.md`

## Summary

Create an MCP (Model Context Protocol) server that exposes task management functionality as stateless tools for OpenAI Agents. The system will provide add_task, list_tasks, complete_task, update_task, and delete_task tools with JWT-based user authentication and SQLModel database integration. This implements the Agent-First Architecture principle where all operations are mediated by AI agents through standardized MCP tools.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, SQLModel, mcp-sdk, asyncpg, python-jose, passlib
**Storage**: Neon PostgreSQL with SQLModel ORM
**Testing**: pytest for integration and unit tests
**Target Platform**: Linux server deployment
**Project Type**: Backend service (web application)
**Performance Goals**: <1 second response time for tool calls under normal load
**Constraints**: Stateless execution with no in-memory session storage, all operations must go through MCP tools as required by constitution
**Scale/Scope**: Support multiple concurrent AI agents accessing user-specific tasks with proper isolation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ **Agent-First Architecture**: MCP tools will mediate all database operations as required
- ✅ **Stateless Backend Design**: MCP server will hold no runtime memory, all state in database
- ✅ **Tool-Based Execution**: All database mutations via MCP tools only, no direct access
- ✅ **Deterministic Behavior**: Tool operations will be predictable and reproducible
- ✅ **User Isolation & Security**: JWT verification will enforce user_id scoping
- ✅ **Natural Language Reliability**: MCP tools designed for agent consumption
- ✅ **Transparency**: Tool invocations and results will be transparent to agents

## Project Structure

### Documentation (this feature)

```text
specs/004-mcp-server-tools/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
mcp-server/
├── src/
│   ├── models/
│   │   └── task.py          # Task model with SQLModel
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── add_task.py      # add_task MCP tool
│   │   ├── list_tasks.py    # list_tasks MCP tool
│   │   ├── complete_task.py # complete_task MCP tool
│   │   ├── update_task.py   # update_task MCP tool
│   │   └── delete_task.py   # delete_task MCP tool
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py    # Database connection setup
│   │   └── migrations.py    # Migration management
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── jwt_handler.py   # JWT verification middleware
│   │   └── security.py      # Authentication utilities
│   ├── utils/
│   │   ├── __init__.py
│   │   └── errors.py        # Standardized error handling
│   └── main.py              # MCP server entry point
├── tests/
│   ├── unit/
│   │   └── test_models.py   # Unit tests for models
│   ├── integration/
│   │   ├── test_add_task.py
│   │   ├── test_list_tasks.py
│   │   ├── test_complete_task.py
│   │   ├── test_update_task.py
│   │   └── test_delete_task.py
│   └── conftest.py          # Test fixtures
├── Dockerfile               # Container definition
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── pyproject.toml          # Project configuration
└── README.md               # Service documentation
```

**Structure Decision**: Backend service structure selected to host the MCP server with dedicated modules for models, tools, database, authentication, and utilities. The structure supports the stateless, tool-based architecture required by the constitution.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
|           |            |                                     |