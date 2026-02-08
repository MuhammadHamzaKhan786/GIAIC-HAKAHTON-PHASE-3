"""
Integration test for conversation persistence.
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.models.conversation import Conversation
from backend.models.message import Message
from backend.database import get_session
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
@patch('backend.agent.runner.run_agent')
def test_conversation_persistence(mock_run_agent):
    """Test that conversations persist across requests."""
    # Mock agent responses
    def mock_run_agent_side_effect(messages, user_id):
        if len(messages) == 1:  # First message
            return {
                "response": "I've added the task.",
                "tool_calls": [{"name": "add_task", "arguments": {"task": "test task"}}]
            }
        else:  # Subsequent message
            return {
                "response": "Here are your tasks.",
                "tool_calls": [{"name": "list_tasks", "arguments": {}}]
            }

    mock_run_agent.side_effect = mock_run_agent_side_effect

    # Use TestClient
    with TestClient(app) as client:
        # First request - create conversation
        response1 = client.post(
            "/api/test_user_id/chat",
            json={
                "message": "Add a task to test persistence"
            },
            headers={
                "Authorization": "Bearer test_token"
            }
        )

        assert response1.status_code == 200
        data1 = response1.json()
        conversation_id = data1["conversation_id"]
        assert conversation_id is not None

        # Second request - continue same conversation
        response2 = client.post(
            "/api/test_user_id/chat",
            json={
                "conversation_id": conversation_id,
                "message": "What tasks do I have?"
            },
            headers={
                "Authorization": "Bearer test_token"
            }
        )

        assert response2.status_code == 200
        data2 = response2.json()
        assert data2["conversation_id"] == conversation_id  # Same conversation continued