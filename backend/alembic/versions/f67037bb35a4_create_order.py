"""Create order

Revision ID: f67037bb35a4
Revises: 0c22e62bee71
Create Date: 2024-01-07 12:51:33.603416

"""
from alembic import op
import sqlalchemy as sa
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 'f67037bb35a4'
down_revision = '0c22e62bee71'
branch_labels = None
depends_on = None

# ingresar un pedido de un cliente por cantidad y tipo de producto,
#  especificando: cliente, fecha del pedido, producto, cantidad y status
#  del mismo: si fue entregado y en que fecha 

def create_order() -> None:
    op.create_table(
        "order",
        sa.Column("id", UUID, primary_key=True, default=uuid4()),
        sa.Column("quantity", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("discount", sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column("total", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('is_delivered', sa.Boolean, default=False),
        sa.Column('order_date', sa.DateTime),
        sa.Column('delivery_date', sa.DateTime, nullable=True),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('product_offered_id', UUID, sa.ForeignKey('product_offered.id'), nullable=True),
        sa.Column("created_by", UUID, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_by", UUID, nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )


def upgrade() -> None:
    create_order()


def downgrade() -> None:
    op.drop_table("order")
