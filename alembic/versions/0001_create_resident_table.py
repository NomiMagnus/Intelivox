"""create resident table

Revision ID: 0001_create_resident_table
Revises: 
Create Date: 2026-06-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001_create_resident_table'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # create enums if they do not already exist, using raw SQL to handle conditional creation
    conn = op.get_bind()
    
    # Check and create resident_type enum
    try:
        conn.execute("CREATE TYPE resident_type AS ENUM ('individual', 'organization', 'institution')")
    except Exception:
        # Enum already exists, continue
        pass
    
    # Check and create resident_status enum
    try:
        conn.execute("CREATE TYPE resident_status AS ENUM ('new', 'active', 'pending', 'inactive')")
    except Exception:
        # Enum already exists, continue
        pass

    op.create_table(
        'resident',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('type', sa.Enum('individual', 'organization', 'institution', name='resident_type'), nullable=False, server_default='individual'),
        sa.Column('status', sa.Enum('new', 'active', 'pending', 'inactive', name='resident_status'), nullable=False, server_default='new'),
        sa.Column('first_name', sa.String(length=128), nullable=True),
        sa.Column('last_name', sa.String(length=128), nullable=True),
        sa.Column('organization_name', sa.String(length=256), nullable=True),
        sa.Column('mobile_phone', sa.String(length=32), nullable=True),
        sa.Column('home_phone', sa.String(length=32), nullable=True),
        sa.Column('work_phone', sa.String(length=32), nullable=True),
        sa.Column('email', sa.String(length=254), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    op.create_index(op.f('ix_resident_type'), 'resident', ['type'], unique=False)
    op.create_index(op.f('ix_resident_status'), 'resident', ['status'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_resident_status'), table_name='resident')
    op.drop_index(op.f('ix_resident_type'), table_name='resident')
    op.drop_table('resident')
    
    # Drop enums if they exist
    conn = op.get_bind()
    try:
        conn.execute("DROP TYPE IF EXISTS resident_status")
    except Exception:
        pass
    try:
        conn.execute("DROP TYPE IF EXISTS resident_type")
    except Exception:
        pass
