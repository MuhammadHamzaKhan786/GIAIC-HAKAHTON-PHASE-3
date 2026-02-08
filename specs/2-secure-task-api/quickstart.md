# Quickstart Guide: Spec-2 — Secure Backend Task Management API

## Development Setup

### Prerequisites
- Python 3.9+ for FastAPI backend
- PostgreSQL-compatible database (Neon Serverless recommended)
- JWT authentication system that generates valid tokens

### Environment Variables
Create a `.env` file in the backend directory with these variables:

```
DATABASE_URL=postgresql://username:password@localhost:5432/task_management_db
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
BETTER_AUTH_SECRET=your-better-auth-secret
```

## Project Structure
```
secure-task-api/
├── backend/                 # FastAPI application
│   ├── src/                 # Source code
│   │   ├── api/             # API route definitions
│   │   ├── models/          # SQLModel database models
│   │   ├── auth/            # Authentication dependencies
│   │   ├── database/        # Database connection and session management
│   │   └── main.py          # Application entry point
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables
└── docs/                    # API documentation
```

## Running the Application

### Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in `.env` file
4. Run the server: `uvicorn src.main:app --reload`

## Development Workflow

### Creating New Features
1. Update the specification in `specs/2-secure-task-api/spec.md`
2. Run `/sp.plan` to update the implementation plan
3. Run `/sp.tasks` to generate development tasks
4. Implement tasks using appropriate agents (Backend, DB)

### API Development
1. Update the API contract in `specs/2-secure-task-api/contracts/api-contract.yaml`
2. Implement the corresponding backend endpoints
3. Test with the API documentation at `/docs`

### Database Changes
1. Update the data model in `specs/2-secure-task-api/data-model.md`
2. Modify the SQLModel models in the backend
3. Generate and run migrations
4. Update any dependent services

## Authentication Flow
1. External authentication system generates JWT token with user ID in "sub" claim
2. Client includes token in `Authorization: Bearer {token}` header
3. Backend validates token and extracts user ID from claims
4. All database operations filter by user ID from JWT
5. Cross-user access is prevented by design

## Security Guidelines
- Never trust user_id from request body or URL
- Always derive user identity from JWT claims
- Validate JWT token on every authenticated request
- Filter all queries by authenticated user ID
- Return 401 for invalid tokens, 404 for unauthorized access

## Testing Guidelines
- Test all endpoints reject requests without valid JWT
- Verify authenticated users can only access their own tasks
- Test cross-user access attempts are properly denied
- Validate full CRUD lifecycle for each user
- Test error handling and edge cases

## Common Commands
- `uvicorn src.main:app --reload` - Start development server
- `pytest` - Run backend tests
- `flake8 .` - Lint backend code
- `black .` - Format Python code