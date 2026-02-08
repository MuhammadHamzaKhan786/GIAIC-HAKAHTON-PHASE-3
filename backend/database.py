from sqlmodel import create_engine, Session
from typing import Generator
import os


# Create the database engine
database_url = os.getenv("DATABASE_URL", "sqlite:///todo_app.db")

# For SQLite, we need to add connect_args for proper threading
if database_url.startswith("sqlite"):
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},  # Required for SQLite
    )
else:
    engine = create_engine(database_url)


def get_session() -> Generator[Session, None, None]:
    """Get a database session."""
    with Session(engine) as session:
        yield session