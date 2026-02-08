"""
Initialize OpenAI Agent with MCP tools and system prompt.
"""
from openai import OpenAI
from .prompts import AGENT_SYSTEM_PROMPT
from ..services.mcp_client import mcp_client
import json
import os


def create_tools_list():
    """Create the list of available tools for the OpenAI agent."""
    tools = [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Add a new task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task": {"type": "string", "description": "The task to add"},
                        "user_id": {"type": "string", "description": "The user ID"}
                    },
                    "required": ["task", "user_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "List all current tasks for a user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user ID"}
                    },
                    "required": ["user_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Mark a task as complete",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The ID of the task to complete"},
                        "user_id": {"type": "string", "description": "The user ID"}
                    },
                    "required": ["task_id", "user_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Delete a task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The ID of the task to delete"},
                        "user_id": {"type": "string", "description": "The user ID"}
                    },
                    "required": ["task_id", "user_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update a task's content",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The ID of the task to update"},
                        "new_content": {"type": "string", "description": "The new content for the task"},
                        "user_id": {"type": "string", "description": "The user ID"}
                    },
                    "required": ["task_id", "new_content", "user_id"]
                }
            }
        }
    ]
    return tools


def create_agent():
    """Initialize and return an OpenAI Agent with MCP tools and system prompt."""
    api_key = os.getenv("OPENAI_API_KEY")

    print(f"DEBUG: OpenAI API key available: {'Yes' if api_key else 'No'}")

    if not api_key:
        # Return a mock agent for development/testing when API key is not available
        class MockAgent:
            def __init__(self):
                self.id = "mock-assistant-id"

        class MockClient:
            def beta(self):
                pass

        print("DEBUG: Using mock agent due to missing API key")
        return MockAgent(), MockClient()

    try:
        client = OpenAI(api_key=api_key)

        # Create the agent with tools and system prompt
        agent = client.beta.assistants.create(
            name="Todo Assistant",
            instructions=AGENT_SYSTEM_PROMPT,
            model="gpt-4-turbo-preview",  # Changed from gpt-4.1-mini which may not exist
            tools=create_tools_list()
        )

        print(f"DEBUG: OpenAI agent created successfully with ID: {getattr(agent, 'id', 'unknown')}")
        return agent, client
    except Exception as e:
        print(f"DEBUG: Error creating OpenAI agent: {str(e)}")

        # Return a mock agent if OpenAI fails
        class MockAgent:
            def __init__(self):
                self.id = "mock-assistant-id"

        class MockClient:
            def beta(self):
                pass

        print("DEBUG: Falling back to mock agent due to OpenAI error")
        return MockAgent(), MockClient()