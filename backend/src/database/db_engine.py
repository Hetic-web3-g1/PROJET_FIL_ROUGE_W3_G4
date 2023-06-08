from sqlalchemy import create_engine, MetaData
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.exc import SQLAlchemyError

from src.utils.log import logging
from src.utils.env import settings

# Connection to database
engine = create_engine(
    settings.database_url, connect_args={"options": "-c timezone=utc"}
)


# Check existence of db, if not, create it
if not database_exists(engine.url):
    create_database(engine.url)

# Try except to test db conncection
try:
    engine.connect()
    logging.info("DB connection success")

except SQLAlchemyError as err:
    engine.connect()
    logging.error("Error", err.__cause__)

metadata = MetaData()
