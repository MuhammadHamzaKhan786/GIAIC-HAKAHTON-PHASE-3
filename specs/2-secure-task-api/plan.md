# Implementation Plan: Spec-2 — Secure Backend Task Management API

## Technical Context

This plan outlines the architecture and implementation approach for a secure, authenticated backend API for task management that enforces strict per-user data ownership using JWT tokens and Neon Serverless PostgreSQL. The system will be built using Python FastAPI with SQLModel ORM for database operations.

### Architecture Components

- **Backend Framework**: Python FastAPI for RESTful API endpoints
- **ORM**: SQLModel for schema definitions and database operations
- **Database**: Neon Serverless PostgreSQL for persistent storage
- **Authentication**: JWT verification via dependency injection
- **Security**: Strict user identification from JWT claims, no trust of user_id from request

### Technology Stack Alignment

- **Backend**: Python FastAPI - RESTful API endpoints, business logic, and JWT authentication dependency
- **ORM**: SQLModel - Database schema management and object-relational mapping
- **Database**: Neon Serverless PostgreSQL - Persistent data storage with automatic scaling
- **Authentication**: JWT tokens - User identification and authorization via verified claims
- **Development Framework**: Claude Code + Spec-Kit Plus - Agentic development workflow

## Constitution Check

### I. Spec-Driven Development Compliance
- ✅ All implementation will derive strictly from written specifications
- ✅ Following Spec → Plan → Tasks → Code workflow using Agentic Dev Stack
- ✅ No manual coding - all development through specialized agents

### II. Agentic Workflow Purity
- ✅ Using specialized agents (Backend, DB)
- ✅ Prioritizing MCP tools and CLI commands for all operations
- ✅ Following agentic development patterns

### III. Security by Design
- ✅ JWT tokens required for all API access via Authorization: Bearer header
- ✅ Token verification handled via dependency injection using shared secret
- ✅ Task ownership validated on every read/write operation
- ✅ Requests without valid JWT return 401 Unauthorized
- ✅ Backend never trusts user_id from request body or URL - only from JWT claims

### IV. Deterministic Behavior
- ✅ RESTful API design conventions will be followed strictly
- ✅ API responses and state transitions will be predictable and consistent
- ✅ Standard HTTP status codes will be used (401, 403, 404)

### V. Production Realism
- ✅ Using real database (Neon PostgreSQL) with proper connection handling
- ✅ Environment configuration will be explicit and reproducible

### VI. Decoupled Architecture
- ✅ Backend API designed to be consumed by frontend applications
- ✅ Clear separation between auth, data, and route layers
- ✅ No direct database access from frontend (not applicable - this is backend only)

## Phase 0: Research & Unknown Resolution

### Decision: JWT dependency injection vs global middleware
- **Chosen**: JWT dependency injection at endpoint level
- **Rationale**: Provides granular control over authentication requirements per endpoint while maintaining clear separation of concerns. Allows endpoints to access user identity directly from the dependency.
- **Alternatives considered**: Global authentication middleware (would apply to all endpoints uniformly, less flexibility)

### Decision: SQLModel relationship strategy for task ownership
- **Chosen**: Foreign key relationship between User and Task entities
- **Rationale**: Enforces referential integrity at the database level and enables efficient querying with proper filtering
- **Alternatives considered**: Storing user_id as plain field without foreign key (less secure, no referential integrity)

### Decision: Database session lifecycle management
- **Chosen**: Session dependency injection per request
- **Rationale**: Ensures proper cleanup of database connections and follows FastAPI best practices for database session management
- **Alternatives considered**: Global session management (would complicate connection pooling and cleanup)

### Decision: Error response standardization strategy
- **Chosen**: Consistent error response format with standard HTTP status codes
- **Rationale**: Follows RESTful API conventions and is well-understood by API consumers
- **Alternatives considered**: Custom error formats (non-standard, harder for clients to handle)

### Decision: Endpoint structure and naming conventions
- **Chosen**: RESTful endpoint structure with consistent naming
- **Rationale**: Follows industry standards and makes the API intuitive to use
- **Alternatives considered**: Non-standard naming (would confuse API consumers)

## Phase 1: Design & Contracts

### Data Model

#### Task Entity
- `id`: UUID (primary key)
- `user_id`: UUID (foreign key to User, indexed, derived from JWT)
- `title`: String (task content, max 500 characters)
- `completed`: Boolean (completion status, default false)
- `created_at`: DateTime (timestamp, auto-populated)
- `updated_at`: DateTime (timestamp, auto-updated)

#### User (Referenced from JWT)
- `id`: UUID (derived from JWT claims, referenced by tasks)
- Authentication status: Validated JWT token

### API Contract Definitions

#### Task Management Endpoints

**GET /api/tasks**
- Description: Retrieve authenticated user's tasks
- Headers: `Authorization: Bearer {valid_jwt_token}`
- Response: `{ "tasks": [{ "id": "...", "title": "...", "completed": false, "created_at": "...", "updated_at": "..." }] }`
- Error: 401 (unauthorized - invalid/expired JWT)

**POST /api/tasks**
- Description: Create new task for authenticated user
- Headers: `Authorization: Bearer {valid_jwt_token}`
- Request: `{ "title": "New task title" }`
- Response: `{ "id": "...", "user_id": "...", "title": "New task title", "completed": false, "created_at": "...", "updated_at": "..." }`
- Error: 400 (invalid input), 401 (unauthorized)

**GET /api/tasks/{id}**
- Description: Retrieve specific task for authenticated user
- Headers: `Authorization: Bearer {valid_jwt_token}`
- Response: `{ "id": "...", "user_id": "...", "title": "Task title", "completed": false, "created_at": "...", "updated_at": "..." }`
- Error: 401 (unauthorized), 404 (task not found or not owned by user)

**PUT /api/tasks/{id}**
- Description: Update task for authenticated user
- Headers: `Authorization: Bearer {valid_jwt_token}`
- Request: `{ "title": "Updated task title", "completed": true }`
- Response: `{ "id": "...", "user_id": "...", "title": "Updated task title", "completed": true, "created_at": "...", "updated_at": "..." }`
- Error: 400 (invalid input), 401 (unauthorized), 404 (task not found or not owned by user)

**PATCH /api/tasks/{id}/complete**
- Description: Toggle task completion status for authenticated user
- Headers: `Authorization: Bearer {valid_jwt_token}`
- Response: `{ "success": true, "completed": true }`
- Error: 401 (unauthorized), 404 (task not found or not owned by user)

**DELETE /api/tasks/{id}**
- Description: Delete task for authenticated user
- Headers: `Authorization: Bearer {valid_jwt_token}`
- Response: `{ "success": true }`
- Error: 401 (unauthorized), 404 (task not found or not owned by user)

### Authentication and Authorization Flow

1. **JWT Token Validation**
   - All endpoints require valid JWT in Authorization header
   - Token is validated using shared secret
   - User identity is extracted from token claims

2. **User Identity Derivation**
   - User ID is extracted exclusively from JWT claims
   - Backend never trusts user_id from request body or URL
   - User context is passed to endpoints via dependency injection

3. **Task Ownership Enforcement**
   - All queries filter tasks by authenticated user's ID
   - Update/Delete operations verify task ownership before execution
   - Cross-user access attempts return 404 (not found) or 403 (forbidden)

### Task Lifecycle and Ownership Model

1. **Task Creation**
   - User sends POST request to `/api/tasks` with valid JWT
   - Backend validates JWT and extracts user ID from claims
   - New task is created with user_id set to authenticated user from JWT
   - Task is saved to database

2. **Task Retrieval**
   - User sends GET request to `/api/tasks` with valid JWT
   - Backend validates JWT and extracts user ID from claims
   - Only tasks with matching user_id are returned

3. **Task Update**
   - User sends PUT request to `/api/tasks/{id}` with valid JWT
   - Backend validates JWT and extracts user ID from claims
   - Backend verifies task belongs to user (user_id match) before update
   - Task is updated if ownership verified

4. **Task Deletion**
   - User sends DELETE request to `/api/tasks/{id}` with valid JWT
   - Backend validates JWT and extracts user ID from claims
   - Backend verifies task belongs to user (user_id match) before deletion
   - Task is deleted if ownership verified

## Phase 2: Implementation Approach

### Phase 2A: Data & Persistence Foundation
1. Set up database connection configuration for Neon Serverless PostgreSQL
2. Define SQLModel Task schema with proper fields and constraints
3. Implement database initialization and session management
4. Create database utility functions

### Phase 2B: Auth Enforcement Layer
1. Implement JWT verification dependency for FastAPI
2. Create user identity extraction from verified JWT token
3. Develop authentication middleware/dependency
4. Ensure all user identification comes from JWT claims only

### Phase 2C: Task API Implementation
1. Implement GET /api/tasks endpoint (user-scoped)
2. Implement POST /api/tasks endpoint (create task for user)
3. Implement GET /api/tasks/{id} endpoint (ownership enforced)
4. Implement PUT /api/tasks/{id} endpoint (update task)
5. Implement PATCH /api/tasks/{id}/complete endpoint (toggle completion)
6. Implement DELETE /api/tasks/{id} endpoint (delete task)
7. Implement consistent error responses (401, 403, 404)

### Phase 2D: Validation & Security Review
1. Validate all endpoints reject unauthenticated requests (401)
2. Verify authenticated users can only access their own tasks
3. Test cross-user access attempts and confirm denial (403/404)
4. Validate full CRUD lifecycle per user
5. Validate task persistence in Neon PostgreSQL

## Testing Strategy

### Auth Validation
- Requests without JWT return 401 Unauthorized
- Invalid JWT tokens return 401 Unauthorized
- Expired tokens return 401 Unauthorized

### Authorization Validation
- Cross-user access attempts return 404 (not found) or 403 (forbidden)
- Users can only access their own data
- Proper error responses for unauthorized access

### CRUD Validation
- Full task lifecycle (create, read, update, delete) per user
- Data persists across server restarts
- Validation rules enforced at API and database levels

### Security Validation
- Backend never trusts user_id from request body or URL
- All user identification comes from verified JWT claims
- Task ownership is validated on every operation

## Validation and Review Checklist

- [ ] All API endpoints properly authenticate requests
- [ ] User data isolation is enforced at backend level
- [ ] JWT tokens are properly validated
- [ ] SQLModel schemas include proper relationships
- [ ] Error handling follows standard HTTP status codes
- [ ] Backend never trusts user_id from request body or URL
- [ ] All user identification comes from verified JWT claims
- [ ] Cross-user access is prevented
- [ ] Database connections are handled safely and efficiently
- [ ] API contracts match implementation

## Re-evaluation of Constitution Check Post-Design

After designing the system architecture, all constitution principles remain satisfied:
- ✅ Spec-driven development: Architecture designed based on feature specification
- ✅ Agentic workflow purity: Implementation will use specialized agents
- ✅ Security by design: Strong authentication and authorization built into design
- ✅ Deterministic behavior: Well-defined API contracts and state transitions
- ✅ Production realism: Real technologies selected for production use
- ✅ Decoupled architecture: Clear separation between auth, data, and route layers