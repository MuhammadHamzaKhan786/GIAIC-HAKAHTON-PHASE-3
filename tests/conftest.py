"""
Pytest configuration for MCP Task Server tests
"""
import pytest
import sys
import os

# Add the backend directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment variables"""
    os.environ['MOCK_USER_ID'] = 'test_user_123'
    os.environ['JWT_SECRET_KEY'] = 'test_secret_key'
    os.environ['DATABASE_URL'] = 'sqlite:///./test.db'

    yield

    # Clean up environment variables after tests
    if 'MOCK_USER_ID' in os.environ:
        del os.environ['MOCK_USER_ID']
    if 'JWT_SECRET_KEY' in os.environ:
        del os.environ['JWT_SECRET_KEY']
    if 'DATABASE_URL' in os.environ:
        del os.environ['DATABASE_URL']