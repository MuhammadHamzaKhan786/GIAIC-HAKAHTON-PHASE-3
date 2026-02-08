# Quickstart Guide: Spec-3 — Frontend Application & System Integration

## Development Setup

### Prerequisites
- Node.js 18+ for Next.js frontend
- A running backend API server with the task management endpoints
- Better Auth configured for user authentication
- Access to the Neon PostgreSQL database through the backend

### Environment Variables
Create a `.env.local` file in the frontend directory with these variables:

```
NEXT_PUBLIC_API_BASE_URL=https://your-backend-api.com
NEXT_PUBLIC_BETTER_AUTH_URL=https://your-better-auth.com
NEXTAUTH_SECRET=your-nextauth-secret
NEXTAUTH_URL=http://localhost:3000
```

## Project Structure
```
frontend-app/
├── src/
│   ├── app/                 # App Router pages and layouts
│   │   ├── layout.tsx       # Root layout component
│   │   ├── page.tsx         # Home page
│   │   ├── signin/          # Sign-in page
│   │   ├── signup/          # Sign-up page
│   │   ├── dashboard/       # Protected dashboard page
│   │   └── globals.css      # Global styles
│   ├── components/          # Reusable UI components
│   │   ├── auth/            # Authentication components
│   │   ├── tasks/           # Task management components
│   │   └── ui/              # Base UI components
│   ├── lib/                 # Utility functions and API client
│   │   ├── auth.ts          # Authentication utilities
│   │   ├── api.ts           # Centralized API client
│   │   └── utils.ts         # General utilities
│   └── contexts/            # React context providers
│       └── auth-context.ts  # Authentication state context
├── public/                  # Static assets
├── package.json             # Project dependencies
└── next.config.js           # Next.js configuration
```

## Running the Application

### Frontend Setup
1. Navigate to the frontend directory: `cd frontend-app`
2. Install dependencies: `npm install`
3. Create environment variables file: `.env.local`
4. Run the development server: `npm run dev`

## Development Workflow

### Creating New Features
1. Update the specification in `specs/3-frontend-integration/spec.md`
2. Run `/sp.plan` to update the implementation plan
3. Run `/sp.tasks` to generate development tasks
4. Implement tasks using appropriate agents (Frontend, Auth)

### Authentication Integration
1. Configure Better Auth with your Next.js application
2. Set up protected routes using authentication context
3. Implement sign-in and sign-up flows
4. Test authentication state management

### API Integration
1. Update the API client in `src/lib/api.ts` for new endpoints
2. Create service functions for API operations
3. Integrate API calls into components
4. Handle loading and error states appropriately

## Authentication Flow
1. User visits protected route
2. Authentication context checks for valid JWT token
3. If no valid token, user is redirected to sign-in page
4. User enters credentials and submits form
5. Better Auth validates credentials and returns JWT
6. JWT token is stored in browser storage
7. User is redirected to requested route
8. All API requests include Authorization header with JWT

## UI State Management
- Authentication state managed by React context
- Task data fetched from backend API
- Loading and error states managed per operation
- Form states managed by individual components
- Global state changes propagated via context

## Testing Guidelines
- Test authentication flows across all protected routes
- Verify JWT tokens are attached to all authenticated requests
- Test full CRUD lifecycle for tasks
- Validate responsive behavior across screen sizes
- Test error handling and loading states
- Verify user isolation (users can't access other users' tasks)

## Common Commands
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run code linting
- `npm test` - Run tests (if implemented)