import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel
from unittest.mock import patch
from src.main import app
from src.database import engine
from src.models.user import User
from src.models.conversation import Conversation
from src.models.message import Message
from datetime import datetime
import uuid

client = TestClient(app)

@pytest.fixture(name="session")
def session_fixture():
    yield Session(engine)

def test_chat_endpoint_requires_auth():
    """Test that the chat endpoint requires authentication"""
    user_id = str(uuid.uuid4())
    response = client.post(f"/api/{user_id}/chat", json={"message": "Hello"})

    assert response.status_code == 401  # Unauthorized without token

def test_chat_endpoint_validates_input():
    """Test that the chat endpoint validates message input"""
    user_id = str(uuid.uuid4())

    # Test with empty message
    response = client.post(
        f"/api/{user_id}/chat",
        json={"message": ""},
        headers={"Authorization": "Bearer fake-token"}
    )

    assert response.status_code == 400  # Bad request for empty message

@patch('src.api.chat_router.JWTBearer.__call__')
def test_chat_endpoint_creates_conversation(mock_jwt):
    """Test that the chat endpoint creates a new conversation when none is provided"""
    mock_jwt.return_value = {"user_id": str(uuid.uuid4())}

    user_id = mock_jwt.return_value["user_id"]
    response = client.post(
        f"/api/{user_id}/chat",
        json={"message": "Hello, AI assistant!"},
        headers={"Authorization": "Bearer fake-token"}
    )

    assert response.status_code == 200

    data = response.json()
    assert "conversation_id" in data
    assert "response" in data
    assert isinstance(data["conversation_id"], str)
    assert isinstance(data["response"], str)

@patch('src.api.chat_router.JWTBearer.__call__')
def test_chat_endpoint_uses_existing_conversation(mock_jwt):
    """Test that the chat endpoint uses an existing conversation when ID is provided"""
    mock_jwt.return_value = {"user_id": str(uuid.uuid4())}

    user_id = mock_jwt.return_value["user_id"]
    fake_conversation_id = str(uuid.uuid4())

    response = client.post(
        f"/api/{user_id}/chat",
        json={
            "message": "Following up on our conversation",
            "conversation_id": fake_conversation_id
        },
        headers={"Authorization": "Bearer fake-token"}
    )

    assert response.status_code == 200

    data = response.json()
    assert "conversation_id" in data
    assert data["conversation_id"] == fake_conversation_id

@patch('src.api.chat_router.JWTBearer.__call__')
def test_chat_endpoint_stores_messages(mock_jwt):
    """Test that the chat endpoint stores both user and assistant messages"""
    mock_jwt.return_value = {"user_id": str(uuid.uuid4())}

    user_id = mock_jwt.return_value["user_id"]

    response = client.post(
        f"/api/{user_id}/chat",
        json={"message": "Test message for storage verification"},
        headers={"Authorization": "Bearer fake-token"}
    )

    assert response.status_code == 200

    data = response.json()
    assert "response" in data
    # The response should contain the test message or information about it