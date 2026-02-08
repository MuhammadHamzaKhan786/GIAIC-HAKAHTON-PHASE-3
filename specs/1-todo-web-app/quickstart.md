# Quickstart Guide: Todo Full-Stack Web Application

## Development Setup

### Prerequisites
- Node.js 18+ for Next.js frontend
- Python 3.9+ for FastAPI backend
- PostgreSQL-compatible database (Neon Serverless recommended)
- Better Auth account or local setup

### Environment Variables
Create `.env` files for both frontend and backend with these variables:

**Frontend (.env.local):**
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
```

**Backend (.env):**
```
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
JWT_SECRET=your-super-secret-jwt-key-here
BETTER_AUTH_SECRET=your-better-auth-secret
```

## Project Structure
```
todo-fullstack-app/
├── frontend/                 # Next.js application
│   ├── app/                  # App Router pages
│   ├── components/          # Reusable UI components
│   ├── lib/                 # Utilities and API calls
│   └── public/              # Static assets
├── backend/                 # FastAPI application
│   ├── api/                 # API route definitions
│   ├── models/              # SQLModel database models
│   ├── auth/                # Authentication middleware
│   └── database/            # Database connection and setup
└── docs/                    # Documentation
```

## Running the Application

### Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up database: `python -m database.init`
4. Run the server: `uvicorn main:app --reload`

### Frontend Setup
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Run the development server: `npm run dev`

## Development Workflow

### Creating New Features
1. Update the specification in `specs/1-todo-web-app/spec.md`
2. Run `/sp.plan` to update the implementation plan
3. Run `/sp.tasks` to generate development tasks
4. Implement tasks using appropriate agents (Auth, Frontend, Backend, DB)

### API Development
1. Update the API contract in `specs/1-todo-web-app/contracts/api-contract.yaml`
2. Implement the corresponding backend endpoints
3. Update frontend API calls to match the contract
4. Test with the API documentation at `/docs`

### Database Changes
1. Update the data model in `specs/1-todo-web-app/data-model.md`
2. Modify the SQLModel models in the backend
3. Generate and run migrations
4. Update frontend to handle any new fields

## Authentication Flow
1. User registers via `/auth/signup` or signs in via `/auth/signin`
2. Better Auth returns JWT token
3. Frontend stores token in secure storage
4. All API requests include `Authorization: Bearer {token}` header
5. Backend validates token and extracts user ID
6. User-specific data is accessed based on validated user ID

## Testing Guidelines
- Write unit tests for all API endpoints
- Test authentication and authorization for each endpoint
- Verify cross-user data isolation
- Test error handling and edge cases
- Validate API contract compliance

## Common Commands
- `npm run dev` - Start frontend development server
- `uvicorn main:app --reload` - Start backend development server
- `npm test` - Run frontend tests
- `pytest` - Run backend tests
- `npm run lint` - Lint frontend code
- `flake8 .` - Lint backend code