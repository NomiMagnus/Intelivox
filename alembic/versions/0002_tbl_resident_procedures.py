"""create tbl_resident table and read procedures

Revision ID: 0002_tbl_resident_procedures
Revises: 0001_create_resident_table
Create Date: 2026-06-16 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002_tbl_resident_procedures'
down_revision = '0001_create_resident_table'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # Rename the original table to the new table name if it exists.
    if conn.execute(sa.text("SELECT to_regclass('public.resident')")).scalar() is not None:
        op.rename_table('resident', 'tbl_resident')

    op.execute(
        """
        CREATE OR REPLACE FUNCTION prc_get_residents()
        RETURNS SETOF tbl_resident
        LANGUAGE sql
        AS $$
            SELECT * FROM tbl_resident;
        $$;
        """
    )

    op.execute(
        """
        CREATE OR REPLACE FUNCTION prc_get_resident(resident_id uuid)
        RETURNS tbl_resident
        LANGUAGE sql
        AS $$
            SELECT * FROM tbl_resident WHERE id = resident_id LIMIT 1;
        $$;
        """
    )

    op.execute(
        """
        CREATE OR REPLACE FUNCTION prc_search_residents(q text)
        RETURNS SETOF tbl_resident
        LANGUAGE sql
        AS $$
            SELECT *
            FROM tbl_resident
            WHERE q IS NULL
               OR LOWER(first_name) LIKE LOWER('%' || q || '%')
               OR LOWER(last_name) LIKE LOWER('%' || q || '%')
               OR LOWER(organization_name) LIKE LOWER('%' || q || '%')
               OR LOWER(email) LIKE LOWER('%' || q || '%')
               OR LOWER(mobile_phone) LIKE LOWER('%' || q || '%')
               OR LOWER(home_phone) LIKE LOWER('%' || q || '%')
               OR LOWER(work_phone) LIKE LOWER('%' || q || '%');
        $$;
        """
    )


def downgrade():
    op.execute("DROP FUNCTION IF EXISTS prc_search_residents(text)")
    op.execute("DROP FUNCTION IF EXISTS prc_get_resident(uuid)")
    op.execute("DROP FUNCTION IF EXISTS prc_get_residents()")

    conn = op.get_bind()
    if conn.execute(sa.text("SELECT to_regclass('public.tbl_resident')")).scalar() is not None:
        op.rename_table('tbl_resident', 'resident')
