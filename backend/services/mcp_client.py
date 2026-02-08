"""
MCP Client wrapper to connect to MCP server and expose task management functions.
Each function accepts params, calls MCP server, and returns structured result.
No local state is maintained.
"""
import asyncio
from typing import Dict, Any, Optional
import httpx


class MCPTaskClient:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or "http://localhost:8000"  # Default to localhost
        self.client = httpx.AsyncClient(timeout=30.0)

    async def add_task(self, task: str, user_id: str = None) -> Dict[str, Any]:
        """Add a new task via MCP server."""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/add_task",
                json={
                    "task": task,
                    "user_id": user_id
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "task_id": None
            }

    async def list_tasks(self, user_id: str = None) -> Dict[str, Any]:
        """List all tasks via MCP server."""
        try:
            url = f"{self.base_url}/api/list_tasks"
            if user_id:
                url += f"?user_id={user_id}"
            response = await self.client.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "tasks": []
            }

    async def complete_task(self, task_id: str, user_id: str = None) -> Dict[str, Any]:
        """Complete a task via MCP server."""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/complete_task",
                json={
                    "task_id": task_id,
                    "user_id": user_id
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Could not find that task. Please check your list of tasks."
            }

    async def delete_task(self, task_id: str, user_id: str = None) -> Dict[str, Any]:
        """Delete a task via MCP server."""
        try:
            response = await self.client.delete(
                f"{self.base_url}/api/delete_task",
                json={
                    "task_id": task_id,
                    "user_id": user_id
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Could not find that task. Please check your list of tasks."
            }

    async def update_task(self, task_id: str, new_content: str = None, user_id: str = None) -> Dict[str, Any]:
        """Update a task via MCP server."""
        try:
            response = await self.client.put(
                f"{self.base_url}/api/update_task",
                json={
                    "task_id": task_id,
                    "new_content": new_content,
                    "user_id": user_id
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Could not find that task. Please check your list of tasks."
            }

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


# Global instance for easy access
mcp_client = MCPTaskClient()