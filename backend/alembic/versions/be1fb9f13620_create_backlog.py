"""Create backlog

Revision ID: be1fb9f13620
Revises: f67037bb35a4
Create Date: 2024-01-07 17:08:12.808707

"""
from alembic import op
import sqlalchemy as sa
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 'be1fb9f13620'
down_revision = 'f67037bb35a4'
branch_labels = None
depends_on = None


def create_backlog_table():
    op.create_table(
        'backlog',
        sa.Column("id", UUID, primary_key=True, default=uuid4()),
        sa.Column('product_id', UUID(as_uuid=True), sa.ForeignKey('product.id')),
        sa.Column('required_quantity', sa.Integer, nullable=False),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', UUID, nullable=True),
        sa.Column('updated_by', UUID, nullable=True),
    )

def upgrade() -> None:
    create_backlog_table()


def downgrade() -> None:
    op.drop_table('backlog')
