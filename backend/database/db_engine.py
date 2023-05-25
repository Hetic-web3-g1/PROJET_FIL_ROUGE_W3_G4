from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.exc import SQLAlchemyError

DATABASE_URL = "postgresql://root:root@db-postgres:5432/db_saline_royale"

# Connection to database
engine = create_engine(
    DATABASE_URL,
    connect_args={"options": "-c timezone=utc"}
)

# Check existence of db, if not, create it
if not database_exists(engine.url):
    create_database(engine.url)

# Try except to test db conncection
try:
    engine.connect()
    print("DB connection success")

except SQLAlchemyError as err:
    engine.connect()
    print("Error", err.__cause__)