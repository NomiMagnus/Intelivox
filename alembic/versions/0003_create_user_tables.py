"""create user, role and user_role tables

Revision ID: 0003_create_user_tables
Revises: 0002_tbl_resident_procedures
Create Date: 2026-06-24 00:00:00.000000
"""
import hashlib
import secrets
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0003_create_user_tables'
down_revision = '0002_tbl_resident_procedures'
branch_labels = None
depends_on = None


def _hash(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(salt), 100_000).hex()


def upgrade():
    conn = op.get_bind()

    # Create enum types up front. Use checkfirst-style guards via DO blocks so
    # the migration is re-runnable without aborting the surrounding transaction.
    for type_name in ("user_status", "role_status", "user_role_status"):
        op.execute(
            sa.text(
                f"""
                DO $$ BEGIN
                    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = '{type_name}') THEN
                        CREATE TYPE {type_name} AS ENUM ('active', 'inactive');
                    END IF;
                END $$;
                """
            )
        )

    # create_type=False: the enum types are created above, so the table DDL
    # must not try to create them again.
    user_status = postgresql.ENUM('active', 'inactive', name='user_status', create_type=False)
    role_status = postgresql.ENUM('active', 'inactive', name='role_status', create_type=False)
    user_role_status = postgresql.ENUM('active', 'inactive', name='user_role_status', create_type=False)

    op.create_table(
        'tbl_user',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('id_number', sa.String(length=32), nullable=False),
        sa.Column('first_name', sa.String(length=128), nullable=True),
        sa.Column('last_name', sa.String(length=128), nullable=True),
        sa.Column('username', sa.String(length=64), nullable=False),
        sa.Column('email', sa.String(length=254), nullable=False),
        sa.Column('phone', sa.String(length=32), nullable=True),
        sa.Column('password', sa.String(length=256), nullable=False),
        sa.Column('salt', sa.String(length=64), nullable=False),
        sa.Column('department', sa.String(length=128), nullable=True),
        sa.Column('status', user_status, nullable=False, server_default='active'),
        sa.Column('must_change_password', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_tbl_user_id_number', 'tbl_user', ['id_number'], unique=True)
    op.create_index('ix_tbl_user_username', 'tbl_user', ['username'], unique=True)
    op.create_index('ix_tbl_user_email', 'tbl_user', ['email'], unique=True)

    op.create_table(
        'tbl_role',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('code', sa.String(length=32), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=True),
        sa.Column('status', role_status, nullable=False, server_default='active'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_tbl_role_code', 'tbl_role', ['code'], unique=True)

    op.create_table(
        'tbl_user_role',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tbl_user.id'), nullable=False),
        sa.Column('role_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tbl_role.id'), nullable=False),
        sa.Column('start_date', sa.Date(), server_default=sa.text('CURRENT_DATE'), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('status', user_role_status, nullable=False, server_default='active'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_tbl_user_role_user_id', 'tbl_user_role', ['user_id'])
    op.create_index('ix_tbl_user_role_role_id', 'tbl_user_role', ['role_id'])

    # ----- seed roles -----
    admin_role_id = str(uuid.uuid4())
    user_role_id = str(uuid.uuid4())
    conn.execute(
        sa.text(
            "INSERT INTO tbl_role (id, code, name, status) VALUES "
            "(:aid, 'admin', 'Administrator', 'active'), "
            "(:uid, 'user', 'User', 'active')"
        ),
        {"aid": admin_role_id, "uid": user_role_id},
    )

    # ----- seed an admin user (password: Admin123!, ready to use) -----
    admin_user_id = str(uuid.uuid4())
    salt = secrets.token_hex(16)
    conn.execute(
        sa.text(
            "INSERT INTO tbl_user "
            "(id, id_number, first_name, last_name, username, email, phone, password, salt, department, status, must_change_password) "
            "VALUES (:id, '000000000', 'System', 'Administrator', 'admin', 'admin@intelivox.local', NULL, :pw, :salt, 'IT', 'active', false)"
        ),
        {"id": admin_user_id, "pw": _hash("Admin123!", salt), "salt": salt},
    )
    conn.execute(
        sa.text(
            "INSERT INTO tbl_user_role (id, user_id, role_id, status) VALUES (:id, :uid, :rid, 'active')"
        ),
        {"id": str(uuid.uuid4()), "uid": admin_user_id, "rid": admin_role_id},
    )


def downgrade():
    op.drop_table('tbl_user_role')
    op.drop_table('tbl_role')
    op.drop_table('tbl_user')

    conn = op.get_bind()
    for enum_name in ('user_role_status', 'role_status', 'user_status'):
        try:
            conn.execute(sa.text(f"DROP TYPE IF EXISTS {enum_name}"))
        except Exception:
            pass
