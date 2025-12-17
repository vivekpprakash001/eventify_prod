# reset_db.py
import os
import sys
import django
from django.core.management import call_command
from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eventify.settings")
django.setup()

def reset_postgres_schema():
    user = connection.settings_dict.get("USER", "postgres")
    with connection.cursor() as cursor:
        cursor.execute("""
            DROP SCHEMA public CASCADE;
            CREATE SCHEMA public;
            GRANT ALL ON SCHEMA public TO {user};
            GRANT ALL ON SCHEMA public TO public;
        """.format(user=user))

def main():
    if "--force" not in sys.argv:
        print("Refusing to run without --force (this DROPS ALL TABLES).")
        sys.exit(1)

    engine = connection.settings_dict.get("ENGINE", "")
    if "postgresql" not in engine:
        print("This script is intended for PostgreSQL. Aborting.")
        sys.exit(1)

    print("Dropping all tables by recreating public schema…")
    reset_postgres_schema()

    print("Running migrations…")
    call_command("migrate", interactive=False)

    print("Done.")

if __name__ == "__main__":
    main()