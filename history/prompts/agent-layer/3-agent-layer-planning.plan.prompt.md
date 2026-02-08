---
id: 3
title: Agent Layer Planning
stage: plan
date: 2026-02-07
surface: agent
model: claude-opus-4-6
feature: agent-layer
branch: 005-agent-layer
user: claude
command: '/sp.plan.spec3.md'
labels: [plan,agent,conversational-memory,constitution]
links:
  spec: specs/005-agent-layer/spec.md
  plan: specs/005-agent-layer/plan.md
  research: specs/005-agent-layer/research.md
  data-model: specs/005-agent-layer/data-model.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-agent-layer/plan.md
 - specs/005-agent-layer/research.md
 - specs/005-agent-layer/data-model.md
 - specs/005-agent-layer/contracts/chat-api.yaml
 - specs/005-agent-layer/quickstart.md
 - CLAUDE.md
tests:

---

## Prompt

/sp.plan.spec3.md

Project: Phase III – Agent Layer + Conversational Memory

Purpose:
Define architecture, implementation phases, decisions, validation strategy for Spec-3.

---

==========================
ARCHITECTURE OVERVIEW
==========================

Frontend:
ChatKit UI

Backend:
FastAPI

AI:
OpenAI Agents SDK

Tools:
Official MCP SDK

Database:
Neon PostgreSQL via SQLModel

Auth:
Better Auth

Flow:

Client
→ POST /api/chat
→ Load Conversation + Messages
→ OpenAI Agent
→ MCP Tools
→ Database
→ Response

Stateless backend:
All state stored in Neon DB.

---

==========================
PHASED IMPLEMENTATION
==========================

PHASE 1 — DATABASE FOUNDATION

- Create Conversation model
- Create Message model
- Setup migrations
- Verify persistence

Output:
Chat memory storage ready.

---

PHASE 2 — CHAT ENDPOINT

- POST /api/chat
- Create conversation if missing
- Load message history
- Save user message

Output:
Stateless conversational API.

---

PHASE 3 — AGENT LAYER

- Initialize OpenAI Agent
- Attach MCP tools
- Load prompts
- Run agent

Output:
AI reasoning operational.

---

PHASE 4 — MCP BRIDGE

- Connect MCP client
- Forward tool calls
- Return structured outputs

Output:
Agent controls tasks.

---

PHASE 5 — RESPONSE PIPELINE

- Save assistant messages
- Return conversation_id
- Return tool_calls

Output:
Full conversational loop.

---

PHASE 6 — ERROR + SECURITY

- Task not found handling
- MCP failure recovery
- Auth ownership validation

Output:
Production-safe behavior.

---

PHASE 7 — TESTING

Manual flows:

✓ Create task via chat
✓ List pending
✓ Complete task
✓ Delete task
✓ Restart server → resume chat

---

==========================
KEY DESIGN DECISIONS
==========================

1. Stateless Server
Pros:
- Horizontally scalable
- Restart-safe

Cons:
- DB dependency

Accepted.

---

2. Conversation in Database vs Memory

Chosen:
Database

Reason:
Persistence + auditability.

---

3. MCP as Tool Layer

Reason:
Decouples AI from business logic.

---

==========================
RESEARCH APPROACH
==========================

Concurrent:

- Build while referencing:
  - OpenAI Agents SDK docs
  - MCP SDK examples
  - SQLModel patterns

No upfront research freeze.

---

==========================
QUALITY VALIDATION
==========================

Acceptance Checks:

✓ Agent calls correct MCP tools
✓ Messages persist
✓ Conversations resume
✓ User isolation enforced
✓ Natural language works
✓ Errors human-readable

---

==========================
DELIVERABLES
==========================

/backend
- agent.py
- runner.py
- prompts.py
- chat.py

/models
- conversation.py
- message.py

/mcp
- client.py

README updates

---

NEXT FILE:

sp.implement.spec3.md

## Response snapshot

Completed comprehensive planning for the Agent Layer & Conversational Memory feature. Generated:

- Enhanced plan.md with constitution compliance checks and detailed technical context
- research.md documenting technology decisions and patterns
- data-model.md defining Conversation and Message entities
- contracts/chat-api.yaml specifying the API contract
- quickstart.md with validation steps
- Updated CLAUDE.md with new technology context

All artifacts align with the constitution's principles: agent-first architecture, stateless backend design, tool-based execution, user isolation, and transparency.

## Outcome

- ✅ Impact: Created complete architectural plan compliant with project constitution
- 🧪 Tests: Added API contracts and quickstart validation procedures
- 📁 Files: Created 6 files across spec documentation, contracts, and system updates
- 🔁 Next prompts: Ready for task breakdown with /sp.tasks
- 🧠 Reflection: Successfully integrated detailed requirements with constitutional compliance

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All constitution checks passed
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to implementation planning