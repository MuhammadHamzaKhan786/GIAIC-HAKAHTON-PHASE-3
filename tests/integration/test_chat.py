"""
Integration test for chat functionality.
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.models.init_db import create_db_and_tables
from unittest.mock import patch, AsyncMock


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.mark.asyncio
@patch('backend.agent.runner.run_agent')
def test_chat_functionality(mock_run_agent, client):
    """Test that chat functionality works end-to-end."""
    # Mock the agent response
    mock_run_agent.return_value = {
        "response": "I've added the task to buy groceries.",
        "tool_calls": [{"name": "add_task", "arguments": {"task": "buy groceries"}}]
    }

    # Make a request to the chat endpoint
    response = client.post(
        "/api/test_user_id/chat",
        json={
            "message": "Add a task to buy groceries"
        },
        headers={
            "Authorization": "Bearer test_token"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "conversation_id" in data
    assert "response" in data
    assert "tool_calls" in data
    assert isinstance(data["tool_calls"], list)