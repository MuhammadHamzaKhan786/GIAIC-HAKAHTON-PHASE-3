from sqlmodel import create_engine, Session
from typing import Optional
import os
from .models.task import Task  # Import the Task model from models folder


# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")  # Default to SQLite for testing
engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables():
    """Create database tables"""
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get database session"""
    with Session(engine) as session:
        yield session


# Only create tables on import if environment variable is set to do so
if os.getenv("CREATE_TABLES_ON_IMPORT", "true").lower() == "true":
    create_db_and_tables()