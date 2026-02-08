# Quickstart Guide: AI Todo Chatbot (Spec 1: Chat Interface & Stateless Messaging)

**Feature**: 1-chat-interface
**Date**: 2026-02-04
**Version**: 1.0

## Overview
This guide provides the essential steps to set up and run the AI Todo Chatbot's conversational interface. The system implements a stateless design with persistent conversation storage in Neon PostgreSQL, integrated with the existing todo application architecture (Next.js frontend + FastAPI backend).

## Prerequisites
- Node.js 18+ for frontend development
- Python 3.11+ for backend development
- Neon PostgreSQL database instance
- Better Auth configured for JWT authentication (as used in existing system)
- OpenAI API key for agent functionality
- Git for version control

## Environment Setup

### 1. Navigate to Project Root
The chat interface integrates with the existing application structure:
```bash
cd [repository-directory]  # Already in the project root
```

### 2. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Install Frontend Dependencies
```bash
cd frontend
npm install
```

### 4. Set Up Environment Variables

#### Backend (.env) - Extends existing configuration
```bash
# Database Configuration (same as existing app)
DATABASE_URL="postgresql://username:password@ep-xxxxxx.us-east-1.aws.neon.tech/dbname?sslmode=require"

# Authentication (same as existing Better Auth)
AUTH_JWT_SECRET="your-jwt-secret-key"

# OpenAI Configuration for agent functionality
OPENAI_API_KEY="sk-your-openai-api-key"

# Server Configuration (same as existing app)
SERVER_HOST="0.0.0.0"
SERVER_PORT=8000
DEBUG=false
```

#### Frontend (.env.local) - Extends existing configuration
```bash
# Backend API URL (same as existing app)
NEXT_PUBLIC_API_BASE_URL="http://localhost:8000"

# Authentication (same as existing Better Auth)
NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:3000"
NEXT_PUBLIC_BETTER_AUTH_TOKEN="your-auth-token"

# Chat Configuration
NEXT_PUBLIC_CHAT_ENABLED=true
```

## Database Setup

### 1. Verify Neon PostgreSQL Database
The chat interface extends the existing database schema:
1. Ensure your existing Neon PostgreSQL database is set up
2. Verify your `.env` DATABASE_URL is properly configured

### 2. Run Database Migrations (extends existing tables)
```bash
cd backend
# Run existing migrations plus new conversation/message tables
python -m src.database  # Uses existing database setup in src/database.py
```

This will create the `conversations` and `messages` tables alongside the existing `tasks` and `users` tables with appropriate indexes and constraints.

## Running the Application

### 1. Start the Backend Server
```bash
cd backend
python -m src.main
```
The API will be available at `http://localhost:8000`, extending the existing API with new chat endpoints.

### 2. Start the Frontend Development Server
```bash
cd frontend
npm run dev
```
The application (including chat interface) will be available at `http://localhost:3000`.

### 3. Access the Chat Interface
1. Navigate to `http://localhost:3000`
2. Authenticate using your existing Better Auth credentials
3. Access the chat interface through the new navigation (likely in the dashboard area)
4. Start a conversation in the chat interface

## API Endpoints

### Extended API Routes
The chat interface extends the existing API structure:

#### Chat Endpoint
```
POST /api/{user_id}/chat
Authorization: Bearer {jwt_token} (using existing auth system)
Content-Type: application/json

Request Body:
{
  "message": "Your message here",
  "conversation_id": "optional_conversation_uuid"
}

Response:
{
  "response": "Assistant response",
  "conversation_id": "conversation_uuid"
}
```

#### Existing API Compatibility
The chat interface maintains compatibility with existing endpoints:
- `/api/` - existing task operations
- `/auth/` - existing authentication
- `/api/{user_id}/chat` - new chat endpoint

## Development Workflow

### Backend Development (extending existing patterns)
1. Add new functionality to existing modules in `backend/src/`
2. Create new files in appropriate directories (`models/`, `services/`, `api/`)
3. Follow existing patterns from task endpoints
4. Restart the server (`python -m src.main`) to see changes
5. Run tests: `pytest tests/`

### Frontend Development (extending existing patterns)
1. Add new components to `frontend/src/components/chat/`
2. Create new page in `frontend/src/app/chat/`
3. Follow existing component patterns from `src/components/ui/`
4. Changes will hot-reload automatically
5. Run tests: `npm test`

## Testing the Integrated Chat Interface

### 1. Basic Functionality Test
1. Log in to the application using existing auth system
2. Navigate to the chat interface
3. Send a message to the assistant
4. Verify the assistant responds appropriately
5. Check that the message appears in your conversation history

### 2. Conversation Persistence Test
1. Send multiple messages in a conversation
2. Refresh the page
3. Verify that your conversation history is preserved
4. Test that conversations survive server restarts

### 3. New Conversation Test
1. Click the "New Conversation" button
2. Verify you start with a clean conversation
3. Send messages and confirm they're in the new conversation
4. Switch between conversations to ensure isolation

### 4. Authentication Integration Test
1. Try to access the chat interface without authentication
2. Verify you're handled by the existing authentication system
3. Log in using existing credentials and confirm access to the chat interface
4. Test that user_id is properly validated in JWT and URL parameter

### 5. Integration with Existing Features
1. Verify existing task functionality still works
2. Test that chat interface doesn't interfere with dashboard or other pages
3. Confirm database operations don't conflict between systems

## Troubleshooting

### Common Integration Issues

#### Database Migration Errors
- Verify existing database is properly connected
- Check that new table creation doesn't conflict with existing tables
- Ensure foreign key relationships with existing User model work correctly

#### Authentication Issues
- Confirm JWT token format matches existing system
- Verify user_id extraction works with existing auth middleware
- Check that chat endpoints properly validate tokens using existing system

#### API Endpoint Conflicts
- Verify new `/api/{user_id}/chat` endpoint doesn't conflict with existing routes
- Check that existing task endpoints remain accessible
- Ensure proper URL parameter validation

#### Frontend Integration Problems
- Verify chat interface follows existing layout patterns
- Check that new components are properly styled with existing Tailwind
- Confirm navigation between existing pages and chat works properly

## Configuration Options

### Chat-Specific Settings
- `MAX_HISTORY_TOKENS`: Maximum tokens sent to agent (default: 4096)
- `CONVERSATION_TIMEOUT`: Timeout for agent responses (default: 30s)
- `MESSAGE_MAX_LENGTH`: Maximum character length for messages (default: 4000)

### Integration Settings
- Follow existing database connection pool settings from main app
- Use existing authentication timeout and validation rules
- Maintain consistent error handling with existing API

## Next Steps
- Implement MCP tools for todo operations (Spec 2)
- Add advanced conversation features
- Integrate with existing task management functionality
- Configure production deployment maintaining existing infrastructure

## Support
For assistance with setup or issues, consult the full documentation in the `docs/` directory or reach out to the development team. For integration-specific issues, refer to existing code patterns in the respective frontend and backend directories.