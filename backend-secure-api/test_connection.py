import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"DATABASE_URL: {DATABASE_URL}")

if DATABASE_URL:
    try:
        # Test the connection string
        engine = create_engine(DATABASE_URL, poolclass=QueuePool)
        print("Engine created successfully!")

        # Test the connection
        with engine.connect() as conn:
            print("Connection successful!")

        # Import and create tables
        from src.models.task import Task
        from sqlmodel import SQLModel
        SQLModel.metadata.create_all(bind=engine)
        print("Tables created successfully!")

    except Exception as e:
        print(f"Error: {e}")
else:
    print("DATABASE_URL not found")