# Research Notes: AI Todo Chatbot (Spec 1: Chat Interface & Stateless Messaging)

**Feature**: 1-chat-interface
**Date**: 2026-02-04
**Researcher**: Claude Code

## Overview
This document captures research findings for implementing the conversational AI system with stateless design, focusing on technical feasibility and implementation approaches for the chat interface and messaging pipeline. This research builds upon the existing architecture with Next.js frontend and FastAPI backend.

## Frontend Research

### OpenAI ChatKit Integration with Existing Architecture
- OpenAI ChatKit provides pre-built UI components for conversational interfaces
- Must integrate with existing Next.js 16+ App Router structure
- Supports customizable styling compatible with existing Tailwind CSS
- Requires backend API endpoint to handle message processing
- Handles message bubbles, typing indicators, and scroll behavior automatically
- Needs proper API endpoint configuration for sending/receiving messages
- Should follow existing component patterns in src/components/ui/

### Authentication with Better Auth (Existing System)
- Leverage existing Better Auth integration from package.json
- Tokens are passed in Authorization header: "Bearer {token}" using existing auth patterns
- Frontend needs to store and include token with each API request
- Use existing authentication context from src/contexts/
- Token expiration handling required for seamless experience
- Unauthenticated users handled by existing middleware patterns

### Responsive Design with Existing Patterns
- Chat interface needs to adapt to various screen sizes using existing Tailwind patterns
- Mobile optimization important for touch targets and viewport handling
- Desktop experience should utilize full screen for conversation focus
- Need to consider keyboard accessibility following existing component patterns
- Leverage existing global styles from globals.css

## Backend Research

### FastAPI Integration with Existing Architecture
- Extend existing FastAPI application in src/main.py rather than creating new service
- Leverage existing database connection from src/database.py
- Use existing CORSMiddleware configuration
- Integrate new chat endpoints with existing router patterns in src/api/
- Follow existing startup procedures and table creation patterns
- Maintain consistency with existing API response formats

### Existing Model Integration
- Extend existing SQLModel setup from src/models/
- Create Conversation and Message models compatible with existing User/Task models
- Share same database connection pool and session patterns
- Use same authentication middleware patterns from src/auth/
- Follow existing model validation and relationship patterns

### JWT Authentication Middleware (Existing System)
- Use existing authentication system from src/auth/auth_bearer.py
- Extract user_id from existing JWT token format
- Verify token using existing validation patterns
- Return 401 for invalid tokens following existing error patterns
- Leverage existing dependency injection for auth checks

### OpenAI Agents SDK Integration
- Agent requires structured input for conversation context
- Need to format conversation history into agent-compatible format
- Agent responses need to be parsed and stored back to database using existing session patterns
- Error handling required for agent timeouts or failures
- Must follow existing service architecture patterns in src/services/

## Database Research

### Neon PostgreSQL with Existing Setup
- Leverage existing PostgreSQL connection from src/database.py
- Serverless PostgreSQL with auto-scaling capabilities
- Share connection pool with existing models (Task, User)
- Use existing migration and initialization patterns
- Leverage existing SQLModel configurations

### Conversation Schema Integration
- Conversation table needs user_id foreign key for isolation following existing patterns
- Created_at and updated_at timestamps for ordering using existing DateTime patterns
- Indexes required on user_id and timestamps for performance using existing patterns
- Need to consider data size limitations per conversation

### Message Schema Integration
- Role field to distinguish user vs assistant messages using existing String/Enum patterns
- Content field with appropriate size limits
- Foreign key linking to conversation using existing relationship patterns
- Timestamp for chronological ordering using existing DateTime patterns
- Indexes for efficient retrieval of conversation history using existing patterns

## Statelessness Implementation

### Session Management with Existing Patterns
- No in-memory session storage allowed (constitutional requirement)
- Each request must reconstruct conversation context from database
- Use existing database session patterns from existing endpoints
- Potential performance impact of frequent DB queries
- Need to balance consistency with performance

### Optimization Strategies
- Database indexing on conversation/user relationships following existing patterns
- Efficient query patterns to minimize DB load using existing select statements
- Consider pagination for very long conversations
- Leverage existing transaction patterns for consistency

## Security Considerations

### User Isolation with Existing Patterns
- All queries must filter by user_id using existing patterns from task endpoints
- Conversation access limited to owning user following existing access patterns
- API endpoint validation to prevent ID manipulation
- Proper error messages without information disclosure using existing HTTPException patterns
- Leverage existing ownership verification patterns

### Input Validation
- Sanitize user inputs before storing/displaying using existing validation
- Validate conversation_id format
- Rate limiting to prevent abuse
- Content length restrictions
- Use existing Pydantic model validation patterns

## API Design Integration

### Chat Endpoint Design
- Extend existing API router from src/api/router.py rather than creating new file
- POST /api/{user_id}/chat pattern allows for user context using existing auth patterns
- Request body includes message content and optional conversation_id
- Response includes assistant reply and conversation_id using existing response models
- HTTP status codes for different scenarios following existing patterns (200, 401, 500)

### Error Handling Consistency
- Consistent error response format following existing patterns
- Specific error codes for different failure modes
- Logging for debugging without exposing internal details using existing patterns
- Retry mechanisms where appropriate

## Testing Strategy

### Unit Testing Areas
- Authentication middleware validation using existing patterns
- Database model operations following existing patterns
- Message formatting functions
- API response formatting using existing patterns
- Service layer functions following existing patterns

### Integration Testing Areas
- End-to-end chat flow
- Authentication enforcement using existing patterns
- Conversation persistence
- Error scenario handling using existing patterns
- Integration with existing auth system

### Manual Testing Areas
- UI component behavior with existing patterns
- Mobile responsiveness using existing Tailwind patterns
- Authentication flow with existing system
- Message display and formatting with existing UI components
- Integration with existing dashboard/user flows

## Potential Risks

### Performance Risks
- Database queries on every request could slow response times
- Large conversation histories impacting performance
- Agent processing time affecting user experience
- Integration with existing system causing conflicts

### Scalability Risks
- High concurrent user load on stateless design
- Database connection limits with shared pool
- Agent API rate limits
- Existing system limitations affecting new features

### Security Risks
- User data leakage between accounts using existing patterns
- Authentication bypass possibilities through new endpoints
- Injection attacks through message content
- Integration points introducing vulnerabilities

## Next Steps

1. Analyze existing codebase structure in frontend/src/ and backend/src/
2. Extend existing database models in backend/src/models/ with Conversation and Message
3. Create new chat endpoint in backend/src/api/chat_router.py following existing patterns
4. Develop frontend chat page in frontend/src/app/chat/ following existing app structure
5. Integrate with existing authentication system
6. Test integration with existing services
7. Connect to OpenAI Agent implementation