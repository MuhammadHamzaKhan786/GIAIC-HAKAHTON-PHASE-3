import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect

# Load environment variables
load_dotenv(dotenv_path='./.env')

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("DATABASE_URL not found in environment variables")
    exit(1)

print(f"Connecting to database: {DATABASE_URL}")

try:
    # Create engine
    engine = create_engine(DATABASE_URL)

    # Create inspector to get table information
    inspector = inspect(engine)

    # Get list of table names
    table_names = inspector.get_table_names()

    print("\nTables in the database:")
    for i, table_name in enumerate(table_names, 1):
        print(f"{i}. {table_name}")

        # Get column information for each table
        columns = inspector.get_columns(table_name)
        print("   Columns:")
        for col in columns:
            print(f"     - {col['name']} ({col['type']})")
        print()

    if not table_names:
        print("No tables found in the database")

except Exception as e:
    print(f"Error connecting to database: {str(e)}")