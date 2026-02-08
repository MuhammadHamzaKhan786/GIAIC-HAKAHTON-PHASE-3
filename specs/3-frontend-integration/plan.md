# Implementation Plan: Spec-3 — Frontend Application & System Integration

## Technical Context

This plan outlines the architecture and implementation approach for a responsive frontend application that consumes the secured backend API using Next.js 16+ with App Router. The system will integrate Better Auth for user authentication and session management, providing a complete user-facing task management experience with seamless end-to-end integration across all system components.

### Architecture Components

- **Frontend Framework**: Next.js 16+ with App Router for responsive UI components and client-side routing
- **Authentication**: Better Auth with JWT issuance enabled for user signup/signin and session management
- **API Client**: Centralized API client handling authentication headers and data fetching
- **UI Components**: Responsive UI components for task management with clear separation of concerns
- **Routing**: Auth-protected routes enforcing user access

### Technology Stack Alignment

- **Frontend**: Next.js 16+ (App Router) - Responsive UI components, client-side routing, and API integration
- **Authentication**: Better Auth with JWT tokens - User signup/signin and session management
- **API Integration**: Centralized API client with authentication header management
- **Styling**: Tailwind CSS for responsive design across desktop and mobile
- **Development Framework**: Claude Code + Spec-Kit Plus - Agentic development workflow

## Constitution Check

### I. Spec-Driven Development Compliance
- ✅ All implementation will derive strictly from written specifications
- ✅ Following Spec → Plan → Tasks → Code workflow using Agentic Dev Stack
- ✅ No manual coding - all development through specialized agents

### II. Agentic Workflow Purity
- ✅ Using specialized agents (Frontend, Auth)
- ✅ Prioritizing MCP tools and CLI commands for all operations
- ✅ Following agentic development patterns

### III. Security by Design
- ✅ JWT tokens required for all API access via Authorization: Bearer header
- ✅ Frontend properly attaches JWT tokens to authenticated requests
- ✅ Unauthorized users redirected to authentication flows
- ✅ No hardcoded secrets in frontend code

### IV. Deterministic Behavior
- ✅ API responses and state transitions will be predictable and consistent
- ✅ Proper loading and error states will be implemented

### V. Production Realism
- ✅ Using real backend API endpoints with proper environment configuration
- ✅ Environment configuration will be explicit and reproducible

### VI. Decoupled Architecture
- ✅ Frontend remains an independent service communicating only through REST APIs
- ✅ No direct database access from frontend
- ✅ Clear separation between UI, auth, and data-fetching logic

## Phase 0: Research & Unknown Resolution

### Decision: Auth-aware routing strategy in Next.js App Router
- **Chosen**: Client-side authentication check with redirect to sign-in page
- **Rationale**: Provides better user experience by checking auth status on route change and redirecting unauthorized users to login. Works well with Next.js App Router's client-side navigation.
- **Alternatives considered**: Server-side auth checks (would require additional server-side logic)

### Decision: JWT storage and retrieval mechanism
- **Chosen**: Browser localStorage with secure handling
- **Rationale**: Provides persistent storage across browser sessions while maintaining security best practices. Easy to implement with proper cleanup on logout.
- **Alternatives considered**: Cookies (more complex to implement, potential CORS issues)

### Decision: Centralized API client vs per-component requests
- **Chosen**: Centralized API client handling authentication headers
- **Rationale**: Ensures consistent authentication header management across all API calls, easier to maintain and update, follows DRY principles.
- **Alternatives considered**: Per-component requests (would lead to code duplication and inconsistent auth handling)

### Decision: UI state management approach
- **Chosen**: React state hooks with context for global state
- **Rationale**: Leverages React's built-in state management capabilities while providing a clean way to share global state like authentication status.
- **Alternatives considered**: External state management libraries (would add unnecessary complexity for this use case)

### Decision: Error and loading UX conventions
- **Chosen**: Consistent loading spinners and toast notifications for errors
- **Rationale**: Provides immediate visual feedback to users during API operations and clear error messaging when operations fail.
- **Alternatives considered**: Inline error messages only (less prominent feedback)

## Phase 1: Design & Contracts

### Data Model

#### User Session Entity (Managed by Better Auth)
- **Authentication status**: Boolean (signed in/signed out)
- **JWT token**: String (stored securely in browser storage)
- **User profile**: Object (contains user information from auth provider)
- **Session state**: Enum (loading, authenticated, unauthenticated, error)

#### Task Entity (Consumed from Backend API)
- **id**: UUID (unique identifier)
- **title**: String (task content)
- **completed**: Boolean (completion status)
- **user_id**: UUID (owner identifier from JWT, not displayed to user)
- **created_at**: DateTime (creation timestamp)
- **updated_at**: DateTime (update timestamp)

#### UI State Entity
- **Current route**: String (active page)
- **Loading states**: Object (per-operation loading indicators)
- **Error states**: Object (per-operation error messages)
- **Form states**: Object (input validation and values)
- **Task list state**: Array (filtered and sorted tasks)

### API Contract Definitions

#### Authentication Endpoints (Handled by Better Auth)
- **POST /api/auth/register**: Create new user account
- **POST /api/auth/login**: Authenticate user and return JWT
- **POST /api/auth/logout**: Clear user session

#### Task Management Endpoints (Consumed from backend API)
- **GET /api/tasks**: Retrieve authenticated user's tasks
- **POST /api/tasks**: Create new task for authenticated user
- **GET /api/tasks/{id}**: Retrieve specific task for authenticated user
- **PUT /api/tasks/{id}**: Update task for authenticated user
- **DELETE /api/tasks/{id}**: Delete task for authenticated user
- **PATCH /api/tasks/{id}/complete**: Toggle task completion status

### Authentication Flow

1. **User Registration**
   - User navigates to registration page
   - Better Auth handles user creation and JWT issuance
   - JWT token is stored in browser localStorage
   - User is redirected to dashboard

2. **User Sign-In**
   - User navigates to sign-in page
   - Better Auth validates credentials and returns JWT
   - JWT token is stored in browser localStorage
   - User is redirected to dashboard

3. **Protected Route Access**
   - User attempts to access protected route
   - Client-side check verifies JWT existence and validity
   - If valid, user proceeds to route
   - If invalid/expired, user is redirected to sign-in

4. **API Request with Authentication**
   - Frontend prepares API request
   - JWT token is retrieved from localStorage
   - Authorization: Bearer header is added to request
   - Request is sent to backend API

### Task Management Flow

1. **Task Creation**
   - User enters task details in UI form
   - Form validation passes
   - POST request is sent to /api/tasks with JWT header
   - New task is added to UI upon successful response

2. **Task Viewing**
   - GET request is sent to /api/tasks with JWT header
   - Tasks are retrieved and displayed in UI
   - Loading states are shown during fetch

3. **Task Update**
   - User modifies task details in UI
   - PUT request is sent to /api/tasks/{id} with JWT header
   - Task is updated in UI upon successful response

4. **Task Deletion**
   - User triggers delete action in UI
   - DELETE request is sent to /api/tasks/{id} with JWT header
   - Task is removed from UI upon successful response

5. **Task Completion Toggle**
   - User toggles completion status in UI
   - PATCH request is sent to /api/tasks/{id}/complete with JWT header
   - Task status is updated in UI upon successful response

## Phase 2: Implementation Approach

### Phase 2A: Auth Integration & Routing
1. Integrate Better Auth with Next.js App Router
2. Implement protected route components
3. Create authentication context and hooks
4. Implement sign-in and sign-up pages
5. Implement authentication state management

### Phase 2B: API Client Foundation
1. Create centralized API client with authentication handling
2. Implement request/response interceptors for JWT headers
3. Add error handling and retry mechanisms
4. Create API service functions for all task operations
5. Implement loading and error state management

### Phase 2C: Task UI Implementation
1. Create dashboard layout with navigation
2. Implement task list component
3. Create task creation form
4. Implement task editing and deletion UI
5. Add task completion toggle functionality
6. Implement responsive design for all components

### Phase 2D: Integration & UX Validation
1. Validate authentication flow across all routes
2. Verify JWT tokens are attached to all API requests
3. Test full CRUD task lifecycle via UI
4. Confirm UI reflects backend-enforced user isolation
5. Validate responsive behavior across viewports
6. Test error handling and loading states

## Testing Strategy

### Auth Validation
- Unauthenticated users cannot access protected routes
- JWT tokens are properly attached to every API request
- Logout clears authentication state and redirects to sign-in
- Session expiration is handled gracefully

### Task Management Validation
- Full CRUD lifecycle works via UI components
- Task ownership is respected (backend enforces isolation)
- Real-time UI updates reflect backend changes
- Form validation prevents invalid submissions

### Responsive Design Validation
- UI adapts properly to different screen sizes
- Touch targets meet accessibility standards
- Layout remains functional on mobile devices
- Performance is acceptable across all viewports

### Error Handling Validation
- Network errors are properly caught and displayed
- API errors are communicated clearly to users
- Loading states provide feedback during operations
- Form errors guide users toward valid inputs

## Validation and Review Checklist

- [ ] Authentication flows work correctly across all pages
- [ ] JWT tokens are properly attached to API requests
- [ ] Protected routes redirect unauthorized users
- [ ] Task management CRUD operations work via UI
- [ ] UI accurately reflects task ownership and state
- [ ] Error handling provides clear user feedback
- [ ] Loading states improve perceived performance
- [ ] Responsive design works on all target devices
- [ ] API client centralizes authentication header management
- [ ] Frontend-backend integration works end-to-end

## Re-evaluation of Constitution Check Post-Design

After designing the system architecture, all constitution principles remain satisfied:
- ✅ Spec-driven development: Architecture designed based on feature specification
- ✅ Agentic workflow purity: Implementation will use specialized agents
- ✅ Security by design: Proper authentication and authorization handling built into design
- ✅ Deterministic behavior: Well-defined API contracts and state transitions
- ✅ Production realism: Real technologies selected for production use
- ✅ Decoupled architecture: Clear separation between frontend and backend services