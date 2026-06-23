"""create user read procedures

Revision ID: 0004_tbl_user_procedures
Revises: 0003_create_user_tables
Create Date: 2026-06-24 00:00:01.000000
"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '0004_tbl_user_procedures'
down_revision = '0003_create_user_tables'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        CREATE OR REPLACE FUNCTION prc_get_users()
        RETURNS SETOF tbl_user
        LANGUAGE sql
        AS $$
            SELECT * FROM tbl_user ORDER BY created_at DESC;
        $$;
        """
    )

    op.execute(
        """
        CREATE OR REPLACE FUNCTION prc_get_user(user_id uuid)
        RETURNS tbl_user
        LANGUAGE sql
        AS $$
            SELECT * FROM tbl_user WHERE id = user_id LIMIT 1;
        $$;
        """
    )

    op.execute(
        """
        CREATE OR REPLACE FUNCTION prc_search_users(q text)
        RETURNS SETOF tbl_user
        LANGUAGE sql
        AS $$
            SELECT *
            FROM tbl_user
            WHERE q IS NULL
               OR LOWER(first_name) LIKE LOWER('%' || q || '%')
               OR LOWER(last_name) LIKE LOWER('%' || q || '%')
               OR LOWER(username) LIKE LOWER('%' || q || '%')
               OR LOWER(email) LIKE LOWER('%' || q || '%')
               OR LOWER(id_number) LIKE LOWER('%' || q || '%')
               OR LOWER(department) LIKE LOWER('%' || q || '%')
               OR LOWER(phone) LIKE LOWER('%' || q || '%');
        $$;
        """
    )

    op.execute(
        """
        CREATE OR REPLACE FUNCTION prc_get_roles()
        RETURNS SETOF tbl_role
        LANGUAGE sql
        AS $$
            SELECT * FROM tbl_role ORDER BY code;
        $$;
        """
    )

    op.execute(
        """
        CREATE OR REPLACE FUNCTION prc_get_user_roles(p_user_id uuid)
        RETURNS SETOF tbl_user_role
        LANGUAGE sql
        AS $$
            SELECT * FROM tbl_user_role WHERE user_id = p_user_id;
        $$;
        """
    )


def downgrade():
    op.execute("DROP FUNCTION IF EXISTS prc_get_user_roles(uuid)")
    op.execute("DROP FUNCTION IF EXISTS prc_get_roles()")
    op.execute("DROP FUNCTION IF EXISTS prc_search_users(text)")
    op.execute("DROP FUNCTION IF EXISTS prc_get_user(uuid)")
    op.execute("DROP FUNCTION IF EXISTS prc_get_users()")
