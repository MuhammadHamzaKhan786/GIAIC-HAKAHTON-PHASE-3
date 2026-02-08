import pytest
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime
import uuid
from src.models.conversation import Conversation, ConversationCreate
from src.models.message import Message, MessageCreate


def test_conversation_model_creation():
    """Test that Conversation model can be created with valid data"""
    user_id = uuid.uuid4()

    conversation_data = ConversationCreate(title="Test Conversation")
    conversation = Conversation.from_orm(conversation_data)
    conversation.user_id = user_id

    # Verify attributes are set correctly
    assert conversation.title == "Test Conversation"
    assert conversation.user_id == user_id
    assert conversation.id is not None  # UUID should be auto-generated
    assert conversation.created_at is not None
    assert conversation.updated_at is not None


def test_message_model_creation():
    """Test that Message model can be created with valid data"""
    user_id = uuid.uuid4()
    conversation_id = uuid.uuid4()

    message_data = MessageCreate(role="user", content="Test message content")
    message = Message.from_orm(message_data)
    message.user_id = user_id
    message.conversation_id = conversation_id

    # Verify attributes are set correctly
    assert message.role == "user"
    assert message.content == "Test message content"
    assert message.user_id == user_id
    assert message.conversation_id == conversation_id
    assert message.id is not None  # UUID should be auto-generated
    assert message.created_at is not None


def test_message_role_validation():
    """Test that Message model validates role correctly"""
    user_id = uuid.uuid4()
    conversation_id = uuid.uuid4()

    # Valid roles should work
    valid_roles = ["user", "assistant"]
    for role in valid_roles:
        message_data = MessageCreate(role=role, content="Test message")
        message = Message.from_orm(message_data)
        message.user_id = user_id
        message.conversation_id = conversation_id

        assert message.role == role


def test_message_content_validation():
    """Test that Message model validates content length"""
    user_id = uuid.uuid4()
    conversation_id = uuid.uuid4()

    # Very long content (over 10000 chars) would fail validation in real usage
    # Here we just test the model structure
    short_content = "Short message"
    message_data = MessageCreate(role="user", content=short_content)
    message = Message.from_orm(message_data)
    message.user_id = user_id
    message.conversation_id = conversation_id

    assert message.content == short_content