from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

DATABASE_URL = "postgresql://root:root@db-postgres:5432/db_saline_royale"

# Connection to database
engine = create_engine(
    DATABASE_URL,
    connect_args={"options": "-c timezone=utc"}
)

try:
    engine.connect()
    print("DB connection success")

except SQLAlchemyError as err:
    engine.connect()
    print("Error", err.__cause__)