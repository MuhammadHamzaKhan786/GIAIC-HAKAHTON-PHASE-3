# Implementation Plan: AI Todo Chatbot (Spec 1: Chat Interface & Stateless Messaging)

**Branch**: `1-chat-interface` | **Date**: 2026-02-04 | **Spec**: specs/1-chat-interface/spec.md
**Input**: Feature specification from `/specs/1-chat-interface/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a stateless conversational AI system enabling authenticated users to interact with an assistant via ChatKit UI, with all conversation history persisted in Neon PostgreSQL. The architecture extends the existing frontend (Next.js with Better Auth) and backend (FastAPI with SQLModel) to integrate OpenAI ChatKit and Agents SDK while maintaining the stateless design and security requirements.

## Technical Context

**Language/Version**: Python 3.11, TypeScript/React for frontend (Next.js 16+), SQL for Neon PostgreSQL
**Primary Dependencies**: OpenAI ChatKit, FastAPI, OpenAI Agents SDK, SQLModel, Neon PostgreSQL, Better Auth for JWT
**Storage**: Neon Serverless PostgreSQL with existing Task/User models extended with Conversation and Message tables
**Testing**: pytest for backend, Jest/Cypress for frontend (to be determined)
**Target Platform**: Web application with responsive design supporting mobile, tablet, and desktop
**Project Type**: Web (dual structure: frontend + backend) - building upon existing architecture
**Performance Goals**: Sub-5 second response time for chat interactions, support for concurrent users as per Neon tier limits
**Constraints**: Stateless backend design, JWT authentication required for all requests, Claude Code only (no manual coding), integration with existing auth system
**Scale/Scope**: Individual user conversations, isolated by user_id, designed for typical todo management load

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Agent-First Architecture: Backend will integrate with OpenAI Agents SDK as required
- ✅ Stateless Backend Design: Architecture enforces zero runtime memory, all state reconstructed from database
- ✅ Tool-Based Execution: Backend will route requests through MCP tools (in future specs)
- ✅ Deterministic Behavior: Each request rebuilds conversation context from database
- ✅ User Isolation & Security: All operations scoped to authenticated user_id via JWT verification
- ✅ Natural Language Reliability: AI agent will handle conversational intent parsing
- ✅ Transparency: API responses will include information about agent actions taken

## Project Structure

### Documentation (this feature)

```text
specs/1-chat-interface/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (extending existing architecture)

**Existing Backend Structure (to be extended)**:
```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py          # Existing task model
│   │   ├── user.py          # Existing user model
│   │   ├── conversation.py  # NEW: Conversation SQLModel
│   │   └── message.py       # NEW: Message SQLModel
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py          # Existing JWT verification
│   │   ├── chat_service.py  # NEW: Core chat functionality
│   │   └── agent_runner.py  # NEW: OpenAI Agent interaction
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py        # Existing task API routes
│   │   └── chat_router.py   # NEW: /api/{user_id}/chat endpoint
│   ├── auth/
│   │   └── auth_bearer.py   # Existing auth middleware
│   ├── database/
│   │   └── __init__.py      # Existing DB configuration
│   └── main.py              # Existing FastAPI app entry point
└── tests/
    ├── unit/
    └── integration/
```

**Existing Frontend Structure (to be extended)**:
```text
frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx              # Existing home page
│   │   ├── layout.tsx            # Existing layout
│   │   ├── signin/               # Existing auth
│   │   ├── signup/               # Existing auth
│   │   ├── dashboard/            # Existing dashboard
│   │   └── chat/                 # NEW: Chat page with authentication guard
│   ├── components/
│   │   ├── ui/                   # Existing UI components
│   │   └── chat/                 # NEW: Chat components
│   │       ├── ChatInterface.tsx # Main chat UI component
│   │       ├── MessageBubble.tsx # Message display component
│   │       ├── TypingIndicator.tsx # Loading state component
│   │       └── NewConversationBtn.tsx # Control component
│   ├── contexts/                 # Existing auth context
│   ├── lib/                      # Existing utilities
│   ├── styles/                   # Existing styles
│   └── globals.css               # Existing global styles
├── package.json                  # Contains better-auth, next.js, react
├── next.config.js               # Existing Next.js config
├── tsconfig.json                # Existing TS config
└── tailwind.config.js           # Existing styling config
```

**Structure Decision**: Extending existing dual structure (Option 2: Web application) to maintain consistency with established architecture while adding new chat functionality. This leverages existing authentication, UI patterns, and infrastructure.

## Implementation Phases

### Phase 1 — Foundation
- Integrate OpenAI ChatKit into existing Next.js frontend
- Create Conversation and Message SQLModels compatible with existing models
- Configure Neon PostgreSQL connection using existing database setup
- Implement JWT verification using existing auth middleware
- Scaffold /api/{user_id}/chat endpoint in existing FastAPI app

**Deliverable**: Running empty chat UI connected to protected endpoint, integrated with existing auth system

### Phase 2 — Messaging Pipeline
- Implement storing incoming user messages in database using existing session patterns
- Create conversation if missing for user using existing database transaction patterns
- Load complete conversation history from database using existing select patterns
- Construct agent input array from history
- Return placeholder assistant response initially
- Persist assistant messages to database using existing patterns

**Deliverable**: End-to-end stateless message roundtrip with database persistence, consistent with existing API patterns

### Phase 3 — UI Integration
- Render user and assistant messages in distinct bubbles compatible with existing UI
- Add typing indicator during agent processing
- Implement auto-scroll to latest message
- Handle various loading states in UI using existing patterns
- Add "New Conversation" control functionality
- Ensure mobile responsiveness across all devices using existing Tailwind patterns
- Apply light theme styling consistent with existing UI

**Deliverable**: Fully usable and visually appealing chat interface integrated with existing design system

### Phase 4 — Validation & Error Handling
- Handle invalid or non-existent conversation IDs appropriately
- Implement graceful handling of authentication failures using existing patterns
- Reject empty messages with appropriate feedback
- Display user-friendly error messages in UI using existing components
- Verify user ownership enforcement on all data access using existing patterns

**Deliverable**: Robust user experience with comprehensive error handling consistent with existing app behavior

### Phase 5 — QA + Documentation
- Manual testing of complete chat flow end-to-end
- Verify conversation history persists after page refresh
- Test system recovery after server restart
- Update main README with chat setup instructions
- Document chat API endpoint with examples

**Deliverable**: Production-ready system with complete documentation integrated with existing project

## Architecture Decisions

### Integration Strategy
- Extend existing backend models and API router rather than creating separate services
- Integrate with existing Better Auth authentication system for consistent user experience
- Use existing database session patterns and transaction handling for consistency
- Leverage existing frontend layout and authentication context

### Conversation Management Strategy
- Each user session maintains a conversation context identified by conversation_id
- Conversations are loaded from database on each request (stateless)
- New conversations created automatically when user starts chatting
- Conversation history limited to prevent performance issues (configurable window)
- Share existing database connection pool with other models

### Message Pagination Approach
- Retrieve all messages for conversation context in stateless request
- Future optimization: implement pagination for very long conversations
- Current design assumes typical todo management conversations remain manageable in size

### History Window Size for Agent
- Full conversation history sent to agent for context
- Future implementation will need to consider token limits
- Configurable maximum context window for agent input

### Authentication Strategy
- Leverage existing JWT verification middleware from auth/auth_bearer.py
- User_id extracted from JWT claims and matched with URL parameter
- 401 responses for invalid/unauthorized requests using existing patterns
- Frontend authentication guard integrated with existing auth context

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Extension of existing architecture | Consistency with established patterns | Separate services would create maintenance overhead |
| Shared database with existing models | Efficient resource utilization | Separate databases would complicate transactions |