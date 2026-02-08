---
description: "Task list for implementing Agent Layer & Conversational Memory"
---

# Tasks: Agent Layer & Conversational Memory

**Input**: Design documents from `/specs/005-agent-layer/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create required directories: backend/agent/, backend/api/, backend/models/
- [x] T002 Install OpenAI SDK dependency in backend requirements
- [x] T003 [P] Install and configure SQLModel dependency for database models

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create Conversation SQLModel in backend/models/conversation.py
- [x] T005 Create Message SQLModel in backend/models/message.py
- [x] T006 [P] Create DB migration for Conversation + Message tables
- [x] T007 Create MCP client wrapper in backend/services/mcp_client.py
- [x] T008 [P] Create prompts module in backend/agent/prompts.py
- [x] T009 Setup authentication validation middleware

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Chat with AI Assistant (Priority: P1) 🎯 MVP

**Goal**: Enable users to chat with an AI assistant that can manage their tasks using natural language

**Independent Test**: Send natural language commands like "add a task to buy groceries" and verify that the system correctly interprets and executes the command, delivering immediate value to users.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T010 [P] [US1] Integration test for chat functionality in tests/integration/test_chat.py

### Implementation for User Story 1

- [x] T011 [P] [US1] Create agent module in backend/agent/agent.py
- [x] T012 [P] [US1] Create runner module in backend/agent/runner.py
- [x] T013 [US1] Create POST /api/chat route in backend/api/chat.py
- [x] T014 [US1] Implement conversation creation logic in backend/api/chat.py
- [x] T015 [US1] Implement message persistence in backend/api/chat.py
- [x] T016 [US1] Integrate OpenAI Agent with MCP tools in runner.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Conversation Persistence (Priority: P2)

**Goal**: Maintain conversation with the AI assistant to be remembered across sessions so users can continue their previous conversation when they return

**Independent Test**: Start a conversation, close the app, reopen it, and verify that the system recognizes the ongoing conversation and its history.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [x] T017 [P] [US2] Integration test for conversation persistence in tests/integration/test_conversation_persistence.py

### Implementation for User Story 2

- [x] T018 [P] [US2] Implement conversation loading in backend/api/chat.py
- [x] T019 [US2] Fetch full message history for conversation in backend/api/chat.py
- [x] T020 [US2] Sort messages by created_at in ascending order in backend/api/chat.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Tool Integration via MCP (Priority: P3)

**Goal**: Enable the AI assistant to seamlessly integrate with the backend tools via MCP to perform various todo operations reliably

**Independent Test**: Issue various commands to the AI and verify that appropriate MCP tool calls are made and processed correctly.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [x] T021 [P] [US3] Integration test for MCP tool integration in tests/integration/test_mcp_integration.py

### Implementation for User Story 3

- [x] T022 [P] [US3] Create MCP tool exposure in backend/agent/runner.py
- [x] T023 [US3] Forward agent tool calls to MCP in backend/agent/runner.py
- [x] T024 [US3] Return structured responses from MCP in backend/agent/runner.py
- [x] T025 [US3] Handle MCP failures with user-friendly error messages

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T026 [P] Add comprehensive error handling in all modules
- [x] T027 [P] Implement JWT validation for user identity in backend/api/chat.py
- [x] T028 [P] Ensure user owns conversation + tasks in backend/api/chat.py
- [x] T029 [P] Add logging for all operations in agent and API modules
- [x] T030 [P] Update response payload to include conversation_id, response, and tool_calls
- [x] T031 [P] Store assistant responses in Message table in backend/agent/runner.py
- [x] T032 Handle missing tasks gracefully with user-friendly messages
- [x] T033 Run end-to-end integration test to validate complete functionality

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Integration test for chat functionality in tests/integration/test_chat.py"

# Launch all models for User Story 1 together:
Task: "Create agent module in backend/agent/agent.py"
Task: "Create runner module in backend/agent/runner.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence