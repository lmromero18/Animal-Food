"""Create purchase table

Revision ID: 0c22e62bee71
Revises: f078664881c3
Create Date: 2024-01-06 17:05:16.442055

"""
from alembic import op
import sqlalchemy as sa
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '0c22e62bee71'
down_revision = 'f078664881c3'
branch_labels = None
depends_on = None

def create_purchase_table():
    op.create_table(
        'purchase',
        sa.Column("id", UUID, primary_key=True, default=uuid4()),
        sa.Column('supplier_id', UUID(as_uuid=True), sa.ForeignKey('supplier.id')),
        sa.Column('order_date', sa.DateTime),
        sa.Column('delivery_date', sa.DateTime, nullable=True),
        sa.Column('raw_material_id', UUID(as_uuid=True), sa.ForeignKey('rawmaterial.id')),
        sa.Column('quantity', sa.Integer),
        sa.Column('is_delivered', sa.Boolean, default=False),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', UUID, nullable=True),
        sa.Column('updated_by', UUID, nullable=True),
    )

def upgrade() -> None:
    create_purchase_table()


def downgrade() -> None:
    op.drop_table('purchase')
