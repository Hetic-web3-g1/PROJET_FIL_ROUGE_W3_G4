from sqlalchemy import create_engine, MetaData
from sqlalchemy_utils import database_exists, create_database

from src.utils.env import settings
from src.utils.log.log_manager import log

# Connection to database
engine = create_engine(
    settings.database_url, connect_args={"options": "-c timezone=utc"}
)


# Check existence of db, if not, create it
if not database_exists(engine.url):
    create_database(engine.url)
    log(level="INFO", message="Database created.")

metadata = MetaData()
