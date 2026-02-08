"""
Final validation test for MCP Server & Task Tooling
"""
import asyncio
from backend.mcp.models.task import Task
from backend.mcp.db import get_session
from sqlmodel import select
from backend.mcp.tool_registry import (
    add_task_handler, list_tasks_handler, complete_task_handler,
    update_task_handler, delete_task_handler
)
import json

async def test_all_operations():
    print("=== Testing MCP Task Server Operations ===")

    # Test 1: Add a task
    print("\n1. Testing add_task...")
    add_params = {"title": "Test Task", "description": "This is a test task"}
    add_result = await add_task_handler(add_params)
    print(f"   Added task: {add_result}")
    assert "task_id" in add_result
    assert add_result["title"] == "Test Task"
    task_id = add_result["task_id"]

    # Test 2: List tasks
    print("\n2. Testing list_tasks...")
    list_params = {"status": "all"}
    list_result = await list_tasks_handler(list_params)
    print(f"   Listed tasks: {len(list_result['tasks'])} tasks found")
    assert len(list_result["tasks"]) >= 1

    # Test 3: Complete task
    print(f"\n3. Testing complete_task (task_id: {task_id})...")
    complete_params = {"task_id": task_id}
    complete_result = await complete_task_handler(complete_params)
    print(f"   Completed task: {complete_result}")
    assert complete_result["task_id"] == task_id
    assert complete_result["completed"] == True

    # Test 4: Update task
    print(f"\n4. Testing update_task (task_id: {task_id})...")
    update_params = {"task_id": task_id, "title": "Updated Test Task", "description": "Updated description"}
    update_result = await update_task_handler(update_params)
    print(f"   Updated task: {update_result}")
    assert update_result["task_id"] == task_id
    assert update_result["title"] == "Updated Test Task"

    # Test 5: Delete task
    print(f"\n5. Testing delete_task (task_id: {task_id})...")
    delete_params = {"task_id": task_id}
    delete_result = await delete_task_handler(delete_params)
    print(f"   Deleted task: {delete_result}")
    assert delete_result["task_id"] == task_id
    assert delete_result["status"] == "deleted"

    # Verify deletion
    print("\n6. Verifying task was deleted...")
    list_after_delete = await list_tasks_handler({"status": "all"})
    task_exists = any(task['id'] == task_id for task in list_after_delete['tasks'])
    print(f"   Task still exists after deletion: {task_exists}")
    assert not task_exists  # Task should not exist after deletion

    print("\n✅ All tests passed! MCP Server is working correctly.")

if __name__ == "__main__":
    # Set up environment
    import os
    os.environ['CREATE_TABLES_ON_IMPORT'] = 'false'
    os.environ['MOCK_USER_ID'] = 'test_user_validation'

    # Run the test
    asyncio.run(test_all_operations())