import pytest
import sqlalchemy as sa
from config import settings
from sqlalchemy import text
from src.database.db_engine import engine, metadata

if settings.environment != "test":
    raise ValueError("Tests must run with ENVIRONMENT=test")
else:
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS logging"))


@pytest.fixture(scope="class", autouse=True)
def connector():
    metadata.create_all(engine)

    yield

    drop_all(engine)


def drop_all(engine: sa.Engine):
    """
    Replacement for metadata.drop_all(engine) to drop constraints before tables.
    """

    inspector = sa.inspect(engine)
    meta = sa.MetaData()

    tables = []
    all_fkeys = []

    with engine.begin() as conn:
        for table_name in inspector.get_table_names():
            fkeys = []
            for fkey in inspector.get_foreign_keys(table_name):
                if not fkey["name"]:
                    continue

                fkeys.append(sa.ForeignKeyConstraint((), (), name=fkey["name"]))

            tables.append(sa.Table(table_name, meta, *fkeys))
            all_fkeys.extend(fkeys)

        for fkey in all_fkeys:
            conn.execute(sa.schema.DropConstraint(fkey))

        for table in tables:
            conn.execute(sa.schema.DropTable(table))
