from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

# Use the database URL from environment, defaulting to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_chatbot.db")

# For SQLite, we need to add connect_args for proper threading
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False  # Required for SQLite

engine = create_engine(DATABASE_URL, poolclass=QueuePool, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session