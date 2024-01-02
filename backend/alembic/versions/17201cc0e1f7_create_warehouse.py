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
        "warehouse",
        sa.Column("id", UUID, primary_key=True, default=uuid4()),
        sa.Column("type", sa.String(50), nullable=False),
        sa.Column("number", sa.Integer, autoincrement=True, nullable=True),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("name", sa.String, nullable=True, unique=True, index=True),
        sa.Column("created_by", UUID, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_by", UUID, nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.execute("""
        CREATE OR REPLACE FUNCTION update_warehouse_name()
        RETURNS TRIGGER AS $$
        DECLARE
            existing_count INTEGER;
        BEGIN
            SELECT COUNT(*) INTO existing_count
            FROM warehouse
            WHERE type = NEW.type;
            
            IF existing_count > 0 THEN
                NEW.number := (
                    SELECT COALESCE(MAX(number), 0) + 1
                    FROM warehouse
                    WHERE type = NEW.type
                );
            ELSE
                NEW.number := 1;
            END IF;
            
            NEW.name := CONCAT(NEW.type, '-', NEW.number);
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        CREATE TRIGGER trigger_update_warehouse_name
        BEFORE INSERT OR UPDATE ON warehouse
        FOR EACH ROW
        EXECUTE FUNCTION update_warehouse_name();
    """)

    op.execute("ALTER TABLE warehouse ALTER COLUMN number SET DEFAULT 1;")

def upgrade() -> None:
    create_warehouse_table()   
     
def downgrade() -> None:
    op.execute("DROP TRIGGER trigger_update_warehouse_name ON warehouse")
    op.execute("DROP FUNCTION update_warehouse_name")
    op.drop_table("warehouse")

