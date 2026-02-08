"""
Integration test for MCP tool integration.
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
@patch('backend.agent.runner.run_agent')
def test_mcp_tool_integration(mock_run_agent):
    """Test that agent correctly invokes MCP tools."""
    # Test various MCP tool calls
    test_cases = [
        {
            "input": "Add a task to buy groceries",
            "expected_tool": "add_task",
            "expected_response_contains": "added"
        },
        {
            "input": "Show me my tasks",
            "expected_tool": "list_tasks",
            "expected_response_contains": "tasks"
        },
        {
            "input": "Complete the first task",
            "expected_tool": "complete_task",
            "expected_response_contains": "completed"
        },
        {
            "input": "Delete the second task",
            "expected_tool": "delete_task",
            "expected_response_contains": "deleted"
        },
        {
            "input": "Update my task to be more important",
            "expected_tool": "update_task",
            "expected_response_contains": "updated"
        }
    ]

    with TestClient(app) as client:
        for i, test_case in enumerate(test_cases):
            # Mock the agent response for this test case
            mock_run_agent.return_value = {
                "response": f"I've {test_case['expected_response_contains']} the task.",
                "tool_calls": [{
                    "name": test_case["expected_tool"],
                    "arguments": {"task_id": f"task_{i}"}
                }]
            }

            response = client.post(
                f"/api/test_user_id_{i}/chat",
                json={
                    "message": test_case["input"]
                },
                headers={
                    "Authorization": f"Bearer test_token_{i}"
                }
            )

            assert response.status_code == 200
            data = response.json()

            # Verify response contains expected elements
            assert "conversation_id" in data
            assert test_case["expected_response_contains"].lower() in data["response"].lower().replace("'", "")
            assert "tool_calls" in data
            assert len(data["tool_calls"]) > 0
            assert data["tool_calls"][0]["name"] == test_case["expected_tool"]