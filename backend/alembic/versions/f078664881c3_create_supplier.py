"""Create supplier

Revision ID: f078664881c3
Revises: 13ac768875ae
Create Date: 2024-01-06 15:16:24.311436

"""
from alembic import op
import sqlalchemy as sa
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 'f078664881c3'
down_revision = '13ac768875ae'
branch_labels = None
depends_on = None

def create_supplier_table():
    op.create_table(
        'supplier',
        sa.Column("id", UUID, primary_key=True, default=uuid4()),
        sa.Column('name', sa.String(100), unique=True),
        sa.Column('address', sa.String(100)),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', UUID, nullable=True),
        sa.Column('updated_by', UUID, nullable=True),
    )

def upgrade() -> None:
    create_supplier_table()


def downgrade() -> None:
    op.drop_table('supplier')
