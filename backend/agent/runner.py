"""
Function to run the agent with conversation history and capture tool calls.
"""
from openai import OpenAI
from .agent import create_agent
from ..services.mcp_client import mcp_client
from typing import List, Dict, Any
import os
import asyncio
import logging

logger = logging.getLogger(__name__)


def compress_response(response: str) -> str:
    """Compress response to use minimum tokens."""
    # Remove extra whitespace
    compressed = " ".join(response.split())
    # Remove common verbose patterns
    replacements = [
        ("I have", "I've"),
        ("I would", "I'd"),
        ("you want to", "you"),
        ("the OpenAI API key is not configured", "API key missing"),
        ("Please set the OPENAI_API_KEY environment variable", "Set OPENAI_API_KEY"),
        ("I encountered an error while processing your request", "Error"),
        ("Could you try again", "Retry"),
        ("I am", "I'm"),
        ("that is", "that's"),
        ("would you like", "do you"),
        ("is not", "isn't"),
        ("do not", "don't"),
    ]
    for old, new in replacements:
        compressed = compressed.replace(old, new)
    return compressed


async def run_agent(messages: List[Dict[str, str]], user_id: str) -> Dict[str, Any]:
    """
    Run the OpenAI agent with the given message history and capture tool calls.

    Args:
        messages: List of messages in the format {"role": "user/assistant", "content": "message content"}
        user_id: The ID of the user for whom the agent is running

    Returns:
        Dictionary containing assistant response and tool calls
    """
    try:
        # Create the agent
        print("DEBUG: Attempting to create agent...")
        agent, client = create_agent()
        print(f"DEBUG: Agent created successfully: {type(agent)}")

        # Check if we're using the mock agent (when API key is not available)
        if hasattr(agent, 'id') and agent.id == "mock-assistant-id":
            # Handle the case when API key is not available
            # Just return a default response based on the user's message
            last_message = messages[-1]['content'].lower() if messages else ""

            last_message = messages[-1]['content'].lower() if messages else ""

            if 'add' in last_message or 'create' in last_message:
                response = "Task add requires API key. Set OPENAI_API_KEY."
            elif 'list' in last_message or 'show' in last_message:
                response = "Task list requires API key. Set OPENAI_API_KEY."
            elif 'complete' in last_message or 'done' in last_message:
                response = "Task complete requires API key. Set OPENAI_API_KEY."
            elif 'delete' in last_message or 'remove' in last_message:
                response = "Task delete requires API key. Set OPENAI_API_KEY."
            else:
                response = "Ready to help. Set OPENAI_API_KEY."

            return {
                "response": compress_response(response),
                "tool_calls": []
            }

        # Create a thread with the messages
        thread = client.beta.threads.create()

        # Add each message to the thread
        for msg in messages:
            client.beta.threads.messages.create(
                thread_id=thread.id,
                role=msg['role'],
                content=msg['content']
            )

        # Run the agent
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=agent.id
        )

        # Poll for completion
        while run.status in ['queued', 'in_progress', 'requires_action']:
            await asyncio.sleep(0.5)
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

            if run.status == 'requires_action':
                # Handle tool calls
                tool_outputs = []

                if run.required_action and run.required_action.submit_tool_outputs:
                    for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                        function_name = tool_call.function.name
                        try:
                            function_args = eval(tool_call.function.arguments)
                        except Exception:
                            # Safer way to parse arguments
                            import json
                            try:
                                function_args = json.loads(tool_call.function.arguments)
                            except:
                                function_args = {}

                        # Add user_id to function args if not present
                        if 'user_id' not in function_args:
                            function_args['user_id'] = user_id

                        # Call the appropriate MCP function based on the tool
                        try:
                            if function_name == "add_task":
                                result = await mcp_client.add_task(task=function_args.get('task'), user_id=user_id)
                            elif function_name == "list_tasks":
                                result = await mcp_client.list_tasks(user_id=user_id)
                            elif function_name == "complete_task":
                                result = await mcp_client.complete_task(task_id=function_args.get('task_id'), user_id=user_id)
                            elif function_name == "delete_task":
                                result = await mcp_client.delete_task(task_id=function_args.get('task_id'), user_id=user_id)
                            elif function_name == "update_task":
                                result = await mcp_client.update_task(
                                    task_id=function_args.get('task_id'),
                                    new_content=function_args.get('new_content'),
                                    user_id=user_id
                                )
                            else:
                                result = {"success": False, "error": f"Unknown function: {function_name}"}
                        except Exception as e:
                            result = {
                                "success": False,
                                "error": str(e),
                                "message": "I encountered an error while processing your request. Could you try again?"
                            }

                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": str(result)
                        })

                # Submit tool outputs back to the agent
                if tool_outputs:
                    run = client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread.id,
                        run_id=run.id,
                        tool_outputs=tool_outputs
                    )

        # Retrieve the messages from the thread
        response_messages = client.beta.threads.messages.list(thread_id=thread.id, order="asc")

        # Extract the assistant's response
        assistant_response = ""
        for msg in response_messages.data:
            if msg.role == "assistant":
                # Combine all content parts
                content_parts = []
                for content_item in msg.content:
                    if content_item.type == "text":
                        content_parts.append(content_item.text.value)
                assistant_response = " ".join(content_parts)
                break

        # Prepare the result with compressed response
        result = {
            "response": compress_response(assistant_response),
            "tool_calls": []  # This will be populated based on actual tool calls if needed
        }

        # Clean up - delete the thread
        try:
            client.beta.threads.delete(thread.id)
        except:
            pass  # Ignore errors when deleting thread

        return result

    except Exception as e:
        return {
            "response": "Error. Retry.",
            "tool_calls": [],
            "error": str(e)
        }