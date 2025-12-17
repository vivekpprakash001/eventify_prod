# pg_to_sqlite_backup.py
import os
import sys
import django
from django.conf import settings
from django.core.management import call_command
from django.db import connections, DEFAULT_DB_ALIAS

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eventify.settings")
django.setup()

SQLITE_PATH = "backup.sqlite3"
BACKUP_ALIAS = "backup"


def ensure_backup_db():
    # Add a SQLite backup database alias
    settings.DATABASES[BACKUP_ALIAS] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.abspath(SQLITE_PATH),
    }
    # Remove existing file so migrate creates a fresh DB
    if os.path.exists(SQLITE_PATH):
        os.remove(SQLITE_PATH)

    # Run migrations on the backup DB
    print("Running migrations on backup (SQLite)…")
    call_command("migrate", database=BACKUP_ALIAS, interactive=False, verbosity=0)
    print("SQLite schema created at", SQLITE_PATH)


def copy_all_tables():
    pg_conn = connections[DEFAULT_DB_ALIAS]          # default = PostgreSQL
    sqlite_conn = connections[BACKUP_ALIAS]          # new SQLite

    pg_cursor = pg_conn.cursor()
    sqlite_cursor = sqlite_conn.cursor()

    tables = pg_conn.introspection.table_names()

    for table in tables:
        # Fetch column names from PostgreSQL
        cols = [c.name for c in pg_conn.introspection.get_table_description(pg_cursor, table)]
        col_list = ", ".join(f'"{c}"' for c in cols)
        placeholders = ", ".join(["?"] * len(cols))

        # Fetch all rows
        pg_cursor.execute(f'SELECT {col_list} FROM "{table}"')
        rows = pg_cursor.fetchall()

        # Insert into SQLite
        if rows:
            insert_sql = f'INSERT INTO "{table}" ({col_list}) VALUES ({placeholders})'
            sqlite_cursor.executemany(insert_sql, rows)

        print(f"Copied {len(rows)} rows from {table}")

    sqlite_conn.commit()
    pg_cursor.close()
    sqlite_cursor.close()


def main():
    if "--force" not in sys.argv:
        print("Refusing to run without --force (destructive for existing backup file).")
        sys.exit(1)

    # Safety: ensure default DB is PostgreSQL
    engine = settings.DATABASES[DEFAULT_DB_ALIAS]["ENGINE"]
    if "postgresql" not in engine:
        print("Default database is not PostgreSQL. Aborting.")
        sys.exit(1)

    ensure_backup_db()
    copy_all_tables()
    print("Done. SQLite backup at", SQLITE_PATH)


if __name__ == "__main__":
    main()