---
id: 1
title: Agent Layer Specification
stage: spec
date: 2026-02-07
surface: agent
model: claude-opus-4-6
feature: agent-layer
branch: 005-agent-layer
user: claude
command: '/sp.specify.spec3.md'
labels: [spec,agent,conversational-memory]
links:
  spec: specs/005-agent-layer/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-agent-layer/spec.md
 - specs/005-agent-layer/checklists/requirements.md
tests:

---

## Prompt

/sp.specify.spec3.md

Project: Phase III – Agent Layer & Conversational Memory

Goal:
Create OpenAI Agent powered chatbot that communicates with MCP server and persists conversations.

This spec builds:

✓ OpenAI Agents SDK integration
✓ Stateless chat endpoint
✓ Conversation storage
✓ Tool calling via MCP
✓ Natural language task management

---

=========================
SYSTEM OBJECTIVES
=========================

The system must:

- Accept natural language input
- Restore conversation history
- Run OpenAI Agent
- Call MCP tools
- Persist all messages
- Return AI responses

Backend remains stateless.

All memory stored in Neon.

---

=========================
DIRECTORY STRUCTURE
=========================

backend/
  agent/
    agent.py
    runner.py
    prompts.py

  api/
    chat.py

  models/
    conversation.py
    message.py

---

=========================
DATABASE MODELS
=========================

Conversation:

id
user_id
created_at
updated_at

Message:

id
conversation_id
user_id
role
content
created_at

---

=========================
CHAT ENDPOINT
=========================

POST /api/chat

Request:

conversation_id (optional)
message (required)

Response:

conversation_id
response
tool_calls

---

=========================
CONVERSATION FLOW
=========================

1. Receive message
2. Validate JWT
3. Load conversation (or create)
4. Fetch message history
5. Store user message
6. Run agent
7. Agent calls MCP tools
8. Store assistant reply
9. Return response

Server holds ZERO session state.

---

=========================
OPENAI AGENT
=========================

Use OpenAI Agents SDK.

Agent system prompt:

"You are a Todo assistant.
Manage tasks using MCP tools.
Always confirm actions.
Be concise and friendly."

Agent has access to:

add_task
list_tasks
complete_task
update_task
delete_task

Agent never modifies DB directly.

Only via MCP.

---

=========================
TOOL BRIDGE
=========================

Create MCP client inside runner.py.

Forward tool calls to MCP server.

Return structured outputs.

---

=========================
NATURAL LANGUAGE RULES
=========================

User intent → Tool mapping:

Add → add_task
Show → list_tasks
Complete → complete_task
Delete → delete_task
Update → update_task

Ambiguous delete/update:

Call list_tasks first.

---

=========================
ERROR BEHAVIOR
=========================

If task not found:

Respond politely.

If tool fails:

Explain simply.

Never expose stack traces.

---

=========================
DELIVERABLES
=========================

Working chatbot:

✓ remembers conversations
✓ resumes after restart
✓ manages todos via chat
✓ confirms actions

---

NEXT FILES:

sp.task.spec3.md
sp.plan.spec3.md
sp.implement.spec3.md

## Response snapshot

Created feature specification for the Agent Layer & Conversational Memory feature. Generated:
- Specification document at specs/005-agent-layer/spec.md
- Quality checklist at specs/005-agent-layer/checklists/requirements.md

The specification includes:
- User scenarios for conversational task management
- Functional requirements for the chatbot system
- Key entities (Conversation and Message)
- Success criteria for measuring the feature's effectiveness

## Outcome

- ✅ Impact: Created complete specification for OpenAI Agent powered chatbot with MCP integration
- 🧪 Tests: None yet, planning phase next
- 📁 Files: Created spec.md and requirements checklist
- 🔁 Next prompts: /sp.plan, /sp.tasks
- 🧠 Reflection: Successfully transformed user requirements into a structured specification with clear user value

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to planning phase