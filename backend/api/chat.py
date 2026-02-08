from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from pydantic import BaseModel
from backend.models.conversation import Conversation, ConversationCreate
from backend.models.message import Message, MessageCreate
from backend.database import get_session
from backend.api.auth import validate_user_token
from backend.agent.runner import run_agent
from typing import Optional, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


router = APIRouter()


class ChatRequest(BaseModel):
    """Request body for chat endpoint"""
    message: str
    conversation_id: Optional[str] = None


@router.post("/{user_id}/chat")
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    token_data: Dict[str, Any] = Depends(validate_user_token),
    session: Session = Depends(get_session)
):
    """
    Main chat endpoint that handles conversation with the AI agent.

    Process:
    1. Validate user token and ensure user_id matches
    2. Create conversation if missing
    3. Load previous messages
    4. Save user message
    5. Build agent message array
    6. Call run_agent()
    7. Save assistant message
    8. Return conversation_id, response, tool_calls
    """
    # Validate that the user_id from the token matches the one in the path/route
    if token_data["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied: User ID mismatch")

    # Extract values from request body
    conversation_id = request.conversation_id
    message = request.message

    # Create or load conversation
    if conversation_id:
        # Verify that the conversation belongs to the user
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation = session.exec(statement).first()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found or access denied")
    else:
        # Create a new conversation
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        conversation_id = conversation.id

    # Save the user's message
    user_message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role="user",
        content=message
    )
    session.add(user_message)
    session.commit()

    # Load all messages for this conversation in chronological order
    statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
    messages = session.exec(statement).all()

    # Format messages for the agent
    formatted_messages = []
    for msg in messages:
        formatted_messages.append({
            "role": msg.role,
            "content": msg.content
        })

    # Run the agent with the message history
    agent_result = await run_agent(formatted_messages, user_id)

    # Save the assistant's response
    assistant_message = Message(
        conversation_id=conversation_id,
        user_id=user_id,  # The assistant is acting on behalf of the system for the user
        role="assistant",
        content=agent_result["response"]
    )
    session.add(assistant_message)
    session.commit()

    # Update the conversation's updated_at timestamp
    conversation.updated_at = datetime.utcnow()
    session.add(conversation)
    session.commit()

    # Return the response with conversation_id and tool calls
    return {
        "conversation_id": conversation_id,
        "response": agent_result["response"],
        "tool_calls": agent_result.get("tool_calls", [])
    }