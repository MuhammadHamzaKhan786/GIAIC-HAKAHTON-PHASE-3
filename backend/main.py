from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from backend.api.chat import router as chat_router
from backend.src.auth.router import router as auth_router
from backend.models.init_db import create_db_and_tables
from backend.database import engine
from sqlmodel import SQLModel
import uvicorn


app = FastAPI(title="Todo AI Chatbot with MCP Integration")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001", "*"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    # Create database tables
    create_db_and_tables()


# Include the auth router
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Include the chat router
app.include_router(chat_router, prefix="/api", tags=["chat"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo AI Chatbot API!"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "todo-ai-chatbot"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)