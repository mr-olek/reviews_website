"""Copy a stopped site's SQLite backup to an empty PostgreSQL database.

Usage: DATABASE_URL=postgresql+psycopg://... python scripts/migrate_database.py backup.db
Credentials stay in the environment and are never printed.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app, db
from sqlalchemy import create_engine, select, func, text

if not os.environ.get('DATABASE_URL', '').startswith('postgresql'):
    raise SystemExit('DATABASE_URL must point to PostgreSQL')
source = create_engine('sqlite:///' + str(Path(sys.argv[1]).resolve()))
app = create_app('production')
with app.app_context(), source.connect() as src, db.engine.begin() as dest:
    tables = db.metadata.sorted_tables
    for table in tables:
        if dest.scalar(select(func.count()).select_from(table)):
            raise SystemExit('Destination must be empty; no data was changed')
    for table in tables:
        rows = src.execute(select(table))
        count = 0
        while True:
            batch = rows.fetchmany(500)
            if not batch:
                break
            dest.execute(table.insert(), [dict(row._mapping) for row in batch])
            count += len(batch)
        if dest.scalar(select(func.count()).select_from(table)) != count:
            raise RuntimeError(f'Row count mismatch for {table.name}')
        if 'id' in table.c:
            dest.execute(text(f"SELECT setval(pg_get_serial_sequence('{table.name}', 'id'), "
                              f"COALESCE((SELECT MAX(id) FROM {table.name}), 1), "
                              f"EXISTS(SELECT 1 FROM {table.name}))"))
        print(f'{table.name}: copied and verified {count} rows', flush=True)
print('Migration committed successfully')
