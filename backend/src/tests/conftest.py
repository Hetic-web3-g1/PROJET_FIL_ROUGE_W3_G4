import pytest
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

    metadata.drop_all(engine)
