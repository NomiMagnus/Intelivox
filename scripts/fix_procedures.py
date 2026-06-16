import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))

with engine.connect() as conn:
    conn.execute(text("""
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
    """))
    conn.commit()
    print("prc_search_residents created successfully")
