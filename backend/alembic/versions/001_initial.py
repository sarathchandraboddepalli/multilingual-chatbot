"""Initial tables

Revision ID: 001
Revises:
Create Date: 2026-01-01
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'chat_users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('phone', sa.String(15), unique=True),
        sa.Column('name', sa.String(255)),
        sa.Column('preferred_language', sa.String(10), default='en'),
        sa.Column('district', sa.String(100)),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        'conversations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('chat_users.id'), nullable=True),
        sa.Column('channel', sa.String(20), default='web'),
        sa.Column('language', sa.String(10), default='en'),
        sa.Column('status', sa.String(20), default='active'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        'messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('conversation_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', sa.String(10), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('original_content', sa.Text),
        sa.Column('language', sa.String(10), default='en'),
        sa.Column('scheme_referenced', sa.String(255)),
        sa.Column('confidence_score', sa.Float),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        'schemes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('scheme_id', sa.String(100), unique=True, nullable=False),
        sa.Column('name', sa.String(500), nullable=False),
        sa.Column('name_telugu', sa.String(500)),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('eligibility', sa.Text),
        sa.Column('benefits', sa.Text),
        sa.Column('documents_required', sa.Text),
        sa.Column('application_url', sa.String(1024)),
        sa.Column('department', sa.String(255)),
        sa.Column('category', sa.String(100)),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('messages')
    op.drop_table('conversations')
    op.drop_table('chat_users')
    op.drop_table('schemes')
