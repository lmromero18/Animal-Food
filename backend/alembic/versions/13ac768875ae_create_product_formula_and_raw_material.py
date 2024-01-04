"""Create product ,formula and raw material

Revision ID: 13ac768875ae
Revises: 17201cc0e1f7
Create Date: 2024-01-03 18:56:15.541472

"""
from alembic import op
import sqlalchemy as sa
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '13ac768875ae'
down_revision = '17201cc0e1f7'
branch_labels = None
depends_on = None

def create_product_table():
    op.create_table(
        'product',
        sa.Column("id", UUID, primary_key=True, default=uuid4()),
        sa.Column('name', sa.String(100), unique=True),
        sa.Column('description', sa.String(100)),
        sa.Column('quantity', sa.Integer),        
        sa.Column('price', sa.Numeric(precision=10, scale=2)),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', UUID, nullable=True),
        sa.Column('updated_by', UUID, nullable=True),
        sa.Column('warehouse_id', UUID, sa.ForeignKey('warehouse.id'), nullable=True)        
    )
    
    
def create_raw_material_table():    
   op.create_table(
        'rawmaterial',
        sa.Column("id", UUID, primary_key=True, default=uuid4()),
        sa.Column('code', sa.String(50), unique=True),
        sa.Column('name', sa.String(100)),
        sa.Column('available_quantity', sa.Integer),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', UUID, nullable=True),
        sa.Column('updated_by', UUID, nullable=True),
        sa.Column('warehouse_id', UUID, sa.ForeignKey('warehouse.id'), nullable=True)
    )
    
def create_formula_table():
    op.create_table(
        'formula',
        sa.Column('product_id', UUID, sa.ForeignKey('product.id'), primary_key=True),
        sa.Column('raw_material_id', UUID, sa.ForeignKey('rawmaterial.id'), primary_key=True),
        sa.Column('required_quantity', sa.Integer),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', UUID, nullable=True),
        sa.Column('updated_by', UUID, nullable=True)
    )


def upgrade() -> None:
    create_product_table()
    create_raw_material_table()
    create_formula_table()


def downgrade() -> None:
    op.drop_table('Formula')    
    op.drop_table('RawMaterial')    
    op.drop_table('Product')