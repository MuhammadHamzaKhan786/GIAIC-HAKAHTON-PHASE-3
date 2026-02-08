"""Create conversation and message tables

Revision ID: 001_create_conversation_message_tables
Revises:
Create Date: 2026-02-06 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
import uuid
from datetime import datetime

# revision identifiers
revision = '001_create_conversation_message_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create conversation table
    op.create_table('conversation',
        sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=True),
        sa.Column('user_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_conversation_id'), 'conversation', ['id'], unique=False)

    # Create message table
    op.create_table('message',
        sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('content', sa.String(length=10000), nullable=False),
        sa.Column('conversation_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('user_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversation.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_id'), 'message', ['id'], unique=False)

    # Update default title for conversations
    op.execute("UPDATE conversation SET title = 'New Conversation' WHERE title IS NULL OR title = ''")


def downgrade():
    op.drop_table('message')
    op.drop_table('conversation')