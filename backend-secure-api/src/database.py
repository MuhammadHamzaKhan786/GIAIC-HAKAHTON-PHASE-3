from sqlalchemy import create_engine
from sqlmodel import SQLModel
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Use the database URL directly
if DATABASE_URL:
    database_url = DATABASE_URL
else:
    # Use a default SQLite URL for development if no DATABASE_URL is provided
    database_url = "sqlite:///./secure_tasks.db"

engine = create_engine(database_url, poolclass=QueuePool)