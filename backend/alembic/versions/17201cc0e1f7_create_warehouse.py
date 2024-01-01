"""Create Warehouse

Revision ID: 17201cc0e1f7
Revises: 492eec39b72d
Create Date: 2024-01-01 14:18:22.805543

"""
from alembic import op
import sqlalchemy as sa
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '17201cc0e1f7'
down_revision = '492eec39b72d'
branch_labels = None
depends_on = None

# Create Warehouse Table
def create_warehouse_table():
    op.create_table(
        "Warehouse",
        sa.Column("id", UUID, primary_key=True, default=uuid4()),
        sa.Column("type", sa.String(50), nullable=False, unique=True),
        sa.Column("number", sa.Integer),
        sa.Column("name", sa.String, nullable=False, unique=True),
        sa.Column("created_by", UUID, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_by", UUID, nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "name",
            sa.String,
            nullable=False,
            unique=True,
            server_default=sa.text("concat(type, '-', number)")
        ).label("name")
    )

def upgrade() -> None:
    create_warehouse_table()    

def downgrade() -> None:
    op.drop_table("Warehouse")