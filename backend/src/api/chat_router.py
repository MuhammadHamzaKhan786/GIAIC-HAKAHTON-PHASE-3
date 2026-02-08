from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
import uuid
from datetime import datetime

from backend.src.database import get_session
from backend.src.auth.auth_bearer import get_current_user_from_token
from backend.src.models import (
    Conversation,
    ConversationCreate,
    ConversationRead,
    Message,
    MessageCreate,
    MessageRead,
    User
)

router = APIRouter()

@router.post("/{user_id}/chat", response_model=dict)
async def chat_endpoint(
    user_id: UUID,
    message: str = Body(..., embed=False),
    conversation_id: Optional[UUID] = Body(None, embed=False),
    current_user: dict = Depends(get_current_user_from_token),
    session: Session = Depends(get_session)
):
    """
    Main chat endpoint that handles conversation between user and AI assistant.

    Args:
        user_id: UUID of the authenticated user (extracted from JWT)
        message: The message content from the user
        conversation_id: Optional conversation ID (creates new if not provided)
        current_user: Current authenticated user data
        session: Database session

    Returns:
        dict containing conversation_id and assistant response
    """
    # Extract user_id from JWT token and verify it matches the path parameter
    token_user_id = current_user.get("sub")

    # Debug logging to help troubleshoot
    print(f"DEBUG: Path user_id: {user_id} (type: {type(user_id)})")
    print(f"DEBUG: Token user_id: {token_user_id} (type: {type(token_user_id)})")

    if not token_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No user ID found in token"
        )

    if str(token_user_id) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User ID mismatch. Path: {user_id}, Token: {token_user_id}"
        )

    # Validate input message
    if not message or not message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty"
        )

    # Find or create conversation
    conversation = None
    if conversation_id:
        # Look for existing conversation owned by this user
        conversation = session.exec(
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .where(Conversation.user_id == user_id)
        ).first()

    # If no valid conversation found, create a new one
    if not conversation:
        new_conversation_data = ConversationCreate()
        conversation = Conversation(**new_conversation_data.model_dump())
        conversation.user_id = user_id
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

    # Store the user's message
    user_message = Message(
        role="user",
        content=message,
        conversation_id=conversation.id,
        user_id=user_id
    )
    session.add(user_message)
    session.commit()
    session.refresh(user_message)

    # Fetch the full conversation history
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at)
    )
    messages = session.exec(statement).all()

    # Format messages for the agent
    formatted_messages = []
    for msg in messages:
        formatted_messages.append({
            "role": msg.role,
            "content": msg.content
        })

    # Import and run the agent with the message history
    from backend.agent.runner import run_agent
    agent_result = await run_agent(formatted_messages, str(user_id))
    agent_response_content = agent_result["response"]

    # Store the assistant's response
    assistant_message = Message(
        role="assistant",
        content=agent_response_content,
        conversation_id=conversation.id,
        user_id=user_id  # Note: assistant messages are associated with the user for ownership
    )
    session.add(assistant_message)
    session.commit()
    session.refresh(assistant_message)

    # Return the response with conversation_id and tool calls
    return {
        "conversation_id": str(conversation.id),
        "response": agent_response_content,
        "tool_calls": agent_result.get("tool_calls", [])
    }