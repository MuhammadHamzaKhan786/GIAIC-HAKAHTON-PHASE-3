# TaskFlow AI - Conversational Task Management

A modern full-stack web application featuring an authenticated conversational AI assistant that enables users to manage tasks and interact with an intelligent chatbot while persisting conversation history.

![Next.js](https://img.shields.io/badge/Next.js-16-black?style=flat-square&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-white?style=flat-square&logo=fastapi)
![TypeScript](https://img.shields.io/badge/TypeScript-5.9-blue?style=flat-square&logo=typescript)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-blueviolet?style=flat-square&logo=postgresql)

## 🌟 Features

### Authentication System
- Secure JWT-based authentication
- User registration and login flows
- Protected routes requiring valid tokens
- Automatic redirect to login when unauthenticated
- Token expiration handling

### Task Management
- Create, read, update, delete tasks
- Mark tasks as complete/incomplete
- Task ownership enforcement (users only see their own tasks)
- Responsive task list with visual status indicators

### Conversational AI Interface
- Real-time chat interface with AI assistant
- Persistent conversation history stored in database
- Stateful conversations that survive page refreshes
- Support for multiple concurrent conversations per user
- Typing indicators during AI processing

### Responsive Design
- Mobile-first approach with progressive enhancement
- Adapts seamlessly to mobile, tablet, and desktop screens
- Touch-friendly inputs and buttons optimized for mobile devices
- Unified light theme with soft backgrounds

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Frontend     │────▶│   Backend API   │────▶│   Database      │
│   (Next.js)    │◀────│   (FastAPI)     │◀────│   (Neon Postgres)│
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Technology Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Next.js 16+ (App Router), TypeScript, Tailwind CSS |
| **Backend** | FastAPI, Python 3.9+ |
| **Database** | Neon Serverless PostgreSQL, SQLModel ORM |
| **Authentication** | JWT (JSON Web Tokens), Better Auth |
| **Migrations** | Alembic |

## 📁 Project Structure

```
├── backend/                    # FastAPI backend
│   ├── src/
│   │   ├── api/               # API routes
│   │   │   ├── chat_router.py # Chat endpoints
│   │   │   └── router.py     # Main router
│   │   ├── models/           # Database models
│   │   │   ├── conversation.py
│   │   │   ├── message.py
│   │   │   ├── task.py
│   │   │   └── user.py
│   │   ├── auth/             # Authentication
│   │   │   ├── auth_bearer.py
│   │   │   ├── jwt_handler.py
│   │   │   └── router.py
│   │   └── database/        # DB configuration
│   ├── alembic/              # Database migrations
│   ├── agent/                # AI agent logic
│   ├── mcp/                  # Model Context Protocol
│   ├── main.py               # Entry point
│   └── requirements.txt
│
├── frontend/                  # Next.js frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── chat/         # Chat interface
│   │   │   ├── dashboard/    # Task dashboard
│   │   │   ├── signin/       # Login page
│   │   │   └── signup/       # Registration page
│   │   ├── components/
│   │   │   ├── chat/         # Chat components
│   │   │   └── ui/           # Reusable UI
│   │   ├── contexts/         # React contexts
│   │   └── lib/              # Utilities
│   ├── package.json
│   └── tailwind.config.js
│
└── README.md                 # This file
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- Python 3.9+
- PostgreSQL database (Neon recommended)
- npm or yarn

### Environment Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd todo-cli/phase-III
   ```

2. **Configure Backend:**
   
   Create `backend/.env`:
   ```env
   DATABASE_URL=postgresql://user:password@host/database
   SECRET_KEY=your-secret-key-change-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

3. **Configure Frontend:**
   
   Create `frontend/.env.local`:
   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   ```

### Installation

**Backend:**
```bash
cd backend
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start server
cd src
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/signup` | Register new user |
| POST | `/api/auth/signin` | Login user |

### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | Get all user tasks |
| POST | `/api/{user_id}/tasks` | Create new task |
| PUT | `/api/{user_id}/tasks/{task_id}` | Update task |
| DELETE | `/api/{user_id}/tasks/{task_id}` | Delete task |

### Chat
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/{user_id}/chat` | Send message to AI assistant |

## 🔐 Security Features

- JWT token verification for all protected routes
- User ID validation against token claims
- Foreign key constraints preventing unauthorized access
- Input validation for all user inputs
- Password hashing with bcrypt
- Environment-based secret management

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📄 License

MIT License - feel free to use this project for your own purposes.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

Built with ❤️ using Next.js and FastAPI
