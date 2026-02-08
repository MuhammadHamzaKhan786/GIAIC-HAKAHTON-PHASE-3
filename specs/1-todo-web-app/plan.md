# Implementation Plan: Todo Full-Stack Web Application (Hackathon Phase-2)

## Technical Context

This plan outlines the architecture and implementation approach for transforming a console-based Todo application into a secure, multi-user web application with authentication, authorization, and persistent storage. The system will follow a microservices architecture with a Next.js frontend, FastAPI backend, and Neon PostgreSQL database, secured with Better Auth and JWT tokens.

### Architecture Components

- **Frontend**: Next.js 16+ App Router application with responsive UI
- **Backend**: Python FastAPI API with JWT authentication middleware
- **Authentication**: Better Auth service issuing JWT tokens
- **Database**: Neon Serverless PostgreSQL with SQLModel ORM
- **Security**: JWT-based authentication and user data isolation

### Technology Stack Alignment

- **Frontend**: Next.js 16+ (App Router) - Responsive UI components, client-side routing, and API integration
- **Backend**: Python FastAPI - RESTful API endpoints, business logic, and JWT authentication middleware
- **ORM**: SQLModel - Database schema management and object-relational mapping
- **Database**: Neon Serverless PostgreSQL - Persistent data storage with automatic scaling
- **Authentication**: Better Auth with JWT tokens - User signup/signin and session management

## Constitution Check

### I. Spec-Driven Development Compliance
- ✅ All implementation will derive strictly from written specifications
- ✅ Following Spec → Plan → Tasks → Code workflow using Agentic Dev Stack
- ✅ No manual coding - all development through specialized agents

### II. Agentic Workflow Purity
- ✅ Using specialized agents (Auth, Frontend, Backend, DB)
- ✅ Prioritizing MCP tools and CLI commands for all operations
- ✅ Following agentic development patterns

### III. Security by Design
- ✅ JWT tokens required for all API access via Authorization: Bearer header
- ✅ Token verification handled in backend middleware using shared secret
- ✅ Task ownership validated on every read/write operation
- ✅ Requests without valid JWT return 401 Unauthorized

### IV. Deterministic Behavior
- ✅ RESTful API design conventions will be followed strictly
- ✅ API responses and state transitions will be predictable and consistent

### V. Production Realism
- ✅ Using real database (Neon PostgreSQL) and real authentication (Better Auth)
- ✅ Environment configuration will be explicit and reproducible

### VI. Decoupled Architecture
- ✅ Frontend and backend will remain independent services
- ✅ Communication only through defined RESTful APIs
- ✅ No direct database access from frontend

## Phase 0: Research & Unknown Resolution

### Decision: JWT-based auth vs session-based auth
- **Chosen**: JWT for stateless backend
- **Rationale**: JWT tokens provide stateless authentication which scales better and aligns with microservices architecture. No server-side session storage needed.
- **Alternatives considered**: Session-based auth with server-side storage (requires session management infrastructure)

### Decision: Better Auth integration strategy with FastAPI
- **Chosen**: JWT token validation middleware in FastAPI
- **Rationale**: Better Auth can issue JWT tokens that can be validated by FastAPI backend using shared secrets
- **Alternatives considered**: Direct session integration (would require tighter coupling)

### Decision: User identity propagation method
- **Chosen**: Token claims extraction (vs URL params)
- **Rationale**: Extracting user ID from JWT claims is more secure than relying on URL parameters which can be manipulated
- **Alternatives considered**: Passing user ID in URL path (less secure, vulnerable to manipulation)

### Decision: SQLModel schema design for multi-user task isolation
- **Chosen**: Foreign key relationship between User and Task entities
- **Rationale**: Enforces referential integrity at the database level and enables efficient querying
- **Alternatives considered**: Storing user ID as plain field without foreign key (less secure, no referential integrity)

### Decision: Error-handling and status-code conventions
- **Chosen**: Standard HTTP status codes (401, 403, 404, 500)
- **Rationale**: Follows RESTful API conventions and is well-understood by clients
- **Alternatives considered**: Custom error codes (non-standard, harder for clients to handle)

## Phase 1: Design & Contracts

### Data Model

#### User Entity
- `id`: UUID (primary key)
- `email`: String (unique, indexed)
- `password_hash`: String (encrypted password)
- `created_at`: DateTime (timestamp)
- `updated_at`: DateTime (timestamp)

#### Task Entity
- `id`: UUID (primary key)
- `user_id`: UUID (foreign key to User, indexed)
- `title`: String (task content)
- `completed`: Boolean (completion status)
- `created_at`: DateTime (timestamp)
- `updated_at`: DateTime (timestamp)

### API Contract Definitions

#### Authentication Endpoints

**POST /auth/signup**
- Description: Create new user account
- Request: `{ "email": "user@example.com", "password": "secure_password" }`
- Response: `{ "success": true, "token": "jwt_token" }`
- Error: 400 (invalid input), 409 (email already exists)

**POST /auth/signin**
- Description: Authenticate user and return JWT token
- Request: `{ "email": "user@example.com", "password": "secure_password" }`
- Response: `{ "success": true, "token": "jwt_token" }`
- Error: 400 (invalid input), 401 (invalid credentials)

**POST /auth/signout**
- Description: Invalidate user session
- Headers: `Authorization: Bearer {token}`
- Response: `{ "success": true }`
- Error: 401 (unauthorized)

#### Task Management Endpoints

**GET /api/tasks**
- Description: Retrieve user's tasks
- Headers: `Authorization: Bearer {token}`
- Response: `{ "tasks": [{ "id": "...", "title": "...", "completed": false }] }`
- Error: 401 (unauthorized)

**POST /api/tasks**
- Description: Create new task for user
- Headers: `Authorization: Bearer {token}`
- Request: `{ "title": "New task" }`
- Response: `{ "task": { "id": "...", "title": "New task", "completed": false } }`
- Error: 400 (invalid input), 401 (unauthorized)

**PUT /api/tasks/{id}**
- Description: Update task for user
- Headers: `Authorization: Bearer {token}`
- Request: `{ "title": "Updated task", "completed": true }`
- Response: `{ "task": { "id": "...", "title": "Updated task", "completed": true } }`
- Error: 400 (invalid input), 401 (unauthorized), 404 (task not found)

**DELETE /api/tasks/{id}**
- Description: Delete task for user
- Headers: `Authorization: Bearer {token}`
- Response: `{ "success": true }`
- Error: 401 (unauthorized), 404 (task not found)

### Authentication and Authorization Flow

1. **User Registration**
   - User provides email and password
   - Better Auth creates user account
   - JWT token is issued and returned to client

2. **User Login**
   - User provides email and password
   - Better Auth validates credentials
   - JWT token is issued and returned to client

3. **API Access**
   - Client includes JWT in Authorization header
   - Backend middleware extracts and validates JWT
   - User ID is extracted from token claims
   - Request is processed with user context

4. **Authorization Check**
   - For each data operation, user ID from token is compared with data ownership
   - Only operations on user's own data are permitted
   - Cross-user access is blocked

### Task Lifecycle and Ownership Model

1. **Task Creation**
   - User sends POST request to `/api/tasks`
   - Backend validates JWT and extracts user ID
   - New task is created with user_id set to authenticated user
   - Task is saved to database

2. **Task Retrieval**
   - User sends GET request to `/api/tasks`
   - Backend validates JWT and extracts user ID
   - Only tasks with matching user_id are returned

3. **Task Update**
   - User sends PUT request to `/api/tasks/{id}`
   - Backend validates JWT and extracts user ID
   - Backend verifies task belongs to user (user_id match)
   - Task is updated if ownership verified

4. **Task Deletion**
   - User sends DELETE request to `/api/tasks/{id}`
   - Backend validates JWT and extracts user ID
   - Backend verifies task belongs to user (user_id match)
   - Task is deleted if ownership verified

## Phase 2: Implementation Approach

### Phase 2A: Identity & Security Foundation
1. Set up Better Auth with JWT configuration
2. Configure JWT secret and validation in FastAPI
3. Implement authentication middleware
4. Create User model with proper security practices

### Phase 2B: Backend API & Data Layer
1. Implement SQLModel models with proper relationships
2. Create FastAPI endpoints with authentication middleware
3. Implement authorization checks for data access
4. Set up Neon PostgreSQL connection

### Phase 2C: Frontend Integration & UX
1. Create Next.js App Router pages for auth and tasks
2. Implement JWT token storage and retrieval
3. Connect frontend to backend API endpoints
4. Create responsive UI for task management

### Phase 2D: End-to-End Validation & Review
1. Test complete user registration/login flow
2. Verify all CRUD operations work correctly
3. Validate cross-user data isolation
4. Test error handling and edge cases

## Testing Strategy

### Auth Validation
- Requests without JWT return 401 Unauthorized
- Invalid JWT tokens return 401 Unauthorized
- Expired tokens return 401 Unauthorized

### Authorization Validation
- Cross-user access attempts are blocked
- Users can only access their own data
- Proper error responses for unauthorized access

### CRUD Validation
- Full task lifecycle (create, read, update, delete) per user
- Data persists across server restarts
- Validation rules enforced at API and database levels

### Frontend Validation
- Responsive UI that works on various screen sizes
- Proper authenticated routing (protected routes)
- Error handling and user feedback

## Validation and Review Checklist

- [ ] All API endpoints properly authenticate requests
- [ ] User data isolation is enforced at backend level
- [ ] JWT tokens are properly validated
- [ ] SQLModel schemas include proper relationships
- [ ] Error handling follows standard HTTP status codes
- [ ] Frontend properly handles authentication state
- [ ] Cross-user access is prevented
- [ ] Database migrations work correctly
- [ ] API contracts match implementation
- [ ] All functionality works end-to-end

## Re-evaluation of Constitution Check Post-Design

After designing the system architecture, all constitution principles remain satisfied:
- ✅ Spec-driven development: Architecture designed based on feature specification
- ✅ Agentic workflow purity: Implementation will use specialized agents
- ✅ Security by design: Strong authentication and authorization built into design
- ✅ Deterministic behavior: Well-defined API contracts and state transitions
- ✅ Production realism: Real technologies selected for production use
- ✅ Decoupled architecture: Clear separation between frontend and backend