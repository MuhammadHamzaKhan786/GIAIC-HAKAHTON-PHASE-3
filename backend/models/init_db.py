from sqlalchemy import create_engine
from sqlmodel import SQLModel
from .conversation import Conversation
from .message import Message
import os


def create_db_and_tables():
    """Create database tables for Conversation and Message."""
    database_url = os.getenv("DATABASE_URL", "sqlite:///todo_app.db")
    engine = create_engine(database_url)

    # Create all tables
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()